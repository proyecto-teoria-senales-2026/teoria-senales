@echo off
setlocal
cd /d "%~dp0"
call "INICIAR_APLICACION.bat"
exit /b %errorlevel%
