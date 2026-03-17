"""
La Figa · Plataforma Editorial Inteligente
Punto de entrada principal de la aplicación.

Uso:
    python main.py pipeline "placer femenino y autoconocimiento"
    python main.py chatbot "¿cómo puedo comunicar mejor mis deseos?"
    python main.py cargar-articulos
"""

import sys
import asyncio
import argparse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from orchestrator.pipeline import build_editorial_pipeline, build_chatbot
from rag.vector_store import cargar_articulos

APP_NAME = "la_figa"


async def _run_agent_async(agent, user_id: str, mensaje: str) -> str:
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=user_id)
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    resultado = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message={"role": "user", "parts": [{"text": mensaje}]},
    ):
        if event.is_final_response():
            resultado = event.content.parts[0].text
    return resultado


def run_agent(agent, user_id: str, mensaje: str) -> str:
    return asyncio.run(_run_agent_async(agent, user_id, mensaje))


def cmd_pipeline(tema: str):
    """Ejecuta el pipeline editorial completo para un tema dado."""
    print(f"\n🌸  LA FIGA — Pipeline Editorial")
    print(f"    Tema: {tema}\n")
    print("→ Iniciando agentes...\n")

    pipeline = build_editorial_pipeline()
    resultado = run_agent(pipeline, "editor", tema)

    print("=" * 60)
    print(resultado)
    print("=" * 60)


def cmd_chatbot(pregunta: str):
    """Lanza el chatbot de lectoras en modo interactivo (o responde una pregunta)."""
    chatbot = build_chatbot()

    if pregunta:
        print(f"\n🌸  LA FIGA — Chatbot\n")
        respuesta = run_agent(chatbot, "lectora", pregunta)
        print(respuesta)
        return

    # Modo interactivo
    print("\n🌸  LA FIGA — Chatbot de Lectoras")
    print("    Escribe 'salir' para terminar.\n")
    while True:
        try:
            entrada = input("Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta pronto!")
            break
        if entrada.lower() in ("salir", "exit", "quit"):
            print("¡Hasta pronto!")
            break
        if not entrada:
            continue
        respuesta = run_agent(chatbot, "lectora", entrada)
        print(f"\nLa Figa: {respuesta}\n")


def cmd_cargar_articulos():
    """Carga los artículos de ejemplo en ChromaDB."""
    import json
    import os

    ruta = os.path.join("data", "articles", "sample_articles.json")
    if not os.path.exists(ruta):
        print(f"❌  No se encontró el archivo {ruta}")
        sys.exit(1)

    with open(ruta, "r", encoding="utf-8") as f:
        articulos = json.load(f)

    cargar_articulos(articulos)
    print(f"✅  {len(articulos)} artículos cargados en ChromaDB.")


def main():
    parser = argparse.ArgumentParser(
        prog="la_figa",
        description="La Figa · Plataforma Editorial Inteligente",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # pipeline
    p_pipeline = subparsers.add_parser("pipeline", help="Ejecutar el pipeline editorial")
    p_pipeline.add_argument("tema", help="Tema editorial a trabajar")

    # chatbot
    p_chatbot = subparsers.add_parser("chatbot", help="Chatbot de lectoras/es")
    p_chatbot.add_argument(
        "pregunta",
        nargs="?",
        default="",
        help="Pregunta puntual (omite para modo interactivo)",
    )

    # cargar-articulos
    subparsers.add_parser("cargar-articulos", help="Cargar artículos de ejemplo en ChromaDB")

    args = parser.parse_args()

    if args.comando == "pipeline":
        cmd_pipeline(args.tema)
    elif args.comando == "chatbot":
        cmd_chatbot(args.pregunta)
    elif args.comando == "cargar-articulos":
        cmd_cargar_articulos()


if __name__ == "__main__":
    main()
