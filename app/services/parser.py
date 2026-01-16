import logging
import io
from pypdf import PdfReader

logger = logging.getLogger(__name__)

async def extract_text(file_content: bytes, filename: str) -> str:
    """
    Extrai texto de bytes de arquivos text/plain ou application/pdf.
    """
    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            logger.error(f"Erro ao ler PDF: {e}")
            raise ValueError("Falha na leitura do arquivo PDF.")
    else:
        # Assume texto plano por padrão
        try:
            return file_content.decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Erro ao decodificar texto: {e}")
            raise ValueError("Falha na decodificação do arquivo de texto.")
