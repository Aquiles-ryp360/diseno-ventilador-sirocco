# Estado del arte preliminar

## Enfoque del tema

El ventilador tipo Sirocco pertenece a los ventiladores centrifugos multialabe con alabes curvados hacia adelante. Su uso es conveniente cuando se necesita alto caudal, presion baja a media y compacidad, como en ventilacion HVAC, extractores, unidades de tratamiento de aire y sistemas de ductos.

Para el Grupo 2, el punto de diseno es:

- `Q = 3 m3/s`
- `Delta p = 882.6 Pa`
- Potencia util al aire: `2.65 kW`

## Lineas modernas de investigacion 2020-2026

1. **Interaccion rodete-voluta-lengua.** Estudios recientes muestran que la region de la lengua concentra fluctuaciones de presion, estructuras coherentes y fuentes de ruido. Esto afecta directamente el rendimiento y la estabilidad del ventilador.
2. **CFD como validacion del diseno 1D.** La teoria unidimensional sigue siendo adecuada para predimensionar rodete y voluta, pero se recomienda validar presion, velocidad y recuperacion de presion con CFD.
3. **Optimizacion de geometria.** Variables como angulos de entrada/salida, numero de alabes, curvatura de linea media, ancho del rodete y forma de la lengua pueden mejorar eficiencia y reducir separacion.
4. **Metodos DOE/Taguchi/ANOVA.** La literatura reciente usa arreglos experimentales para reducir el numero de simulaciones y encontrar parametros dominantes.
5. **Construccion y prototipado.** La impresion 3D y los modelos a escala son compatibles con la semejanza dinamica cuando se controlan relaciones geometricas y, si es posible, el regimen de Reynolds.

## Brecha aplicable al proyecto

El proyecto puede aportar un diseno reproducible de un Sirocco academico, combinando:

- Calculo 1D transparente.
- Dimensionamiento de rodete y voluta.
- Estimacion de perdidas.
- Herramienta de calculo.
- Propuesta de modelo por semejanza.
- Revision bibliografica 2020-2026 enfocada en alabes curvados hacia adelante y voluta.

## Hipotesis de trabajo

Un ventilador tipo Sirocco dimensionado mediante teoria unidimensional, con control de velocidad periferica, area de voluta y separacion de lengua, puede cumplir `Q = 3 m3/s` y `Delta p = 882.6 Pa` con una eficiencia global preliminar de `50% a 60%`, requiriendo un motor comercial cercano a `5.5 kW`.
