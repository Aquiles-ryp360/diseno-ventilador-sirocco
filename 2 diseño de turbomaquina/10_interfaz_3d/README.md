# Interfaz 3D portable

## Windows

Ejecutar `ABRIR_MODELO_3D.bat` desde la raiz del proyecto. No necesita Python,
servidor ni internet: abre `index.html` con el navegador predeterminado.

## Linux y macOS

Abrir `10_interfaz_3d/index.html` directamente en Chrome, Chromium, Edge,
Firefox o Safari. El archivo `.bat` es exclusivo de Windows.

## Controles

- Arrastrar con el mouse: rotar.
- Rueda del mouse: acercar o alejar.
- Botones de vista: isometrica, frontal, lateral y superior.
- Vista explotada: separa rodete y voluta.
- Transparencia: permite observar los alabes dentro de la carcasa.
- Guardar captura: descarga la vista actual como PNG.

Los modelos OBJ exportables estan en `07_modelos_3d/`. La interfaz utiliza
Three.js `0.128.0`, incluido localmente bajo licencia MIT.
