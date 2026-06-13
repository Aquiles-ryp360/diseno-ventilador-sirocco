from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cada_carpeta_principal_tiene_documentacion():
    documentos = [
        "00_gestion/DOCUMENTACION.md",
        "04_bibliografia/DOCUMENTACION.md",
        "05_avances/DOCUMENTACION.md",
        "06_calculos/DOCUMENTACION.md",
        "07_planos/DOCUMENTACION.md",
        "07_modelos_3d/DOCUMENTACION.md",
        "08_software/DOCUMENTACION.md",
        "09_reporte/DOCUMENTACION.md",
        "10_interfaz_3d/DOCUMENTACION.md",
        "1 artículo de investigación/DOCUMENTACION.md",
        "2 diseño de turbomaquina/DOCUMENTACION.md",
        "3 resolución de problemas/DOCUMENTACION.md",
        "documento_latex/DOCUMENTACION.md",
        "presentacion/DOCUMENTACION.md",
    ]
    for documento in documentos:
        ruta = ROOT / documento
        assert ruta.is_file(), documento
        assert len(ruta.read_text(encoding="utf-8")) > 300, documento


def test_manual_visual_pdf_fue_generado():
    pdf = ROOT / "11_documentacion" / "Manual_Documentacion_Proyecto_Sirocco.pdf"
    assert pdf.is_file()
    assert pdf.read_bytes().startswith(b"%PDF")
    assert pdf.stat().st_size > 1_000_000
