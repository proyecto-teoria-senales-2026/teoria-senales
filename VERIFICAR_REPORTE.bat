@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo No se encontro Python en este computador.
    pause
    exit /b 2
)

if "%~1"=="" (
    echo Arrastra el reporte PDF sobre este archivo para verificarlo.
    pause
    exit /b 2
)

if not exist ".venv\Scripts\python.exe" (
    echo Primero abre INICIAR_APLICACION.bat para preparar la herramienta.
    pause
    exit /b 2
)

".venv\Scripts\python.exe" verificar_reporte.py "%~1" --sessions "session_outputs"
echo.
if errorlevel 1 (
    echo Resultado: el reporte esta alterado o no puede verificarse.
) else (
    echo Resultado: el reporte coincide con la sesion original.
)
pause
