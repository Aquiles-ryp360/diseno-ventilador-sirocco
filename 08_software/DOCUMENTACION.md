# Documentación de `08_software`

## Propósito

Esta carpeta convierte el diseño en un proceso reproducible. Los scripts
calculan el punto aerodinámico y mecánico, generan geometría CAD y 3D, producen
el informe PDF y verifican resultados mediante pruebas automáticas.

## Requisitos

- Python 3.10 o superior.
- Biblioteca estándar para los cálculos, CSV, JSON, DXF y OBJ.
- `pytest` para pruebas.
- `matplotlib`, `numpy` y `reportlab` para generar el informe PDF.

## Scripts

### `calculo_sirocco.py`

Responsable del cálculo aerodinámico unidimensional.

Funciones importantes:

- `factor_bloqueo()`: fracción abierta del paso.
- `resolver_entrada_sin_incidencia()`: iteración de `β1`.
- `factor_deslizamiento_wiesner()`: corrección de salida.
- `tabla_voluta()`: ley de área y radio exterior.
- `semejanza()`: modelo a escala.
- `calcular()`: reúne presión, potencia, pérdidas, voluta y torsión.
- `exportar()`: crea CSV, JSON y SVG.

Uso:

```bash
python3 08_software/calculo_sirocco.py
python3 08_software/calculo_sirocco.py --json
python3 08_software/calculo_sirocco.py --caudal 3 --presion 90 --rpm 1100
python3 08_software/calculo_sirocco.py \
  --exportar 06_calculos/resultados_v1
```

### `calculo_mecanico_sirocco.py`

Calcula volumen y masa de piezas, torque, carga radial de correa, reacciones,
momento flector, diámetro ASME, flecha, velocidad crítica y capacidad dinámica
de rodamientos.

```bash
python3 08_software/calculo_mecanico_sirocco.py
```

### `generar_geometria_cad.py`

Resuelve un arco circular compatible con `D1`, `D2`, `β1` y `β2`; genera 48
contornos de álabe, la espiral de voluta y exporta DXF R12, CSV, JSON y SVG.

```bash
python3 08_software/generar_geometria_cad.py --salida 07_planos
```

### `generar_modelo_3d.py`

Extruye los contornos 2D, crea cilindros y la malla de voluta, y exporta OBJ,
MTL, JSON y JavaScript.

```bash
python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d
```

### `generar_reporte_pdf.py`

Importa directamente los calculadores para evitar copiar números manualmente.
Genera gráficos de pérdidas, voluta, afinidad y momento; después crea el PDF A4
de 12 páginas y su resumen Markdown.

```bash
python3 08_software/generar_reporte_pdf.py
```

### `generar_manual_documentacion.py`

Reúne los archivos `DOCUMENTACION.md`, inserta las figuras técnicas, genera un
HTML con estilo y lo imprime como PDF mediante Chromium. También produce una
copia DOCX con Pandoc.

```bash
python3 08_software/generar_manual_documentacion.py
```

## Mapa de ecuaciones implementadas

| Tema | Ecuación principal | Script |
|---|---|---|
| Conversión de presión | `Δp = H·9.80665` | `calculo_sirocco.py` |
| Potencia útil | `P = QΔp` | `calculo_sirocco.py` |
| Velocidad periférica | `U = πDn/60` | `calculo_sirocco.py` |
| Bloqueo | `k_b = 1-Zt/(πD sinβ)` | `calculo_sirocco.py` |
| Flujo meridional | `C_m = Q/(πDbk_b)` | `calculo_sirocco.py` |
| Deslizamiento | `σ = 1-sqrt(sinβ2)/Z^0.7` | `calculo_sirocco.py` |
| Euler | `Δp_E = ρU2C_u2` | `calculo_sirocco.py` |
| Voluta | `A(θ)=A_s θ/360` | `calculo_sirocco.py` |
| Torque | `T=P/ω` | ambos calculadores |
| Eje | `d=[16M_eq/(πτ)]^(1/3)` | `calculo_mecanico_sirocco.py` |
| Velocidad crítica | `n_cr=(30/π)sqrt(g/δ)` | `calculo_mecanico_sirocco.py` |
| Rodamiento | `C=P(60nL_h/10⁶)^(1/3)` | `calculo_mecanico_sirocco.py` |
| Semejanza | `Q∝nD³`, `Δp∝n²D²`, `P∝n³D⁵` | `calculo_sirocco.py` |

La explicación completa está en `06_calculos/DOCUMENTACION.md`.

## Pruebas automáticas

La suite contiene 14 pruebas:

- Conversión de unidades y punto de operación.
- Cierre de presión, potencia y geometría.
- Crecimiento monótono de la voluta.
- Leyes de semejanza.
- Sobrecarga a `1500 rpm`.
- Masa, correa, flexión, eje y rodamientos.
- Radios y curvatura del álabe CAD.
- Archivos y tamaño mínimo de las mallas OBJ.
- Portabilidad y parámetros de la interfaz 3D.
- Existencia de documentación en todas las carpetas.
- Integridad básica del manual PDF consolidado.

Ejecutar:

```bash
python3 -m pytest -q 08_software
```

## Flujo completo de regeneración

```bash
python3 08_software/calculo_sirocco.py \
  --exportar 06_calculos/resultados_v1
python3 08_software/calculo_mecanico_sirocco.py \
  --salida 06_calculos/resultados_mecanicos_v1
python3 08_software/generar_geometria_cad.py --salida 07_planos
python3 08_software/generar_modelo_3d.py --salida 07_modelos_3d
python3 08_software/generar_reporte_pdf.py
python3 08_software/generar_manual_documentacion.py
python3 -m pytest -q 08_software
```

## Cómo modificar el diseño

Los valores base están en la clase `DatosDiseno`. Para cambios permanentes,
editar esa clase y regenerar todos los entregables. Para tanteos de caudal,
presión y rpm se pueden usar argumentos de línea de comandos.

Después de cualquier cambio debe revisarse:

1. Que el motor continúe superando la potencia calculada.
2. Que `β1`, bloqueo y velocidades permanezcan en rangos coherentes.
3. Que no se mezclen resultados de versiones diferentes.
4. Que todas las pruebas pasen.

## Limitaciones del software

No ejecuta CFD, FEA, optimización automática, selección comercial ni análisis
de ruido. Los resultados son predimensionamientos y geometría conceptual.
