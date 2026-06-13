# Documentación de `09_reporte`

## Propósito

Contener el informe principal de presentación y las figuras que lo sustentan.
El PDF se genera desde los calculadores para mantener consistencia entre texto,
tablas y resultados.

## Informe principal

### `Informe_Diseno_Ventilador_Sirocco.pdf`

- Formato A4.
- 12 páginas.
- Incluye resumen, metodología, rodete, presión, pérdidas, potencia, voluta,
  mecánica, semejanza, interfaz 3D, archivos reproducibles, conclusiones y
  referencias.
- Punto vigente: `10 800 m³/h`, `882.6 Pa`, `1100 rpm`, motor `5.5 kW`.

### `Informe_Diseno_Ventilador_Sirocco.md`

Resumen textual del informe y enlace lógico con los entregables. No contiene
todo el desarrollo visual del PDF.

## Figuras

- `modelo_3d_rotor.png`: rodete, eje, polea y soportes.
- `modelo_3d_assembly.png`: conjunto con voluta.
- `interfaz_3d.png`: captura completa del visor.
- `geometria_cad_2d.png`: geometría de rodete y voluta.
- `perdidas_presion.png`: presupuesto de pérdidas.
- `ley_area_voluta.png`: área y radio frente al ángulo.
- `leyes_afinidad.png`: variación con rpm.
- `momento_flector.png`: diagrama del eje.

## Regeneración

```bash
python3 08_software/generar_reporte_pdf.py
```

El generador importa `calculo_sirocco.py` y `calculo_mecanico_sirocco.py`. Por
eso los cambios de diseño deben hacerse primero en los calculadores.

## Cómo revisar

1. Comprobar portada y nombres de integrantes.
2. Verificar que las tablas coincidan con `06_calculos/`.
3. Revisar que las imágenes no estén cortadas.
4. Confirmar que se mantenga la advertencia de diseño preliminar.
5. No presentar los resultados como ensayo o certificación.

## Documento recomendado para entregar

Usar este PDF como memoria principal. El PDF de `documento_latex/` es una
versión alternativa más breve y no incluye toda la revisión V1.2.
