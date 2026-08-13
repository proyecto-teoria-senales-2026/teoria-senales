@echo off
setlocal
cd /d "%~dp0"
title Verificador de reportes - Teoria de Senales

if not exist ".venv\Scripts\python.exe" (
    echo Preparando el verificador por primera vez. Este proceso puede tardar unos minutos.
    echo.

    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv .venv
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo No se encontro Python en este computador.
            echo Instala Python 3.12 o 3.13 y vuelve a ejecutar este archivo.
            echo.
            pause
            exit /b 2
        )
        python -m venv .venv
    )

    if not exist ".venv\Scripts\python.exe" (
        echo No fue posible preparar el verificador.
        echo.
        pause
        exit /b 2
    )

    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo No fue posible instalar los componentes del verificador.
        echo.
        pause
        exit /b 2
    )
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
