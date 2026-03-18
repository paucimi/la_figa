import asyncio
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from orchestrator.pipeline import build_editorial_pipeline, build_chatbot
from rag.vector_store import cargar_articulos
import json
import os

APP_NAME = "la_figa"

async def run_pipeline(tema: str):
    """Ejecuta el pipeline editorial completo."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id="editor"
    )

    pipeline = build_editorial_pipeline()
    runner = Runner(
        agent=pipeline,
        app_name=APP_NAME,
        session_service=session_service
    )

    print(f"\n{'='*50}")
    print(f"PIPELINE LA FIGA — Tema: {tema}")
    print(f"{'='*50}\n")

    async for event in runner.run_async(
        user_id="editor",
        session_id=session.id,
        new_message=_to_content(tema)
    ):
        if event.is_final_response():
            print("\nRESULTADO FINAL:")
            print(event.content.parts[0].text)


def _to_content(texto: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=texto)])


async def run_chatbot(pregunta_inicial: str | None = None):
    """Ejecuta el chatbot de lectoras en modo conversacional."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, user_id="lectora"
    )

    chatbot = build_chatbot()
    runner = Runner(
        agent=chatbot,
        app_name=APP_NAME,
        session_service=session_service
    )

    print("\n" + "="*50)
    print("  LA FIGA — Chatbot de lectoras/es")
    print("  Escribe 'salir' para terminar la conversación")
    print("="*50 + "\n")

    pregunta = pregunta_inicial
    while True:
        if pregunta is None:
            try:
                pregunta = input("Tú: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nHasta pronto 💫")
                break

        if not pregunta:
            pregunta = None
            continue

        if pregunta.lower() in ("salir", "exit", "quit", "bye"):
            print("\nHasta pronto 💫")
            break

        async for event in runner.run_async(
            user_id="lectora",
            session_id=session.id,
            new_message=_to_content(pregunta)
        ):
            if event.is_final_response():
                print(f"\nLa Figa: {event.content.parts[0].text}\n")

        pregunta = None


def cargar_datos_iniciales():
    """Carga artículos de ejemplo en ChromaDB si el archivo existe."""
    ruta = "data/articles/sample_articles.json"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            articulos = json.load(f)
        cargar_articulos(articulos)


if __name__ == "__main__":
    import sys

    # Cargar datos RAG al inicio
    cargar_datos_iniciales()

    modo = sys.argv[1] if len(sys.argv) > 1 else "pipeline"

    if modo == "pipeline":
        tema = sys.argv[2] if len(sys.argv) > 2 else "placer femenino y autoconocimiento"
        asyncio.run(run_pipeline(tema))

    elif modo == "chatbot":
        pregunta_inicial = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(run_chatbot(pregunta_inicial))
