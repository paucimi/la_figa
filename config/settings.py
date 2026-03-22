import os
import vertexai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
# Regiones recomendadas para Gemini 2.5 Flash (razonamiento avanzado disponible primero aquí):
#   europe-west1  → menor latencia desde Europa (recomendado si tu audiencia es europea)
#   us-central1   → menor latencia desde EEUU
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1")

if not GOOGLE_CLOUD_PROJECT:
    raise ValueError(
        "❌ No se encontró GOOGLE_CLOUD_PROJECT en el archivo .env\n"
        "   Crea un .env con: GOOGLE_CLOUD_PROJECT=tu-project-id"
    )

# Inicializar Vertex AI — en Cloud Run usa ADC automático (service account)
# En local usa GOOGLE_APPLICATION_CREDENTIALS o `gcloud auth application-default login`
vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

# Indicar al ADK que use Vertex AI como backend (no Gemini API Key)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT
os.environ["GOOGLE_CLOUD_LOCATION"] = GOOGLE_CLOUD_LOCATION

NEWSPAPER_NAME = os.getenv("NEWSPAPER_NAME", "la_figa")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
LANGUAGE = os.getenv("LANGUAGE", "español")

ARTICLES_DIR = os.getenv("ARTICLES_DIR", "data/articles")
os.makedirs(ARTICLES_DIR, exist_ok=True)

CHROMA_DIR = os.getenv("CHROMA_DIR", "/tmp/chroma_db")
os.makedirs(CHROMA_DIR, exist_ok=True)

SESSIONS_DIR = os.getenv("SESSIONS_DIR", "/tmp/sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)
