@echo off
setlocal
set "HTML=%~dp0index.html"
if not exist "%HTML%" (
  echo No se encontro la interfaz 3D.
  echo Mantenga este archivo dentro de la carpeta 10_interfaz_3d.
  pause
  exit /b 1
)
start "Ventilador Sirocco 3D" "%HTML%"
exit /b 0
