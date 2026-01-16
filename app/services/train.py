import sqlite3
import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import os
import shutil
import datetime
import logging
from app.services.classify import PORTUGUESE_STOPWORDS, classifier

# Configurar logger
logger = logging.getLogger(__name__)

# Caminhos absolutos para garantir funcionamento independente de onde é chamado
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "triage.db")
DATASET_PATH = os.path.join(BASE_DIR, "data", "train.csv")
BACKUP_DIR = os.path.join(BASE_DIR, "data", "backups")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def retrain():
    logger.info("🚀 Iniciando processo de retreino...")
    try:
        # 1. Carregar dataset original
        if os.path.exists(DATASET_PATH):
            df_original = pd.read_csv(DATASET_PATH)
        else:
            df_original = pd.DataFrame(columns=["text", "label"])

        # 2. Carregar novos feedbacks do Banco de Dados
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT text, correct as label FROM feedback"
        df_feedback = pd.read_sql_query(query, conn)
        conn.close()

        if df_feedback.empty:
            logger.info("ℹ️ Nenhum feedback encontrado. Nada para treinar.")
            return

        logger.info(f"📢 Total de feedbacks recuperados: {len(df_feedback)}")

        # 3. Normalizar
        df_feedback['label'] = df_feedback['label'].str.lower()
        
        # 4. Combinar
        df_combined = pd.concat([df_original, df_feedback])
        
        # Remove duplicatas (mantendo versão mais recente do feedback se houver conflito)
        df_combined = df_combined.drop_duplicates(subset=['text'], keep='last')

        # 5. Backup
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(DATASET_PATH, os.path.join(BACKUP_DIR, f"train_backup_{timestamp}.csv"))

        # 6. Salvar novo dataset full
        df_combined.to_csv(DATASET_PATH, index=False)
        logger.info("📝 Dataset atualizado salvo.")

        # 7. Treinamento
        logger.info("🏋️‍♂️ Treinando modelo...")
        training_data = df_combined.copy()
        
        # Cria o pipeline de Machine Learning (Idêntico ao classify.py)
        classification_pipeline = make_pipeline(
            TfidfVectorizer(
                min_df=1, 
                stop_words=PORTUGUESE_STOPWORDS, 
                ngram_range=(1, 2) 
            ),
            LogisticRegression(C=10.0, solver='liblinear') 
        )

        classification_pipeline.fit(training_data["text"], training_data["label"])

        # 8. Salvar Modelo Unificado
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)
            
        model_path = os.path.join(MODELS_DIR, "clf_pipeline.joblib")
        dump(classification_pipeline, model_path)
        
        logger.info(f"✅ Modelo retreinado e salvo em {model_path}")
        
        # Recarregar o classificador em memória
        classifier.load_model()
        logger.info("🔄 Classificador em memória atualizado.")

    except Exception as e:
        logger.error(f"❌ Erro crítico no retreino: {e}")
        raise e

if __name__ == "__main__":
    retrain()
