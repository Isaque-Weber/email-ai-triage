import os
import joblib
import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

logger = logging.getLogger(__name__)

SERIALIZED_MODEL_DIRECTORY = "models"
SERIALIZED_MODEL_FILE_PATH = os.path.join(SERIALIZED_MODEL_DIRECTORY, "clf_pipeline.joblib")

# Lista de stopwords em português para remover ruído
PORTUGUESE_STOPWORDS = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "no", 
    "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele", "das", "à", "seu", "sua", 
    "ou", "quando", "muito", "nos", "já", "eu", "também", "só", "pelo", "pela", "até", "isso", 
    "ela", "entre", "depois", "sem", "mesmo", "aos", "seus", "quem", "nas", "me", "esse", "eles", 
    "você", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", 
    "qual", "nós", "lhe", "deles", "essas", "esses", "pelas", "este", "dele", "tu", "te", "vocês", 
    "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", 
    "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", 
    "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", 
    "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", 
    "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", 
    "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", 
    "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", 
    "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram", 
    "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", 
    "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos", "seriam", 
    "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", 
    "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", 
    "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos", "teriam"
]

class EmailClassifier:
    def __init__(self):
        self.classification_pipeline = None
        self._initialize_model()

    def _initialize_model(self):
        """Tenta carregar um modelo existente ou treina um novo."""
        if os.path.exists(SERIALIZED_MODEL_FILE_PATH):
            try:
                self.classification_pipeline = joblib.load(SERIALIZED_MODEL_FILE_PATH)
                logger.info(f"Modelo carregado do disco: {SERIALIZED_MODEL_FILE_PATH}")
                return
            except Exception as e:
                logger.error(f"Falha ao carregar modelo existente: {e}")
        
        logger.info("Iniciando treinamento de novo modelo...")
        self._train_new_model()

    def _train_new_model(self):
        # Caminho absoluto para garantir que o arquivo seja encontrado independente de onde o script roda
        base_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dataset_file_path = os.path.join(base_directory, "data", "train.csv")
        
        training_data = None

        if os.path.exists(dataset_file_path):
            try:
                training_data = pd.read_csv(dataset_file_path)
                logger.info(f"DATASET ENCONTRADO: Usando {len(training_data)} exemplos de '{dataset_file_path}'")
            except Exception as e:
                logger.error(f"Erro ao ler arquivo CSV: {e}")

        # Fallback se algo der errado com o CSV
        if training_data is None or training_data.empty:
            logger.warning("ALERTA: Usando dados HARDCODED de emergência (CSV não encontrado ou vazio).")
            training_data = self._get_fallback_data()
        
        # Cria o pipeline de Machine Learning
        # 1. TfidfVectorizer: Transforma texto em números
        #    - stop_words: Ignora palavras comuns (o, a, de, para...)
        #    - ngram_range=(1, 2): Aprende palavras sozinhas ("nota") e pares ("nota fiscal")
        # 2. LogisticRegression: Classificador estatístico
        #    - C=10.0: Menor regularização -> Ajusta mais 'forte' aos dados (aumenta confiança)
        self.classification_pipeline = make_pipeline(
            TfidfVectorizer(
                min_df=1, 
                stop_words=PORTUGUESE_STOPWORDS, 
                ngram_range=(1, 2) 
            ),
            LogisticRegression(C=10.0, solver='liblinear') 
        )
        
        try:
            self.classification_pipeline.fit(training_data["text"], training_data["label"])
            
            os.makedirs(SERIALIZED_MODEL_DIRECTORY, exist_ok=True)
            joblib.dump(self.classification_pipeline, SERIALIZED_MODEL_FILE_PATH)
            logger.info("Novo modelo treinado e salvo com sucesso.")
        except Exception as e:
            logger.error(f"Erro fatal no treinamento do modelo: {e}")

    def _get_fallback_data(self):
        """Dados de emergência apenas para o sistema não quebrar se não houver CSV."""
        fallback_examples = [
            ("Reunião de orçamento amanhã", "Produtivo"),
            ("Segue em anexo a nota fiscal", "Produtivo"),
            ("Solicito cancelamento do serviço", "Produtivo"),
            ("Desconto imperdível só hoje", "Improdutivo"),
            ("Ganhe dinheiro fácil clique aqui", "Improdutivo"),
        ]
        return pd.DataFrame(fallback_examples, columns=["text", "label"])

    def predict(self, email_text: str):
        if not self.classification_pipeline:
            return "Desconhecido", 0.0
            
        # Realiza a predição
        predicted_category = self.classification_pipeline.predict([email_text])[0]
        
        # Calcula a confiança (probabilidade)
        probabilities = self.classification_pipeline.predict_proba([email_text])[0]
        classes = self.classification_pipeline.classes_
        
        confidence_score = 0.0
        for class_label, probability in zip(classes, probabilities):
            if class_label == predicted_category:
                confidence_score = probability
                break
                
        return predicted_category, float(confidence_score)

# Singleton global
classifier = EmailClassifier()
