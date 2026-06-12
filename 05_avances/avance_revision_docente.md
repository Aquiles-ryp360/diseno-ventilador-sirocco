# Avance para revision docente

## Titulo preliminar

Diseno preliminar de un ventilador centrifugo tipo Sirocco para `Q = 3 m3/s` y `H = 90 mmH2O`

## Datos de diseno

- Tipo de turbomaquina: ventilador centrifugo multialabe tipo Sirocco.
- Caudal: `Q = 3 m3/s`.
- Presion requerida: `H = 90 mmH2O = 882.6 Pa`.
- Fluido: aire.
- Densidad asumida: `rho = 1.2 kg/m3`.
- Potencia util al aire: `P_aire = 2.65 kW`.
- Eficiencia estatica estimada por el modelo V1: `eta_s = 0.545`.
- Potencia al eje estimada: `4.86 kW`.
- Motor preliminar sugerido: `5.5 kW`.

## Diseno preliminar propuesto

| Parametro | Valor preliminar | Criterio |
|---|---:|---|
| Configuracion | Doble entrada | Reduce la velocidad en los ojos para `3 m3/s` |
| Diametro exterior del rodete, `D2` | `0.60 m` | Dimension conservada del tanteo inicial |
| Velocidad nominal, `n` | `1100 rpm` | Cierre de Euler compatible con motor de `5.5 kW` |
| Velocidad periferica, `U2` | `34.56 m/s` | `U2 = pi D2 n / 60` |
| Ancho del rodete, `b` | `0.23 m` | Relacion `b/D2 = 0.383` |
| Velocidad radial salida, `Cm2` | `7.19 m/s` | Incluye bloqueo por espesor |
| Diametro interior, `D1` | `0.51 m` | Relacion `D1/D2 = 0.85` |
| Numero de alabes | `48` | Rodete multialabe |
| Angulos de alabe | `beta1 = 18`, `beta2 = 125 grados` | Medidos desde la tangente |
| Area de descarga de voluta | `0.20 m2` | Velocidad de salida `15 m/s` |
| Holgura lengua-rodete | `48 mm` | `8 % de D2` |

## Calculos base

```text
Delta p = 90 x 9.80665 = 882.6 Pa
P_aire = Q Delta p = 3 x 882.6 = 2647.8 W
U2 = pi x 0.60 x 1100 / 60 = 34.56 m/s
Cm2 = 7.19 m/s, incluyendo factor de bloqueo 0.963
Cu2 = 37.51 m/s, con factor de deslizamiento 0.940
Delta p_Euler = rho U2 Cu2 = 1555.5 Pa
P_eje = Q Delta p_Euler / 0.96 = 4.86 kW
eta_estatica = 2.648 / 4.861 = 54.5 %
```

## Trabajo pendiente

- Construir la curva media exacta del alabe y el CAD 3D.
- Calcular eje a flexion, vida de rodamientos y velocidad critica.
- Validar deslizamiento, perdidas y recuperacion de presion mediante CFD.
- Obtener curvas de presion, potencia y eficiencia.
- Preparar planos de taller despues de la validacion.
- Construir y ensayar el modelo por semejanza.
