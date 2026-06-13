# Documentación de `05_avances`

## Propósito

Conservar borradores y cortes parciales presentables durante el desarrollo.
Estos archivos muestran la evolución del diseño, pero no sustituyen la memoria
vigente de `06_calculos/`.

## Archivos

### `articulo_investigacion_borrador.md`

Borrador académico con autores, resumen, introducción, objetivos, metodología,
resultados preliminares, discusión, conclusiones y referencias. Es una base
editable para el artículo del curso.

### `avance_revision_docente.md`

Resumen corto preparado para revisión docente. Presenta el punto de diseño,
dimensiones seleccionadas y los cálculos principales de velocidad, presión y
potencia.

## Ecuaciones resumidas en los avances

```text
Δp = H · 9.80665
P_aire = Q · Δp
U₂ = π D₂ n / 60
C_m2 = Q / (π D₂ b k_b2)
Δp_Euler = ρ U₂ C_u2
P_eje = Q Δp_Euler / η_m
```

Los desarrollos completos, definición de variables y limitaciones están en
`06_calculos/DOCUMENTACION.md`.

## Precaución histórica

Si un avance contiene valores distintos, usar la revisión vigente:

- `1100 rpm`, no el tanteo inicial de `1500 rpm`.
- `D1 = 510 mm`, `D2 = 600 mm` y ancho `230 mm`.
- Eje mecánico preliminar de `35 mm`, no el mínimo torsional de `30 mm`.

## Uso recomendado

Actualizar estos borradores solamente después de regenerar los resultados con
los scripts. Para la exposición principal usar el PDF de `09_reporte/`.
