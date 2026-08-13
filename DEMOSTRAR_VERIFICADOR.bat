@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Primero abre INICIAR_APLICACION.bat para preparar la herramienta.
    pause
    exit /b 2
)

set "EVIDENCIA=docs\evidencias\verificacion"
echo.
echo 1. Verificando el reporte original...
".venv\Scripts\python.exe" verificar_reporte.py "%EVIDENCIA%\reporte_original_valido_C-3-3.pdf" --sessions "%EVIDENCIA%"
echo.
echo 2. Verificando la copia alterada...
".venv\Scripts\python.exe" verificar_reporte.py "%EVIDENCIA%\reporte_copia_alterada_C-3-3.pdf" --sessions "%EVIDENCIA%"
echo.
echo La demostracion debe mostrar VALIDO para el original y ALTERADO O NO VALIDO para la copia.
pause
