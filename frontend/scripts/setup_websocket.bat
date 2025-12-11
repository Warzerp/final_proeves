@echo off
REM SmartHealth WebSocket Setup Script
REM Este script configura el entorno para WebSocket en Windows

echo.
echo ====================================
echo SmartHealth WebSocket Setup
echo ====================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo [OK] Python instalado
echo.

REM Crear virtual environment si no existe
if not exist "venv" (
    echo Creando virtual environment...
    python -m venv venv
    echo [OK] Virtual environment creado
) else (
    echo [OK] Virtual environment ya existe
)
echo.

REM Activar virtual environment
echo Activando virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activado
echo.

REM Instalar dependencias
echo Instalando dependencias...
cd ..\..\backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
cd ..\frontend\scripts
echo [OK] Dependencias instaladas
echo.

REM Mostrar información
echo.
echo ====================================
echo SmartHealth WebSocket Configurado
echo ====================================
echo.
echo Para iniciar el servidor:
echo   cd ..\..\backend
echo   python start_server.py
echo.
echo Para ejecutar los tests:
echo   cd ..\..\backend
echo   python test_db_connection.py
echo.
echo Para salir del virtual environment:
echo   deactivate
echo.

pause
