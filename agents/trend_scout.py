# agents/trend_scout.py
# ==============================
# AGENTE 1 – Trend Scout
# ==============================
# Este agente busca en internet qué temas están en tendencia
# y los convierte en propuestas de artículos para el periódico.
#
# Tecnologías usadas:
#   - DuckDuckGo Search (búsqueda web gratuita, sin API key)
#   - LangChain (para estructurar el agente con herramientas)
#   - Gemini (para analizar y filtrar los resultados)

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, NEWSPAPER_NAME

import google.generativeai as genai
from duckduckgo_search import DDGS

genai.configure(api_key=GEMINI_API_KEY)


def search_trending_topics(location: str = "España", num_results: int = 10) -> list[str]:
    """
    Busca noticias recientes usando DuckDuckGo.

    Parámetros:
        location: Ciudad o región de interés. Ej: "Madrid", "España"
        num_results: Cuántos resultados de búsqueda recuperar

    Devuelve:
        Lista de titulares/snippets encontrados
    """
    print(f"🔍 Buscando tendencias en: {location}...")

    raw_results = []

    # Hacemos varias búsquedas para tener diversidad de temas
    search_queries = [
        f"noticias {location} hoy",
        f"tendencias {location} actualidad",
        f"novedades locales {location}"
    ]

    with DDGS() as ddgs:
        for query in search_queries:
            results = list(ddgs.news(
                keywords=query,
                region="es-es",
                max_results=num_results // len(search_queries)
            ))
            for r in results:
                raw_results.append(f"{r['title']}: {r['body'][:200]}")

    print(f"   → Encontrados {len(raw_results)} resultados crudos")
    return raw_results


def analyze_and_filter_topics(raw_results: list[str], location: str) -> list[dict]:
    """
    Usa Gemini para analizar los resultados de búsqueda y seleccionar
    los 5 temas más relevantes para un periódico local.

    Esto es lo que convierte una búsqueda en web en un agente inteligente:
    el modelo razona sobre qué es relevante, qué tiene ángulo periodístico
    y qué interesa a los lectores locales.

    Devuelve:
        Lista de dicts con: tema, angulo, urgencia
    """
    print("🧠 Analizando tendencias con Gemini...")

    # Preparamos el contexto para Gemini
    results_text = "\n".join([f"- {r}" for r in raw_results])

    prompt = f"""
Eres el director editorial de '{NEWSPAPER_NAME}', un periódico local de {location}.

Has recibido estos resultados de búsqueda de noticias recientes:
{results_text}

TAREA: Analiza estos resultados y selecciona los 5 temas más interesantes 
para cubrir en el periódico. Prioriza:
1. Relevancia local (que afecte a la comunidad)
2. Interés público real
3. Posibilidad de generar debate o engagement
4. Originalidad (evita temas ya muy cubiertos)

FORMATO DE RESPUESTA (solo JSON, sin texto adicional):
{{
    "temas": [
        {{
            "tema": "Descripción clara del tema en 1 frase",
            "angulo": "Enfoque periodístico sugerido (ej: impacto en vecinos, coste para el ayuntamiento...)",
            "urgencia": "alta/media/baja",
            "estilo_recomendado": "informativo/reportaje/opinión/breve"
        }}
    ]
}}
"""

    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    result = json.loads(raw_text)
    return result["temas"]


def run_trend_scout(location: str = "España") -> list[dict]:
    """
    Función principal del agente: busca y analiza tendencias.
    Esta es la función que llaman otros agentes del sistema.
    """
    raw_results = search_trending_topics(location)
    topics = analyze_and_filter_topics(raw_results, location)

    print(f"\n✅ Trend Scout encontró {len(topics)} temas:")
    for i, t in enumerate(topics, 1):
        print(f"   {i}. [{t['urgencia'].upper()}] {t['tema']}")

    return topics


# ---- PRUEBA DIRECTA ----
if __name__ == "__main__":
    print("🤖 Iniciando Trend Scout Agent...")
    topics = run_trend_scout(location="España")

    print("\n📋 Temas detallados:")
    for t in topics:
        print(f"\n→ {t['tema']}")
        print(f"  Ángulo: {t['angulo']}")
        print(f"  Urgencia: {t['urgencia']} | Estilo: {t['estilo_recomendado']}")