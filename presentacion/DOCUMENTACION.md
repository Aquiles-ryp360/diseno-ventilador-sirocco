# Documentación de `presentacion`

## Propósito

Contener dos formas de exposición: una presentación web interactiva y un
archivo PowerPoint generado con Python.

## Presentación web

### Archivos

- `index.html`: siete secciones o diapositivas.
- `style.css`: tema oscuro y distribución visual.
- `script.js`: navegación, cálculo interactivo y dibujo SVG.

### Diapositivas

1. Portada.
2. Requerimientos de diseño.
3. Geometría del rotor.
4. Triángulo de velocidades interactivo.
5. Voluta y difusión.
6. Comparación de `1100 rpm` y `1500 rpm`.
7. Estructura del repositorio.

La calculadora visual permite modificar parámetros y redibujar el triángulo de
velocidades. Para valores oficiales deben usarse los scripts de
`08_software/`, no el cálculo del navegador.

## PowerPoint

### `presentacion_sirocco.pptx`

Presentación de 7 diapositivas en formato panorámico 16:9.

### `generate_pptx.py`

Genera el PowerPoint mediante `python-pptx`. Define colores, tarjetas,
tipografías, tablas e imágenes.

Ejecutar desde la carpeta para que las rutas de `assets/` sean correctas:

```bash
cd presentacion
python3 generate_pptx.py
```

## Recursos

- `assets/sirocco_fan_render.jpg`: render empleado en la portada.
- `assets/placeholder.txt`: marcador de la carpeta de recursos.

## Revisión antes de exponer

1. Confirmar que todos los valores sean V1.2.
2. No usar `1500 rpm` como velocidad seleccionada.
3. Indicar que la eficiencia de `54.5 %` es estimada.
4. Explicar que el modelo 3D es conceptual.
5. Mantener visible la necesidad de CFD y ensayo.
