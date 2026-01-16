import sqlite3
import datetime
import logging
from typing import Optional

DB_PATH = "triage.db"
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela emails
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        category TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabela feedback
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        predicted TEXT,
        correct TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Banco de dados inicializado.")

def save_email(text: str, category: str, confidence: float):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emails (text, category, confidence) VALUES (?, ?, ?)", 
                       (text, category, confidence))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Erro ao salvar email: {e}")

def save_feedback(text: str, predicted: str, correct: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (text, predicted, correct) VALUES (?, ?, ?)", 
                       (text, predicted, correct))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Erro ao salvar feedback: {e}")

def count_feedback() -> int:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.error(f"Erro ao contar feedback: {e}")
        return 0
