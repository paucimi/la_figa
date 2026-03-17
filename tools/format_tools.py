"""
Herramientas de formato compartidas entre agentes.
"""

import re


def formatear_para_markdown(texto: str) -> str:
    """
    Limpia y normaliza el texto generado por los agentes para presentarlo
    en Markdown (Streamlit, README, etc.).

    Args:
        texto: Texto en bruto generado por el modelo

    Returns:
        Texto con formato Markdown limpio
    """
    # Eliminar líneas en blanco múltiples consecutivas
    texto = re.sub(r"\n{3,}", "\n\n", texto.strip())

    # Normalizar separadores de sección (guiones múltiples → ---  Markdown)
    texto = re.sub(r"(?m)^[-—]{3,}$", "---", texto)

    return texto


def extraer_titulo(texto: str) -> str:
    """
    Extrae el título de un artículo generado por el Content Writer.
    Busca la primera línea no vacía o el primer encabezado Markdown.

    Args:
        texto: Texto completo del artículo

    Returns:
        Título extraído, o 'Sin título' si no se encuentra
    """
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea:
            continue
        # Encabezado Markdown H1 o H2
        if linea.startswith("#"):
            return linea.lstrip("#").strip()
        # Primera línea con contenido real (no separador)
        if linea not in ("---", "===", "***"):
            return linea
    return "Sin título"
