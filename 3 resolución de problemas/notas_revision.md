# Notas de revisión

## Problemas numéricos

- Primera parte, problema 1: altura de bomba y potencia paramétricas.
- Primera parte, problema 2: número específico de diseño de doble succión.
- Segunda parte, problema 5: turbina Francis lenta.
- Segunda parte, problema 6: turbina Pelton de un chorro.
- Segunda parte, problema 7: ventilador centrífugo con resbalamiento.

## Problemas teóricos o gráficos

- Primera parte, problemas 3, 4 y 6: estator, rotor Francis y trayectoria absoluta.
- Primera parte, problemas 5 y 7: demostraciones de semejanza y potencia eólica.
- Segunda parte, problemas 1 a 4: reacción, giro eficiente, altura teórica y flujo secundario.

## Supuestos usados

- Flujo estacionario e incompresible en los problemas hidráulicos.
- Agua con `rho = 1000 kg/m^3` y `g = 9.81 m/s^2` cuando corresponde.
- Descarga sin remolino en los problemas Francis que así lo requieren.
- Entrada radial sin prerrotación en los ventiladores numéricos.
- Ángulos medidos desde la tangente cuando se declara expresamente.
- Potencia hidráulica ideal en el cálculo de caudal de la Francis lenta, al no darse eficiencia.

## Datos faltantes

- No se proporcionaron las figuras 1 a 5.
- Primera parte, problema 1: faltan desnivel geométrico, factor de Darcy, pérdidas locales y eficiencia.
- En problemas gráficos no puede fijarse una letra o sentido horario/antihorario absoluto sin la figura.
- La referencia de `alpha_1 = 90 grados` del rotor Francis es ambigua sin el dibujo original.

## Resultados principales

- Primera 1: `H_B = (z_d-z_s) + 131.99 f + 0.2115 K_tot` m; `P_motor = 0.981 H_B/eta` kW.
- Primera 2: `Nq_diseno = 9.97`, aproximadamente `10.0`.
- Segunda 1: `R = 0.5`.
- Segunda 3: `beta_2 > 90 grados` produce mayor altura teórica ideal.
- Segunda 5: `D_e = 0.294 m`, `D_i = 0.196 m`, `beta_2 = 26.0 grados`, `psi = 1` o `Psi = 2`, `Q = 0.0812 m^3/s`.
- Segunda 6: `d = 0.1155 m`, `D = 1.617 m`, `n = 425 rpm`.
- Segunda 7, evaluación trigonométrica directa: `sigma = 0.858`, desviación `3.74 grados`, `R = 0.746`.
- Segunda 7, usando el valor intermedio de la pauta: `sigma = 0.864`, desviación `3.6 grados`, `R = 0.744`.
