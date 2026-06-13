#!/usr/bin/env python3
"""Genera modelos OBJ y datos JavaScript del ventilador Sirocco V1.2."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from math import cos, pi, sin
from pathlib import Path

from calculo_mecanico_sirocco import calcular_mecanica
from calculo_sirocco import DatosDiseno, calcular, tabla_voluta
from generar_geometria_cad import contorno_alabe, perfil_voluta, resolver_arco_alabe, rotar


Punto2D = tuple[float, float]
Punto3D = tuple[float, float, float]
Cara = tuple[int, ...]


@dataclass
class ModeloOBJ:
    vertices: list[Punto3D] = field(default_factory=list)
    secciones: list[tuple[str, str, list[Cara]]] = field(default_factory=list)

    def agregar(self, nombre: str, material: str, vertices: list[Punto3D], caras: list[Cara]) -> None:
        desplazamiento = len(self.vertices)
        self.vertices.extend(vertices)
        self.secciones.append(
            (nombre, material, [tuple(indice + desplazamiento for indice in cara) for cara in caras])
        )

    def escribir(self, ruta: Path, nombre_mtl: str = "materiales_sirocco.mtl") -> None:
        lineas = [
            "# Ventilador centrifugo Sirocco V1.2",
            "# Unidades: milimetros",
            f"mtllib {nombre_mtl}",
        ]
        for x, y, z in self.vertices:
            lineas.append(f"v {x:.6f} {y:.6f} {z:.6f}")
        for nombre, material, caras in self.secciones:
            lineas.extend((f"o {nombre}", f"usemtl {material}"))
            for cara in caras:
                lineas.append("f " + " ".join(str(indice + 1) for indice in cara))
        ruta.write_text("\n".join(lineas) + "\n", encoding="ascii")


def prisma_poligono(poligono: list[Punto2D], z0: float, z1: float) -> tuple[list[Punto3D], list[Cara]]:
    n = len(poligono)
    vertices = [(x, y, z0) for x, y in poligono] + [(x, y, z1) for x, y in poligono]
    cx = sum(x for x, _ in poligono) / n
    cy = sum(y for _, y in poligono) / n
    centro0 = len(vertices)
    vertices.append((cx, cy, z0))
    centro1 = len(vertices)
    vertices.append((cx, cy, z1))
    caras: list[Cara] = []
    for i in range(n):
        j = (i + 1) % n
        caras.extend(
            [
                (i, j, n + j, n + i),
                (centro0, j, i),
                (centro1, n + i, n + j),
            ]
        )
    return vertices, caras


def cilindro_anular(r_exterior: float, r_interior: float, z0: float, z1: float, segmentos: int = 96) -> tuple[list[Punto3D], list[Cara]]:
    vertices: list[Punto3D] = []
    for z in (z0, z1):
        for radio in (r_exterior, r_interior):
            vertices.extend(
                (radio * cos(2 * pi * i / segmentos), radio * sin(2 * pi * i / segmentos), z)
                for i in range(segmentos)
            )
    caras: list[Cara] = []
    oe, ie, os, is_ = 0, segmentos, 2 * segmentos, 3 * segmentos
    for i in range(segmentos):
        j = (i + 1) % segmentos
        caras.extend(
            [
                (oe + i, oe + j, os + j, os + i),
                (ie + j, ie + i, is_ + i, is_ + j),
                (os + i, os + j, is_ + j, is_ + i),
                (oe + j, oe + i, ie + i, ie + j),
            ]
        )
    return vertices, caras


def cilindro_solido(radio: float, z0: float, z1: float, segmentos: int = 72) -> tuple[list[Punto3D], list[Cara]]:
    vertices = [
        (radio * cos(2 * pi * i / segmentos), radio * sin(2 * pi * i / segmentos), z)
        for z in (z0, z1)
        for i in range(segmentos)
    ]
    vertices.extend([(0.0, 0.0, z0), (0.0, 0.0, z1)])
    c0, c1 = 2 * segmentos, 2 * segmentos + 1
    caras: list[Cara] = []
    for i in range(segmentos):
        j = (i + 1) % segmentos
        caras.extend(
            [
                (i, j, segmentos + j, segmentos + i),
                (c0, j, i),
                (c1, segmentos + i, segmentos + j),
            ]
        )
    return vertices, caras


def caja(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> tuple[list[Punto3D], list[Cara]]:
    vertices = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    caras = [
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0),
    ]
    return vertices, caras


def pasaje_voluta(d: DatosDiseno, segmentos: int = 180) -> tuple[list[Punto3D], list[Cara]]:
    z0, z1 = -d.ancho_voluta_m * 500.0, d.ancho_voluta_m * 500.0
    r_interior = (d.diametro_exterior_m / 2.0 + d.holgura_lengua_relativa * d.diametro_exterior_m) * 1000.0
    area_salida = d.caudal_m3_s / d.velocidad_descarga_m_s
    vertices: list[Punto3D] = []
    for z in (z0, z1):
        for i in range(segmentos + 1):
            theta = 2.0 * pi * i / segmentos
            area = area_salida * i / segmentos
            r_ext = (d.diametro_exterior_m / 2.0 + d.holgura_lengua_relativa * d.diametro_exterior_m + area / d.ancho_voluta_m) * 1000.0
            vertices.extend(
                [
                    (r_interior * cos(theta), r_interior * sin(theta), z),
                    (r_ext * cos(theta), r_ext * sin(theta), z),
                ]
            )
    capa = 2 * (segmentos + 1)
    caras: list[Cara] = []
    for i in range(segmentos):
        a, b = 2 * i, 2 * i + 1
        c, e = 2 * (i + 1), 2 * (i + 1) + 1
        caras.extend(
            [
                (a, c, e, b),
                (capa + a, capa + b, capa + e, capa + c),
                (a, capa + a, capa + c, c),
                (b, e, capa + e, capa + b),
            ]
        )
    return vertices, caras


def agregar_rodete(modelo: ModeloOBJ, d: DatosDiseno) -> None:
    resultado = calcular(d)
    beta1 = round(resultado["rodete"]["beta1_grados"] * 2.0) / 2.0
    arco = resolver_arco_alabe(d, beta1)
    base = [(x * 1000.0, y * 1000.0) for x, y in contorno_alabe(d, arco)]
    z0, z1 = -d.ancho_rodete_m * 500.0, d.ancho_rodete_m * 500.0
    for indice in range(d.numero_alabes):
        angulo = 2.0 * pi * indice / d.numero_alabes
        poligono = [rotar(punto, angulo) for punto in base]
        modelo.agregar(f"alabe_{indice + 1:02d}", "alabes", *prisma_poligono(poligono, z0, z1))
    modelo.agregar("anillo_entrada_1", "anillos", *cilindro_anular(300.0, 255.0, z0 - 2.0, z0))
    modelo.agregar("anillo_entrada_2", "anillos", *cilindro_anular(300.0, 255.0, z1, z1 + 2.0))
    modelo.agregar("disco_central", "disco", *cilindro_anular(300.0, 40.0, -1.5, 1.5))
    modelo.agregar("cubo", "cubo", *cilindro_anular(40.0, 17.5, -40.0, 40.0))
    modelo.agregar("eje", "eje", *cilindro_solido(17.5, -360.0, 360.0))
    modelo.agregar("polea", "polea", *cilindro_anular(100.0, 18.0, 245.0, 285.0))


def agregar_voluta(modelo: ModeloOBJ, d: DatosDiseno) -> None:
    modelo.agregar("pasaje_espiral", "voluta", *pasaje_voluta(d))
    r0 = (d.diametro_exterior_m / 2.0 + d.holgura_lengua_relativa * d.diametro_exterior_m) * 1000.0
    r1 = tabla_voluta(d)[-1]["radio_exterior_m"] * 1000.0
    z0, z1 = -d.ancho_voluta_m * 500.0, d.ancho_voluta_m * 500.0
    modelo.agregar("descarga", "voluta", *caja(r0, r1, 0.0, 500.0, z0, z1))


def escribir_mtl(ruta: Path) -> None:
    ruta.write_text(
        """# Materiales del ventilador Sirocco
newmtl alabes
Kd 0.08 0.42 0.78
Ks 0.55 0.55 0.55
Ns 80
newmtl anillos
Kd 0.12 0.55 0.88
Ks 0.6 0.6 0.6
Ns 100
newmtl disco
Kd 0.17 0.30 0.43
newmtl cubo
Kd 0.18 0.20 0.23
newmtl eje
Kd 0.55 0.58 0.62
Ks 0.75 0.75 0.75
Ns 120
newmtl polea
Kd 0.85 0.38 0.08
newmtl voluta
Kd 0.10 0.62 0.72
d 0.32
Tr 0.68
""",
        encoding="ascii",
    )


def datos_interfaz(d: DatosDiseno) -> dict:
    aero = calcular(d)
    mecanico = calcular_mecanica(d)
    beta1 = round(aero["rodete"]["beta1_grados"] * 2.0) / 2.0
    arco = resolver_arco_alabe(d, beta1)
    alabe = [[x * 1000.0, y * 1000.0] for x, y in contorno_alabe(d, arco)]
    espiral = [[x * 1000.0, y * 1000.0] for x, y in perfil_voluta(d, 3)]
    return {
        "version": "V1.2",
        "dimensiones": {
            "D2_mm": d.diametro_exterior_m * 1000.0,
            "D1_mm": d.diametro_interior_m * 1000.0,
            "ancho_rodete_mm": d.ancho_rodete_m * 1000.0,
            "ancho_voluta_mm": d.ancho_voluta_m * 1000.0,
            "eje_mm": mecanico["eje"]["diametro_recomendado_mm"],
            "cubo_exterior_mm": 80.0,
            "numero_alabes": d.numero_alabes,
            "espesor_alabe_mm": d.espesor_alabe_m * 1000.0,
            "holgura_lengua_mm": d.holgura_lengua_relativa * d.diametro_exterior_m * 1000.0,
            "altura_descarga_mm": aero["voluta"]["altura_salida_m"] * 1000.0,
            "radio_final_voluta_mm": tabla_voluta(d)[-1]["radio_exterior_m"] * 1000.0,
        },
        "operacion": {
            "caudal_m3_s": d.caudal_m3_s,
            "caudal_m3_h": aero["punto_operacion"]["caudal_m3_h"],
            "presion_pa": aero["punto_operacion"]["presion_objetivo_pa"],
            "presion_mmh2o": d.altura_mmh2o,
            "rpm": d.rpm,
            "potencia_eje_kw": aero["potencias"]["potencia_eje_euler_kw"],
            "motor_kw": d.potencia_motor_kw,
            "eficiencia_estatica": aero["potencias"]["eficiencia_estatica_estimada"],
            "masa_rotor_kg": mecanico["masas"]["masa_rotor_con_soldadura_kg"],
        },
        "geometria": {
            "contorno_alabe_mm": alabe,
            "espiral_voluta_mm": espiral,
        },
    }


def exportar(directorio: Path) -> dict:
    d = DatosDiseno()
    directorio.mkdir(parents=True, exist_ok=True)
    escribir_mtl(directorio / "materiales_sirocco.mtl")

    rodete = ModeloOBJ()
    agregar_rodete(rodete, d)
    rodete.escribir(directorio / "rodete_sirocco_v1_2.obj")

    voluta = ModeloOBJ()
    agregar_voluta(voluta, d)
    voluta.escribir(directorio / "voluta_sirocco_v1_2.obj")

    conjunto = ModeloOBJ()
    agregar_rodete(conjunto, d)
    agregar_voluta(conjunto, d)
    conjunto.escribir(directorio / "conjunto_sirocco_v1_2.obj")

    datos = datos_interfaz(d)
    (directorio / "modelo_sirocco_v1_2.json").write_text(
        json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (directorio / "modelo_sirocco_v1_2.js").write_text(
        "window.SIROCCO_DATA = "
        + json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    return datos


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=Path("07_modelos_3d"))
    args = parser.parse_args()
    datos = exportar(args.salida)
    print("Modelos 3D generados en", args.salida.resolve())
    print("Rodete:", datos["dimensiones"]["D2_mm"], "mm x", datos["dimensiones"]["ancho_rodete_mm"], "mm")
    print("Alabes:", datos["dimensiones"]["numero_alabes"])


if __name__ == "__main__":
    main()
