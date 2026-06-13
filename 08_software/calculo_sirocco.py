#!/usr/bin/env python3
"""Calculo reproducible del ventilador centrifugo tipo Sirocco.

El modelo cierra un predimensionamiento unidimensional. No sustituye una curva
AMCA, un ensayo de laboratorio ni una simulacion CFD del conjunto rodete-voluta.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from math import atan2, ceil, cos, degrees, pi, radians, sin, sqrt, tan
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DatosDiseno:
    caudal_m3_s: float = 3.0
    altura_mmh2o: float = 90.0
    densidad_kg_m3: float = 1.2
    diametro_exterior_m: float = 0.60
    diametro_interior_m: float = 0.51
    ancho_rodete_m: float = 0.23
    rpm: float = 1100.0
    numero_alabes: int = 48
    espesor_alabe_m: float = 0.0012
    beta2_grados: float = 125.0
    diametro_cubo_m: float = 0.12
    numero_entradas: int = 2
    eficiencia_mecanica: float = 0.96
    velocidad_descarga_m_s: float = 15.0
    ancho_voluta_m: float = 0.28
    holgura_lengua_relativa: float = 0.08
    factor_servicio_eje: float = 1.5
    esfuerzo_cortante_admisible_pa: float = 30e6
    potencia_motor_kw: float = 5.5


def _validar(d: DatosDiseno) -> None:
    positivos = {
        "caudal": d.caudal_m3_s,
        "altura": d.altura_mmh2o,
        "densidad": d.densidad_kg_m3,
        "D2": d.diametro_exterior_m,
        "D1": d.diametro_interior_m,
        "ancho": d.ancho_rodete_m,
        "rpm": d.rpm,
        "espesor": d.espesor_alabe_m,
        "velocidad de descarga": d.velocidad_descarga_m_s,
        "ancho de voluta": d.ancho_voluta_m,
    }
    for nombre, valor in positivos.items():
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero")
    if d.diametro_interior_m >= d.diametro_exterior_m:
        raise ValueError("D1 debe ser menor que D2")
    if not 90.0 < d.beta2_grados < 180.0:
        raise ValueError("beta2 debe corresponder a un alabe curvado hacia adelante")
    if d.numero_alabes < 3 or d.numero_entradas not in (1, 2):
        raise ValueError("numero de alabes o entradas no valido")
    if not 0.0 < d.eficiencia_mecanica <= 1.0:
        raise ValueError("la eficiencia mecanica debe estar entre 0 y 1")


def factor_bloqueo(
    diametro_m: float,
    beta_grados: float,
    numero_alabes: int,
    espesor_alabe_m: float,
) -> float:
    """Fraccion abierta de la corona por espesor proyectado de los alabes."""
    factor = 1.0 - (
        numero_alabes
        * espesor_alabe_m
        / (pi * diametro_m * sin(radians(beta_grados)))
    )
    if factor <= 0.0:
        raise ValueError("el bloqueo geometrico cierra por completo el paso")
    return factor


def resolver_entrada_sin_incidencia(d: DatosDiseno) -> dict[str, float]:
    """Resuelve beta1 incluyendo el bloqueo que depende del propio angulo."""
    u1 = pi * d.diametro_interior_m * d.rpm / 60.0
    beta1 = 20.0
    for _ in range(100):
        bloqueo1 = factor_bloqueo(
            d.diametro_interior_m,
            beta1,
            d.numero_alabes,
            d.espesor_alabe_m,
        )
        cm1 = d.caudal_m3_s / (
            pi * d.diametro_interior_m * d.ancho_rodete_m * bloqueo1
        )
        beta_nuevo = degrees(atan2(cm1, u1))
        if abs(beta_nuevo - beta1) < 1e-10:
            break
        beta1 = 0.5 * (beta1 + beta_nuevo)
    return {
        "u1_m_s": u1,
        "cm1_m_s": cm1,
        "beta1_grados": beta_nuevo,
        "factor_bloqueo_1": bloqueo1,
    }


def factor_deslizamiento_wiesner(beta2_grados: float, numero_alabes: int) -> float:
    """Estimacion de Wiesner; requiere validacion para un Sirocco real."""
    return 1.0 - sqrt(sin(radians(beta2_grados))) / numero_alabes**0.7


def tabla_voluta(d: DatosDiseno, paso_grados: int = 45) -> list[dict[str, float]]:
    area_salida = d.caudal_m3_s / d.velocidad_descarga_m_s
    holgura = d.holgura_lengua_relativa * d.diametro_exterior_m
    filas = []
    for theta in range(0, 361, paso_grados):
        fraccion = theta / 360.0
        area = area_salida * fraccion
        altura_flujo = area / d.ancho_voluta_m
        separacion_total = holgura + altura_flujo
        filas.append(
            {
                "angulo_grados": float(theta),
                "fraccion_caudal": fraccion,
                "area_m2": area,
                "altura_flujo_m": altura_flujo,
                "separacion_radial_total_m": separacion_total,
                "radio_exterior_m": d.diametro_exterior_m / 2.0
                + separacion_total,
            }
        )
    return filas


def semejanza(d: DatosDiseno, escala: float = 0.5) -> list[dict[str, float | str]]:
    if not 0.0 < escala < 1.0:
        raise ValueError("la escala del modelo debe estar entre cero y uno")
    delta_p = d.altura_mmh2o * 9.80665
    potencia_eje = calcular(d)["potencias"]["potencia_eje_euler_kw"]
    return [
        {
            "modo": "misma_rpm",
            "escala": escala,
            "diametro_m": d.diametro_exterior_m * escala,
            "rpm": d.rpm,
            "caudal_m3_s": d.caudal_m3_s * escala**3,
            "presion_pa": delta_p * escala**2,
            "potencia_eje_kw": potencia_eje * escala**5,
        },
        {
            "modo": "misma_velocidad_periferica",
            "escala": escala,
            "diametro_m": d.diametro_exterior_m * escala,
            "rpm": d.rpm / escala,
            "caudal_m3_s": d.caudal_m3_s * escala**2,
            "presion_pa": delta_p,
            "potencia_eje_kw": potencia_eje * escala**2,
        },
    ]


def calcular(d: DatosDiseno | None = None) -> dict[str, Any]:
    d = d or DatosDiseno()
    _validar(d)

    delta_p = d.altura_mmh2o * 9.80665
    potencia_aire_kw = d.caudal_m3_s * delta_p / 1000.0
    entrada = resolver_entrada_sin_incidencia(d)

    u2 = pi * d.diametro_exterior_m * d.rpm / 60.0
    bloqueo2 = factor_bloqueo(
        d.diametro_exterior_m,
        d.beta2_grados,
        d.numero_alabes,
        d.espesor_alabe_m,
    )
    cm2 = d.caudal_m3_s / (
        pi * d.diametro_exterior_m * d.ancho_rodete_m * bloqueo2
    )
    sigma = factor_deslizamiento_wiesner(d.beta2_grados, d.numero_alabes)
    cu2 = sigma * u2 - cm2 / tan(radians(d.beta2_grados))
    delta_p_euler = d.densidad_kg_m3 * u2 * cu2
    potencia_euler_kw = d.caudal_m3_s * delta_p_euler / 1000.0
    potencia_eje_kw = potencia_euler_kw / d.eficiencia_mecanica
    eficiencia_estatica = potencia_aire_kw / potencia_eje_kw

    area_ojos = (
        d.numero_entradas
        * pi
        / 4.0
        * (d.diametro_interior_m**2 - d.diametro_cubo_m**2)
    )
    velocidad_ojos = d.caudal_m3_s / area_ojos
    presion_dinamica_entrada = 0.5 * d.densidad_kg_m3 * velocidad_ojos**2
    perdida_entrada = 0.20 * presion_dinamica_entrada
    perdida_salida = 0.5 * d.densidad_kg_m3 * d.velocidad_descarga_m_s**2
    diferencia = delta_p_euler - delta_p
    residual = max(diferencia - perdida_entrada - perdida_salida, 0.0)
    perdidas = [
        {"componente": "entrada_y_bellmouth", "presion_pa": perdida_entrada},
        {"componente": "pasajes_y_separacion", "presion_pa": residual * 0.45},
        {"componente": "recirculacion_y_fugas", "presion_pa": residual * 0.20},
        {"componente": "voluta_y_lengua", "presion_pa": residual * 0.25},
        {"componente": "margen_modelo_1d", "presion_pa": residual * 0.10},
        {"componente": "energia_cinetica_descarga", "presion_pa": perdida_salida},
    ]

    omega = 2.0 * pi * d.rpm / 60.0
    torque_nm = potencia_eje_kw * 1000.0 / omega
    torque_diseno_nm = torque_nm * d.factor_servicio_eje
    diametro_minimo_m = (
        16.0
        * torque_diseno_nm
        / (pi * d.esfuerzo_cortante_admisible_pa)
    ) ** (1.0 / 3.0)
    diametro_redondeado_mm = ceil(diametro_minimo_m * 1000.0 / 5.0) * 5.0
    diametro_recomendado_mm = max(30.0, diametro_redondeado_mm)

    area_salida = d.caudal_m3_s / d.velocidad_descarga_m_s
    altura_salida = area_salida / d.ancho_voluta_m
    holgura_lengua = d.holgura_lengua_relativa * d.diametro_exterior_m
    margen_motor = d.potencia_motor_kw / potencia_eje_kw - 1.0

    return {
        "entradas": asdict(d),
        "punto_operacion": {
            "presion_objetivo_pa": delta_p,
            "caudal_m3_h": d.caudal_m3_s * 3600.0,
            "velocidad_ojos_m_s": velocidad_ojos,
        },
        "rodete": {
            **entrada,
            "u2_m_s": u2,
            "cm2_m_s": cm2,
            "cu2_m_s": cu2,
            "factor_bloqueo_2": bloqueo2,
            "factor_deslizamiento": sigma,
            "presion_euler_pa": delta_p_euler,
            "coeficiente_flujo_cm2_u2": cm2 / u2,
            "coeficiente_presion_estatica": delta_p / (d.densidad_kg_m3 * u2**2),
        },
        "potencias": {
            "potencia_util_aire_kw": potencia_aire_kw,
            "potencia_euler_kw": potencia_euler_kw,
            "potencia_eje_euler_kw": potencia_eje_kw,
            "eficiencia_estatica_estimada": eficiencia_estatica,
            "potencia_motor_kw": d.potencia_motor_kw,
            "margen_motor_relativo": margen_motor,
        },
        "voluta": {
            "area_salida_m2": area_salida,
            "ancho_interior_m": d.ancho_voluta_m,
            "altura_salida_m": altura_salida,
            "holgura_lengua_m": holgura_lengua,
            "tabla": tabla_voluta(d),
        },
        "perdidas": perdidas,
        "mecanica": {
            "torque_nominal_nm": torque_nm,
            "torque_diseno_nm": torque_diseno_nm,
            "diametro_minimo_torsion_mm": diametro_minimo_m * 1000.0,
            "diametro_eje_recomendado_mm": diametro_recomendado_mm,
        },
    }


def _escribir_csv(ruta: Path, filas: list[dict[str, Any]]) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=list(filas[0]), lineterminator="\n"
        )
        escritor.writeheader()
        escritor.writerows(filas)


def generar_svg(d: DatosDiseno, resultado: dict[str, Any], ruta: Path) -> None:
    tabla = resultado["voluta"]["tabla"]
    puntos = []
    escala = 360.0
    origen_x, origen_y = 430.0, 430.0
    for fila in tabla:
        theta = radians(fila["angulo_grados"])
        radio = fila["radio_exterior_m"]
        x = origen_x + escala * radio * cos(theta)
        y = origen_y - escala * radio * sin(theta)
        puntos.append(f"{x:.1f},{y:.1f}")

    r_rodete = escala * d.diametro_exterior_m / 2.0
    r_entrada = escala * d.diametro_interior_m / 2.0
    ancho_salida = escala * resultado["voluta"]["altura_salida_m"]
    salida_x = origen_x + r_rodete
    salida_y = origen_y - 180.0
    texto_puntos = " ".join(puntos)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="820" viewBox="0 0 1100 820">
  <rect width="1100" height="820" fill="white"/>
  <style>
    text {{ font-family: Arial, sans-serif; fill: #172033; }}
    .titulo {{ font-size: 26px; font-weight: bold; }}
    .etiqueta {{ font-size: 17px; }}
    .cota {{ font-size: 15px; fill: #34415c; }}
  </style>
  <text x="40" y="42" class="titulo">Ventilador Sirocco - esquema dimensional preliminar</text>
  <text x="40" y="72" class="cota">Vista frontal de la voluta y vista axial del rodete de doble entrada</text>
  <polyline points="{texto_puntos}" fill="none" stroke="#175d9c" stroke-width="5"/>
  <circle cx="{origen_x}" cy="{origen_y}" r="{r_rodete:.1f}" fill="#dceeff" stroke="#173f6b" stroke-width="4"/>
  <circle cx="{origen_x}" cy="{origen_y}" r="{r_entrada:.1f}" fill="white" stroke="#3483bd" stroke-width="3" stroke-dasharray="8 7"/>
  <rect x="{salida_x:.1f}" y="{salida_y:.1f}" width="{ancho_salida:.1f}" height="180" fill="none" stroke="#175d9c" stroke-width="5"/>
  <line x1="{origen_x-r_rodete:.1f}" y1="{origen_y+135:.1f}" x2="{origen_x+r_rodete:.1f}" y2="{origen_y+135:.1f}" stroke="#a33b32" stroke-width="2"/>
  <text x="{origen_x-78:.1f}" y="{origen_y+128:.1f}" class="cota">D2 = {d.diametro_exterior_m:.2f} m</text>
  <text x="{origen_x-72:.1f}" y="{origen_y+8:.1f}" class="cota">D1 = {d.diametro_interior_m:.2f} m</text>
  <text x="700" y="155" class="etiqueta">Salida: {d.ancho_voluta_m:.2f} x {resultado['voluta']['altura_salida_m']:.2f} m</text>
  <text x="700" y="185" class="etiqueta">Holgura lengua: {resultado['voluta']['holgura_lengua_m']*1000:.0f} mm</text>
  <text x="700" y="215" class="etiqueta">Velocidad: {d.rpm:.0f} rpm</text>
  <text x="700" y="245" class="etiqueta">Alabes: {d.numero_alabes}, beta2 = {d.beta2_grados:.0f} grados</text>
  <g transform="translate(705,360)">
    <text x="0" y="-45" class="titulo">Vista axial</text>
    <rect x="0" y="0" width="260" height="180" fill="#dceeff" stroke="#173f6b" stroke-width="4"/>
    <rect x="25" y="22" width="210" height="136" fill="white" stroke="#3483bd" stroke-width="3"/>
    <line x1="-65" y1="90" x2="25" y2="90" stroke="#2a8a4b" stroke-width="5" marker-end="url(#flecha)"/>
    <line x1="325" y1="90" x2="235" y2="90" stroke="#2a8a4b" stroke-width="5" marker-end="url(#flecha)"/>
    <text x="42" y="205" class="cota">Rodete b = {d.ancho_rodete_m:.2f} m</text>
    <text x="32" y="230" class="cota">Voluta B = {d.ancho_voluta_m:.2f} m</text>
    <text x="55" y="75" class="etiqueta">doble entrada</text>
  </g>
  <defs>
    <marker id="flecha" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#2a8a4b"/>
    </marker>
  </defs>
  <text x="40" y="785" class="cota">No usar para fabricar sin cerrar resistencia, tolerancias, balanceo y validacion CFD/experimental.</text>
</svg>
"""
    ruta.write_text(svg, encoding="utf-8")


def exportar(d: DatosDiseno, resultado: dict[str, Any], directorio: Path) -> None:
    directorio.mkdir(parents=True, exist_ok=True)
    resumen = []
    for seccion in ("punto_operacion", "rodete", "potencias", "mecanica"):
        for variable, valor in resultado[seccion].items():
            resumen.append({"seccion": seccion, "variable": variable, "valor": valor})
    for variable, valor in resultado["voluta"].items():
        if variable != "tabla":
            resumen.append({"seccion": "voluta", "variable": variable, "valor": valor})
    _escribir_csv(directorio / "resumen_diseno.csv", resumen)
    _escribir_csv(directorio / "tabla_voluta.csv", resultado["voluta"]["tabla"])
    _escribir_csv(directorio / "presupuesto_perdidas.csv", resultado["perdidas"])
    _escribir_csv(directorio / "semejanza_modelo.csv", semejanza(d))
    (directorio / "resultado_completo.json").write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    generar_svg(d, resultado, directorio / "esquema_dimensional_sirocco.svg")


def imprimir_resumen(r: dict[str, Any]) -> None:
    p = r["punto_operacion"]
    rodete = r["rodete"]
    pot = r["potencias"]
    voluta = r["voluta"]
    mec = r["mecanica"]
    print("Diseno preliminar - Ventilador Sirocco Grupo 2")
    print(f"Punto: {p['caudal_m3_h']:.0f} m3/h y {p['presion_objetivo_pa']:.1f} Pa")
    print(f"beta1 sin incidencia: {rodete['beta1_grados']:.1f} grados")
    print(f"U2: {rodete['u2_m_s']:.2f} m/s; Cm2: {rodete['cm2_m_s']:.2f} m/s")
    print(f"Presion Euler estimada: {rodete['presion_euler_pa']:.1f} Pa")
    print(f"Potencia util: {pot['potencia_util_aire_kw']:.2f} kW")
    print(f"Potencia al eje: {pot['potencia_eje_euler_kw']:.2f} kW")
    print(f"Eficiencia estatica estimada: {pot['eficiencia_estatica_estimada']:.1%}")
    print(f"Salida voluta: {voluta['ancho_interior_m']:.2f} x {voluta['altura_salida_m']:.2f} m")
    print(f"Holgura de lengua: {voluta['holgura_lengua_m']*1000:.0f} mm")
    print(f"Eje minimo por torsion: {mec['diametro_eje_recomendado_mm']:.0f} mm")
    print(f"Margen del motor: {pot['margen_motor_relativo']:.1%}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--caudal", type=float, default=3.0, help="caudal en m3/s")
    parser.add_argument("--presion", type=float, default=90.0, help="presion en mmH2O")
    parser.add_argument("--rpm", type=float, default=1100.0)
    parser.add_argument("--exportar", type=Path, help="directorio para CSV, JSON y SVG")
    parser.add_argument("--json", action="store_true", help="imprime el resultado JSON")
    args = parser.parse_args()

    datos = DatosDiseno(
        caudal_m3_s=args.caudal,
        altura_mmh2o=args.presion,
        rpm=args.rpm,
    )
    resultado = calcular(datos)
    if args.json:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        imprimir_resumen(resultado)
    if args.exportar:
        exportar(datos, resultado, args.exportar)


if __name__ == "__main__":
    main()
