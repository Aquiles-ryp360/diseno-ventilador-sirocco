# Documentación de `documento_latex`

## Propósito

Conservar una versión alternativa del informe escrita en LaTeX.

## Archivos

### `reporte_diseno_sirocco.tex`

Fuente LaTeX con portada, índice, configuración seleccionada, geometría,
triángulo de velocidades, potencia, voluta, comparación de rpm y estructura del
repositorio.

### `reporte_diseno_sirocco.pdf`

Compilación A4 de 5 páginas. Es una memoria breve de revisión V1.

### `assets/sirocco_fan_render.jpg`

Imagen utilizada en materiales visuales.

## Ecuaciones incluidas

```text
U2 = π D2 n / 60
C_m2 = Q / (π D2 b k_b2)
σ = 1 - sqrt(sin β2) / Z^0.7
C_u2 = σ U2 - C_m2 cot β2
Δp_E = ρ U2 C_u2
```

## Compilación

Desde esta carpeta:

```bash
pdflatex reporte_diseno_sirocco.tex
pdflatex reporte_diseno_sirocco.tex
```

La segunda ejecución actualiza el índice y las referencias internas.

## Relación con el informe principal

El documento recomendado para presentar es
`09_reporte/Informe_Diseno_Ventilador_Sirocco.pdf`, porque incluye la revisión
mecánica, el modelo 3D y más figuras. Esta versión LaTeX puede mantenerse como
alternativa editable.
