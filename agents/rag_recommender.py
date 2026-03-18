from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from rag.retriever import buscar_articulos_similares
from config.settings import GEMINI_MODEL, LANGUAGE

SYSTEM_PROMPT = f"""
Eres el agente de recomendación de contenido de La Figa.
Recibirás un artículo (clave: 'articulo') y debes encontrar los 3 artículos
del archivo más relevantes para recomendar a las lectoras.
Responde siempre en {LANGUAGE}.

Usa la herramienta 'buscar_articulos_similares' con los temas clave del artículo.
Para cada recomendación incluye:
- Título del artículo
- Por qué es relevante (1 línea)
- Extracto más destacado
- Puntuación de relevancia
"""

def rag_recommender_agent():
    return LlmAgent(
        name="rag_recommender",
        description="Recomienda artículos relacionados del archivo de La Figa",
        model=GEMINI_MODEL,
        instruction=SYSTEM_PROMPT,
        tools=[FunctionTool(buscar_articulos_similares)],
        output_key="recomendaciones",
    )
