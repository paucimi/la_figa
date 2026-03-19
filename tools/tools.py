"""
Herramientas compartidas — La Figa
Funciones reutilizables disponibles para todos los agentes.
"""

from datetime import datetime


def obtener_fecha_actual() -> str:
    """
    Devuelve la fecha actual formateada.

    Returns:
        Fecha en formato legible: 'Jueves, 19 de marzo de 2026'
    """
    MESES = [
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    now = datetime.now()
    dia_semana = DIAS[now.weekday()]
    mes = MESES[now.month]
    return f"{dia_semana.capitalize()}, {now.day} de {mes} de {now.year}"


def contar_palabras(texto: str) -> str:
    """
    Cuenta palabras y caracteres de un texto.

    Args:
        texto: El texto a analizar

    Returns:
        Estadísticas de longitud del texto
    """
    palabras = len(texto.split())
    caracteres = len(texto)
    tiempo_lectura = max(1, round(palabras / 200))
    return (
        f"Palabras: {palabras} | "
        f"Caracteres: {caracteres} | "
        f"Tiempo de lectura estimado: {tiempo_lectura} min"
    )


def formatear_para_revista(titulo: str, contenido: str, autor: str = "La Figa") -> str:
    """
    Da formato de revista a un artículo con encabezado editorial.

    Args:
        titulo: Título del artículo
        contenido: Cuerpo del artículo
        autor: Firma del artículo (por defecto 'La Figa')

    Returns:
        Artículo con formato editorial completo
    """
    fecha = obtener_fecha_actual()
    separador = "─" * 60
    return (
        f"{separador}\n"
        f"LA FIGA · REVISTA DIGITAL\n"
        f"{fecha}\n"
        f"{separador}\n\n"
        f"# {titulo}\n\n"
        f"*Por {autor}*\n\n"
        f"{separador}\n\n"
        f"{contenido}\n\n"
        f"{separador}\n"
        f"© La Figa 2026 · lafiga.es"
    )


def extraer_hashtags_sugeridos(tema: str) -> str:
    """
    Genera hashtags base sugeridos para redes sociales a partir de un tema.

    Args:
        tema: El tema del artículo o contenido

    Returns:
        Lista de hashtags sugeridos en español e inglés
    """
    tema_slug = tema.lower().replace(" ", "").replace(",", "").replace("á", "a").replace(
        "é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    base_hashtags = [
        "#LaFiga",
        "#SexualidadFemenina",
        "#PlanetaFemenino",
        "#SexEducation",
        "#FemaleHealth",
        "#CuerpoFemenino",
        "#SaludSexual",
        "#Feminismo",
    ]

    tema_hashtag = f"#{tema_slug.capitalize()}"
    if tema_hashtag not in base_hashtags:
        base_hashtags.insert(1, tema_hashtag)

    return " ".join(base_hashtags[:8])


def validar_longitud_articulo(texto: str) -> str:
    """
    Valida si un artículo cumple con la extensión mínima recomendada para La Figa.

    Args:
        texto: El texto del artículo a validar

    Returns:
        Mensaje con el resultado de la validación y sugerencias
    """
    palabras = len(texto.split())
    MIN_PALABRAS = 400
    IDEAL_PALABRAS = 700

    if palabras < MIN_PALABRAS:
        falta = MIN_PALABRAS - palabras
        return (
            f"⚠️  Artículo corto: {palabras} palabras. "
            f"Faltan al menos {falta} palabras para cumplir el mínimo de La Figa ({MIN_PALABRAS})."
        )
    elif palabras < IDEAL_PALABRAS:
        return (
            f"✓ Longitud aceptable: {palabras} palabras. "
            f"Puedes enriquecerlo para alcanzar las {IDEAL_PALABRAS} palabras ideales."
        )
    else:
        return f"✓ Longitud óptima: {palabras} palabras. Artículo listo para publicar."
