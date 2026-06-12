from math import atan2, degrees, hypot

from calculo_sirocco import DatosDiseno, calcular
from generar_geometria_cad import puntos_arco, resolver_arco_alabe


def test_arco_cumple_radios_de_entrada_y_salida():
    datos = DatosDiseno()
    beta1 = round(calcular(datos)["rodete"]["beta1_grados"] * 2.0) / 2.0
    arco = resolver_arco_alabe(datos, beta1)
    puntos = puntos_arco(arco, arco.radio_curvatura_m, 80)
    assert abs(hypot(*puntos[0]) - datos.diametro_interior_m / 2.0) < 1e-10
    assert abs(hypot(*puntos[-1]) - datos.diametro_exterior_m / 2.0) < 1e-10


def test_arco_tiene_curvatura_y_desfase_constructivos():
    datos = DatosDiseno()
    arco = resolver_arco_alabe(datos, 17.5)
    assert 0.025 < arco.radio_curvatura_m < 0.040
    assert -5.0 < degrees(arco.angulo_polar_salida_rad) < 0.0
    centro_angulo = degrees(atan2(arco.centro_y_m, arco.centro_x_m))
    assert 0.0 < centro_angulo < 5.0
