from google.adk.agents import LlmAgent
from google.adk.tools import google_search, FunctionTool
from config.settings import GEMINI_MODEL, LANGUAGE
from tools.fecha import get_current_date

SYSTEM_PROMPT = f"""
Eres el agente Trend Scout de La Figa, una revista digital sobre sexualidad
desde la perspectiva femenina. Tu misión es analizar tendencias editoriales
actuales sobre el tema recibido. Responde siempre en {LANGUAGE}.

Usa 'get_current_date' al inicio para saber la fecha actual y orientar
la búsqueda hacia contenido reciente y relevante.

Para cada análisis debes identificar:
- 3-5 ángulos editoriales interesantes
- Qué preguntas hace realmente la gente
- Mitos o tabúes persistentes que vale la pena abordar
- Tono recomendado para la audiencia de La Figa

Tu tono es analítico pero accesible. Nunca moralista.
"""

def trend_scout_agent():
    return LlmAgent(
        name="trend_scout",
        description="Investiga tendencias editoriales sobre sexualidad femenina",
        model=GEMINI_MODEL,
        instruction=SYSTEM_PROMPT,
        tools=[google_search, FunctionTool(get_current_date)],
        output_key="tendencias",
    )
