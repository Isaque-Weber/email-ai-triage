# 📧 InboxAI - Desafio Técnico

> **Acesse a Demonstração Online:** [https://desafio.isaqueweber.com.br](https://desafio.isaqueweber.com.br)

Sistema inteligente para triagem automática de emails e geração de respostas, desenvolvido com foco em simplicidade, performance e experiência do usuário. O projeto utiliza Machine Learning (NLP) para classificar mensagens e Inteligência Artificial Generativa (Google Gemini) para sugerir respostas contextuais.

---

## 📋 Sobre o Projeto

O **InboxAI** resolve o problema de caixas de entrada superlotadas em ambientes corporativos. Ele atua como uma primeira camada de filtro inteligente:
1. **Analisa** o conteúdo do email (texto ou anexo).
2. **Classifica** a mensagem como "Produtiva" (importante) ou "Improdutiva" (ruído/spam).
3. **Sugere** uma resposta pronta para envio, economizando tempo do operador.

A aplicação foi desenhada para ser intuitiva (Zero Learning Curve) e fácil de implantar.

---

## ✨ Funcionalidades Principais

*   **Classificação via ML**: Utiliza um pipeline de processamento de linguagem natural (TF-IDF + Regressão Logística) para categorizar emails com alta precisão e nível de confiança.
*   **Respostas Inteligentes (Híbrido)**:
    *   **IA Generativa**: Integração com **Google Gemini 3.0 Flash Preview** para criar respostas personalizadas e humanas.
    *   **Fallback Seguro**: Sistema de templates automáticos caso a API de IA esteja indisponível.
*   **Extração de Arquivos**: Suporte nativo para leitura de arquivos `.txt` e `.pdf` via Drag & Drop.
*   **Feedback Loop**: O sistema aprende com o usuário. Correções manuais são salvas para re-treinar e melhorar o modelo automaticamente.
*   **Interface Premium**: Design responsivo com Dark Mode, Glassmorphism e feedbacks visuais em tempo real.

---

## 🏗️ Arquitetura e Tecnologias

A aplicação segue uma arquitetura modular, facilitando manutenção e escalabilidade.

### Stack Tecnológico
*   **Frontend**: HTML5, CSS3 Moderno, JavaScript Vanilla (Sem frameworks pesados para máxima performance).
*   **Backend**: Python 3.10+, FastAPI (Alta performance e validação automática).
*   **Machine Learning**: `scikit-learn` para classificação supervisionada.
*   **AI Generativa**: Google GenAI SDK (Gemini).
*   **Banco de Dados**: SQLite (Leve e embutido para persistência de logs e feedback).
*   **Infraestrutura**: Docker Ready.

### Fluxo de Dados
1.  **Input**: Usuário envia texto ou arquivo via Frontend.
2.  **Parser**: Backend extrai e limpa o texto (`pypdf` + regex).
3.  **Core ML**: O modelo vetoriza o texto e prevê a categoria + % de confiança.
4.  **Reply Engine**:
    *   Consulta API do Gemini com prompt contextual.
    *   Se falhar, busca template local.
5.  **Output**: Frontend exibe classificação e rascunho de resposta.
6.  **Feedback**: Usuário avalia, e dado retorna ao DB para ciclo de melhoria (`Active Learning`).

---

## 🚀 Guia de Instalação e Execução

O projeto foi projetado para rodar em qualquer ambiente com configuração mínima.

### ⚡ Opção 1: Quick Start (Scripts Automatizados)
Use esta opção para testar localmente sem configurar nada manualmente.

*   **Windows**: Dê um duplo clique no arquivo `run_app.bat`.
*   **Linux/Mac**: Execute `./run_app.sh` no terminal.

O script criará o ambiente virtual e iniciará o servidor.
> **Opcional:** O script criará automaticamente um arquivo `.env` baseado no exemplo. Edite-o com sua chave API para ativar a IA Generativa.

### 🛠️ Opção 2: Instalação Manual
Se preferir ter controle total sobre o ambiente:

**1. Clone o repositório**
```bash
git clone https://github.com/Isaque-Weber/email-ai-triage.git
cd email-ai-triage
```

**2. Configure o ambiente Python**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente (Opcional)**
Para ativar a IA Generativa (Gemini), crie um arquivo `.env` na raiz:
```env
GEMINI_API_KEY=sua_chave_aqui
```
*Sem a chave, o sistema funcionará perfeitamente usando o modo de templates estáticos.*

**5. Execute a aplicação**
```bash
uvicorn app.main:app --reload
```
Acesse em: `http://localhost:8000`

### 🐳 Opção 3: Docker
Para rodar em container isolado:

```bash
# Construir a imagem
docker build -t email-triage .

# Rodar o container (Porta 80 mapeada para 8000 local)
docker run -p 8000:80 email-triage
```

---

## 📚 Documentação da API

A API é documentada automaticamente (OpenAPI/Swagger). Após iniciar a aplicação, acesse:
*   **Swagger UI**: `http://localhost:8000/docs`
*   **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principais
*   `POST /api/process`: Ponto central de inteligência. Recebe texto/arquivo, retorna JSON com classificação e resposta.
*   `POST /api/feedback`: Recebe validação humana para retroalimentar o sistema.

---

## 🧪 Estrutura de Pastas

```
/app
  /main.py       # Entry point e rotas da API
  /services      # Lógica de negócio (Classificação, Texto, Respostas)
  /web           # Frontend estático (SPA)
/data
  /train.csv     # Dataset base para treinamento inicial
/models          # Modelos ML serializados (.joblib)
Dockerfile       # Configuração de container
requirements.txt # Dependências do projeto
```

---

Desenvolvido por **Isaque Weber**.
*Dúvidas? Entre em contato.*

## 📧 Contato

- **Email:** isaque.weber5@gmail.com
- **LinkedIn:** [linkedin.com/in/isaque-weber](https://linkedin.com/in/isaque-weber)

<a href="https://wa.me/5521967398707">
    <img alt="Contato" title="Fale comigo no WhatsApp"
         src="https://custom-icon-badges.demolab.com/badge/-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white"/>
</a>
