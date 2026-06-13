from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_interfaz_es_autonoma_y_tiene_lanzador_windows():
    html = (ROOT / "10_interfaz_3d" / "index.html").read_text(encoding="utf-8")
    bat = (ROOT / "ABRIR_MODELO_3D.bat").read_text(encoding="utf-8")

    recursos = re.findall(r'(?:src|href)="([^"]+)"', html)
    assert recursos
    assert all(not recurso.startswith(("http://", "https://", "//")) for recurso in recursos)
    assert "10_interfaz_3d\\index.html" in bat
    assert (ROOT / "10_interfaz_3d" / "vendor" / "three.min.js").stat().st_size > 500_000
    assert (ROOT / "07_modelos_3d" / "modelo_sirocco_v1_2.js").exists()


def test_interfaz_documenta_parametros_principales():
    html = (ROOT / "10_interfaz_3d" / "index.html").read_text(encoding="utf-8")
    for valor in ("10 800", "882.6", "1100", "5.5", "Ø600", "48"):
        assert valor in html
