import re

def clean_text(text: str) -> str:
    """
    Realiza limpeza básica no texto de entrada:
    - Normaliza espaços em branco
    - Remove caracteres estranhos (opcional)
    """
    if not text:
        return ""
    
    # Substitui múltiplos espaços/quebras de linha por um único espaço
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
