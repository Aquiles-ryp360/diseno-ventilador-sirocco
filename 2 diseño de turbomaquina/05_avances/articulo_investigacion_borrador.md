# Diseno y analisis preliminar de un ventilador centrifugo tipo Sirocco para 3 m3/s y 90 mmH2O

## Autores

Dilmar Humberto Siguayro Coila; Aquiles Taylor Ramos Yapo; Renzo Gabriel Mamani Galindo; Martin Calla Quispe; Abel Yovani Rivera Quispe.

## Resumen

El presente trabajo desarrolla el diseno preliminar de un ventilador centrifugo tipo Sirocco para un caudal de `3 m3/s` y una presion de `90 mmH2O`. La metodologia combina teoria unidimensional de turbomaquinas, predimensionamiento de rodete, estimacion de voluta y revision de literatura cientifica reciente sobre ventiladores centrifugos de alabes curvados hacia adelante. La presion requerida equivale a `882.6 Pa` y la potencia util al aire es `2.65 kW`. El cierre de los triangulos de velocidad conduce a un rodete de doble entrada con `D2 = 0.60 m`, `D1 = 0.51 m`, ancho `b = 0.23 m`, 48 alabes y velocidad cercana a `1100 rpm`. La potencia al eje estimada es `4.86 kW`, por lo que se propone un motor comercial de `5.5 kW`. La revision bibliografica indica que la region de la lengua de voluta, la curvatura de los alabes y la recuperacion de presion son variables criticas para eficiencia, ruido y estabilidad.

## Palabras clave

Ventilador Sirocco; ventilador centrifugo; rodete; voluta; turbomaquinas; CFD.

## 1. Introduccion

Los ventiladores centrifugos tipo Sirocco son turbomaquinas de flujo radial usadas para mover aire en sistemas de ventilacion y ductos. Su configuracion multialabe con alabes curvados hacia adelante permite obtener caudales elevados con dimensiones relativamente compactas. En comparacion con ventiladores axiales, un ventilador centrifugo puede vencer mayores resistencias del sistema, aunque su eficiencia depende fuertemente de la geometria del rodete, la voluta y la interaccion con la lengua.

El problema asignado al Grupo 2 consiste en disenar un ventilador tipo Sirocco para `Q = 3 m3/s` y `H = 90 mmH2O`. Este punto de operacion corresponde a una presion de `882.6 Pa`, lo que situa el equipo en una aplicacion de baja a media presion.

## 2. Objetivos

## Objetivo general

Disenar preliminarmente un ventilador centrifugo tipo Sirocco que entregue `3 m3/s` de aire con una presion de `90 mmH2O`.

## Objetivos especificos

- Calcular la potencia util y potencia al eje.
- Predimensionar el rodete.
- Definir una geometria preliminar de voluta.
- Identificar perdidas principales.
- Revisar literatura cientifica reciente aplicable.
- Preparar una base para software de calculo y modelo por semejanza.

## 3. Metodologia

La metodologia propuesta es:

1. Convertir la presion de mmH2O a Pa.
2. Calcular potencia util al aire.
3. Asumir condiciones estandar de aire y eficiencia preliminar.
4. Seleccionar velocidad nominal y diametro exterior.
5. Calcular velocidad periferica y velocidad radial.
6. Estimar coeficiente de presion.
7. Definir numero de alabes y angulos preliminares.
8. Dimensionar area de descarga de la voluta.
9. Listar perdidas para el balance final.
10. Comparar criterios con literatura reciente.

## 4. Resultados preliminares

```text
Delta p = 90 x 9.80665 = 882.6 Pa
P_aire = 3 x 882.6 = 2647.8 W
U2 = pi x 0.60 x 1100 / 60 = 34.56 m/s
Delta p_Euler = 1555.5 Pa
P_eje = 3 x 1555.5 / 0.96 = 4861 W
```

Se propone:

- Motor preliminar: `5.5 kW`.
- Rodete de doble entrada: `D2 = 0.60 m`, `D1 = 0.51 m`.
- Ancho: `b = 0.23 m`.
- Velocidad nominal: `1100 rpm`.
- Numero de alabes: `48`.
- Angulos: `beta1 = 18 grados`, `beta2 = 125 grados`.
- Velocidad periferica: `34.56 m/s`.
- Velocidad radial de salida: `7.19 m/s`.
- Coeficiente de presion estatica: `0.616`.
- Descarga de voluta: `0.28 x 0.714 m`.

## 5. Discusion

La literatura reciente coincide en que la voluta no debe tratarse como un elemento secundario. Wang et al. muestran que las estructuras coherentes cerca de la lengua generan fluctuaciones de presion importantes. Wang, Ju y Zhang proponen optimizar la lengua de voluta mediante geometria bionica inclinada. Rosa y Toledo muestran que el diseno unidimensional puede ser una base valida si se complementa con CFD.

Para el proyecto academico, esto implica que el calculo debe incluir no solo el rodete, sino tambien la recuperacion de presion en la voluta, la separacion lengua-rodete y la estimacion de perdidas.

## 6. Conclusiones preliminares

- El tema asignado al Grupo 2 es tecnicamente viable con un ventilador centrifugo tipo Sirocco.
- La potencia util al aire es `2.65 kW`; la potencia al eje probable exige un motor de aproximadamente `5.5 kW`.
- La geometria V1 es `D2 = 0.60 m`, `D1 = 0.51 m`, `b = 0.23 m` y `n = 1100 rpm`.
- El calculo a `1500 rpm` exigiria aproximadamente `8.72 kW` al eje, por lo que esa velocidad se descarta.
- La voluta y la lengua son componentes criticos para rendimiento y ruido.
- Falta confirmar el formato exacto del articulo desde el documento de investigacion compuesto por imagenes.

## Referencias preliminares

- Wang, S.; Xu, H.; Qi, Z.; Pan, C. (2023). Coherent Flow Structures Near Tongue Region in a Centrifugal Fan With Forward-Curved Blades. `https://doi.org/10.1115/1.4056279`
- Wang, K.; Ju, Y.; Zhang, C. (2021). Aerodynamic optimization of forward-curved blade centrifugal fan characterized by inclining bionic volute tongue. `https://doi.org/10.1007/s00158-020-02801-2`
- Espinel, E.; Valencia, G.; Duarte Forero, J. (2020). CFD Methodology for the Optimization of a Centrifugal Fan with Backward Inclined Blades Using OpenFOAM. `https://doi.org/10.15866/irecon.v8i3.18641`
- Rosa, H. M. P.; Toledo, G. P. (2021). CFD tool application in predicting the behavior of a centrifugal fan designed by one-dimensional theory. `https://doi.org/10.33448/rsd-v10i12.19653`
- Fang, J.; Yan, P.; Qin, J.; Chen, H. (2023). Research on Centrifugal Blower Design and Optimization Method Based on Mean Camber Line Optimization and CFD. `https://doi.org/10.1088/1742-6596/2419/1/012062`
