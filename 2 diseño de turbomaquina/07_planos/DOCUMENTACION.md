# Documentación de `07_planos`

## Propósito

Contener la geometría bidimensional generada a partir del cálculo vigente. Los
archivos permiten revisar el perfil del álabe, la repetición de los 48 álabes y
la espiral preliminar de la voluta en programas CAD.

## Sistema de unidades y coordenadas

- Los archivos DXF usan milímetros.
- El eje del rodete está en `(0, 0)`.
- La geometría se dibuja en el plano `XY`.
- El eje axial y el ancho del rodete se incorporan posteriormente en 3D.

## Archivos

### `rodete_sirocco_v1.dxf`

DXF ASCII R12 con:

- Círculo de referencia `D2 = 600 mm`.
- Círculo de entrada `D1 = 510 mm`.
- Círculo de cubo de referencia.
- 48 contornos cerrados de álabe.

Capas principales: `D2_REFERENCIA`, `D1_REFERENCIA`, `CUBO_REFERENCIA` y
`ALABES`.

### `voluta_sirocco_v1.dxf`

Incluye el círculo de referencia del rodete, la polilínea exterior de la
voluta y las tres líneas de la descarga.

### `perfil_alabe_v1.csv`

Contiene 81 estaciones de la línea media del álabe: índice, `x`, `y`, radio
global y ángulo polar.

### `parametros_geometria_v1.json`

Parámetros exactos del arco circular:

- Radio de curvatura: `30.07 mm`.
- Centro: `(283.68, 9.04) mm`.
- Desfase polar de salida: `-3.15°`.
- Ángulos: `β1 = 17.5°`, `β2 = 125°`.

### Archivos SVG

- `geometria_cad_v1.svg`: revisión visual del rodete y la voluta.
- `esquema_dimensional_sirocco.svg`: dimensiones globales.

## Construcción del álabe

Se busca un arco circular que pase por los radios:

```text
r1 = D1/2 = 255 mm
r2 = D2/2 = 300 mm
```

y que tenga tangentes compatibles con `β1` y `β2`. El generador resuelve el
desfase angular `δ` imponiendo que el desplazamiento entre extremos y la
diferencia de normales sean colineales:

```text
cross(P2 - P1, n1 - n2) = 0
```

Después calcula el radio de curvatura y el centro. Los puntos del arco son:

```text
x(φ) = x_c + R_c cos φ
y(φ) = y_c + R_c sin φ
```

El contorno se obtiene con dos arcos concéntricos:

```text
R_exterior = R_c + t/2
R_interior = R_c - t/2
```

con `t = 1.2 mm`.

## Repetición circunferencial

Cada punto del álabe base se rota para `i = 0 ... 47`:

```text
α_i = 2π i / Z
x' = x cos α_i - y sin α_i
y' = x sin α_i + y cos α_i
```

## Construcción de la voluta

```text
A_salida = Q / V_salida
A(θ) = A_salida θ / 360°
R_ext(θ) = D2/2 + g + A(θ)/B
x = R_ext cos θ
y = R_ext sin θ
```

El perfil DXF usa una estación cada `2°`.

## Regeneración

```bash
python3 08_software/generar_geometria_cad.py --salida 07_planos
```

## Programas para abrir los archivos

- FreeCAD.
- LibreCAD.
- AutoCAD.
- SolidWorks mediante importación DXF.
- Navegador web para los SVG.
- Hoja de cálculo para el CSV.

## Límites de uso

Estos archivos son geometría conceptual. No incluyen tolerancias, dobleces,
radios de soldadura, espesores de carcasa, agujeros, chaveta, pernos, guardas,
acabados ni especificaciones de balanceo.
