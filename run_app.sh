#!/bin/bash

# ANSI colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================================${NC}"
echo -e "${BLUE}     Email AI Triage - Inicializando Aplicação${NC}"
echo -e "${BLUE}========================================================${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERRO] Python3 não encontrado! Por favor instale o Python 3.8+.${NC}"
    exit 1
fi

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}[INFO] Criando ambiente virtual (.venv)...${NC}"
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install requirements
echo -e "${BLUE}[INFO] Verificando dependências...${NC}"
pip install -r requirements.txt > /dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERRO] Falha ao instalar dependências via requirements.txt.${NC}"
    exit 1
fi

# Run
echo ""
echo -e "${GREEN}[SUCESSO] Dependências ok. Iniciando servidor...${NC}"
echo "A aplicação estará disponível em: http://localhost:8000"
echo ""

python3 -m uvicorn app.main:app --reload
