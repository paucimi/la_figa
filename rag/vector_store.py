import os
import warnings
import chromadb
from chromadb import EmbeddingFunction, Embeddings
from vertexai.language_models import TextEmbeddingModel, TextEmbeddingInput
from config.settings import CHROMA_DIR

# AVISO: si CHROMA_DIR apunta a /tmp (Cloud Run sin volume mount GCS),
# la base vectorial se pierde al reiniciar el contenedor.
# En producción, monta un bucket GCS como volumen en Cloud Run
# (ver terraform/main.tf) o migra a Vertex AI Vector Search.
if CHROMA_DIR.startswith("/tmp"):
    warnings.warn(
        "ChromaDB en /tmp es efímero: los artículos se borrarán si el contenedor "
        "se reinicia. Configura GCS_CHROMA_BUCKET en Terraform para persistencia.",
        stacklevel=2,
    )


class VertexAIEmbeddingFunction(EmbeddingFunction):
    """Embedding function usando Vertex AI Text Embeddings (sin API key)."""

    def __init__(self):
        # text-multilingual-embedding-002 soporta español y 100+ idiomas
        self.model = TextEmbeddingModel.from_pretrained("text-multilingual-embedding-002")

    def __call__(self, input: list[str]) -> Embeddings:
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in input]
        embeddings = self.model.get_embeddings(inputs)
        return [e.values for e in embeddings]


def get_vector_store():
    """Inicializa o carga la base de datos vectorial ChromaDB."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    collection = client.get_or_create_collection(
        name="la_figa_articles",
        embedding_function=VertexAIEmbeddingFunction(),
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
