# Modelos 3D del ventilador Sirocco

Todos los modelos utilizan milimetros y se generan con:

```bash
python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d
```

- `rodete_sirocco_v1_2.obj`: rodete de doble entrada, eje y polea.
- `voluta_sirocco_v1_2.obj`: carcasa espiral y descarga.
- `conjunto_sirocco_v1_2.obj`: ensamble de revision.
- `materiales_sirocco.mtl`: materiales para visores OBJ.
- `modelo_sirocco_v1_2.json`: datos geometricos legibles.
- `modelo_sirocco_v1_2.js`: datos cargados por la interfaz offline.

Estas mallas son modelos conceptuales para revision y presentacion. Antes de
fabricar deben definirse espesores de carcasa, uniones, tolerancias, balanceo y
validaciones CFD/estructurales.
