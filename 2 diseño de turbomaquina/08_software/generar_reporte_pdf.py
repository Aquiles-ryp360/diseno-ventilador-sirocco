#!/usr/bin/env python3
"""Genera la memoria tecnica PDF del ventilador centrifugo Sirocco."""

from __future__ import annotations

import sys
from datetime import date
from math import pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "08_software"))

from calculo_mecanico_sirocco import DatosMecanicos, calcular_mecanica  # noqa: E402
from calculo_sirocco import DatosDiseno, calcular, semejanza  # noqa: E402


AZUL = colors.HexColor("#0B2239")
CIAN = colors.HexColor("#00A6C8")
NARANJA = colors.HexColor("#F39C3D")
GRIS = colors.HexColor("#586875")
CLARO = colors.HexColor("#EAF3F7")
BLANCO = colors.white

SALIDA = ROOT / "09_reporte"
FIGURAS = SALIDA / "figuras"
PDF = SALIDA / "Informe_Diseno_Ventilador_Sirocco.pdf"
MD = SALIDA / "Informe_Diseno_Ventilador_Sirocco.md"

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def registrar_fuentes() -> None:
    global FONT_REGULAR, FONT_BOLD
    paths = [
        ("/usr/share/fonts/TTF/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("C:\\Windows\\Fonts\\DejaVuSans.ttf", "C:\\Windows\\Fonts\\DejaVuSans-Bold.ttf"),
        ("C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"),
    ]
    for r_path, b_path in paths:
        if Path(r_path).exists() and Path(b_path).exists():
            try:
                pdfmetrics.registerFont(TTFont("DejaVu", str(r_path)))
                pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(b_path)))
                pdfmetrics.registerFontFamily(
                    "DejaVu", normal="DejaVu", bold="DejaVu-Bold"
                )
                FONT_REGULAR = "DejaVu"
                FONT_BOLD = "DejaVu-Bold"
                break
            except Exception:
                pass


def estilos() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle(
            "Titulo",
            parent=base["Title"],
            fontName=FONT_BOLD,
            fontSize=25,
            leading=30,
            textColor=BLANCO,
            alignment=TA_LEFT,
            spaceAfter=10,
        ),
        "subtitulo": ParagraphStyle(
            "Subtitulo",
            parent=base["Normal"],
            fontName=FONT_REGULAR,
            fontSize=12,
            leading=17,
            textColor=colors.HexColor("#BDEFFF"),
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=FONT_BOLD,
            fontSize=17,
            leading=21,
            textColor=AZUL,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=FONT_BOLD,
            fontSize=11.5,
            leading=15,
            textColor=CIAN,
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9.2,
            leading=13.4,
            textColor=colors.HexColor("#243540"),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=7.5,
            leading=10,
            textColor=GRIS,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=7.4,
            leading=10,
            textColor=GRIS,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=13,
            leftIndent=13,
            firstLineIndent=-8,
            bulletIndent=3,
            textColor=colors.HexColor("#243540"),
            spaceAfter=3,
        ),
        "formula": ParagraphStyle(
            "Formula",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=9.3,
            leading=14,
            leftIndent=10,
            rightIndent=10,
            textColor=AZUL,
            backColor=CLARO,
            borderPadding=7,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "cover_info": ParagraphStyle(
            "CoverInfo",
            parent=base["Normal"],
            fontName=FONT_REGULAR,
            fontSize=9.4,
            leading=13.5,
            textColor=BLANCO,
        ),
    }


def grafico_base(nombre: str, figsize: tuple[float, float] = (8.6, 4.8)):
    plt.close("all")
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F7FAFC")
    ax.grid(True, color="#D9E4EA", linewidth=0.7, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#7A8C98")
    return fig, ax, FIGURAS / nombre


def generar_graficos(aero: dict, mecanica: dict) -> None:
    FIGURAS.mkdir(parents=True, exist_ok=True)

    perdidas = aero["perdidas"]
    etiquetas = [x["componente"].replace("_", " ") for x in perdidas]
    valores = [x["presion_pa"] for x in perdidas]
    fig, ax, ruta = grafico_base("perdidas_presion.png", (8.5, 4.6))
    barras = ax.barh(etiquetas, valores, color=["#00A6C8", "#2878A5", "#4E95B8", "#75ADCA", "#9FC6D8", "#F39C3D"])
    ax.set_xlabel("Pérdida estimada [Pa]")
    ax.set_title("Presupuesto unidimensional de pérdidas", color="#0B2239", weight="bold")
    ax.invert_yaxis()
    for barra, valor in zip(barras, valores):
        ax.text(valor + 2, barra.get_y() + barra.get_height() / 2, f"{valor:.1f}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=180, bbox_inches="tight")

    tabla_data = aero["voluta"]["tabla"]
    theta = [x["angulo_grados"] for x in tabla_data]
    area = [x["area_m2"] for x in tabla_data]
    radio = [x["radio_exterior_m"] * 1000 for x in tabla_data]
    fig, ax, ruta = grafico_base("ley_area_voluta.png")
    ax.plot(theta, area, marker="o", color="#00A6C8", linewidth=2.4, label="Área acumulada")
    ax.set_xlabel("Ángulo desde la lengua [°]")
    ax.set_ylabel("Área de paso [m²]", color="#007F9B")
    ax.tick_params(axis="y", labelcolor="#007F9B")
    ax2 = ax.twinx()
    ax2.plot(theta, radio, marker="s", color="#F39C3D", linewidth=2, label="Radio exterior")
    ax2.set_ylabel("Radio exterior [mm]", color="#C66E13")
    ax2.tick_params(axis="y", labelcolor="#C66E13")
    ax.set_title("Ley de crecimiento de la voluta", color="#0B2239", weight="bold")
    fig.tight_layout()
    fig.savefig(ruta, dpi=180, bbox_inches="tight")

    rpm = np.linspace(750, 1350, 121)
    relacion = rpm / 1100.0
    q = 3.0 * relacion
    dp = aero["punto_operacion"]["presion_objetivo_pa"] * relacion**2
    p = aero["potencias"]["potencia_eje_euler_kw"] * relacion**3
    fig, ax, ruta = grafico_base("leyes_afinidad.png")
    ax.plot(rpm, q / 3.0, color="#00A6C8", linewidth=2.3, label="Q / Q₀")
    ax.plot(rpm, dp / aero["punto_operacion"]["presion_objetivo_pa"], color="#2878A5", linewidth=2.3, label="Δp / Δp₀")
    ax.plot(rpm, p / aero["potencias"]["potencia_eje_euler_kw"], color="#F39C3D", linewidth=2.3, label="P / P₀")
    ax.axvline(1100, color="#586875", linestyle="--", linewidth=1)
    ax.set_xlabel("Velocidad [rpm]")
    ax.set_ylabel("Relación respecto al punto de diseño")
    ax.set_title("Leyes de afinidad a diámetro constante", color="#0B2239", weight="bold")
    ax.legend(frameon=False, ncol=3, loc="upper left")
    fig.tight_layout()
    fig.savefig(ruta, dpi=180, bbox_inches="tight")

    dm = DatosMecanicos()
    cargas = mecanica["cargas"]
    x = np.linspace(0, dm.luz_rodamientos_m + dm.voladizo_polea_m, 700)
    momento = cargas["reaccion_rodamiento_a_n"] * x
    momento += np.where(x >= dm.luz_rodamientos_m, cargas["reaccion_rodamiento_b_n"] * (x - dm.luz_rodamientos_m), 0)
    momento -= np.where(x >= dm.posicion_rodete_m, mecanica["masas"]["peso_rotor_n"] * (x - dm.posicion_rodete_m), 0)
    x_polea = dm.luz_rodamientos_m + dm.voladizo_polea_m
    momento -= np.where(x >= x_polea, cargas["carga_radial_correa_n"] * (x - x_polea), 0)
    fig, ax, ruta = grafico_base("momento_flector.png")
    ax.plot(x * 1000, momento, color="#2878A5", linewidth=2.5)
    ax.fill_between(x * 1000, momento, color="#00A6C8", alpha=0.22)
    for xpos, texto in [(0, "A"), (dm.posicion_rodete_m, "Rodete"), (dm.luz_rodamientos_m, "B"), (x_polea, "Polea")]:
        ax.axvline(xpos * 1000, color="#F39C3D", linestyle="--", linewidth=1)
        ax.text(xpos * 1000, ax.get_ylim()[1] * 0.82, texto, ha="center", fontsize=8, color="#8A4B0F")
    ax.set_xlabel("Posición sobre el eje [mm]")
    ax.set_ylabel("Momento flector [N·m]")
    ax.set_title("Diagrama de momento flector del eje", color="#0B2239", weight="bold")
    fig.tight_layout()
    fig.savefig(ruta, dpi=180, bbox_inches="tight")


def tabla(datos, anchos=None, encabezado=True, font_size=8.2) -> Table:
    t = Table(datos, colWidths=anchos, repeatRows=1 if encabezado else 0, hAlign="LEFT")
    comandos = [
        ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("LEADING", (0, 0), (-1, -1), font_size + 3),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C4D4DC")),
        ("ROWBACKGROUNDS", (0, 1 if encabezado else 0), (-1, -1), [colors.white, colors.HexColor("#F4F8FA")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if encabezado:
        comandos += [
            ("BACKGROUND", (0, 0), (-1, 0), AZUL),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLANCO),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ]
    t.setStyle(TableStyle(comandos))
    return t


def imagen(ruta: Path, ancho: float, alto_max: float | None = None) -> Image:
    img = Image(str(ruta))
    factor = ancho / img.imageWidth
    alto = img.imageHeight * factor
    if alto_max and alto > alto_max:
        factor = alto_max / img.imageHeight
        ancho = img.imageWidth * factor
        alto = alto_max
    img.drawWidth = ancho
    img.drawHeight = alto
    img.hAlign = "CENTER"
    return img


def pie_pagina(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C7D8E0"))
    canvas.line(18 * mm, 13 * mm, 192 * mm, 13 * mm)
    canvas.setFont(FONT_REGULAR, 7.2)
    canvas.setFillColor(GRIS)
    canvas.drawString(18 * mm, 8.5 * mm, "Diseño preliminar de ventilador Sirocco · Revisión V1.2")
    canvas.drawRightString(192 * mm, 8.5 * mm, f"Página {doc.page}")
    canvas.restoreState()



def portada(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(AZUL)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#0E314B"))
    canvas.circle(181 * mm, 260 * mm, 58 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(CIAN)
    canvas.setLineWidth(2)
    canvas.line(18 * mm, 275 * mm, 83 * mm, 275 * mm)
    canvas.restoreState()


def p(texto: str, st: dict, estilo: str = "body") -> Paragraph:
    return Paragraph(texto, st[estilo])


def b(texto: str, st: dict) -> Paragraph:
    return Paragraph(f"• {texto}", st["bullet"])


def construir_pdf(aero: dict, mec: dict) -> None:
    registrar_fuentes()
    st = estilos()
    doc = SimpleDocTemplate(
        str(PDF),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Informe de diseño del ventilador centrífugo Sirocco",
        author="Grupo 2 - Universidad Nacional del Altiplano",
        subject="Predimensionamiento aerodinámico, mecánico y modelo 3D",
    )
    historia = []

    historia += [
        Spacer(1, 22 * mm),
        p("PROYECTO DE TURBOMÁQUINAS", st, "subtitulo"),
        Spacer(1, 8 * mm),
        p("Diseño preliminar de un ventilador centrífugo tipo Sirocco", st, "titulo"),
        p("Predimensionamiento aerodinámico y mecánico, geometría CAD e interfaz 3D interactiva", st, "subtitulo"),
        Spacer(1, 12 * mm),
        imagen(FIGURAS / "modelo_3d_assembly.png", 172 * mm, 92 * mm),
        Spacer(1, 6 * mm),
        p("<b>Universidad Nacional del Altiplano</b><br/>Curso: Turbomáquinas<br/>Docente: Ing. Armando Cruz Cabrera<br/><br/><b>Integrantes</b><br/>Dilmar Humberto Siguayro Coila<br/>Aquiles Taylor Ramos Yapo<br/>Renzo Gabriel Mamani Galindo<br/>Martin Calla Quispe<br/>Abel Yovani Rivera Quispe<br/><br/>Puno, 2026 · Revisión V1.2", st, "cover_info"),
        PageBreak(),
    ]

    historia += [
        p("Resumen ejecutivo", st, "h1"),
        p(
            "Se desarrolló el predimensionamiento de un ventilador centrífugo multialabe tipo Sirocco para entregar "
            "<b>3.0 m³/s (10 800 m³/h)</b> de aire con una presión estática objetivo de <b>90 mmH₂O (882.6 Pa)</b>. "
            "El cierre unidimensional selecciona un rodete de doble entrada de 600 mm de diámetro exterior, 510 mm de "
            "diámetro interior, 230 mm de ancho y 48 álabes curvados hacia adelante, operando a 1100 rpm.", st),
        p(
            "La potencia útil del aire es 2.65 kW. Al incorporar el triángulo de velocidades, el factor de deslizamiento, "
            "la eficiencia mecánica y un presupuesto preliminar de pérdidas, se obtiene una potencia de eje de "
            f"<b>{aero['potencias']['potencia_eje_euler_kw']:.2f} kW</b> y se selecciona un motor de <b>5.5 kW</b>. "
            "El cálculo mecánico propone un eje de 35 mm y rodamientos con capacidad dinámica mínima de "
            f"{mec['rodamientos']['capacidad_dinamica_minima_kn']:.1f} kN.", st),
        p("Resultados principales", st, "h2"),
        tabla([
            ["Magnitud", "Resultado", "Criterio"],
            ["Punto de operación", "10 800 m³/h · 882.6 Pa", "Requisito de diseño"],
            ["Rodete", "D₂ 600 mm · D₁ 510 mm · b 230 mm", "Doble entrada"],
            ["Álabes", f"48 · β₁ {aero['rodete']['beta1_grados']:.1f}° · β₂ 125°", "Curvados hacia adelante"],
            ["Velocidad / motor", "1100 rpm · 5.5 kW", f"Margen {aero['potencias']['margen_motor_relativo']*100:.1f}%"],
            ["Voluta / descarga", "280 mm · 280 × 714 mm", "15 m/s en la salida"],
            ["Rotor / eje", f"{mec['masas']['masa_rotor_con_soldadura_kg']:.2f} kg · Ø35 mm", "Predimensionamiento ASME"],
        ], [55 * mm, 65 * mm, 52 * mm]),
        Spacer(1, 5 * mm),
        p("Alcance y condición de uso", st, "h2"),
        p(
            "Este documento corresponde a una <b>revisión preliminar de ingeniería</b>. La geometría todavía no es un plano "
            "liberado para fabricación: debe verificarse mediante CFD, análisis estructural de álabes y soldaduras, balanceo "
            "dinámico, definición de tolerancias y ensayo de desempeño con un procedimiento reconocido.", st),
        PageBreak(),
    ]

    historia += [
        p("1. Requisitos y metodología", st, "h1"),
        p("El diseño se abordó como una secuencia trazable de requisitos, cálculo, geometría y verificación digital:", st),
        b("Definir el punto de operación, propiedades del aire y restricciones geométricas.", st),
        b("Resolver velocidades periféricas, meridionales y tangenciales en el rodete.", st),
        b("Estimar la presión de Euler, potencia, eficiencia estática y pérdidas internas.", st),
        b("Dimensionar la voluta con una ley de área proporcional al caudal acumulado.", st),
        b("Predimensionar masa del rotor, transmisión por polea, eje y rodamientos.", st),
        b("Generar geometría CAD 2D, mallas OBJ y una inspección 3D interactiva sin conexión.", st),
        p("Datos de entrada", st, "h2"),
        tabla([
            ["Variable", "Símbolo", "Valor"],
            ["Caudal", "Q", "3.0 m³/s"],
            ["Presión estática", "Δpₛ", "882.6 Pa"],
            ["Densidad del aire", "ρ", "1.20 kg/m³"],
            ["Diámetro exterior", "D₂", "0.600 m"],
            ["Diámetro interior", "D₁", "0.510 m"],
            ["Ancho del rodete", "b", "0.230 m"],
            ["Velocidad", "n", "1100 rpm"],
            ["Número de álabes", "Z", "48"],
        ], [72 * mm, 35 * mm, 62 * mm]),
        p("Hipótesis de cálculo", st, "h2"),
        p(
            "Se considera flujo estacionario, aire incompresible a densidad constante y reparto uniforme del caudal entre "
            "las dos entradas. El modelo usa una formulación unidimensional en el diámetro medio de paso; el bloqueo por "
            "espesor, el deslizamiento y las pérdidas son estimaciones de ingeniería. Estas hipótesis permiten seleccionar "
            "dimensiones iniciales, pero no capturan separación tridimensional, interacción lengua-rodete ni ruido.", st),
        PageBreak(),
    ]

    historia += [
        p("2. Diseño aerodinámico del rodete", st, "h1"),
        p("Las velocidades periféricas se obtienen mediante <b>u = πDn/60</b>. El caudal fija la velocidad meridional considerando el área anular y el bloqueo geométrico de los álabes.", st),
        p("u₂ = π D₂ n / 60 &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; c<sub>m2</sub> = Q / (π D₂ b k<sub>b2</sub>)", st, "formula"),
        p(
            "Para la entrada se iteró el ángulo β₁ hasta obtener incidencia aproximadamente nula. En la salida se adoptó "
            "β₂ = 125°, propio de una configuración curvada hacia adelante. El factor de deslizamiento se estimó con la "
            "correlación de Wiesner como referencia inicial.", st),
        tabla([
            ["Parámetro", "Entrada", "Salida"],
            ["Diámetro", "510 mm", "600 mm"],
            ["Velocidad periférica", f"{aero['rodete']['u1_m_s']:.2f} m/s", f"{aero['rodete']['u2_m_s']:.2f} m/s"],
            ["Velocidad meridional", f"{aero['rodete']['cm1_m_s']:.2f} m/s", f"{aero['rodete']['cm2_m_s']:.2f} m/s"],
            ["Ángulo relativo", f"β₁ = {aero['rodete']['beta1_grados']:.2f}°", "β₂ = 125°"],
            ["Factor de bloqueo", f"{aero['rodete']['factor_bloqueo_1']:.3f}", f"{aero['rodete']['factor_bloqueo_2']:.3f}"],
            ["Factor de deslizamiento", "—", f"σ = {aero['rodete']['factor_deslizamiento']:.3f}"],
        ], [64 * mm, 53 * mm, 53 * mm]),
        Spacer(1, 5 * mm),
        imagen(FIGURAS / "modelo_3d_rotor.png", 166 * mm, 89 * mm),
        p("Figura 1. Modelo 3D del rodete de doble entrada, eje, polea y soportes preliminares.", st, "caption"),
        PageBreak(),
    ]

    historia += [
        p("3. Presión, pérdidas y potencia", st, "h1"),
        p("La presión teórica se calcula con la ecuación de Euler para turbomáquinas, tomando nula la componente tangencial en la entrada:", st),
        p("Δp<sub>Euler</sub> = ρ (u₂ c<sub>u2</sub> − u₁ c<sub>u1</sub>) ≈ ρ u₂ c<sub>u2</sub>", st, "formula"),
        tabla([
            ["Resultado", "Valor"],
            ["Presión teórica de Euler", f"{aero['rodete']['presion_euler_pa']:.1f} Pa"],
            ["Presión estática objetivo", f"{aero['punto_operacion']['presion_objetivo_pa']:.1f} Pa"],
            ["Potencia útil del aire", f"{aero['potencias']['potencia_util_aire_kw']:.2f} kW"],
            ["Potencia transferida por Euler", f"{aero['potencias']['potencia_euler_kw']:.2f} kW"],
            ["Potencia requerida en el eje", f"{aero['potencias']['potencia_eje_euler_kw']:.2f} kW"],
            ["Eficiencia estática estimada", f"{aero['potencias']['eficiencia_estatica_estimada']*100:.1f}%"],
            ["Motor seleccionado", "5.5 kW"],
        ], [102 * mm, 67 * mm]),
        Spacer(1, 5 * mm),
        imagen(FIGURAS / "perdidas_presion.png", 164 * mm, 84 * mm),
        p("Figura 2. Distribución estimada de pérdidas. Debe calibrarse con CFD o ensayo.", st, "caption"),
        p(
            "La potencia del motor supera la potencia de eje calculada y proporciona margen para dispersión del modelo, "
            "transmisión y operación. Aun así, no debe aumentarse la velocidad sin revisar la potencia: a diámetro constante "
            "el consumo crece aproximadamente con el cubo de las rpm.", st),
        PageBreak(),
    ]

    historia += [
        p("4. Voluta y descarga", st, "h1"),
        p(
            "La voluta recoge progresivamente el caudal descargado por el rodete. Se adoptó una ley lineal del área de paso "
            "con el ángulo desde la lengua: A(θ) = (Q / V<sub>salida</sub>) θ/360°. Con 15 m/s en la descarga se requiere "
            "un área final de 0.20 m².", st),
        tabla([
            ["Parámetro", "Valor"],
            ["Ancho interior de voluta", "280 mm"],
            ["Área final", f"{aero['voluta']['area_salida_m2']:.3f} m²"],
            ["Altura final de descarga", f"{aero['voluta']['altura_salida_m']*1000:.0f} mm"],
            ["Sección de descarga", "280 × 714 mm"],
            ["Holgura radial en la lengua", f"{aero['voluta']['holgura_lengua_m']*1000:.0f} mm"],
        ], [100 * mm, 70 * mm]),
        Spacer(1, 5 * mm),
        imagen(FIGURAS / "ley_area_voluta.png", 163 * mm, 78 * mm),
        p("Figura 3. Crecimiento de área y radio exterior de la voluta.", st, "caption"),
        imagen(FIGURAS / "geometria_cad_2d.png", 151 * mm, 72 * mm),
        p("Figura 4. Geometría CAD 2D exportada en DXF y SVG para revisión dimensional.", st, "caption"),
        PageBreak(),
    ]

    historia += [
        p("5. Predimensionamiento mecánico", st, "h1"),
        p(
            "La masa del rotor se estimó sumando álabes, anillos de entrada, disco central y cubo, con 8% adicional por "
            "soldadura. La transmisión se representó mediante una polea de 200 mm y un factor de carga radial de correa de "
            "2.5 veces la fuerza tangencial. El eje se verificó por flexión y torsión combinadas, incluyendo factores de "
            "choque y reducción por chavetero.", st),
        tabla([
            ["Magnitud", "Resultado"],
            ["Masa estimada del rotor", f"{mec['masas']['masa_rotor_con_soldadura_kg']:.2f} kg"],
            ["Torque nominal", f"{mec['cargas']['torque_nominal_nm']:.1f} N·m"],
            ["Carga radial de correa", f"{mec['cargas']['carga_radial_correa_n']:.0f} N"],
            ["Momento flector máximo", f"{mec['cargas']['momento_flector_maximo_nm']:.1f} N·m"],
            ["Diámetro con factor de chavetero", f"{mec['eje']['diametro_con_factor_chavetero_mm']:.1f} mm"],
            ["Diámetro normalizado adoptado", f"{mec['eje']['diametro_recomendado_mm']:.0f} mm"],
            ["Primera velocidad crítica estimada", f"{mec['eje']['primera_velocidad_critica_rpm']:.0f} rpm"],
            ["Capacidad dinámica mínima de rodamiento", f"{mec['rodamientos']['capacidad_dinamica_minima_kn']:.1f} kN"],
        ], [106 * mm, 64 * mm]),
        Spacer(1, 6 * mm),
        imagen(FIGURAS / "momento_flector.png", 164 * mm, 84 * mm),
        p("Figura 5. Diagrama de momento empleado en el predimensionamiento del eje.", st, "caption"),
        p(
            f"La razón entre la primera velocidad crítica estimada y la velocidad de operación es "
            f"{mec['eje']['relacion_critica_operacion']:.2f}. Esta comprobación es simplificada y debe reemplazarse por "
            "un análisis modal del conjunto eje-rotor-rodamientos cuando se definan rigideces reales y masas de polea.", st),
        PageBreak(),
    ]

    modelos = semejanza(DatosDiseno(), 0.5)
    historia += [
        p("6. Leyes de afinidad y modelo a escala", st, "h1"),
        p(
            "Para una familia geométricamente semejante, el caudal varía con nD³, la presión con n²D² y la potencia con "
            "n³D⁵. Estas relaciones permiten anticipar cambios de operación y diseñar un prototipo de laboratorio.", st),
        p("Q₂/Q₁ = (n₂/n₁)(D₂/D₁)³ &nbsp;&nbsp; | &nbsp;&nbsp; Δp₂/Δp₁ = (n₂/n₁)²(D₂/D₁)² &nbsp;&nbsp; | &nbsp;&nbsp; P₂/P₁ = (n₂/n₁)³(D₂/D₁)⁵", st, "formula"),
        imagen(FIGURAS / "leyes_afinidad.png", 166 * mm, 84 * mm),
        p("Figura 6. Sensibilidad del caudal, presión y potencia frente a las rpm.", st, "caption"),
        tabla([
            ["Modelo D = 0.30 m", "RPM", "Caudal", "Presión", "Potencia eje"],
            ["Misma rpm", f"{modelos[0]['rpm']:.0f}", f"{modelos[0]['caudal_m3_s']:.3f} m³/s", f"{modelos[0]['presion_pa']:.1f} Pa", f"{modelos[0]['potencia_eje_kw']:.3f} kW"],
            ["Misma velocidad periférica", f"{modelos[1]['rpm']:.0f}", f"{modelos[1]['caudal_m3_s']:.3f} m³/s", f"{modelos[1]['presion_pa']:.1f} Pa", f"{modelos[1]['potencia_eje_kw']:.3f} kW"],
        ], [48 * mm, 26 * mm, 38 * mm, 31 * mm, 31 * mm], font_size=7.6),
        p(
            "Las leyes de afinidad no garantizan semejanza exacta cuando cambian el número de Reynolds, holguras relativas, "
            "rugosidad o condiciones de entrada. Por ello, el modelo a escala debe documentar dichas desviaciones.", st),
        PageBreak(),
    ]

    historia += [
        p("7. Geometría 3D e interfaz de inspección", st, "h1"),
        p(
            "Se generaron mallas OBJ en milímetros para el rodete, la voluta y el conjunto. La malla completa contiene más "
            "de 12 000 vértices y 16 000 caras. La interfaz web reconstruye la geometría con Three.js y permite revisar la "
            "disposición sin instalar software CAD.", st),
        imagen(FIGURAS / "interfaz_3d.png", 174 * mm, 101 * mm),
        p("Figura 7. Interfaz 3D autónoma con controles de visualización y datos de diseño.", st, "caption"),
        p("Funciones incluidas", st, "h2"),
        b("Rotación, zoom y vistas frontal, lateral, superior e isométrica.", st),
        b("Activación independiente de rodete, voluta, flujo, soportes y rejilla.", st),
        b("Animación del rodete, vista explosionada, transparencia y captura PNG.", st),
        b("Identificación de componentes mediante clic y panel de parámetros.", st),
        p("Ejecución portátil", st, "h2"),
        p(
            "En Windows se abre <b>ABRIR_MODELO_3D.bat</b>. El archivo BAT localiza el proyecto mediante <b>%~dp0</b> y "
            "abre <b>10_interfaz_3d/index.html</b> en el navegador predeterminado. No requiere Python, Node.js ni conexión a "
            "Internet. En Linux y macOS se abre directamente el mismo archivo HTML; el formato BAT es específico de Windows.", st),
        PageBreak(),
    ]

    historia += [
        p("8. Archivos reproducibles y verificación", st, "h1"),
        p("La entrega se organizó para que los cálculos, geometrías y resultados puedan regenerarse desde el repositorio:", st),
        tabla([
            ["Ruta", "Contenido"],
            ["08_software/calculo_sirocco.py", "Cierre aerodinámico y exportación de resultados"],
            ["08_software/calculo_mecanico_sirocco.py", "Masa, eje, cargas y rodamientos"],
            ["08_software/generar_geometria_cad.py", "DXF, SVG y parámetros 2D"],
            ["08_software/generar_modelo_3d.py", "Mallas OBJ, MTL y datos de interfaz"],
            ["08_software/generar_reporte_pdf.py", "Gráficos y memoria técnica PDF"],
            ["07_modelos_3d/", "Rodete, voluta y conjunto en formato OBJ"],
            ["10_interfaz_3d/", "Visor web autónomo"],
            ["09_reporte/", "PDF y figuras de presentación"],
        ], [74 * mm, 96 * mm], font_size=7.7),
        p("Comandos de regeneración", st, "h2"),
        p(
            "<font name='Courier'>python3 08_software/calculo_sirocco.py --exportar 06_calculos/resultados_v1<br/>"
            "python3 08_software/generar_geometria_cad.py --salida 07_planos<br/>"
            "python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d<br/>"
            "python3 08_software/generar_reporte_pdf.py<br/>"
            "python3 -m pytest -q 08_software</font>", st, "formula"),
        p("Criterios de verificación", st, "h2"),
        b("Consistencia de conversiones, potencia y presión.", st),
        b("Crecimiento monótono del área de la voluta.", st),
        b("Leyes de semejanza y efecto de cambios de rpm.", st),
        b("Geometría de 48 álabes, eje de 35 mm y archivos 3D válidos.", st),
        b("Ausencia de dependencias remotas en la interfaz web.", st),
        PageBreak(),
    ]

    historia += [
        p("9. Conclusiones y trabajo pendiente", st, "h1"),
        p("Conclusiones", st, "h2"),
        b("El punto de 10 800 m³/h y 882.6 Pa puede abordarse preliminarmente con un rodete Sirocco de 600 mm a 1100 rpm.", st),
        b(f"La potencia de eje calculada es {aero['potencias']['potencia_eje_euler_kw']:.2f} kW; el motor de 5.5 kW conserva margen sin justificar aumentos arbitrarios de velocidad.", st),
        b("La voluta de 280 mm de ancho y descarga 280 × 714 mm satisface el área definida para 15 m/s.", st),
        b(f"El rotor estimado de {mec['masas']['masa_rotor_con_soldadura_kg']:.2f} kg conduce a un eje preliminar de 35 mm y rodamientos de al menos {mec['rodamientos']['capacidad_dinamica_minima_kn']:.1f} kN de capacidad dinámica.", st),
        b("La interfaz autónoma y las mallas OBJ permiten comunicar y revisar el diseño sin depender de un programa CAD específico.", st),
        p("Trabajo pendiente antes de fabricar", st, "h2"),
        tabla([
            ["Prioridad", "Actividad", "Resultado esperado"],
            ["Alta", "CFD estacionario y transitorio", "Curva Q-Δp, eficiencia, separación y carga en la lengua"],
            ["Alta", "FEA de álabes, disco y soldaduras", "Tensiones, deformaciones, fatiga y modos propios"],
            ["Alta", "Definir tolerancias y proceso", "Planos de fabricación, soldadura y balanceo"],
            ["Media", "Seleccionar rodamientos y correas comerciales", "Vida L10, tensado, guardas y mantenimiento"],
            ["Media", "Construir prototipo instrumentado", "Curvas de presión, potencia, vibración y ruido"],
        ], [24 * mm, 67 * mm, 79 * mm], font_size=7.5),
        p("Advertencia final", st, "h2"),
        p(
            "El modelo actual sirve para presentación académica, coordinación y predimensionamiento. No debe utilizarse como "
            "única base para fabricar u operar un rotor a velocidad sin una revisión profesional de seguridad, resistencia, "
            "contención, balanceo y cumplimiento normativo.", st),
        PageBreak(),
    ]

    historia += [
        p("Referencias técnicas", st, "h1"),
        p("[1] AMCA International. <i>Derivation of the Fan Laws</i>. Documento técnico sobre relaciones de afinidad para ventiladores.<br/>https://www.amca.org/assets/resources/public/pdf/White%20Papers/2020%20-%20Derivation%20of%20the%20Fan%20Laws.pdf", st),
        p("[2] Greenheck Fan Corporation. <i>Installation, Operation and Maintenance Manual</i>. Recomendaciones generales de instalación y seguridad para ventiladores centrífugos.<br/>https://content.greenheck.com/public/DAMProd/Original/10001/482886_dgdgxtsuvsu_iom_Rev5_September2022.pdf", st),
        p("[3] Hao et al. Investigación sobre optimización y desempeño aerodinámico de ventiladores centrífugos multialabe. DOI: 10.1177/0020294020932360", st),
        p("[4] Wang et al. Estudio de flujo interno y desempeño en ventiladores centrífugos. DOI: 10.1115/1.4056279", st),
        p("[5] Wang, Ju y Zhang. Optimización multidisciplinaria aplicada a ventiladores centrífugos. DOI: 10.1007/s00158-020-02801-2", st),
        p("[6] Scripts, memorias y geometrías del proyecto. Repositorio GitHub del Grupo 2, revisión V1.2.", st),
        Spacer(1, 10 * mm),
        p("Nota sobre las fuentes", st, "h2"),
        p(
            "Las referencias se usan para sustentar principios generales y orientar la siguiente fase. Los resultados "
            "numéricos de esta memoria provienen de los scripts incluidos en el proyecto y de las hipótesis declaradas; no "
            "se presentan como resultados experimentales ni como certificación AMCA.", st),
    ]

    doc.build(historia, onFirstPage=portada, onLaterPages=pie_pagina)


def construir_markdown(aero: dict, mec: dict) -> None:
    contenido = f"""# Informe de diseño del ventilador centrífugo Sirocco

Versión fuente resumida del informe generado en PDF.

## Punto de diseño

- Caudal: 3.0 m³/s = 10 800 m³/h.
- Presión estática: 90 mmH₂O = 882.6 Pa.
- Rodete: D2 600 mm, D1 510 mm, ancho 230 mm y 48 álabes.
- Velocidad: 1100 rpm.
- Potencia de eje estimada: {aero['potencias']['potencia_eje_euler_kw']:.2f} kW.
- Motor seleccionado: 5.5 kW.
- Voluta: ancho 280 mm, descarga 280 x 714 mm.
- Masa estimada del rotor: {mec['masas']['masa_rotor_con_soldadura_kg']:.2f} kg.
- Eje preliminar: {mec['eje']['diametro_recomendado_mm']:.0f} mm.
- Rodamiento: capacidad dinámica mínima {mec['rodamientos']['capacidad_dinamica_minima_kn']:.1f} kN.

## Entregables

- `Informe_Diseno_Ventilador_Sirocco.pdf`: memoria técnica para presentación.
- `../07_modelos_3d/`: mallas OBJ del rodete, voluta y conjunto.
- `../10_interfaz_3d/index.html`: interfaz gráfica autónoma.
- `../ABRIR_MODELO_3D.bat`: lanzador para Windows.

## Alcance

El diseño es un predimensionamiento académico. Antes de fabricar se requieren CFD,
análisis estructural, balanceo, tolerancias, selección comercial y ensayo.

Generado el {date.today().isoformat()} mediante `08_software/generar_reporte_pdf.py`.
"""
    MD.write_text(contenido, encoding="utf-8")


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    aero = calcular(DatosDiseno())
    mec = calcular_mecanica(DatosDiseno(), DatosMecanicos())
    generar_graficos(aero, mec)
    construir_pdf(aero, mec)
    construir_markdown(aero, mec)
    print(f"PDF generado: {PDF}")
    print(f"Fuente resumida: {MD}")


if __name__ == "__main__":
    main()
