#!/bin/bash

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================================${NC}"
echo -e "${BLUE}     Email AI Triage - Inicializando${NC}"
echo -e "${BLUE}========================================================${NC}"
echo ""

# 1. Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERRO] Python3 não encontrado!${NC}"
    exit 1
fi

# 2. venv
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}[INFO] Criando venv...${NC}"
    python3 -m venv .venv
fi

source .venv/bin/activate

# 3. Deps
echo -e "${BLUE}[INFO] Dependências...${NC}"
pip install -r requirements.txt > /dev/null

# 4. .env check
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "${YELLOW}[AVISO] .env criado a partir do exemplo.${NC}"
        cp .env.example .env
        echo "Edite o arquivo .env para adicionar sua GEMINI_API_KEY se desejar."
        echo "Pressione ENTER para continuar..."
        read
    fi
fi

# 5. Run
clear
echo -e "${GREEN}SERVIDOR ONLINE: http://localhost:8000${NC}"
echo ""

python3 -m uvicorn app.main:app --reload
