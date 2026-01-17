@echo off
TITLE Email AI Triage
CLS

ECHO ========================================================
ECHO      Email AI Triage - Inicializando
ECHO ========================================================
ECHO.

REM 1. Checar Python
python --version
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERRO] Python nao encontrado.
    PAUSE
    EXIT /B
)

REM 2. venv
IF NOT EXIST ".venv" (
    ECHO [INFO] Criando venv...
    python -m venv .venv
)

REM 3. Dependencias
CALL .venv\Scripts\activate
ECHO [INFO] Verificando dependencias...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERRO] Falha ao instalar dependencias.
    PAUSE
    EXIT /B
)

REM 4. .env check
IF NOT EXIST ".env" (
    IF EXIST ".env.example" (
        ECHO.
        ECHO [AVISO] Arquivo .env nao encontrado!
        ECHO O sistema copiou .env.example para .env automaticamente.
        ECHO Edite o arquivo .env se quiser usar a IA Generativa.
        copy .env.example .env >nul
    )
)

CLS
ECHO ========================================================
ECHO                 SERVIDOR ONLINE
ECHO ========================================================
ECHO.
ECHO Acesso: http://localhost:8000
ECHO.
python -m uvicorn app.main:app --reload
PAUSE
