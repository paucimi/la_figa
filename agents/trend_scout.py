from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from dotenv import load_dotenv
import os

load_dotenv()

SYSTEM_PROMPT = """
Eres el agente Trend Scout de La Figa, una revista digital sobre sexualidad
desde la perspectiva femenina. Tu misión es analizar tendencias editoriales
actuales sobre el tema recibido.

Para cada análisis debes identificar:
- 3-5 ángulos editoriales interesantes
- Qué preguntas hace realmente la gente
- Mitos o tabúes persistentes que vale la pena abordar
- Tono recomendado para la audiencia de La Figa

Tu tono es analítico pero accesible. Nunca moralistas.
"""

def trend_scout_agent():
    return LlmAgent(
        name="trend_scout",
        description="Investiga tendencias editoriales sobre sexualidad femenina",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        instruction=SYSTEM_PROMPT,
        tools=[google_search],
        output_key="tendencias",  # Pasa el resultado al siguiente agente
    )
