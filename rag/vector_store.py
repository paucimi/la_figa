import chromadb
from chromadb.utils import embedding_functions
import os

def get_vector_store():
    """Inicializa o carga la base de datos vectorial ChromaDB."""
    client = chromadb.PersistentClient(path="data/chroma_db")

    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="models/text-embedding-004"
    )

    collection = client.get_or_create_collection(
        name="la_figa_articles",
        embedding_function=gemini_ef,
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
