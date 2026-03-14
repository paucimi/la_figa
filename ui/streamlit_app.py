import streamlit as st
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from orchestrator.pipeline import build_editorial_pipeline, build_chatbot
from rag.vector_store import cargar_articulos
import json

APP_NAME = "la_figa"

# ── Configuración de página ────────────────────────────────────────────────

st.set_page_config(
    page_title="La Figa · Plataforma Editorial IA",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Fondo negro editorial */
    .stApp { background-color: #0a0a0a; color: #e8e0d0; }
    .stApp > header { background-color: #0a0a0a; }

    /* Tipografía */
    html, body, [class*="css"] {
        font-family: 'Georgia', serif;
        color: #e8e0d0;
    }

    /* Título principal */
    .la-figa-title {
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: 6px;
        color: #c9a96e;
        text-align: center;
        margin-top: 1rem;
    }
    .la-figa-tagline {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: -0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Divider dorado */
    hr { border-color: #2a2a2a !important; }
    .gold-line {
        height: 1px;
        background: linear-gradient(to right, transparent, #c9a96e, transparent);
        margin: 0.5rem auto 1.5rem;
        width: 60%;
    }

    /* Badges de tecnología */
    .tech-badges {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 1.5rem;
    }
    .tech-badge {
        background: #111;
        border: 0.5px solid #333;
        color: #888;
        padding: 3px 12px;
        border-radius: 2px;
        font-size: 0.7rem;
        letter-spacing: 1px;
        font-family: 'Courier New', monospace;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #0a0a0a;
        border-bottom: 0.5px solid #222;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #555;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 12px 24px;
        border-radius: 0;
        font-family: 'Courier New', monospace;
    }
    .stTabs [aria-selected="true"] {
        color: #c9a96e !important;
        border-bottom: 1px solid #c9a96e !important;
        background: transparent !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stChatInput textarea {
        background: #111 !important;
        border: 0.5px solid #2a2a2a !important;
        border-radius: 2px !important;
        color: #e8e0d0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #c9a96e !important;
        box-shadow: none !important;
    }

    /* Botón primario */
    .stButton > button {
        background: transparent !important;
        border: 0.5px solid #c9a96e !important;
        color: #c9a96e !important;
        border-radius: 2px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.75rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        padding: 10px 24px !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #c9a96e !important;
        color: #0a0a0a !important;
    }

    /* Status / spinner */
    .stStatus { background: #111 !important; border: 0.5px solid #222 !important; }

    /* Chat messages */
    .stChatMessage {
        background: #111 !important;
        border: 0.5px solid #1e1e1e !important;
        border-radius: 2px !important;
    }

    /* Output text */
    .output-box {
        background: #0f0f0f;
        border: 0.5px solid #222;
        border-left: 2px solid #c9a96e;
        padding: 1.2rem 1.5rem;
        font-size: 0.9rem;
        line-height: 1.8;
        border-radius: 2px;
        font-family: 'Georgia', serif;
        color: #d4c9b5;
        margin-top: 1rem;
    }

    /* Labels */
    label, .stCaption { color: #555 !important; font-family: 'Courier New', monospace !important; font-size: 0.7rem !important; letter-spacing: 1px !important; }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #333;
        font-size: 0.7rem;
        letter-spacing: 2px;
        font-family: 'Courier New', monospace;
        padding: 1rem 0;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 900px; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────

logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
if os.path.exists(logo_path):
    col_logo = st.columns([1, 2, 1])[1]
    with col_logo:
        st.image(logo_path, width=180)
else:
    st.markdown('<div class="la-figa-title">LA FIGA</div>', unsafe_allow_html=True)

st.markdown('<div class="la-figa-tagline">La expresión natural del cuerpo femenino · Vol. 1 · 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="tech-badges">
    <span class="tech-badge">Google ADK</span>
    <span class="tech-badge">Gemini 2.5</span>
    <span class="tech-badge">RAG</span>
    <span class="tech-badge">ChromaDB</span>
    <span class="tech-badge">MCP</span>
</div>
""", unsafe_allow_html=True)

# ── Inicialización RAG ─────────────────────────────────────────────────────

@st.cache_resource
def init_rag():
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "articles", "sample_articles.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            articulos = json.load(f)
        cargar_articulos(articulos)
        return len(articulos)
    return 0

n_articulos = init_rag()

# ── Helper async ───────────────────────────────────────────────────────────

async def run_agent_async(agent, user_id, mensaje):
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=user_id)
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    resultado = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message={"role": "user", "parts": [{"text": mensaje}]}
    ):
        if event.is_final_response():
            resultado = event.content.parts[0].text
    return resultado

def run_agent(agent, user_id, mensaje):
    return asyncio.run(run_agent_async(agent, user_id, mensaje))

# ── Tabs ───────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["PIPELINE EDITORIAL", "CHATBOT DE LECTORAS"])

# ── TAB 1: Pipeline ────────────────────────────────────────────────────────

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    tema = st.text_input(
        "TEMA EDITORIAL",
        placeholder="deseo femenino, orgasmo, comunicación en pareja...",
        key="tema_pipeline"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EJECUTAR PIPELINE"):
        if not tema.strip():
            st.warning("Introduce un tema para continuar.")
        else:
            pipeline = build_editorial_pipeline()
            with st.status("Ejecutando agentes...", expanded=True) as status:
                st.write("→ Trend Scout analizando tendencias...")
                st.write("→ Content Writer redactando artículo...")
                st.write("→ RAG Recommender buscando archivo...")
                st.write("→ Social Publisher generando posts...")
                resultado = run_agent(pipeline, "editor", tema)
                status.update(label="Pipeline completado", state="complete")

            st.markdown(f'<div class="output-box">{resultado}</div>', unsafe_allow_html=True)

# ── TAB 2: Chatbot ─────────────────────────────────────────────────────────

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pregunta = st.chat_input("Este es un espacio seguro. Escribe tu pregunta...")

    if pregunta:
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)
        with st.chat_message("assistant"):
            with st.spinner(""):
                chatbot = build_chatbot()
                respuesta = run_agent(chatbot, "lectora", pregunta)
            st.markdown(respuesta)
        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

    if st.session_state.mensajes:
        if st.button("LIMPIAR CONVERSACIÓN"):
            st.session_state.mensajes = []
            st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<div class="footer-text">LA FIGA · REVISTA DIGITAL & CULTURAL · {n_articulos} ARTÍCULOS EN ARCHIVO</div>', unsafe_allow_html=True)
