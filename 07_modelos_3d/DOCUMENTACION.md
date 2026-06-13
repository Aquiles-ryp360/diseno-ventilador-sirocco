# Documentación de `07_modelos_3d`

## Propósito

Contener los modelos conceptuales tridimensionales generados a partir de las
mismas dimensiones usadas en los cálculos y planos 2D.

## Archivos OBJ

| Archivo | Vértices | Caras | Contenido |
|---|---:|---:|---|
| `rodete_sirocco_v1_2.obj` | `11 570` | `16 248` | Álabes, anillos, disco, cubo, eje y polea |
| `voluta_sirocco_v1_2.obj` | `732` | `726` | Pasaje espiral y descarga |
| `conjunto_sirocco_v1_2.obj` | `12 302` | `16 974` | Rodete y voluta combinados |

Las unidades declaradas en los encabezados son milímetros.

## Archivos auxiliares

- `materiales_sirocco.mtl`: materiales y colores para visores OBJ.
- `modelo_sirocco_v1_2.json`: dimensiones, operación y coordenadas.
- `modelo_sirocco_v1_2.js`: mismos datos asignados a
  `window.SIROCCO_DATA` para abrir la interfaz sin servidor.

## Cómo se genera la malla

### Álabes

El contorno 2D de cada álabe se extruye entre:

```text
z0 = -b/2 = -115 mm
z1 = +b/2 = +115 mm
```

Cada lado del polígono produce una cara lateral y las tapas se triangulan desde
un centro geométrico. El álabe se repite 48 veces mediante rotación.

### Anillos, cubo, eje y polea

Se crean con cilindros sólidos o anulares discretizados en segmentos. El disco
central es un cilindro delgado y el eje usa el diámetro mecánico de `35 mm`.

### Voluta

Para cada estación angular se crean un radio interior fijo y un radio exterior
creciente:

```text
r_in = D2/2 + g
r_ext(i) = D2/2 + g + A_salida(i/N)/B
```

Las estaciones de ambas caras axiales se conectan con cuadriláteros.

## Cómo abrir los OBJ

- Blender: `File > Import > Wavefront (.obj)`.
- FreeCAD: `Archivo > Abrir` o importación de malla.
- MeshLab y visores OBJ compatibles.
- Interfaz incluida en `10_interfaz_3d/` para inspección directa.

Al importar, conservar unidades en milímetros y mantener el archivo MTL junto
a los OBJ para recuperar materiales.

## Regeneración

```bash
python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d
```

## Alcance

Las mallas muestran la arquitectura y proporciones. No son sólidos
paramétricos de fabricación y no contienen tolerancias, soldaduras, tornillos,
espesor definitivo de carcasa ni detalles completos de rodamientos.
