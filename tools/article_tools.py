"""
Herramientas compartidas para gestión de artículos.
Disponibles para cualquier agente del pipeline.
"""

import json
import os
from datetime import datetime

ARTICLES_DIR = os.path.join("data", "articles")


def guardar_articulo(titulo: str, contenido: str, tema: str = "") -> str:
    """
    Guarda un artículo generado en el directorio de datos.

    Args:
        titulo: Título del artículo
        contenido: Cuerpo completo del artículo
        tema: Tema editorial principal (opcional)

    Returns:
        Ruta del archivo guardado
    """
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = titulo.lower().replace(" ", "_")[:40]
    nombre = f"{timestamp}_{slug}.json"
    ruta = os.path.join(ARTICLES_DIR, nombre)

    articulo = {
        "id": f"art_{timestamp}",
        "titulo": titulo,
        "contenido": contenido,
        "tema": tema,
        "fecha": datetime.now().isoformat(),
    }

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(articulo, f, ensure_ascii=False, indent=2)

    return f"Artículo guardado en {ruta}"


def leer_articulo(ruta: str) -> dict:
    """
    Lee un artículo guardado en disco.

    Args:
        ruta: Ruta al archivo JSON del artículo

    Returns:
        Diccionario con los datos del artículo
    """
    if not os.path.exists(ruta):
        return {"error": f"No se encontró el archivo {ruta}"}

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_articulos() -> str:
    """
    Lista todos los artículos guardados en el directorio de datos.

    Returns:
        String con la lista de artículos disponibles
    """
    if not os.path.exists(ARTICLES_DIR):
        return "No hay artículos guardados todavía."

    archivos = [
        f for f in os.listdir(ARTICLES_DIR)
        if f.endswith(".json") and f != "sample_articles.json"
    ]

    if not archivos:
        return "No hay artículos generados todavía."

    archivos.sort(reverse=True)
    lineas = [f"📄 {f}" for f in archivos]
    return f"Artículos disponibles ({len(archivos)}):\n" + "\n".join(lineas)
