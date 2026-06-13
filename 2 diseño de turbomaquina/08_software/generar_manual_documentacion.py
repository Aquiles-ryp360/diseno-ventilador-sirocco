#!/usr/bin/env python3
"""Compila la documentación de todas las carpetas en un manual visual."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT_DISENO = Path(__file__).resolve().parents[1]
ROOT_REP = Path(__file__).resolve().parents[2]
SALIDA = ROOT_DISENO / "11_documentacion"
BASE = SALIDA / "Manual_Documentacion_Proyecto_Sirocco"

DOCUMENTOS = [
    ROOT_DISENO / "00_gestion" / "DOCUMENTACION.md",
    ROOT_DISENO / "04_bibliografia" / "DOCUMENTACION.md",
    ROOT_DISENO / "05_avances" / "DOCUMENTACION.md",
    ROOT_DISENO / "06_calculos" / "DOCUMENTACION.md",
    ROOT_DISENO / "07_planos" / "DOCUMENTACION.md",
    ROOT_DISENO / "07_modelos_3d" / "DOCUMENTACION.md",
    ROOT_DISENO / "08_software" / "DOCUMENTACION.md",
    ROOT_DISENO / "09_reporte" / "DOCUMENTACION.md",
    ROOT_DISENO / "10_interfaz_3d" / "DOCUMENTACION.md",
    ROOT_REP / "1 artículo de investigación" / "DOCUMENTACION.md",
    ROOT_REP / "2 diseño de turbomaquina" / "DOCUMENTACION.md",
    ROOT_REP / "3 resolución de problemas" / "DOCUMENTACION.md",
    ROOT_DISENO / "documento_latex" / "DOCUMENTACION.md",
    ROOT_DISENO / "presentacion" / "DOCUMENTACION.md",
]

FIGURAS_POR_DOCUMENTO = {
    "06_calculos": [
        ("../09_reporte/figuras/perdidas_presion.png", "Presupuesto unidimensional de pérdidas."),
        ("../09_reporte/figuras/ley_area_voluta.png", "Crecimiento del área y radio de la voluta."),
        ("../09_reporte/figuras/leyes_afinidad.png", "Leyes de afinidad a diámetro constante."),
        ("../09_reporte/figuras/momento_flector.png", "Momento flector preliminar del eje."),
    ],
    "07_planos": [
        ("../09_reporte/figuras/geometria_cad_2d.png", "Geometría CAD 2D del rodete y la voluta."),
    ],
    "07_modelos_3d": [
        ("../09_reporte/figuras/modelo_3d_rotor.png", "Rodete de doble entrada, eje y polea."),
        ("../09_reporte/figuras/modelo_3d_assembly.png", "Conjunto conceptual con carcasa espiral."),
    ],
    "10_interfaz_3d": [
        ("../09_reporte/figuras/interfaz_3d.png", "Interfaz gráfica 3D autónoma."),
    ],
}


def figura(ruta: str, leyenda: str) -> str:
    return (
        '\n<div class="figure">\n'
        f'<img src="{ruta}" alt="{leyenda}">\n'
        f'<p>{leyenda}</p>\n'
        "</div>\n"
    )


def portada() -> str:
    return """
<div class="cover">
  <p class="cover-kicker">PROYECTO DE TURBOMÁQUINAS · GRUPO 2</p>
  <h1>Manual integral del diseño del ventilador centrífugo Sirocco</h1>
  <p class="cover-subtitle">Documentación por carpetas, ecuaciones, resultados, planos, modelo 3D, software e informe técnico</p>
  <img src="../09_reporte/figuras/modelo_3d_assembly.png" alt="Modelo 3D del ventilador Sirocco">
  <div class="cover-data">
    <span>10 800 m³/h</span><span>882.6 Pa</span><span>1100 rpm</span><span>5.5 kW</span>
  </div>
  <p class="cover-school"><b>Universidad Nacional del Altiplano</b><br>
  Curso: Turbomáquinas · Docente: Ing. Armando Cruz Cabrera<br><br>
  Dilmar Humberto Siguayro Coila · Aquiles Taylor Ramos Yapo<br>
  Renzo Gabriel Mamani Galindo · Martin Calla Quispe · Abel Yovani Rivera Quispe<br><br>
  github.com/Aquiles-ryp360/diseno-ventilador-sirocco<br>
  Puno, 2026 · Revisión V1.2</p>
</div>

# Guía de lectura

Este manual explica cada carpeta del repositorio y reúne las ecuaciones usadas
en el predimensionamiento. La fuente vigente son los scripts Python, las
memorias de `06_calculos/` y los resultados generados. El diseño todavía
requiere CFD, análisis estructural, balanceo y ensayo antes de fabricar.

## Contenido

1. Gestión y planificación.
2. Bibliografía y estado del arte.
3. Avances académicos.
4. Cálculos aerodinámicos y mecánicos.
5. Planos y geometría CAD 2D.
6. Modelos 3D.
7. Software y pruebas.
8. Informe y figuras.
9. Interfaz gráfica offline.
10. Documentos originales del curso.
11. Informe LaTeX y presentación.

## Resultados principales

| Parámetro | Selección vigente |
|---|---:|
| Caudal | 3.0 m³/s = 10 800 m³/h |
| Presión estática | 90 mmH₂O = 882.6 Pa |
| Rodete | D2 600 mm, D1 510 mm, ancho 230 mm |
| Álabes | 48, curvados hacia adelante |
| Velocidad | 1100 rpm |
| Motor | 5.5 kW |
| Eje preliminar | 35 mm |
| Voluta | ancho 280 mm, descarga 280 × 714 mm |

<div class="page-break"></div>
"""


def ensamblar_markdown() -> Path:
    partes = [portada()]
    for documento in DOCUMENTOS:
        texto = documento.read_text(encoding="utf-8")
        partes.append(texto)
        clave = documento.parent.name
        for ruta, leyenda in FIGURAS_POR_DOCUMENTO.get(clave, []):
            partes.append(figura(ruta, leyenda))
        partes.append('\n<div class="page-break"></div>\n')
    ruta = BASE.with_suffix(".md")
    ruta.write_text("\n\n".join(partes), encoding="utf-8")
    return ruta


def ejecutar(*args: str) -> None:
    subprocess.run(args, cwd=ROOT_DISENO, check=True)


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    markdown = ensamblar_markdown()
    html = BASE.with_suffix(".html")
    pdf = BASE.with_suffix(".pdf")
    docx = BASE.with_suffix(".docx")
    css = SALIDA / "manual.css"

    ejecutar(
        "pandoc",
        str(markdown),
        "--from=gfm+raw_html",
        "--standalone",
        "--metadata",
        "pagetitle=Manual integral del proyecto Sirocco",
        "--css",
        str(css.name),
        "--output",
        str(html),
    )
    chrome_path = "chromium"
    for path in [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    ]:
        if Path(path).exists():
            chrome_path = path
            break

    ejecutar(
        chrome_path,
        "--headless",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    )
    ejecutar(
        "pandoc",
        str(markdown),
        "--from=gfm+raw_html",
        "--toc",
        "--toc-depth=2",
        "--output",
        str(docx),
    )
    print(f"Manual PDF: {pdf}")
    print(f"Manual DOCX: {docx}")


if __name__ == "__main__":
    main()
