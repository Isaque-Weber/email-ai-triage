@echo off
TITLE Email AI Triage - Iniciando...
CLS

ECHO ========================================================
ECHO      Email AI Triage - Inicializando Aplicacao
ECHO ========================================================
ECHO.

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERRO] Python nao encontrado! Por favor instale o Python 3.8+ e adicione ao PATH.
    PAUSE
    EXIT /B
)

REM Check if venv exists, if not create one
IF NOT EXIST ".venv" (
    ECHO [INFO] Criando ambiente virtual (.venv)...
    python -m venv .venv
)

REM Activate venv
CALL .venv\Scripts\activate

REM Install dependencies
ECHO [INFO] Verificando dependencias...
pip install -r requirements.txt >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERRO] Falha ao instalar dependencias via requirements.txt.
    PAUSE
    EXIT /B
)

REM Run the app
ECHO.
ECHO [SUCESSO] Dependencias ok. Iniciando servidor...
ECHO.
ECHO A aplicacao estara disponivel em: http://localhost:8000
ECHO.
python -m uvicorn app.main:app --reload

PAUSE
