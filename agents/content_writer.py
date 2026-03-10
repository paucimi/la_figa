import json
import os
import sys
from google import genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, NEWSPAPER_NAME, ARTICLES_DIR

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_article(topic: str, style: str = "informativo") -> dict:
    prompt = f"""
Eres el redactor jefe de '{NEWSPAPER_NAME}', un periódico local español que está 
modernizando su contenido digital para atraer lectores jóvenes sin perder rigor periodístico.

TAREA: Escribe un artículo periodístico de estilo '{style}' sobre el siguiente tema:
"{topic}"

FORMATO DE RESPUESTA (responde SOLO con este JSON, sin texto adicional):
{{
    "titulo": "Título atractivo y periodístico (máximo 10 palabras)",
    "subtitulo": "Subtítulo que amplía el título (máximo 20 palabras)",
    "cuerpo": "Cuerpo del artículo en 4-5 párrafos.",
    "tags": ["tag1", "tag2", "tag3", "tag4"],
    "resumen_redes": "Frase de máximo 280 caracteres para redes sociales con 2 hashtags"
}}

REGLAS:
- Escribe en español
- Tono profesional pero cercano
- No inventes nombres propios reales ni datos falsos específicos
"""
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()
    article = json.loads(raw_text)
    article["topic"] = topic
    article["style"] = style
    return article

def save_article(article: dict) -> str:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ARTICLES_DIR}/article_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    print(f"✅ Artículo guardado en: {filename}")
    return filename

def display_article(article: dict):
    print("\n" + "="*60)
    print(f"📰 {article['titulo']}")
    print(f"   {article['subtitulo']}")
    print("="*60)
    print(f"\n{article['cuerpo']}")
    print(f"\n🏷️  Tags: {', '.join(article['tags'])}")
    print(f"\n📱 Redes: {article['resumen_redes']}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("🤖 Iniciando Content Writer Agent...")
    print("📝 Generando artículo de prueba...\n")
    article = generate_article(
        topic="apertura de un nuevo espacio cultural en el centro de la ciudad",
        style="informativo"
    )
    display_article(article)
    save_article(article)
