@echo off
setlocal
cd /d "%~dp0"
title Verificador de reportes - Teoria de Senales

if not exist ".venv\Scripts\python.exe" (
    echo Primero abre INICIAR_APLICACION.bat para preparar la herramienta.
    echo.
    pause
    exit /b 2
)

set "REPORT_PATH=%~1"
if not defined REPORT_PATH (
    echo.
    echo Arrastra el reporte PDF a esta ventana y presiona Enter.
    set /p "REPORT_PATH=PDF: "
)

if not defined REPORT_PATH (
    echo.
    echo No se recibio ningun PDF.
    pause
    exit /b 2
)

if not exist %REPORT_PATH% (
    echo.
    echo No se encontro el archivo indicado.
    echo.
    pause
    exit /b 2
)

echo.
echo Comprobando el reporte...
echo.
".venv\Scripts\python.exe" verificar_reporte.py %REPORT_PATH% --sessions "session_outputs"
set "VERIFY_EXIT=%ERRORLEVEL%"

echo.
if "%VERIFY_EXIT%"=="0" (
    echo Resultado: REPORTE VALIDO.
) else (
    echo Resultado: REPORTE ALTERADO O NO VERIFICABLE.
)
echo.
pause
exit /b %VERIFY_EXIT%
