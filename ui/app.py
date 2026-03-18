"""
FastAPI app — La Figa
"""

import asyncio
import json
import os
import sys
import uuid
import re
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from orchestrator.pipeline import build_editorial_pipeline, build_chatbot
from rag.vector_store import cargar_articulos

APP_NAME = "la_figa"
app = FastAPI(title="La Figa")

# ── Almacén de artículos en memoria ───────────────────────────────────────

_articles: list[dict] = []  # [{ id, tema, titulo, extracto, articulo, posts, recomendaciones, fecha }]


def _extract_title(texto: str, fallback: str) -> str:
    """Extrae el primer titular del markdown (###, ##, #) o usa el fallback."""
    for line in texto.splitlines():
        line = line.strip()
        m = re.match(r'^#{1,3}\s+(.+)', line)
        if m:
            return m.group(1).strip('*!¡¿? ')
    return fallback.capitalize()


def _extract_excerpt(texto: str, chars: int = 220) -> str:
    """Primera frase/párrafo real del artículo, sin markdown."""
    for line in texto.splitlines():
        line = re.sub(r'[#*_>`]', '', line).strip()
        if len(line) > 60:
            return line[:chars] + ('…' if len(line) > chars else '')
    return texto[:chars]


# ── Inicialización RAG ─────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "articles", "sample_articles.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            articulos = json.load(f)
        cargar_articulos(articulos)
        # Poblar portada con artículos de muestra
        for a in articulos:
            _articles.append({
                "id": a["id"],
                "tema": "Archivo",
                "titulo": a["titulo"],
                "extracto": _extract_excerpt(a.get("contenido", "")),
                "articulo": a.get("contenido", ""),
                "posts": "",
                "recomendaciones": "",
                "fecha": "ARCHIVO · LA FIGA",
            })


# ── Static files ───────────────────────────────────────────────────────────

static_dir = os.path.join(os.path.dirname(__file__), "static")
assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
        return f.read()


# ── Artículos ──────────────────────────────────────────────────────────────

@app.get("/api/articles")
def list_articles():
    return [
        {k: v for k, v in a.items() if k != "articulo"}
        for a in reversed(_articles)
    ]


@app.get("/api/articles/{article_id}")
def get_article(article_id: str):
    for a in _articles:
        if a["id"] == article_id:
            return a
    return {"error": "No encontrado"}, 404


# ── Pipeline con SSE ───────────────────────────────────────────────────────

def _to_content(texto: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=texto)])


@app.post("/api/pipeline")
async def run_pipeline(request: Request):
    body = await request.json()
    tema = body.get("tema", "").strip()
    if not tema:
        return {"error": "Falta el tema"}

    async def event_stream():
        session_service = InMemorySessionService()
        session = await session_service.create_session(app_name=APP_NAME, user_id="editor")
        pipeline = build_editorial_pipeline()
        runner = Runner(agent=pipeline, app_name=APP_NAME, session_service=session_service)

        accumulated = {"articulo": "", "posts": "", "recomendaciones": ""}

        # Pasos visibles para el usuario (sin nombres internos de agentes)
        STEP_LABELS = {
            "trend_scout":      "Investigando tendencias...",
            "content_writer":   "Redactando el artículo...",
            "rag_recommender":  "Buscando contenido relacionado...",
            "social_publisher": "Preparando posts para redes...",
        }

        async for event in runner.run_async(
            user_id="editor",
            session_id=session.id,
            new_message=_to_content(tema)
        ):
            if not (event.is_final_response() and event.content and event.content.parts):
                continue

            agente = event.author if hasattr(event, "author") else ""
            texto = event.content.parts[0].text or ""
            if not texto:
                continue

            # Acumular para guardar al final
            if agente == "content_writer":
                accumulated["articulo"] = texto
            elif agente == "social_publisher":
                accumulated["posts"] = texto
            elif agente == "rag_recommender":
                accumulated["recomendaciones"] = texto

            label = STEP_LABELS.get(agente, "")
            data = json.dumps({"step": label, "agente": agente, "texto": texto}, ensure_ascii=False)
            yield f"data: {data}\n\n"

        # Guardar artículo
        if accumulated["articulo"]:
            article_id = str(uuid.uuid4())
            _articles.append({
                "id": article_id,
                "tema": tema,
                "titulo": _extract_title(accumulated["articulo"], tema),
                "extracto": _extract_excerpt(accumulated["articulo"]),
                "articulo": accumulated["articulo"],
                "posts": accumulated["posts"],
                "recomendaciones": accumulated["recomendaciones"],
                "fecha": datetime.now().strftime("%d %b %Y").upper(),
            })
            if len(_articles) > 50:
                _articles.pop(0)
            yield f"data: {json.dumps({'done': True, 'article_id': article_id})}\n\n"
        else:
            yield f"data: {json.dumps({'done': True, 'article_id': None})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ── Chatbot multi-turno ────────────────────────────────────────────────────

_chatbot_sessions: dict[str, dict] = {}


@app.post("/api/chat/session")
async def nueva_sesion():
    session_id = str(uuid.uuid4())
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id="lectora")
    chatbot = build_chatbot()
    runner = Runner(agent=chatbot, app_name=APP_NAME, session_service=session_service)
    _chatbot_sessions[session_id] = {
        "session_service": session_service,
        "runner": runner,
        "adk_session": session,
    }
    return {"session_id": session_id}


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    session_id = body.get("session_id", "")
    pregunta = body.get("pregunta", "").strip()

    if not pregunta:
        return {"error": "Falta la pregunta"}
    if session_id not in _chatbot_sessions:
        return {"error": "Sesión no encontrada"}

    ctx = _chatbot_sessions[session_id]
    respuesta = ""
    async for event in ctx["runner"].run_async(
        user_id="lectora",
        session_id=ctx["adk_session"].id,
        new_message=_to_content(pregunta)
    ):
        if event.is_final_response() and event.content and event.content.parts:
            respuesta = event.content.parts[0].text or ""

    return {"respuesta": respuesta}


@app.delete("/api/chat/session/{session_id}")
async def borrar_sesion(session_id: str):
    _chatbot_sessions.pop(session_id, None)
    return {"ok": True}
