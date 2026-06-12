#!/usr/bin/env python3
"""Genera geometria 2D CAD del rodete y la voluta Sirocco V1.1."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from math import atan2, cos, pi, radians, sin
from pathlib import Path
from typing import Iterable

from calculo_sirocco import DatosDiseno, calcular, tabla_voluta


Punto = tuple[float, float]


@dataclass(frozen=True)
class ArcoAlabe:
    radio_curvatura_m: float
    centro_x_m: float
    centro_y_m: float
    angulo_polar_salida_rad: float
    phi_inicio_rad: float
    phi_fin_rad: float
    beta1_grados: float
    beta2_grados: float


def _producto_cruz(a: Punto, b: Punto) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _residuo_arco(delta: float, r1: float, r2: float, beta1: float, beta2: float) -> float:
    desplazamiento = (r2 * cos(delta) - r1, r2 * sin(delta))
    diferencia_normales = (
        cos(beta1) - cos(delta + beta2),
        sin(beta1) - sin(delta + beta2),
    )
    return _producto_cruz(desplazamiento, diferencia_normales)


def resolver_arco_alabe(d: DatosDiseno, beta1_grados: float) -> ArcoAlabe:
    """Encuentra el arco circular que cumple D1, D2, beta1 y beta2."""
    r1 = d.diametro_interior_m / 2.0
    r2 = d.diametro_exterior_m / 2.0
    beta1 = radians(beta1_grados)
    beta2 = radians(d.beta2_grados)

    muestras: list[tuple[float, float]] = []
    for indice in range(4001):
        delta = -pi + 1e-5 + (2.0 * pi - 2e-5) * indice / 4000.0
        muestras.append((delta, _residuo_arco(delta, r1, r2, beta1, beta2)))

    candidatos = []
    for (a, fa), (b, fb) in zip(muestras, muestras[1:]):
        if fa * fb >= 0.0:
            continue
        izquierda, derecha = a, b
        for _ in range(80):
            medio = 0.5 * (izquierda + derecha)
            fm = _residuo_arco(medio, r1, r2, beta1, beta2)
            if fa * fm <= 0.0:
                derecha = medio
            else:
                izquierda, fa = medio, fm
        delta = 0.5 * (izquierda + derecha)
        diferencia_normales = (
            cos(beta1) - cos(delta + beta2),
            sin(beta1) - sin(delta + beta2),
        )
        norma2 = diferencia_normales[0] ** 2 + diferencia_normales[1] ** 2
        if norma2 < 1e-12:
            continue
        desplazamiento = (r2 * cos(delta) - r1, r2 * sin(delta))
        radio = (
            desplazamiento[0] * diferencia_normales[0]
            + desplazamiento[1] * diferencia_normales[1]
        ) / norma2
        if radio > d.espesor_alabe_m:
            candidatos.append((abs(delta), delta, radio))

    if not candidatos:
        raise ValueError("no se encontro un arco circular compatible con los angulos")

    _, delta, radio = min(candidatos)
    centro_x = r1 + radio * cos(beta1)
    centro_y = radio * sin(beta1)
    phi_inicio = beta1 + pi
    phi_fin = delta + beta2 + pi
    if phi_fin <= phi_inicio:
        phi_fin += 2.0 * pi
    return ArcoAlabe(
        radio_curvatura_m=radio,
        centro_x_m=centro_x,
        centro_y_m=centro_y,
        angulo_polar_salida_rad=delta,
        phi_inicio_rad=phi_inicio,
        phi_fin_rad=phi_fin,
        beta1_grados=beta1_grados,
        beta2_grados=d.beta2_grados,
    )


def puntos_arco(arco: ArcoAlabe, radio: float, cantidad: int = 48) -> list[Punto]:
    return [
        (
            arco.centro_x_m + radio * cos(phi),
            arco.centro_y_m + radio * sin(phi),
        )
        for phi in (
            arco.phi_inicio_rad
            + (arco.phi_fin_rad - arco.phi_inicio_rad) * indice / cantidad
            for indice in range(cantidad + 1)
        )
    ]


def contorno_alabe(d: DatosDiseno, arco: ArcoAlabe) -> list[Punto]:
    exterior = puntos_arco(
        arco, arco.radio_curvatura_m + d.espesor_alabe_m / 2.0
    )
    interior = list(
        reversed(
            puntos_arco(
                arco, arco.radio_curvatura_m - d.espesor_alabe_m / 2.0
            )
        )
    )
    return exterior + interior


def rotar(punto: Punto, angulo: float) -> Punto:
    return (
        punto[0] * cos(angulo) - punto[1] * sin(angulo),
        punto[0] * sin(angulo) + punto[1] * cos(angulo),
    )


def todos_los_alabes(d: DatosDiseno, arco: ArcoAlabe) -> list[list[Punto]]:
    base = contorno_alabe(d, arco)
    return [
        [rotar(punto, 2.0 * pi * indice / d.numero_alabes) for punto in base]
        for indice in range(d.numero_alabes)
    ]


def _dxf_cabecera() -> list[str]:
    return [
        "0", "SECTION", "2", "HEADER", "9", "$ACADVER", "1", "AC1009",
        "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES",
    ]


def _dxf_circulo(centro: Punto, radio_m: float, capa: str) -> list[str]:
    return [
        "0", "CIRCLE", "8", capa,
        "10", f"{centro[0] * 1000.0:.6f}",
        "20", f"{centro[1] * 1000.0:.6f}",
        "30", "0.0", "40", f"{radio_m * 1000.0:.6f}",
    ]


def _dxf_polilinea(puntos: Iterable[Punto], capa: str, cerrada: bool) -> list[str]:
    lineas = ["0", "POLYLINE", "8", capa, "66", "1", "70", "1" if cerrada else "0"]
    for x, y in puntos:
        lineas.extend(
            ["0", "VERTEX", "8", capa, "10", f"{x * 1000.0:.6f}",
             "20", f"{y * 1000.0:.6f}", "30", "0.0"]
        )
    lineas.extend(["0", "SEQEND", "8", capa])
    return lineas


def _dxf_linea(inicio: Punto, fin: Punto, capa: str) -> list[str]:
    return [
        "0", "LINE", "8", capa,
        "10", f"{inicio[0] * 1000.0:.6f}",
        "20", f"{inicio[1] * 1000.0:.6f}", "30", "0.0",
        "11", f"{fin[0] * 1000.0:.6f}",
        "21", f"{fin[1] * 1000.0:.6f}", "31", "0.0",
    ]


def escribir_dxf(ruta: Path, entidades: list[list[str]]) -> None:
    lineas = _dxf_cabecera()
    for entidad in entidades:
        lineas.extend(entidad)
    lineas.extend(["0", "ENDSEC", "0", "EOF"])
    ruta.write_text("\n".join(lineas) + "\n", encoding="ascii")


def perfil_voluta(d: DatosDiseno, paso_grados: int = 2) -> list[Punto]:
    area_salida = d.caudal_m3_s / d.velocidad_descarga_m_s
    holgura = d.holgura_lengua_relativa * d.diametro_exterior_m
    puntos = []
    for theta_grados in range(0, 361, paso_grados):
        fraccion = theta_grados / 360.0
        area = area_salida * fraccion
        radio = (
            d.diametro_exterior_m / 2.0
            + holgura
            + area / d.ancho_voluta_m
        )
        theta = radians(theta_grados)
        puntos.append((radio * cos(theta), radio * sin(theta)))
    return puntos


def generar_dxf_rodete(d: DatosDiseno, arco: ArcoAlabe, ruta: Path) -> None:
    entidades = [
        _dxf_circulo((0.0, 0.0), d.diametro_exterior_m / 2.0, "D2_REFERENCIA"),
        _dxf_circulo((0.0, 0.0), d.diametro_interior_m / 2.0, "D1_REFERENCIA"),
        _dxf_circulo((0.0, 0.0), d.diametro_cubo_m / 2.0, "CUBO_REFERENCIA"),
    ]
    entidades.extend(
        _dxf_polilinea(alabe, "ALABES", True)
        for alabe in todos_los_alabes(d, arco)
    )
    escribir_dxf(ruta, entidades)


def generar_dxf_voluta(d: DatosDiseno, ruta: Path) -> None:
    espiral = perfil_voluta(d)
    holgura = d.holgura_lengua_relativa * d.diametro_exterior_m
    radio_lengua = d.diametro_exterior_m / 2.0 + holgura
    radio_salida = espiral[-1][0]
    longitud_salida = 0.50
    entidades = [
        _dxf_circulo((0.0, 0.0), d.diametro_exterior_m / 2.0, "RODETE_REFERENCIA"),
        _dxf_polilinea(espiral, "VOLUTA_EXTERIOR", False),
        _dxf_linea((radio_lengua, 0.0), (radio_lengua, longitud_salida), "SALIDA"),
        _dxf_linea((radio_salida, 0.0), (radio_salida, longitud_salida), "SALIDA"),
        _dxf_linea((radio_lengua, longitud_salida), (radio_salida, longitud_salida), "SALIDA"),
    ]
    escribir_dxf(ruta, entidades)


def generar_svg(
    d: DatosDiseno,
    arco: ArcoAlabe,
    ruta: Path,
) -> None:
    alabes = todos_los_alabes(d, arco)
    espiral = perfil_voluta(d, 3)
    escala_rodete = 760.0
    escala_voluta = 310.0
    ox1, oy1 = 330.0, 380.0
    ox2, oy2 = 865.0, 380.0

    poligonos = []
    for alabe in alabes:
        puntos = " ".join(
            f"{ox1 + x * escala_rodete:.1f},{oy1 - y * escala_rodete:.1f}"
            for x, y in alabe
        )
        poligonos.append(f'<polygon points="{puntos}" class="alabe"/>')
    puntos_voluta = " ".join(
        f"{ox2 + x * escala_voluta:.1f},{oy2 - y * escala_voluta:.1f}"
        for x, y in espiral
    )
    r2_px_rodete = d.diametro_exterior_m / 2.0 * escala_rodete
    r1_px_rodete = d.diametro_interior_m / 2.0 * escala_rodete
    r2_px_voluta = d.diametro_exterior_m / 2.0 * escala_voluta
    radio_lengua = (
        d.diametro_exterior_m / 2.0
        + d.holgura_lengua_relativa * d.diametro_exterior_m
    )
    radio_salida = espiral[-1][0]
    longitud_salida = 0.50
    puntos_salida = " ".join(
        f"{ox2 + x * escala_voluta:.1f},{oy2 - y * escala_voluta:.1f}"
        for x, y in (
            (radio_lengua, 0.0),
            (radio_lengua, longitud_salida),
            (radio_salida, longitud_salida),
            (radio_salida, 0.0),
        )
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1250" height="760" viewBox="0 0 1250 760">
  <rect width="1250" height="760" fill="white"/>
  <style>
    text {{ font-family: Arial, sans-serif; fill: #172033; }}
    .titulo {{ font-size: 25px; font-weight: bold; }}
    .subtitulo {{ font-size: 20px; font-weight: bold; }}
    .nota {{ font-size: 15px; fill: #3c4963; }}
    .alabe {{ fill: #69aee6; stroke: #164b76; stroke-width: 0.8; }}
  </style>
  <text x="35" y="38" class="titulo">Geometria CAD 2D V1.1 - ventilador Sirocco</text>
  <text x="35" y="66" class="nota">Coordenadas DXF en milimetros. Verificar CFD, resistencia y tolerancias antes de fabricar.</text>
  <text x="235" y="105" class="subtitulo">Rodete, 48 alabes</text>
  {''.join(poligonos)}
  <circle cx="{ox1}" cy="{oy1}" r="{r2_px_rodete:.1f}" fill="none" stroke="#173f6b" stroke-width="3"/>
  <circle cx="{ox1}" cy="{oy1}" r="{r1_px_rodete:.1f}" fill="none" stroke="#4a88b7" stroke-width="2" stroke-dasharray="7 5"/>
  <circle cx="{ox1}" cy="{oy1}" r="{d.diametro_cubo_m/2*escala_rodete:.1f}" fill="#d9dde5" stroke="#333" stroke-width="2"/>
  <text x="150" y="690" class="nota">D2 = 600 mm; D1 = 510 mm; arco R = {arco.radio_curvatura_m*1000:.1f} mm</text>
  <text x="150" y="714" class="nota">beta1 = {arco.beta1_grados:.1f} grados; beta2 = {arco.beta2_grados:.1f} grados; espesor = {d.espesor_alabe_m*1000:.1f} mm</text>
  <text x="830" y="105" class="subtitulo">Voluta</text>
  <polyline points="{puntos_voluta}" fill="none" stroke="#175d9c" stroke-width="5"/>
  <polyline points="{puntos_salida}" fill="none" stroke="#175d9c" stroke-width="5"/>
  <circle cx="{ox2}" cy="{oy2}" r="{r2_px_voluta:.1f}" fill="#e8f3fc" stroke="#173f6b" stroke-width="3"/>
  <text x="745" y="690" class="nota">B = 280 mm; lengua = 48 mm; salida = 280 x 714 mm</text>
  <text x="745" y="714" class="nota">Radio exterior final = {espiral[-1][0]*1000:.1f} mm</text>
</svg>
"""
    ruta.write_text(svg, encoding="utf-8")


def exportar(directorio: Path, d: DatosDiseno | None = None) -> dict[str, float]:
    d = d or DatosDiseno()
    resultado = calcular(d)
    beta1 = round(resultado["rodete"]["beta1_grados"] * 2.0) / 2.0
    arco = resolver_arco_alabe(d, beta1)
    directorio.mkdir(parents=True, exist_ok=True)

    centro = puntos_arco(arco, arco.radio_curvatura_m, 80)
    with (directorio / "perfil_alabe_v1.csv").open(
        "w", newline="", encoding="utf-8"
    ) as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(["indice", "x_mm", "y_mm", "radio_global_mm", "theta_global_grados"])
        for indice, (x, y) in enumerate(centro):
            escritor.writerow(
                [
                    indice,
                    f"{x * 1000.0:.6f}",
                    f"{y * 1000.0:.6f}",
                    f"{(x*x + y*y) ** 0.5 * 1000.0:.6f}",
                    f"{atan2(y, x) * 180.0 / pi:.6f}",
                ]
            )

    generar_dxf_rodete(d, arco, directorio / "rodete_sirocco_v1.dxf")
    generar_dxf_voluta(d, directorio / "voluta_sirocco_v1.dxf")
    generar_svg(d, arco, directorio / "geometria_cad_v1.svg")
    parametros = {
        **asdict(arco),
        "diametro_exterior_m": d.diametro_exterior_m,
        "diametro_interior_m": d.diametro_interior_m,
        "ancho_rodete_m": d.ancho_rodete_m,
        "numero_alabes": d.numero_alabes,
        "espesor_alabe_m": d.espesor_alabe_m,
        "radio_exterior_final_voluta_m": tabla_voluta(d)[-1]["radio_exterior_m"],
    }
    (directorio / "parametros_geometria_v1.json").write_text(
        json.dumps(parametros, indent=2), encoding="utf-8"
    )
    return parametros


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida", type=Path, default=Path("07_planos"), help="directorio de salida"
    )
    args = parser.parse_args()
    parametros = exportar(args.salida)
    print("Geometria CAD generada")
    print(f"Radio del arco del alabe: {parametros['radio_curvatura_m']*1000:.2f} mm")
    print(
        "Desfase polar entrada-salida: "
        f"{parametros['angulo_polar_salida_rad']*180.0/pi:.2f} grados"
    )
    print(f"Archivos: {args.salida.resolve()}")


if __name__ == "__main__":
    main()
