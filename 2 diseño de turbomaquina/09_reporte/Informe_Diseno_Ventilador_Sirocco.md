# Informe de diseño del ventilador centrífugo Sirocco

Versión fuente resumida del informe generado en PDF.

## Punto de diseño

- Caudal: 3.0 m³/s = 10 800 m³/h.
- Presión estática: 90 mmH₂O = 882.6 Pa.
- Rodete: D2 600 mm, D1 510 mm, ancho 230 mm y 48 álabes.
- Velocidad: 1100 rpm.
- Potencia de eje estimada: 4.86 kW.
- Motor seleccionado: 5.5 kW.
- Voluta: ancho 280 mm, descarga 280 x 714 mm.
- Masa estimada del rotor: 18.63 kg.
- Eje preliminar: 35 mm.
- Rodamiento: capacidad dinámica mínima 14.3 kN.

## Entregables

- `Informe_Diseno_Ventilador_Sirocco.pdf`: memoria técnica para presentación.
- `../07_modelos_3d/`: mallas OBJ del rodete, voluta y conjunto.
- `../10_interfaz_3d/index.html`: interfaz gráfica autónoma.
- `../ABRIR_MODELO_3D.bat`: lanzador para Windows.

## Alcance

El diseño es un predimensionamiento académico. Antes de fabricar se requieren CFD,
análisis estructural, balanceo, tolerancias, selección comercial y ensayo.

Generado el 2026-06-12 mediante `08_software/generar_reporte_pdf.py`.
