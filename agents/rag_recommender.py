from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from rag.retriever import buscar_articulos_similares
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """
Eres el agente RAG Recommender de La Figa. Tu misión es recomendar artículos
del archivo de la revista que sean relevantes para el contenido actual.

Usa la herramienta 'buscar_articulos_similares' para recuperar los artículos
más relevantes del archivo. Luego presenta las 3 mejores recomendaciones con:
- Título del artículo
- Por qué es relevante (1 frase)
- Extracto clave (2-3 líneas)
"""

def rag_recommender_agent():
    return LlmAgent(
        name="rag_recommender",
        description="Recomienda artículos relacionados usando RAG",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        instruction=SYSTEM_PROMPT,
        tools=[FunctionTool(buscar_articulos_similares)],
        output_key="recomendaciones",
    )
