# Documentación de `10_interfaz_3d`

## Propósito

Proporcionar una interfaz gráfica para inspeccionar el ventilador sin instalar
un programa CAD. Todos los recursos están incluidos localmente y el visor puede
abrirse sin Internet.

## Inicio

### Windows

Desde la raíz del proyecto, ejecutar:

```text
ABRIR_MODELO_3D.bat
```

El BAT usa `%~dp0` para localizar la carpeta del proyecto y abre
`10_interfaz_3d/index.html` en el navegador predeterminado.

### Linux y macOS

Abrir `index.html` directamente con Chrome, Chromium, Edge, Firefox o Safari.

## Archivos

- `index.html`: estructura del panel y del área 3D.
- `styles.css`: diseño adaptable, colores y controles.
- `app.js`: escena, geometría, animación e interacción.
- `ABRIR_MODELO_3D.bat`: lanzador cuando se ejecuta desde esta carpeta.
- `vendor/`: Three.js y OrbitControls locales.

## Datos cargados

La interfaz lee `../07_modelos_3d/modelo_sirocco_v1_2.js`. Este archivo define
`window.SIROCCO_DATA` con dimensiones, punto de operación, perfil de álabe y
espiral de voluta.

## Construcción visual

- El álabe se crea como una forma extruida y se repite 48 veces.
- Anillos, disco, cubo, eje y polea se construyen con geometrías de Three.js.
- La voluta se crea como una forma extruida transparente.
- Flechas y partículas representan cualitativamente la dirección del aire.
- Soportes y rodamientos son elementos conceptuales para comprender el montaje.

## Controles

- Arrastrar: rotar la cámara.
- Rueda: acercar o alejar.
- Clic en un componente: mostrar su nombre.
- Vistas: isométrica, frontal, lateral y superior.
- Casillas: mostrar u ocultar rodete, voluta, flujo y rejilla.
- Velocidad visual: controlar la animación.
- Vista explotada: separar grupos para inspección.
- Transparencia: observar el rotor dentro de la carcasa.
- Guardar captura: descargar la vista en PNG.
- Pantalla completa: ampliar el área de trabajo.

## Portabilidad

Las rutas de scripts y estilos son relativas. Una prueba automática verifica
que no existan recursos `http://` o `https://`. Debe conservarse toda la
estructura del proyecto; si se separa el HTML de `vendor/` o de
`07_modelos_3d/`, dejará de cargar correctamente.

## Modos de captura del informe

Los parámetros `?report=rotor` y `?report=assembly` ocultan controles y ajustan
la cámara para generar figuras limpias del informe.

## Limitaciones

El visor no realiza CFD ni análisis estructural. Las flechas de aire son
ilustrativas, no líneas de corriente calculadas.
