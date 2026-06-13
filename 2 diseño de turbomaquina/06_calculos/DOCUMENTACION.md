# Documentación de `06_calculos`

## Propósito

Esta carpeta contiene la memoria técnica del predimensionamiento aerodinámico y
mecánico. Es la principal referencia para explicar qué se calculó, qué
ecuaciones se usaron, qué resultados se obtuvieron y qué hipótesis todavía
deben validarse.

## Punto de diseño vigente

| Magnitud | Símbolo | Valor |
|---|---:|---:|
| Caudal | `Q` | `3.0 m³/s = 10 800 m³/h` |
| Altura de presión | `H` | `90 mmH₂O` |
| Presión estática | `Δp_s` | `882.6 Pa` |
| Densidad del aire | `ρ` | `1.20 kg/m³` |
| Velocidad | `n` | `1100 rpm` |
| Diámetro exterior | `D2` | `0.600 m` |
| Diámetro de entrada | `D1` | `0.510 m` |
| Ancho de rodete | `b` | `0.230 m` |
| Número de álabes | `Z` | `48` |
| Espesor de álabe | `t` | `1.2 mm` |
| Ángulo de salida | `β2` | `125°` desde la tangente |

## Archivos principales

### `memoria_calculo_sirocco_v1.md`

Memoria aerodinámica vigente. Explica selección de doble entrada, triángulos de
velocidad, presión de Euler, potencia, voluta, pérdidas, semejanza y geometría
del álabe.

### `memoria_mecanica_sirocco_v1.md`

Memoria mecánica vigente. Explica masa, carga de correa, reacciones, flexión,
diámetro del eje, velocidad crítica y capacidad de rodamientos.

### `diseno_preliminar_sirocco.md`

Primer tanteo histórico. Contiene una propuesta a `1500 rpm` que fue descartada
al cerrar potencia y presión. No debe usarse como selección final.

## 1. Conversión de presión

La altura en milímetros de agua se convierte a presión mediante:

```text
Δp_s = H · 9.80665
Δp_s = 90 · 9.80665 = 882.5985 Pa
```

El factor `9.80665` convierte `mmH₂O` a pascales bajo gravedad estándar.

## 2. Potencia útil del aire

```text
P_aire = Q · Δp_s
P_aire = 3.0 · 882.5985 = 2647.8 W = 2.648 kW
```

Esta es la potencia útil entregada al aire. No incluye pérdidas aerodinámicas,
mecánicas ni de transmisión.

## 3. Área y velocidad en los ojos de entrada

El rodete es de doble entrada. El área total de los dos ojos, descontando el
cubo, se calcula como:

```text
A_ojos = N_e · (π/4) · (D1² - D_cubo²)
V_ojos = Q / A_ojos
```

Con `N_e = 2` y `D_cubo = 0.12 m`:

```text
A_ojos = 0.3859 m²
V_ojos = 7.77 m/s
```

## 4. Velocidad periférica

Para cualquier radio de cálculo:

```text
U = π D n / 60
```

Resultados:

```text
U1 = π · 0.510 · 1100 / 60 = 29.37 m/s
U2 = π · 0.600 · 1100 / 60 = 34.56 m/s
```

## 5. Factor de bloqueo por espesor

Los álabes ocupan parte del paso circunferencial. La fracción abierta se estima
mediante:

```text
k_b = 1 - Z t / (π D sin β)
```

Donde `β` se mide desde la tangente. Resultados:

- Entrada: `k_b1 = 0.880`.
- Salida: `k_b2 = 0.963`.

Esta corrección es geométrica y no representa por sí sola la capa límite ni la
estela real del álabe.

## 6. Velocidad meridional

```text
C_m = Q / (π D b k_b)
```

Resultados:

```text
C_m1 = 9.25 m/s
C_m2 = 7.19 m/s
```

## 7. Ángulo de entrada sin incidencia

Se supone que el aire entra sin componente tangencial apreciable. El ángulo de
entrada se obtiene de:

```text
β1 = atan(C_m1 / U1)
```

Como `C_m1` depende de `k_b1` y `k_b1` depende de `β1`, la ecuación se resuelve
iterativamente. El resultado es:

```text
β1 = 17.48°
```

Para geometría CAD se redondea a `17.5°` o `18°` según el nivel de detalle.

## 8. Factor de deslizamiento de Wiesner

La componente tangencial real se reduce por el número finito de álabes. Se usa
la estimación:

```text
σ = 1 - sqrt(sin β2) / Z^0.7
σ = 0.940
```

Su aplicación a un rodete Sirocco es una aproximación que debe contrastarse con
CFD o ensayo.

## 9. Componente tangencial de salida

```text
C_u2 = σ U2 - C_m2 / tan β2
```

Con álabes curvados hacia adelante y `β2 = 125°`:

```text
C_u2 = 37.51 m/s
```

## 10. Ecuación de Euler

La presión teórica transferida por el rodete se estima mediante:

```text
Δp_E = ρ (U2 C_u2 - U1 C_u1)
```

Suponiendo `C_u1 ≈ 0`:

```text
Δp_E = ρ U2 C_u2
Δp_E = 1.2 · 34.56 · 37.51 = 1555.5 Pa
```

La diferencia entre `1555.5 Pa` y la presión estática requerida de `882.6 Pa`
se interpreta como energía cinética y pérdidas internas del sistema.

## 11. Coeficientes adimensionales

```text
φ = C_m2 / U2 = 0.208
ψ_s = Δp_s / (ρ U2²) = 0.616
```

Estos coeficientes permiten comparar el punto con otras geometrías y aplicar
criterios de semejanza.

## 12. Potencia de Euler, potencia al eje y eficiencia

```text
P_Euler = Q · Δp_E = 4.666 kW
P_eje = P_Euler / η_m
P_eje = 4.666 / 0.96 = 4.861 kW
η_estática = P_aire / P_eje = 54.5 %
```

Se selecciona un motor de `5.5 kW`:

```text
Margen = P_motor / P_eje - 1 = 13.1 %
```

## 13. Razón para descartar 1500 rpm

Al aumentar la velocidad, la presión crece aproximadamente con `n²` y la
potencia con `n³`. El cálculo directo a `1500 rpm` entrega más de `8 kW` al eje,
superando el motor de `5.5 kW`. Por eso la revisión vigente usa `1100 rpm`.

## 14. Voluta y descarga

El área de salida se fija con la velocidad deseada:

```text
A_salida = Q / V_salida
A_salida = 3 / 15 = 0.200 m²
```

Con ancho interior `B = 0.280 m`:

```text
h_salida = A_salida / B
h_salida = 0.200 / 0.280 = 0.714 m
```

La descarga preliminar es `280 × 714 mm`.

## 15. Ley de área de la voluta

El caudal acumulado se aproxima linealmente con el ángulo:

```text
A(θ) = A_salida · θ / 360°
```

La holgura de lengua es:

```text
g = 0.08 D2 = 0.048 m
```

El radio exterior se obtiene de:

```text
R_ext(θ) = D2/2 + g + A(θ)/B
```

Por ello el radio crece desde `0.348 m` en la lengua hasta `1.062 m` al
completar la espiral.

## 16. Presupuesto de pérdidas

La diferencia de presión es:

```text
Δp_pérdidas = Δp_E - Δp_s = 672.9 Pa
```

Distribución preliminar:

| Componente | Pérdida |
|---|---:|
| Entrada y bellmouth | `7.3 Pa` |
| Pasajes, estela y separación | `238.8 Pa` |
| Recirculación y fugas | `106.1 Pa` |
| Voluta y lengua | `132.7 Pa` |
| Margen del modelo 1D | `53.1 Pa` |
| Energía cinética de descarga | `135.0 Pa` |

Las pérdidas de entrada y descarga usan presión dinámica:

```text
q_d = 0.5 ρ V²
```

El resto es un reparto de ingeniería para orientar la simulación, no una
medición experimental.

## 17. Torque del eje

```text
ω = 2πn / 60
T = P_eje / ω = 42.20 N·m
```

Para el tanteo torsional se usa factor de servicio `K_s = 1.5`:

```text
T_d = K_s T = 63.30 N·m
d_t = [16 T_d / (π τ_adm)]^(1/3)
```

Con `τ_adm = 30 MPa`, el diámetro matemático es `22.1 mm`. El redondeo
torsional inicial a `30 mm` no es la selección mecánica final.

## 18. Masa del rotor

Cada masa se calcula como:

```text
m = ρ_acero · volumen
```

Se suman álabes, dos anillos, disco central y cubo. Luego se aplica `8 %` por
soldaduras y refuerzos:

```text
m_rotor = 18.63 kg
W_rotor = m_rotor g ≈ 182.7 N
```

## 19. Carga radial de la correa

Para una polea de diámetro `D_p = 0.20 m`:

```text
F_t = 2T / D_p = 422 N
F_correa = 2.5 F_t = 1055 N
```

El factor `2.5` representa la relación preliminar entre carga radial total y
fuerza tangencial transmitida.

## 20. Reacciones y momento flector

Con apoyos separados por `L = 0.50 m`, rodete centrado en `x_r = 0.25 m` y
polea en `x_p = 0.575 m`:

```text
R_B = (W_rotor x_r + F_correa x_p) / L
R_A = W_rotor + F_correa - R_B
```

El diagrama de momentos se obtiene sumando las contribuciones de cada reacción
y carga según la posición. El máximo calculado es `79.0 N·m` junto al apoyo de
la polea.

## 21. Diámetro mecánico del eje

Se usa un momento equivalente tipo ASME:

```text
M_eq = sqrt[(K_b M_max)² + (K_t T)²]
d = [16 M_eq / (π τ_adm)]^(1/3)
```

Con `K_b = K_t = 1.5` se obtiene aproximadamente `28.4 mm`. Aplicando un factor
de `1.20` por chavetero y concentración de esfuerzos:

```text
d_corregido ≈ 34.1 mm
d_adoptado = 35 mm
```

## 22. Flecha y primera velocidad crítica

Para una carga central simplificada:

```text
I = π d⁴ / 64
δ = W_rotor L³ / (48 E I)
n_cr = (30/π) sqrt(g/δ)
```

Con `E = 200 GPa` y eje de `35 mm`:

```text
δ ≈ 0.032 mm
n_cr ≈ 5260 rpm
n_cr / n_operación ≈ 4.8
```

La verificación final debe incluir masa distribuida, polea, rigidez de soportes
y efectos giroscópicos.

## 23. Vida y capacidad del rodamiento

Para rodamientos de bolas se usa el exponente `p = 3`:

```text
L_10 = (C/P)^3 · 10⁶ revoluciones
C = P · (60 n L_h / 10⁶)^(1/3)
```

Con vida objetivo de `20 000 h`, la capacidad dinámica mínima calculada es
`14.3 kN`. La memoria recomienda seleccionar `C ≥ 20 kN` como margen inicial.

## 24. Fuerza centrífuga de un álabe

```text
F_c = m_álabe · ω² · r_medio
```

El resultado preliminar es aproximadamente `437 N` por álabe. Las uniones
soldadas todavía requieren FEA y verificación de fatiga.

## 25. Leyes de semejanza

Para dos ventiladores geométricamente semejantes:

```text
Q₂/Q₁ = (n₂/n₁)(D₂/D₁)³
Δp₂/Δp₁ = (n₂/n₁)²(D₂/D₁)²
P₂/P₁ = (n₂/n₁)³(D₂/D₁)⁵
```

Para escala `λ = 0.5`:

| Condición | rpm | Caudal | Presión | Potencia eje |
|---|---:|---:|---:|---:|
| Misma rpm | `1100` | `0.375 m³/s` | `220.6 Pa` | `0.152 kW` |
| Misma velocidad periférica | `2200` | `0.750 m³/s` | `882.6 Pa` | `1.215 kW` |

Debe revisarse también el número de Reynolds y las holguras relativas.

## Resultados generados

### `resultados_v1/`

- `resultado_completo.json`: todos los resultados aerodinámicos.
- `resumen_diseno.csv`: 29 variables resumidas.
- `tabla_voluta.csv`: 9 estaciones angulares.
- `presupuesto_perdidas.csv`: 6 componentes de pérdida.
- `semejanza_modelo.csv`: 2 condiciones a escala 1:2.
- `esquema_dimensional_sirocco.svg`: esquema visual.

### `resultados_mecanicos_v1/`

- `resultado_mecanico_v1.json`: masas, cargas, eje y rodamientos.

## Regeneración

```bash
python3 08_software/calculo_sirocco.py \
  --exportar 06_calculos/resultados_v1
python3 08_software/calculo_mecanico_sirocco.py \
  --salida 06_calculos/resultados_mecanicos_v1
```

## Limitaciones

- Modelo aerodinámico unidimensional.
- Factor de deslizamiento no calibrado para este rodete.
- Presupuesto de pérdidas asignado, no medido.
- Voluta de ley lineal sin optimización de lengua.
- Eje representado como viga simplificada.
- Sin FEA de álabes, disco, cubo o soldaduras.
- Sin curvas experimentales `Q-Δp`, potencia, eficiencia, ruido o vibración.
