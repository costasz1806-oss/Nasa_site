@echo off
cd /d "%~dp0"
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt -q
echo.
echo Iniciando servidor em http://127.0.0.1:5000
echo Pressione Ctrl+C para parar
echo.
python app.py
