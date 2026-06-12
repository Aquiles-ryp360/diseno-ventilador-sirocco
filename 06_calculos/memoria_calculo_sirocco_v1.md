# Memoria de calculo V1 - Ventilador centrifugo tipo Sirocco

Fecha de revision: 2026-06-12

## 1. Alcance

Esta memoria cierra el predimensionamiento unidimensional de un ventilador
centrifugo multialabe, de doble ancho y doble entrada, para aire limpio. El
punto solicitado por el docente es:

- Caudal: `Q = 3.00 m3/s = 10 800 m3/h`.
- Presion estatica: `Delta p_s = 90 mmH2O = 882.6 Pa`.
- Densidad de calculo: `rho = 1.20 kg/m3`.

Los resultados son adecuados para preparar geometria CAD y un caso CFD. No son
todavia datos certificados de fabricacion. La interaccion tridimensional entre
rodete, lengua y voluta debe verificarse mediante simulacion y ensayo.

## 2. Configuracion seleccionada

Se selecciona doble entrada porque una unica abertura de `D1 = 0.51 m` obligaria
a trabajar con una velocidad axial elevada para `3 m3/s`. Esta configuracion es
coherente con ventiladores comerciales de alabes hacia adelante, que pueden ser
de doble ancho, doble entrada y transmision por correas.

| Parametro | Seleccion V1 |
|---|---:|
| Diametro exterior del rodete `D2` | `0.600 m` |
| Diametro en el borde de entrada `D1` | `0.510 m` |
| Relacion `D1/D2` | `0.850` |
| Ancho del rodete `b` | `0.230 m` |
| Relacion `b/D2` | `0.383` |
| Entradas | `2` |
| Velocidad | `1100 rpm` |
| Numero de alabes `Z` | `48` |
| Espesor preliminar de alabe | `1.2 mm` |
| Angulo de salida `beta2` | `125 grados` desde la tangente |
| Ancho interior de voluta | `0.280 m` |
| Velocidad de descarga | `15 m/s` |

## 3. Potencia requerida

```text
Delta p_s = 90 x 9.80665 = 882.6 Pa
P_aire = Q Delta p_s = 3 x 882.6 = 2.648 kW
```

La potencia util no incluye las perdidas internas ni mecanicas.

## 4. Entrada y triangulo de velocidades

El area total de los dos ojos, descontando un cubo de `0.12 m`, es:

```text
A_ojos = 2 (pi/4) (D1^2 - D_cubo^2) = 0.3859 m2
V_ojos = Q/A_ojos = 7.77 m/s
```

El bloqueo por espesor se calcula proyectando el espesor sobre el paso
circunferencial:

```text
k_b = 1 - Z t / (pi D sin beta)
```

En la entrada, `beta1` se resuelve iterativamente para incidencia nula, porque
el propio bloqueo depende del angulo. El resultado es:

| Magnitud | Resultado |
|---|---:|
| Velocidad periferica `U1` | `29.37 m/s` |
| Factor de paso libre `k_b1` | `0.880` |
| Velocidad meridional `Cm1` | `9.25 m/s` |
| Angulo de entrada `beta1` | `17.5 grados` desde la tangente |

Para fabricacion se puede adoptar `beta1 = 18 grados` y ajustar la curva del
alabe hasta `beta2 = 125 grados`.

## 5. Salida del rodete y trabajo de Euler

```text
U2 = pi D2 n / 60 = 34.56 m/s
k_b2 = 0.963
Cm2 = Q / (pi D2 b k_b2) = 7.19 m/s
```

Como estimacion se usa el factor de deslizamiento de Wiesner:

```text
sigma = 1 - sqrt(sin beta2) / Z^0.7 = 0.940
Cu2 = sigma U2 - Cm2 cot(beta2) = 37.51 m/s
Delta p_E = rho U2 Cu2 = 1555.5 Pa
```

La aplicacion de Wiesner a un rodete Sirocco es una aproximacion. Se conserva
porque permite cerrar un modelo reproducible, pero `Cu2`, el deslizamiento y el
bloqueo efectivo deben extraerse posteriormente del CFD.

Coeficientes del punto V1:

- Coeficiente de flujo `Cm2/U2 = 0.208`.
- Coeficiente de presion estatica `Delta p_s/(rho U2^2) = 0.616`.
- Relacion entre presion estatica y trabajo de Euler: `882.6/1555.5 = 0.567`.

## 6. Potencia al eje y motor

```text
P_Euler = Q Delta p_E = 4.666 kW
P_eje = P_Euler / eta_m = 4.861 kW, con eta_m = 0.96
eta_estatica = P_aire/P_eje = 54.5 %
```

Se mantiene un motor de `5.5 kW`. El margen respecto a la potencia estimada al
eje es `13.1 %`. Se recomienda motor de cuatro polos con transmision por correas
y una relacion aproximada `1100/1750 = 0.629`. Un juego preliminar de poleas de
`125 mm` en el motor y `200 mm` en el ventilador entrega cerca de `1094 rpm`.
La seleccion final de correas depende del catalogo del fabricante.

## 7. Por que se descartan 1500 rpm

La velocidad de `1500 rpm` del primer tanteo no era compatible con el motor
seleccionado al cerrar los triangulos de velocidad.

| Magnitud | `1100 rpm` | `1500 rpm` |
|---|---:|---:|
| Velocidad periferica `U2` | `34.56 m/s` | `47.12 m/s` |
| Presion de Euler estimada | `1555 Pa` | `2789 Pa` |
| Potencia estimada al eje | `4.86 kW` | `8.72 kW` |
| Margen con motor de `5.5 kW` | `+13.1 %` | `-36.9 %` |

Por ello, la velocidad V1 queda fijada en aproximadamente `1100 rpm`.

## 8. Voluta y lengua

La descarga se dimensiona para `15 m/s`:

```text
A_salida = Q/V_salida = 0.200 m2
h_salida = A_salida/B_voluta = 0.714 m
```

La boca rectangular preliminar es `0.28 x 0.714 m`. Puede redondearse para
fabricacion a `0.28 x 0.72 m`, conservando un area de `0.202 m2`.

La separacion minima lengua-rodete se fija en `8 % de D2`, es decir `48 mm`.
Este valor se encuentra cerca de la relacion `0.084` ensayada en un ventilador
multialabe de referencia. En la revision V1.1, la ley de areas de flujo es
lineal y la holgura se incorpora por separado a la geometria radial:

```text
A(theta) = A_salida theta/360
R_exterior(theta) = D2/2 + holgura_lengua + A(theta)/B_voluta
```

| Angulo | Area `m2` | Altura de flujo `m` | Radio exterior `m` |
|---:|---:|---:|---:|
| 0 | 0.000 | 0.000 | 0.348 |
| 45 | 0.025 | 0.089 | 0.437 |
| 90 | 0.050 | 0.179 | 0.527 |
| 135 | 0.075 | 0.268 | 0.616 |
| 180 | 0.100 | 0.357 | 0.705 |
| 225 | 0.125 | 0.446 | 0.794 |
| 270 | 0.150 | 0.536 | 0.884 |
| 315 | 0.175 | 0.625 | 0.973 |
| 360 | 0.200 | 0.714 | 1.062 |

Esta tabla define una primera espiral de seccion rectangular y ancho constante.
La carcasa final puede suavizarse con una curva continua, conservando las areas.

## 9. Presupuesto preliminar de perdidas

La diferencia entre el trabajo de Euler y la presion estatica pedida es
`672.9 Pa`. Se distribuye como presupuesto para orientar el CFD, no como una
medicion:

| Componente | Perdida asignada |
|---|---:|
| Entrada y bellmouth | `7.3 Pa` |
| Pasajes, estela y separacion | `238.8 Pa` |
| Recirculacion y fugas | `106.1 Pa` |
| Voluta y lengua | `132.7 Pa` |
| Margen del modelo 1D | `53.1 Pa` |
| Energia cinetica en descarga | `135.0 Pa` |
| **Total** | **`672.9 Pa`** |

La simulacion debe sustituir esta distribucion por integrales de presion total,
presion estatica y disipacion por regiones.

## 10. Eje y soportes

Con `P_eje = 4.861 kW` y `1100 rpm`:

```text
T = P/omega = 42.20 N m
T_diseno = 1.5 T = 63.30 N m
d_min = (16 T_diseno/(pi tau_adm))^(1/3) = 22.1 mm
```

Para incluir chavetero, flexion, desalineacion e incertidumbre de masa se adopta
un eje preliminar de acero de `30 mm`. Esto permite usar soportes comerciales de
30 mm, pero la seleccion de rodamientos queda pendiente hasta conocer masa del
rodete, distancia entre apoyos y desbalance admisible.

## 11. Modelo por semejanza a escala 1:2

| Condicion | Diametro | rpm | Caudal | Presion | Potencia eje |
|---|---:|---:|---:|---:|---:|
| Misma rpm | `0.30 m` | `1100` | `0.375 m3/s` | `220.6 Pa` | `0.152 kW` |
| Misma velocidad periferica | `0.30 m` | `2200` | `0.750 m3/s` | `882.6 Pa` | `1.215 kW` |

Para una maqueta demostrativa es mas segura la primera opcion. Para reproducir
la presion del prototipo debe usarse la segunda y verificar resistencia,
balanceo y numero de Reynolds.

## 12. Geometria del alabe para CAD V1.1

Para obtener una curva fabricable se adopta un arco circular que pasa por los
radios `D1/2` y `D2/2` y cumple las tangentes `beta1 = 17.5 grados` y
`beta2 = 125 grados`. La solucion geometrica es:

- Radio de curvatura de la linea media: `30.07 mm`.
- Centro del arco respecto al eje del rodete: `(283.68, 9.04) mm`.
- Desfase polar del borde de salida respecto al de entrada: `-3.15 grados`.
- Espesor normal constante inicial: `1.2 mm`.
- Longitud aproximada de la linea media: `54.8 mm`.
- Paso circunferencial en `D2`: `39.3 mm`.
- Solidez aproximada longitud/paso en salida: `1.39`.

El generador repite el contorno 48 veces y crea un DXF R12 en milimetros. La
curva circular es una base constructiva; el CFD puede justificar cambiarla por
una curva Bezier o una distribucion variable de angulo.

## 13. Dimensiones congeladas para CAD V1.1

- Rodete: `D2 = 600 mm`, `D1 = 510 mm`, `b = 230 mm`.
- Alabes: `48`, espesor inicial `1.2 mm`, `beta1 = 18 grados`,
  `beta2 = 125 grados`.
- Voluta: ancho interior `280 mm`, holgura de lengua `48 mm`.
- Descarga: `280 x 714 mm` antes de redondeo constructivo.
- Eje preliminar: `30 mm`.
- Velocidad de operacion: `1100 rpm`.
- Motor: `5.5 kW` con correas o variador para ajustar el punto.

## 14. Trabajo que aun falta

1. Definir discos laterales, cubo, chaveta, soldaduras y tolerancias.
2. Calcular masa, flexion del eje, vida de rodamientos y velocidad critica.
3. Crear CAD 3D del rodete y la voluta a partir de los DXF.
4. Ejecutar CFD estacionario y transitorio con refinamiento en la lengua.
5. Obtener las curvas `Delta p-Q`, potencia y eficiencia.
6. Corregir la geometria y preparar planos finales.
7. Ensayar el prototipo con medicion de caudal, presion, rpm y potencia.

## 15. Referencias tecnicas usadas en esta revision

- AMCA International, *Derivation of the Fan Laws*:
  https://www.amca.org/assets/resources/public/pdf/White%20Papers/2020%20-%20Derivation%20of%20the%20Fan%20Laws.pdf
- Greenheck, ejemplo de ventiladores forward-curved de doble ancho y doble
  entrada: https://content.greenheck.com/public/DAMProd/Original/10001/482886_dgdgxtsuvsu_iom_Rev5_September2022.pdf
- Hao et al. (2020), datos geometricos y estudio experimental de lengua de
  voluta: https://doi.org/10.1177/0020294020932360
- Wang et al. (2023), estructuras de flujo cerca de la lengua:
  https://doi.org/10.1115/1.4056279

Los valores numericos reproducibles se generan con
`08_software/calculo_sirocco.py`.
