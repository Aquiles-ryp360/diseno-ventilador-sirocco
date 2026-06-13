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

## Geometria CAD 2D

```bash
python3 08_software/generar_geometria_cad.py --salida 07_planos
python3 -m pytest -q 08_software/test_geometria_cad.py
```

El generador crea archivos DXF R12 en milimetros para el rodete y la voluta,
un CSV con la curva media del alabe, un JSON de parametros y un SVG de revision.

## Calculo mecanico

```bash
python3 08_software/calculo_mecanico_sirocco.py
python3 -m pytest -q 08_software/test_calculo_mecanico_sirocco.py
```

Incluye masa del rotor, carga de correas, reacciones, momento flector, diametro
del eje, velocidad critica y capacidad dinamica minima de rodamientos.

## Modelo 3D

```bash
python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d
python3 -m pytest -q 08_software/test_modelo_3d.py
```

Genera mallas OBJ en milimetros del rodete, la voluta y el conjunto, junto con
el archivo MTL y los datos geometricos empleados por la interfaz web.

## Informe PDF

```bash
python3 08_software/generar_reporte_pdf.py
```

Genera los graficos y la memoria tecnica de 12 paginas en `09_reporte/`. El
informe se construye directamente desde los resultados aerodinamicos y
mecanicos para mantener consistencia numerica.

## Interfaz 3D offline

En Windows se abre `ABRIR_MODELO_3D.bat`. La interfaz tambien puede iniciarse
abriendo `10_interfaz_3d/index.html` en Linux o macOS. Three.js y los controles
estan incluidos localmente, por lo que no se descargan dependencias al abrirla.

## Limite del modelo

El programa es un calculo unidimensional. El factor de deslizamiento, el
presupuesto de perdidas y la ley de areas son hipotesis de ingenieria que deben
calibrarse con CFD o ensayo. La malla 3D sirve para revision y comunicacion, no
reemplaza un modelo de fabricacion con tolerancias y uniones verificadas.
