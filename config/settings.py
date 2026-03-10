import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ No se encontró GEMINI_API_KEY en el archivo .env")

NEWSPAPER_NAME = os.getenv("NEWSPAPER_NAME", "Doxas")
GEMINI_MODEL = "gemini-2.5-flash-lite"

ARTICLES_DIR = "data/articles"
os.makedirs(ARTICLES_DIR, exist_ok=True)

CHROMA_DIR = "data/chroma_db"
os.makedirs(CHROMA_DIR, exist_ok=True)
