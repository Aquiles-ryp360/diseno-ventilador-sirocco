# Diseno de ventilador centrifugo Sirocco

Proyecto academico del Grupo 2 para disenar un ventilador centrifugo multialabe
tipo Sirocco con:

- Caudal `Q = 3.0 m3/s = 10 800 m3/h`.
- Presion estatica `H = 90 mmH2O = 882.6 Pa`.
- Fluido: aire a `rho = 1.20 kg/m3`.

## Revision V1.1

El cierre unidimensional vigente selecciona:

- Rodete de doble entrada.
- Diametro exterior `D2 = 600 mm`.
- Diametro de entrada `D1 = 510 mm`.
- Ancho `b = 230 mm`.
- 48 alabes curvados hacia adelante.
- Velocidad aproximada `1100 rpm`.
- Motor `5.5 kW`.
- Eje preliminar `35 mm`, incluyendo flexion y carga de correas.
- Voluta de `280 mm` de ancho y lengua a `48 mm` del rodete.

La geometria aun requiere validacion CFD, calculo estructural y ensayo antes de
convertirse en plano de fabricacion.

## Archivos principales

- `06_calculos/memoria_calculo_sirocco_v1.md`: memoria tecnica vigente.
- `06_calculos/resultados_v1/`: tablas CSV, JSON y esquema generado.
- `06_calculos/memoria_mecanica_sirocco_v1.md`: eje, correas y rodamientos.
- `06_calculos/resultados_mecanicos_v1/`: resultados mecanicos reproducibles.
- `07_planos/esquema_dimensional_sirocco.svg`: esquema dimensional V1.
- `07_planos/rodete_sirocco_v1.dxf`: geometria 2D del rodete en milimetros.
- `07_planos/voluta_sirocco_v1.dxf`: perfil 2D de la voluta y descarga.
- `07_planos/geometria_cad_v1.svg`: vista previa de la geometria CAD.
- `08_software/calculo_sirocco.py`: calculador reproducible.
- `08_software/generar_geometria_cad.py`: generador de DXF, CSV, JSON y SVG.
- `08_software/calculo_mecanico_sirocco.py`: masa, eje y rodamientos.
- `08_software/test_calculo_sirocco.py`: pruebas automaticas.
- `05_avances/articulo_investigacion_borrador.md`: borrador academico.

## Ejecutar

```bash
python3 08_software/calculo_sirocco.py
python3 08_software/calculo_sirocco.py --exportar 06_calculos/resultados_v1
python3 08_software/generar_geometria_cad.py --salida 07_planos
python3 -m pytest -q 08_software
```

## Estado

Esta version cierra el predimensionamiento del rodete, potencia, voluta,
presupuesto de perdidas, eje, leyes de semejanza, geometria CAD 2D y calculo
mecanico inicial. Los siguientes hitos son el CAD 3D, la simulacion CFD, las
uniones estructurales y la curva experimental.
