"""
MCP Context Manager — La Figa
Gestiona el contexto compartido entre agentes usando Model Context Protocol.
Permite que el Reader Chatbot mantenga memoria de la conversación.
"""

from datetime import datetime

# Almacén en memoria (en producción sería una base de datos)
_context_store: dict[str, list[dict]] = {}


def get_conversation_context(session_id: str) -> str:
    """
    Recupera el historial de conversación de una sesión.

    Args:
        session_id: Identificador único de la sesión del usuario

    Returns:
        Historial formateado como string, o mensaje vacío si es nueva sesión
    """
    historial = _context_store.get(session_id, [])

    if not historial:
        return "Nueva conversación — sin historial previo."

    salida = []
    for msg in historial[-6:]:  # Últimos 6 mensajes para no saturar el contexto
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
    if session_id not in _context_store:
        _context_store[session_id] = []

    _context_store[session_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

    # Limitar historial a 20 mensajes por sesión
    if len(_context_store[session_id]) > 20:
        _context_store[session_id] = _context_store[session_id][-20:]

    return f"Contexto guardado. Mensajes en sesión: {len(_context_store[session_id])}"


def clear_conversation_context(session_id: str) -> str:
    """
    Limpia el historial de una sesión.

    Args:
        session_id: Identificador único de la sesión

    Returns:
        Confirmación de limpieza
    """
    if session_id in _context_store:
        del _context_store[session_id]
    return f"Historial de sesión {session_id} eliminado."
