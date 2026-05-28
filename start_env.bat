@echo off
echo ===========================================
echo  Configurando Entorno Virtual (Netec Transcriber)
echo ===========================================

IF NOT EXIST "venv" (
    echo [*] Creando entorno virtual...
    python -m venv venv
)

echo [*] Activando entorno e instalando dependencias...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo [OK] Entorno virtual listo. 
echo Para correr el script ejecuta:
echo python transcriber_json.py
cmd /k
