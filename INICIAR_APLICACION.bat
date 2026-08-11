@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo No se encontro Python en este computador.
    echo Instala Python 3.12 o 3.13 y marca la opcion "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Primera apertura: preparando la herramienta...
    python -m venv .venv
    if errorlevel 1 goto :error

    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -m pip check
if errorlevel 1 (
    echo.
    echo Actualizando los componentes necesarios...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :error
)

echo.
echo Abriendo la plataforma de Teoria de Senales...
echo No cierres esta ventana mientras uses la herramienta.
".venv\Scripts\python.exe" -m streamlit run app.py
exit /b 0

:error
echo.
echo No fue posible preparar la herramienta.
echo Toma una captura de este mensaje y compartela con el equipo.
echo.
pause
exit /b 1
