import os
import logging
from google import genai

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = "gemini-3-flash-preview"

def generate_reply(category: str, text: str = "") -> tuple[str, str]:
    """
    Gera uma sugestão de resposta usando Google Gemini.
    Fallback para templates estáticos em caso de erro.
    Retorna: (resposta, fonte)
    """

    if GEMINI_API_KEY:
        try:
            logger.info(f"Tentando gerar resposta com Gemini...")
            client = genai.Client(api_key=GEMINI_API_KEY)

            # Carrega o prompt do arquivo
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prompt_path = os.path.join(base_dir, "prompts", "reply_prompt.txt")
            
            with open(prompt_path, "r", encoding="utf-8") as f:
                template = f.read()

            prompt = template.format(category=category, text=text)

            response = client.models.generate_content(
                model=LLM_MODEL, 
                contents=prompt
            )
            
            if not response.text:
                 logger.error("Gemini respondeu mas o texto está vazio.")
                 raise ValueError("Sem resposta da IA")

            # Formata o nome do modelo para exibição: GEMINI 2 0 FLASH EXP
            model_display = LLM_MODEL.replace(".", " ").replace("-", " ").upper()
            return response.text.strip(), model_display

        except Exception as e:
            logger.error(f"ERRO CRÍTICO GEMINI: {str(e)}")
            # Se for um erro de modelo não encontrado, o log vai ajudar a debugar
    else:
        logger.warning("GEMINI_API_KEY não encontrada.")

    fallback_source = "Erro de Sistema"

    if category == "Improdutivo":
        return (
            "Erro ao gerar resposta:\n\n"
            "Cadastre uma chave de API do Gemini válida, para que possamos ajudar.\n\n"
            "Atenciosamente.\n",
            "Equipe InboxAI",
            fallback_source
        )

    if category == "Produtivo":
        return (
            "Erro ao gerar resposta:\n\n"
            "Cadastre uma chave de API do Gemini válida, para que possamos ajudar.\n\n"
            "Atenciosamente.\n",
            "Equipe InboxAI",
            fallback_source
        )

    return ("Olá, recebemos sua mensagem e entraremos em contato.", fallback_source)