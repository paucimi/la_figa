"""
Context Manager — La Figa
Gestiona el contexto conversacional entre sesiones con persistencia en disco.
"""

import json
import os
import threading
from datetime import datetime

from config.settings import SESSIONS_DIR

_lock = threading.Lock()


def _session_path(session_id: str) -> str:
    safe_id = session_id.replace("/", "_").replace("\\", "_").replace(":", "_")
    return os.path.join(SESSIONS_DIR, f"{safe_id}.json")


def _load(session_id: str) -> list[dict]:
    path = _session_path(session_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _persist(session_id: str, messages: list[dict]) -> None:
    path = _session_path(session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def get_conversation_context(session_id: str) -> str:
    """
    Recupera el historial de conversación de una sesión.

    Args:
        session_id: Identificador único de la sesión del usuario

    Returns:
        Historial formateado como string, o mensaje vacío si es nueva sesión
    """
    with _lock:
        historial = _load(session_id)

    if not historial:
        return "Nueva conversación — sin historial previo."

    salida = []
    for msg in historial[-6:]:
        rol = "Lectora/lector" if msg["role"] == "user" else "La Figa"
        salida.append(f"{rol}: {msg['content']}")

    return "\n".join(salida)


def save_conversation_context(session_id: str, role: str, content: str) -> str:
    """
    Guarda un mensaje en el historial de conversación.

    Args:
        session_id: Identificador único de la sesión
        role: 'user' o 'assistant'
        content: Contenido del mensaje

    Returns:
        Confirmación de guardado
    """
    with _lock:
        historial = _load(session_id)
        historial.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(historial) > 20:
            historial = historial[-20:]
        _persist(session_id, historial)

    return f"Contexto guardado. Mensajes en sesión: {len(historial)}"


def clear_conversation_context(session_id: str) -> str:
    """
    Limpia el historial de una sesión.

    Args:
        session_id: Identificador único de la sesión

    Returns:
        Confirmación de limpieza
    """
    with _lock:
        path = _session_path(session_id)
        if os.path.exists(path):
            os.remove(path)
    return f"Historial de sesión {session_id} eliminado."
