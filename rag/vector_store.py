import chromadb
from chromadb import EmbeddingFunction, Embeddings
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiEmbeddingFunction(EmbeddingFunction):
    """Embedding function usando google-genai (nueva API)."""

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"))

    def __call__(self, input: list[str]) -> Embeddings:
        result = self.client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=input,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
        )
        return [e.values for e in result.embeddings]


def get_vector_store():
    """Inicializa o carga la base de datos vectorial ChromaDB."""
    client = chromadb.PersistentClient(path="data/chroma_db")

    collection = client.get_or_create_collection(
        name="la_figa_articles",
        embedding_function=GeminiEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def cargar_articulos(articulos: list[dict]):
    """
    Carga artículos en ChromaDB.
    Cada artículo: {"id": str, "titulo": str, "contenido": str}
    """
    col = get_vector_store()
    col.upsert(
        ids=[a["id"] for a in articulos],
        documents=[a["contenido"] for a in articulos],
        metadatas=[{"titulo": a["titulo"]} for a in articulos],
    )
    print(f"{len(articulos)} artículos cargados en ChromaDB.")
