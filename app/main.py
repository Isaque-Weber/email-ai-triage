import logging
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

from app.services.parser import extract_text
from app.services.preprocess import clean_text
from app.services.classify import classifier
from app.services.reply import generate_reply
from app.services.storage import init_db, save_email, save_feedback

# Configuração de Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmailTriage")

app = FastAPI(title="Email AI Triage MVP")

# Inicializa DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Monta arquivos estáticos (Frontend)
# Assumindo que app/web está no mesmo nível que app/main.py -> c:\dev\email-ai-triage\app\web
# Mas main.py roda de c:\dev\email-ai-triage geralmente. Vamos ajustar o path relative.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

class ProcessResponse(BaseModel):
    category: str
    confidence: float
    suggested_reply: str
    reply_source: str

class FeedbackRequest(BaseModel):
    text: str
    predicted: str
    correct: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve o index.html
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Frontend não encontrado."

@app.post("/api/process", response_model=ProcessResponse)
async def process_email(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        content = ""
        
        # 1. Extração
        if file:
            file_bytes = await file.read()
            content = await extract_text(file_bytes, file.filename)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Nenhum texto ou arquivo fornecido.")

        if not content.strip():
             raise HTTPException(status_code=400, detail="Conteúdo vazio.")

        # 2. Pré-processamento
        clean_content = clean_text(content)

        # 3. Classificação
        category, confidence = classifier.predict(clean_content)

        # 4. Geração de Resposta
        reply, source = generate_reply(category, clean_content) # Deconstruct tuple

        # 5. Persistência
        save_email(clean_content, category, confidence)

        return {
            "category": category,
            "confidence": round(confidence * 100, 2), # Retorna porcentagem
            "suggested_reply": reply,
            "reply_source": source
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")

from fastapi import BackgroundTasks
from app.services.storage import count_feedback
from app.services.train import retrain

@app.post("/api/feedback")
async def receive_feedback(feedback: FeedbackRequest, background_tasks: BackgroundTasks):
    save_feedback(feedback.text, feedback.predicted, feedback.correct)
    
    # Checa contagem para retreino
    count = count_feedback()
    message = "Feedback salvo."
    
    if count > 0 and count % 10 == 0:
        background_tasks.add_task(retrain)
        logger.info(f"Gatilho de retreino acionado no feedback #{count}")
        
    return {"status": "success", "message": "Feedback salvo."}
