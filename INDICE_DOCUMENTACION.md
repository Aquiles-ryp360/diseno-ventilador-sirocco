# Índice de documentación del proyecto Sirocco

Este índice explica dónde revisar cada parte del proyecto y cuál es la fuente
vigente de los datos. Cada carpeta principal contiene un archivo
`DOCUMENTACION.md` con su propósito, contenido, forma de uso y relación con el
resto del diseño.

## Fuente técnica vigente

Cuando existan diferencias entre archivos, usar este orden de autoridad:

1. `08_software/calculo_sirocco.py` y `calculo_mecanico_sirocco.py`.
2. `06_calculos/memoria_calculo_sirocco_v1.md` y
   `memoria_mecanica_sirocco_v1.md`.
3. Resultados JSON y CSV generados en `06_calculos/resultados_*`.
4. Informe PDF de `09_reporte/`.
5. Presentaciones y documentos históricos.

El punto vigente es `Q = 3.0 m³/s`, `Δp = 882.6 Pa`, rodete de `600 mm`,
`48` álabes, `1100 rpm`, motor de `5.5 kW` y eje preliminar de `35 mm`.

## Documentación por carpeta

| Carpeta | Documento | Contenido |
|---|---|---|
| `00_gestion/` | `00_gestion/DOCUMENTACION.md` | Diagnóstico, tareas y cronograma |
| `04_bibliografia/` | `04_bibliografia/DOCUMENTACION.md` | Fuentes, estado del arte y uso de referencias |
| `05_avances/` | `05_avances/DOCUMENTACION.md` | Borradores y avances para el docente |
| `06_calculos/` | `06_calculos/DOCUMENTACION.md` | Ecuaciones, variables, resultados e hipótesis |
| `07_planos/` | `07_planos/DOCUMENTACION.md` | DXF, SVG, perfil de álabe y geometría 2D |
| `07_modelos_3d/` | `07_modelos_3d/DOCUMENTACION.md` | Mallas OBJ, materiales y datos 3D |
| `08_software/` | `08_software/DOCUMENTACION.md` | Arquitectura de scripts, comandos y pruebas |
| `09_reporte/` | `09_reporte/DOCUMENTACION.md` | Informe PDF y figuras técnicas |
| `10_interfaz_3d/` | `10_interfaz_3d/DOCUMENTACION.md` | Visor 3D, controles y ejecución offline |
| `1 artículo de investigación/` | `DOCUMENTACION.md` | Documento original del primer trabajo |
| `2 diseño de turbomaquina/` | `DOCUMENTACION.md` | Enunciado del trabajo de diseño |
| `3 resolución de problemas/` | `DOCUMENTACION.md` | Copia del enunciado de problemas |
| `documento_latex/` | `documento_latex/DOCUMENTACION.md` | Informe alternativo en LaTeX |
| `presentacion/` | `presentacion/DOCUMENTACION.md` | Presentación web y PowerPoint |

## Recorrido recomendado

1. Leer `README.md` para conocer el resultado general.
2. Revisar `06_calculos/DOCUMENTACION.md` para entender las ecuaciones.
3. Abrir `09_reporte/Informe_Diseno_Ventilador_Sirocco.pdf` para la exposición.
4. Ejecutar `ABRIR_MODELO_3D.bat` en Windows para inspeccionar el conjunto.
5. Consultar `08_software/DOCUMENTACION.md` para regenerar y verificar todo.

## Advertencia de ingeniería

El proyecto es un predimensionamiento académico reproducible. Todavía requiere
CFD, cálculo estructural de álabes y uniones, selección comercial, tolerancias,
balanceo y ensayo antes de convertirse en documentación de fabricación.
