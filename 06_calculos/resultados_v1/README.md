# Resultados aerodinámicos V1

Esta subcarpeta es generada por:

```bash
python3 08_software/calculo_sirocco.py \
  --exportar 06_calculos/resultados_v1
```

## Contenido

- `resultado_completo.json`: entradas y resultados completos.
- `resumen_diseno.csv`: variables principales por sección.
- `tabla_voluta.csv`: área y radio exterior entre `0°` y `360°`.
- `presupuesto_perdidas.csv`: distribución preliminar de `672.9 Pa`.
- `semejanza_modelo.csv`: escalamiento a diámetro `0.30 m`.
- `esquema_dimensional_sirocco.svg`: representación dimensional.

No editar manualmente si se desea conservar reproducibilidad. Cambiar los
datos en `DatosDiseno` o mediante los argumentos del calculador y regenerar.
