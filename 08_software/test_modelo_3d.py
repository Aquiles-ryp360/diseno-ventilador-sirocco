from pathlib import Path

from generar_modelo_3d import exportar


def contar_obj(ruta: Path) -> tuple[int, int]:
    vertices = caras = 0
    for linea in ruta.read_text(encoding="ascii").splitlines():
        vertices += linea.startswith("v ")
        caras += linea.startswith("f ")
    return vertices, caras


def test_exporta_modelos_obj_y_datos(tmp_path):
    datos = exportar(tmp_path)
    for nombre in (
        "rodete_sirocco_v1_2.obj",
        "voluta_sirocco_v1_2.obj",
        "conjunto_sirocco_v1_2.obj",
        "materiales_sirocco.mtl",
        "modelo_sirocco_v1_2.json",
        "modelo_sirocco_v1_2.js",
    ):
        assert (tmp_path / nombre).is_file()
        assert (tmp_path / nombre).stat().st_size > 100
    vertices, caras = contar_obj(tmp_path / "conjunto_sirocco_v1_2.obj")
    assert vertices > 10_000
    assert caras > 10_000
    assert datos["dimensiones"]["numero_alabes"] == 48
    assert datos["dimensiones"]["eje_mm"] == 35.0
