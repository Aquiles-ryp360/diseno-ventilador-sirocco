from calculo_mecanico_sirocco import calcular_mecanica


def test_masa_y_cargas_estan_en_rangos_coherentes():
    r = calcular_mecanica()
    assert 15.0 < r["masas"]["masa_rotor_con_soldadura_kg"] < 22.0
    assert 900.0 < r["cargas"]["carga_radial_correa_n"] < 1200.0
    assert 60.0 < r["cargas"]["momento_flector_maximo_nm"] < 100.0


def test_eje_incluye_flexion_y_chavetero():
    r = calcular_mecanica()
    assert r["eje"]["diametro_recomendado_mm"] == 35.0
    assert r["eje"]["primera_velocidad_critica_rpm"] > 4.0 * 1100.0
    assert 10.0 < r["rodamientos"]["capacidad_dinamica_minima_kn"] < 20.0
