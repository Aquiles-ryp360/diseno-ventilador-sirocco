from calculo_sirocco import DatosDiseno, calcular, semejanza, tabla_voluta


def test_conversion_y_punto_operacion():
    resultado = calcular()
    assert resultado["punto_operacion"]["presion_objetivo_pa"] == 882.5985
    assert resultado["punto_operacion"]["caudal_m3_h"] == 10800.0


def test_diseno_base_cierra_potencia_y_geometria():
    resultado = calcular()
    assert 1500.0 < resultado["rodete"]["presion_euler_pa"] < 1600.0
    assert 4.7 < resultado["potencias"]["potencia_eje_euler_kw"] < 5.0
    assert resultado["potencias"]["potencia_motor_kw"] > resultado["potencias"]["potencia_eje_euler_kw"]
    assert 16.0 < resultado["rodete"]["beta1_grados"] < 19.0
    assert resultado["mecanica"]["diametro_eje_recomendado_mm"] == 30.0


def test_voluta_crece_monotonicamente():
    filas = tabla_voluta(DatosDiseno())
    areas = [fila["area_m2"] for fila in filas]
    assert areas == sorted(areas)
    assert abs(areas[-1] - 0.2) < 1e-12


def test_leyes_de_semejanza_a_media_escala():
    modelos = {fila["modo"]: fila for fila in semejanza(DatosDiseno(), 0.5)}
    misma_rpm = modelos["misma_rpm"]
    misma_u = modelos["misma_velocidad_periferica"]
    assert misma_rpm["caudal_m3_s"] == 0.375
    assert abs(misma_rpm["presion_pa"] - 220.649625) < 1e-9
    assert misma_u["rpm"] == 2200.0
    assert misma_u["caudal_m3_s"] == 0.75
    assert misma_u["presion_pa"] == 882.5985


def test_1500_rpm_sobrecarga_el_predimensionamiento():
    resultado = calcular(DatosDiseno(rpm=1500.0))
    assert resultado["rodete"]["presion_euler_pa"] > 2700.0
    assert resultado["potencias"]["potencia_eje_euler_kw"] > 8.0
