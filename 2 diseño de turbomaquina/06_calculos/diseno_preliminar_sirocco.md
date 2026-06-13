# Diseno preliminar del ventilador Sirocco

> **Documento historico.** Este fue el primer tanteo del proyecto. La revision
> aerodinamica vigente esta en `memoria_calculo_sirocco_v1.md`. En particular,
> la velocidad de `1500 rpm`, `D1 = 0.42 a 0.45 m` y `b2 = 0.25 m` ya no son la
> seleccion recomendada: el cierre unidimensional llevo a `1100 rpm`, doble
> entrada, `D1 = 0.51 m` y `b = 0.23 m`.

## 1. Datos de entrada

| Magnitud | Simbolo | Valor |
|---|---:|---:|
| Caudal | `Q` | `3 m3/s` |
| Altura de presion | `H` | `90 mmH2O` |
| Presion equivalente | `Delta p` | `882.6 Pa` |
| Densidad del aire | `rho` | `1.2 kg/m3` |
| Eficiencia global preliminar | `eta_g` | `0.50 a 0.60` |

## 2. Potencia

```text
Delta p = 90 x 9.80665 = 882.6 Pa
P_aire = Q Delta p = 3 x 882.6 = 2647.8 W
P_eje = P_aire / eta_g
```

| Eficiencia | Potencia al eje |
|---:|---:|
| 0.50 | 5.30 kW |
| 0.55 | 4.81 kW |
| 0.60 | 4.41 kW |

Seleccion preliminar: motor de `5.5 kW`.

## 3. Predimensionamiento del rodete

Supuestos preliminares:

- Rodete centrifugo multialabe de alabes curvados hacia adelante.
- Velocidad nominal cercana a `1500 rpm`.
- Diametro exterior inicial `D2 = 0.60 m`.
- Ancho `b2 = 0.25 m`.

```text
U2 = pi D2 n / 60
U2 = pi x 0.60 x 1500 / 60 = 47.1 m/s

Cm2 = Q / (pi D2 b2)
Cm2 = 3 / (pi x 0.60 x 0.25) = 6.37 m/s

psi = Delta p / (rho U2^2)
psi = 882.6 / (1.2 x 47.1^2) = 0.33
```

El coeficiente de presion `psi = 0.33` es razonable para un ventilador centrifugo de baja-media presion.

## 4. Geometria preliminar

| Parametro | Valor recomendado inicial |
|---|---:|
| `D2` | `0.60 m` |
| `D1` | `0.42 a 0.45 m` |
| `b2` | `0.25 m` |
| `n` | `1500 rpm` |
| `Z` | `36 a 48 alabes` |
| `beta2` | `120 a 140 grados` |
| `beta1` | pendiente de definir con triangulo de entrada |
| Separacion lengua-rodete | `5% a 10% de D2` como punto de partida |

## 5. Voluta preliminar

Para limitar perdidas de descarga:

```text
A_salida = Q / V_salida
```

Si `V_salida = 12 a 15 m/s`:

| Velocidad de salida | Area requerida |
|---:|---:|
| 12 m/s | 0.250 m2 |
| 15 m/s | 0.200 m2 |

Se recomienda una boca rectangular inicial de aproximadamente:

- `0.50 m x 0.50 m` para `A = 0.25 m2`, o
- `0.40 m x 0.50 m` para `A = 0.20 m2`.

La voluta debe crecer con el angulo para conservar momento angular o velocidad media aproximadamente controlada:

```text
A(theta) = A_salida x theta / 360
```

Esta ley debe refinarse con el ancho real de carcasa y el radio de la espiral.

## 6. Perdidas a incluir

- Perdida de entrada y contraccion.
- Perdidas por incidencia en el rodete.
- Perdidas por friccion en canales entre alabes.
- Perdida por deslizamiento.
- Recirculacion interna.
- Perdida por choque en lengua de voluta.
- Perdidas por difusion/recuperacion en voluta.
- Perdidas mecanicas: rodamientos, transmision y ventilacion secundaria.

## 7. Semejanza para modelo

Si se construye un modelo a escala `lambda = D_modelo / D_prototipo`, mantener:

```text
Q_modelo / Q_prototipo = lambda^3 x (n_modelo / n_prototipo)
Delta p_modelo / Delta p_prototipo = lambda^2 x (n_modelo / n_prototipo)^2
P_modelo / P_prototipo = lambda^5 x (n_modelo / n_prototipo)^3
```

Para un modelo geometrico a escala debe verificarse tambien que el regimen de Reynolds no quede demasiado bajo.
