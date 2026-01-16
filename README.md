# 📧 Email AI Triage MVP

MVP de triagem automática de emails utilizando Inteligência Artificial e Processamento de Linguagem Natural (NLP). O sistema classifica emails como **Produtivos** ou **Improdutivos** e sugere respostas automáticas.

## 🚀 Funcionalidades

- **Classificação Automática**: Identifica se um email é útil (Produtivo) ou spam/desnecessário (Improdutivo).
- **Extração de Texto**: Suporta texto colado e upload de arquivos (`.txt`, `.pdf`).
- **Sugestão de Resposta**: Gera rascunhos de resposta baseados na categoria do email.
- **Auto-Treinamento**: O sistema aprende automaticamente com novos dados no arquivo `data/train.csv` ao iniciar.
- **Feedback Loop**: Interface para o usuário corrigir a classificação, salvando dados para futuros treinamentos.
- **API REST**: Backend em FastAPI pronto para integração.

## 🛠️ Tecnologias

- **Backend**: Python 3.8+, FastAPI, Uvicorn.
- **IA/NLP**: scikit-learn (TF-IDF + Regressão Logística), spaCy, pypdf.
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
- **Banco de Dados**: SQLite (para histórico e feedback).

## 📦 Como Rodar

### 1. Pré-requisitos

Certifique-se de ter o Python instalado.

```bash
# Instalar dependências
pip install -r requirements.txt
```

#### Como obter a chave de API do Google Gemini (Opcional)
Para habilitar as sugestões de resposta inteligentes:
1. Acesse o [Google AI Studio](https://aistudio.google.com/).
2. Faça login com sua conta Google.
3. Clique em **"Get API key"** no canto inferior esquerdo.
4. Crie uma nova chave clicando em **"Create API key"** e siga as instruções, criando um novo projeto.
5. Copie o valor da chave gerada.

#### Configuração da Chave
Você pode configurar a chave de duas formas:

**Opção 1: Arquivo .env (Recomendado)**
Crie um arquivo chamado `.env` na raiz do projeto e adicione a seguinte linha:
```env
GEMINI_API_KEY=sua_chave_aqui
```

**Opção 2: Variável de Ambiente**
```bash
# Linux/Mac
export GEMINI_API_KEY="sua_chave_aqui"
# Windows (PowerShell)
$env:GEMINI_API_KEY="sua_chave_aqui"
```

### 2. Executar a Aplicação

```bash
uvicorn app.main:app --reload
```

Acesse no navegador: [http://localhost:8000](http://localhost:8000)

## 📚 Documentação da API

A documentação interativa (Swagger UI) está disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints Principais

- **`POST /api/process`**: Processa um email.
    - **Input**: `text` (string) OU `file` (upload).
    - **Output**: JSON com categoria, confiança (%) e sugestão de resposta.
- **`POST /api/feedback`**: Recebe correção do usuário.
    - **Input**: JSON com texto original, predição e correção.

## 📂 Estrutura do Projeto

```
/app
  /main.py       # Ponto de entrada da API
  /services      # Lógica de negócio (Classificação, Parser, Storage)
  /web           # Frontend (HTML/CSS/JS)
/data
  /train.csv     # Dataset para treinamento do modelo
/models          # Modelos serializados (.joblib)
/scripts         # Scripts utilitários (verificação, testes)
```

## 📝 Personalização

- **Treinamento**: Adicione novos exemplos em `data/train.csv` e reinicie a aplicação para re-treinar o modelo.
- **Respostas**: Edite `app/services/reply.py` para alterar os templates de resposta.
