# Planos y geometria V1

El archivo `esquema_dimensional_sirocco.svg` se genera desde el calculador y
muestra las dimensiones congeladas para iniciar CAD:

- Rodete `D2 = 600 mm`, `D1 = 510 mm`, ancho `230 mm`.
- Doble entrada.
- Voluta de `280 mm` de ancho interior.
- Descarga teorica `280 x 714 mm`.
- Holgura lengua-rodete `48 mm`.
- Eje preliminar `35 mm` segun la memoria mecanica.

El SVG es un esquema de predimensionamiento, no un plano de taller. Todavia
faltan tolerancias, materiales definitivos, uniones, balanceo y calculo
estructural.

## Archivos CAD V1.1

- `rodete_sirocco_v1.dxf`: vista 2D con 48 contornos de alabe y circulos de referencia.
- `voluta_sirocco_v1.dxf`: espiral exterior, rodete de referencia y conducto de salida.
- `perfil_alabe_v1.csv`: coordenadas de la linea media de un alabe.
- `parametros_geometria_v1.json`: parametros exactos usados por el generador.
- `geometria_cad_v1.svg`: vista previa del rodete y la voluta.

La curva media del alabe es un arco circular que satisface `D1`, `D2`,
`beta1 = 17.5 grados` y `beta2 = 125 grados`. El DXF usa milimetros y formato
ASCII R12 para facilitar su importacion en programas CAD.
