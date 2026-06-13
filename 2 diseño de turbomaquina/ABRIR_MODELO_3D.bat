@echo off
setlocal
set "HTML=%~dp010_interfaz_3d\index.html"
if not exist "%HTML%" (
  echo No se encontro 10_interfaz_3d\index.html
  echo No separe el BAT de las carpetas del proyecto.
  pause
  exit /b 1
)
start "Ventilador Sirocco 3D" "%HTML%"
exit /b 0
