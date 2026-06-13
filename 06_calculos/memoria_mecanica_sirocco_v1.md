# Memoria mecanica V1 - Ventilador Sirocco

## 1. Objetivo y supuestos

Este calculo complementa la memoria aerodinamica incorporando masa del rodete,
carga de correas, flexion del eje, velocidad critica y vida de rodamientos.
Hipotesis preliminares:

- Acero al carbono: `rho = 7850 kg/m3`, `E = 200 GPa`.
- Alabes: `48`, espesor `1.2 mm`, ancho total `230 mm`.
- Dos anillos de entrada: espesor `2 mm`.
- Disco central: espesor `3 mm`.
- Cubo: diametro exterior `80 mm`, longitud `80 mm`.
- Luz entre rodamientos: `500 mm`.
- Rodete centrado entre apoyos.
- Polea de ventilador: `200 mm`, a `75 mm` del rodamiento.
- Carga radial de correa: `2.5` veces la fuerza tangencial.
- Vida objetivo de rodamientos: `20 000 h`.

## 2. Masa estimada

| Componente | Masa |
|---|---:|
| 48 alabes | `5.70 kg` |
| Dos anillos de entrada | `2.46 kg` |
| Disco central | `6.54 kg` |
| Cubo | `2.55 kg` |
| Subtotal | `17.25 kg` |
| Rotor con 8 % para soldadura/refuerzos | `18.63 kg` |

La masa debe actualizarse desde el CAD 3D antes del plano final.

## 3. Correa, reacciones y flexion

Con `P_eje = 4.86 kW`, `n = 1100 rpm` y polea de `200 mm`:

```text
T = 42.20 N m
F_t = 2 T / D_polea = 422 N
F_correa = 2.5 F_t = 1055 N
```

El modelo de viga con rodete centrado y polea en voladizo entrega:

- Reaccion maxima en rodamiento: `1.30 kN`.
- Momento flector maximo: `79.0 N m`, junto al rodamiento de la polea.
- Fuerza centrifuga por alabe: `437 N`.
- Tension centrifuga de referencia `rho U2^2`: `9.4 MPa`.

La polea debe instalarse tan cerca como sea posible del rodamiento. Duplicar el
voladizo casi duplica el momento flector y puede obligar a usar un eje mayor.

## 4. Diametro del eje

Se usa un momento equivalente tipo ASME con factores de choque de `1.5` para
flexion y torsion y `tau_adm = 30 MPa`:

```text
M_eq = sqrt((1.5 M)^2 + (1.5 T)^2)
d = (16 M_eq/(pi tau_adm))^(1/3)
```

El diametro basico queda cerca de `28.4 mm`. Al aplicar un factor de `1.20` por
chavetero, concentracion de esfuerzos e incertidumbre, se obtiene cerca de
`34.1 mm`. Se selecciona:

**Eje preliminar V1 mecanico: `35 mm`.**

Este valor reemplaza la recomendacion anterior de `30 mm`, que solo consideraba
torsion.

## 5. Velocidad critica

Con eje macizo de `35 mm`, luz de `500 mm` y la masa del rotor concentrada en
el centro, la flecha estatica es `0.032 mm`. La primera velocidad critica
estimada es `5260 rpm`, unas `4.8` veces la velocidad de trabajo de `1100 rpm`.

La comprobacion final debe incluir masa distribuida del eje, polea, rigidez de
soportes y efectos giroscopicos.

## 6. Rodamientos

Para `20 000 h` a `1100 rpm`, la capacidad dinamica minima calculada es
`14.3 kN`. Se debe seleccionar un rodamiento o soporte de `35 mm` con:

- Capacidad dinamica `C >= 20 kN` como margen preliminar.
- Capacidad para desalineacion compatible con la carcasa soldada.
- Sellado adecuado para polvo ambiental.
- Engrase y temperatura compatibles con el servicio.

Un soporte tipo `UCP207` o equivalente puede ser candidato, pero debe
confirmarse con el catalogo real del fabricante.

## 7. Pendientes mecanicos

1. Confirmar material y proceso de soldadura.
2. Modelar el rotor 3D y obtener masa, centro de gravedad e inercia reales.
3. Calcular uniones alabe-anillo y alabe-disco central.
4. Dimensionar chaveta, cubo, pernos y poleas.
5. Verificar fatiga y velocidad critica con el eje completo.
6. Definir tolerancias y balanceo dinamico.

Los resultados reproducibles estan en
`08_software/calculo_mecanico_sirocco.py`.
