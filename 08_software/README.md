# Software de calculo del ventilador Sirocco

`calculo_sirocco.py` reproduce el predimensionamiento V1 del rodete, voluta,
potencia, perdidas, eje y modelo por semejanza.

## Ejecucion

```bash
python3 08_software/calculo_sirocco.py
```

Cambiar el punto o la velocidad:

```bash
python3 08_software/calculo_sirocco.py --caudal 3 --presion 90 --rpm 1100
```

Exportar CSV, JSON y el esquema SVG:

```bash
python3 08_software/calculo_sirocco.py \
  --exportar 06_calculos/resultados_v1
```

## Pruebas

```bash
python3 -m pytest -q 08_software/test_calculo_sirocco.py
```

Las pruebas verifican conversion de unidades, cierre de potencia, crecimiento
de la voluta, leyes de semejanza y la sobrecarga que produciria mantener
`1500 rpm`.

## Limite del modelo

El programa es un calculo unidimensional. El factor de deslizamiento, el
presupuesto de perdidas y la ley de areas son hipotesis de ingenieria que deben
calibrarse con CFD o ensayo. No genera por si solo un plano de fabricacion.
