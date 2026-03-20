import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️  ADVERTENCIA: No se encontró GEMINI_API_KEY ni GOOGLE_API_KEY. "
          "La app arrancará pero las llamadas a la IA fallarán.")

NEWSPAPER_NAME = os.getenv("NEWSPAPER_NAME", "Doxas")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
LANGUAGE = os.getenv("LANGUAGE", "español")

ARTICLES_DIR = os.getenv("ARTICLES_DIR", "data/articles")
os.makedirs(ARTICLES_DIR, exist_ok=True)

CHROMA_DIR = os.getenv("CHROMA_DIR", "/tmp/chroma_db")
os.makedirs(CHROMA_DIR, exist_ok=True)

SESSIONS_DIR = os.getenv("SESSIONS_DIR", "/tmp/sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)
