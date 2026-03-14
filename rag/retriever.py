from rag.vector_store import get_vector_store


def buscar_articulos_similares(consulta: str, n_resultados: int = 3) -> str:
    """
    Busca artículos similares a la consulta en el archivo de La Figa.

    Args:
        consulta: Texto o tema a buscar
        n_resultados: Número de resultados a devolver (por defecto 3)

    Returns:
        String con los artículos más relevantes encontrados
    """
    col = get_vector_store()

    resultados = col.query(
        query_texts=[consulta],
        n_results=n_resultados,
        include=["documents", "metadatas", "distances"]
    )

    if not resultados["documents"][0]:
        return "No se encontraron artículos relacionados en el archivo."

    salida = []
    for doc, meta, dist in zip(
        resultados["documents"][0],
        resultados["metadatas"][0],
        resultados["distances"][0]
    ):
        relevancia = round((1 - dist) * 100, 1)
        salida.append(
            f"TÍTULO: {meta['titulo']}\n"
            f"RELEVANCIA: {relevancia}%\n"
            f"EXTRACTO: {doc[:300]}...\n"
        )

    return "\n---\n".join(salida)
