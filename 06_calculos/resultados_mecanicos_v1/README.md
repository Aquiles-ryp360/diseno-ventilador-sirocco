# Resultados mecánicos V1

Esta subcarpeta se genera con:

```bash
python3 08_software/calculo_mecanico_sirocco.py \
  --salida 06_calculos/resultados_mecanicos_v1
```

`resultado_mecanico_v1.json` contiene:

- Geometría usada por el modelo mecánico.
- Masa de cada componente y masa total del rotor.
- Torque, carga de correa, reacciones y momento máximo.
- Diámetro ASME y diámetro adoptado del eje.
- Flecha estática y primera velocidad crítica.
- Vida objetivo y capacidad dinámica mínima de rodamientos.

Los valores son preliminares y deben actualizarse con masa CAD, polea real,
soportes definitivos y análisis estructural.
