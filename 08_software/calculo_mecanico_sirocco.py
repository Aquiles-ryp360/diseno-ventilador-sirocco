#!/usr/bin/env python3
"""Predimensionamiento mecanico del conjunto rotativo del ventilador Sirocco."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from math import ceil, pi, sqrt
from pathlib import Path

from calculo_sirocco import DatosDiseno, calcular
from generar_geometria_cad import resolver_arco_alabe


@dataclass(frozen=True)
class DatosMecanicos:
    densidad_acero_kg_m3: float = 7850.0
    espesor_anillos_m: float = 0.002
    espesor_disco_central_m: float = 0.003
    diametro_exterior_cubo_m: float = 0.080
    longitud_cubo_m: float = 0.080
    factor_masa_soldadura: float = 1.08
    luz_rodamientos_m: float = 0.50
    posicion_rodete_m: float = 0.25
    voladizo_polea_m: float = 0.075
    diametro_polea_ventilador_m: float = 0.20
    factor_carga_correa: float = 2.5
    factor_choque_flexion: float = 1.5
    factor_choque_torsion: float = 1.5
    factor_chavetero_diametro: float = 1.20
    esfuerzo_cortante_admisible_pa: float = 30e6
    modulo_elasticidad_pa: float = 200e9
    vida_objetivo_h: float = 20_000.0


def calcular_mecanica(
    aero: DatosDiseno | None = None,
    mecanica: DatosMecanicos | None = None,
) -> dict:
    aero = aero or DatosDiseno()
    mecanica = mecanica or DatosMecanicos()
    resultado_aero = calcular(aero)
    beta1 = round(resultado_aero["rodete"]["beta1_grados"] * 2.0) / 2.0
    arco = resolver_arco_alabe(aero, beta1)
    longitud_alabe = arco.radio_curvatura_m * (arco.phi_fin_rad - arco.phi_inicio_rad)

    volumen_alabes = (
        aero.numero_alabes
        * longitud_alabe
        * aero.ancho_rodete_m
        * aero.espesor_alabe_m
    )
    volumen_anillos = (
        2.0
        * pi
        / 4.0
        * (aero.diametro_exterior_m**2 - aero.diametro_interior_m**2)
        * mecanica.espesor_anillos_m
    )
    volumen_disco = (
        pi
        / 4.0
        * (aero.diametro_exterior_m**2 - mecanica.diametro_exterior_cubo_m**2)
        * mecanica.espesor_disco_central_m
    )
    diametro_eje_iteracion = 0.035
    volumen_cubo = (
        pi
        / 4.0
        * (mecanica.diametro_exterior_cubo_m**2 - diametro_eje_iteracion**2)
        * mecanica.longitud_cubo_m
    )
    masas = {
        "alabes_kg": volumen_alabes * mecanica.densidad_acero_kg_m3,
        "anillos_entrada_kg": volumen_anillos * mecanica.densidad_acero_kg_m3,
        "disco_central_kg": volumen_disco * mecanica.densidad_acero_kg_m3,
        "cubo_kg": volumen_cubo * mecanica.densidad_acero_kg_m3,
    }
    masa_subtotal = sum(masas.values())
    masa_rotor = masa_subtotal * mecanica.factor_masa_soldadura
    peso_rotor = masa_rotor * 9.80665

    potencia_eje_w = resultado_aero["potencias"]["potencia_eje_euler_kw"] * 1000.0
    omega = 2.0 * pi * aero.rpm / 60.0
    torque = potencia_eje_w / omega
    fuerza_tangencial_correa = 2.0 * torque / mecanica.diametro_polea_ventilador_m
    carga_radial_correa = fuerza_tangencial_correa * mecanica.factor_carga_correa

    luz = mecanica.luz_rodamientos_m
    x_rodete = mecanica.posicion_rodete_m
    x_polea = luz + mecanica.voladizo_polea_m
    reaccion_b = (peso_rotor * x_rodete + carga_radial_correa * x_polea) / luz
    reaccion_a = peso_rotor + carga_radial_correa - reaccion_b

    momentos = []
    for indice in range(1001):
        x = x_polea * indice / 1000.0
        momento = reaccion_a * x
        if x >= luz:
            momento += reaccion_b * (x - luz)
        if x >= x_rodete:
            momento -= peso_rotor * (x - x_rodete)
        if x >= x_polea:
            momento -= carga_radial_correa * (x - x_polea)
        momentos.append((x, momento))
    x_momento, momento_maximo = max(momentos, key=lambda fila: abs(fila[1]))
    momento_equivalente = sqrt(
        (mecanica.factor_choque_flexion * momento_maximo) ** 2
        + (mecanica.factor_choque_torsion * torque) ** 2
    )
    diametro_asme = (
        16.0
        * abs(momento_equivalente)
        / (pi * mecanica.esfuerzo_cortante_admisible_pa)
    ) ** (1.0 / 3.0)
    diametro_con_chavetero = diametro_asme * mecanica.factor_chavetero_diametro
    diametro_recomendado_mm = ceil(diametro_con_chavetero * 1000.0 / 5.0) * 5.0

    diametro_eje_m = diametro_recomendado_mm / 1000.0
    inercia_eje = pi * diametro_eje_m**4 / 64.0
    flecha_estatica = (
        peso_rotor
        * luz**3
        / (48.0 * mecanica.modulo_elasticidad_pa * inercia_eje)
    )
    rpm_critica = 30.0 / pi * sqrt(9.80665 / flecha_estatica)

    carga_rodamiento = max(abs(reaccion_a), abs(reaccion_b))
    millones_revoluciones = 60.0 * aero.rpm * mecanica.vida_objetivo_h / 1e6
    capacidad_dinamica_requerida = carga_rodamiento * millones_revoluciones ** (1.0 / 3.0)

    masa_alabe = masas["alabes_kg"] / aero.numero_alabes
    radio_medio = (aero.diametro_interior_m + aero.diametro_exterior_m) / 4.0
    fuerza_centrifuga_alabe = masa_alabe * omega**2 * radio_medio
    tension_centrifuga_referencia = mecanica.densidad_acero_kg_m3 * (
        pi * aero.diametro_exterior_m * aero.rpm / 60.0
    ) ** 2

    return {
        "entradas_mecanicas": asdict(mecanica),
        "geometria": {
            "longitud_linea_media_alabe_mm": longitud_alabe * 1000.0,
            "diametro_polea_ventilador_mm": mecanica.diametro_polea_ventilador_m * 1000.0,
        },
        "masas": {
            **masas,
            "masa_subtotal_kg": masa_subtotal,
            "masa_rotor_con_soldadura_kg": masa_rotor,
            "peso_rotor_n": peso_rotor,
        },
        "cargas": {
            "torque_nominal_nm": torque,
            "fuerza_tangencial_correa_n": fuerza_tangencial_correa,
            "carga_radial_correa_n": carga_radial_correa,
            "reaccion_rodamiento_a_n": reaccion_a,
            "reaccion_rodamiento_b_n": reaccion_b,
            "momento_flector_maximo_nm": abs(momento_maximo),
            "posicion_momento_maximo_m": x_momento,
            "fuerza_centrifuga_por_alabe_n": fuerza_centrifuga_alabe,
            "tension_centrifuga_referencia_mpa": tension_centrifuga_referencia / 1e6,
        },
        "eje": {
            "momento_equivalente_nm": abs(momento_equivalente),
            "diametro_asme_sin_chavetero_mm": diametro_asme * 1000.0,
            "diametro_con_factor_chavetero_mm": diametro_con_chavetero * 1000.0,
            "diametro_recomendado_mm": diametro_recomendado_mm,
            "flecha_estatica_centro_mm": flecha_estatica * 1000.0,
            "primera_velocidad_critica_rpm": rpm_critica,
            "relacion_critica_operacion": rpm_critica / aero.rpm,
        },
        "rodamientos": {
            "vida_objetivo_h": mecanica.vida_objetivo_h,
            "carga_radial_calculo_n": carga_rodamiento,
            "capacidad_dinamica_minima_kn": capacidad_dinamica_requerida / 1000.0,
            "diametro_interior_requerido_mm": diametro_recomendado_mm,
        },
    }


def exportar(directorio: Path) -> dict:
    resultado = calcular_mecanica()
    directorio.mkdir(parents=True, exist_ok=True)
    (directorio / "resultado_mecanico_v1.json").write_text(
        json.dumps(resultado, indent=2), encoding="utf-8"
    )
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida", type=Path, default=Path("06_calculos/resultados_mecanicos_v1")
    )
    args = parser.parse_args()
    r = exportar(args.salida)
    print("Predimensionamiento mecanico V1")
    print(f"Masa estimada del rotor: {r['masas']['masa_rotor_con_soldadura_kg']:.2f} kg")
    print(f"Carga radial de correa: {r['cargas']['carga_radial_correa_n']:.0f} N")
    print(f"Momento flector maximo: {r['cargas']['momento_flector_maximo_nm']:.1f} N m")
    print(f"Eje recomendado: {r['eje']['diametro_recomendado_mm']:.0f} mm")
    print(f"Primera velocidad critica: {r['eje']['primera_velocidad_critica_rpm']:.0f} rpm")
    print(f"Capacidad dinamica minima de rodamiento: {r['rodamientos']['capacidad_dinamica_minima_kn']:.1f} kN")


if __name__ == "__main__":
    main()
