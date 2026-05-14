@echo off
setlocal

echo ==============================================
echo Iniciando entorno Protocolo Titan
echo ==============================================

:: Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo [INFO] Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo [WARNING] No se encontro el entorno virtual en .venv
    echo Por favor, asegurese de crearlo con: python -m venv .venv
    pause
    exit /b 1
)

:: Set PYTHONPATH
set PYTHONPATH=src

:MENU
echo.
echo Seleccione una opcion:
echo 1. Ejecutar simulacion completa (main.py)
echo 2. Iniciar Dashboard Interactivo (Streamlit)
echo 3. Iniciar Notebook Docente (Jupyter)
echo 4. Instalar dependencias (requirements.txt)
echo 5. Salir
echo.

set /p option="Opcion (1-5): "

if "%option%"=="1" (
    echo.
    echo [INFO] Ejecutando main.py...
    python -m protocolo_titan.main
    pause
    goto MENU
)

if "%option%"=="2" (
    echo.
    echo [INFO] Iniciando Streamlit app...
    streamlit run src/protocolo_titan/streamlit_app.py
    pause
    goto MENU
)

if "%option%"=="3" (
    echo.
    echo [INFO] Iniciando Jupyter Notebook...
    jupyter notebook notebooks/protocolo_titan_replanteado.ipynb
    pause
    goto MENU
)

if "%option%"=="4" (
    echo.
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
    pause
    goto MENU
)

if "%option%"=="5" (
    echo Saliendo...
    exit /b 0
)

echo.
echo [ERROR] Opcion no valida.
goto MENU
