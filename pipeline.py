# pipeline.py
# ==============================
# PIPELINE EDITORIAL – Coordinador de Agentes
# ==============================
# Este archivo conecta los agentes entre sí.
# Es el "director de orquesta" del sistema.
#
# FLUJO:
#   1. Trend Scout busca temas en tendencia
#   2. El usuario (o el sistema) elige un tema
#   3. Content Writer genera el artículo
#   4. Se guarda y muestra el resultado
#
# Este patrón se llama "pipeline de agentes" y es
# uno de los patrones más comunes en sistemas multi-agente.

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.trend_scout import run_trend_scout
from agents.content_writer import generate_article, save_article, display_article


def run_editorial_pipeline(location: str = "España", auto_select: bool = False):
    """
    Ejecuta el pipeline editorial completo.

    Parámetros:
        location: Ciudad/región para buscar tendencias
        auto_select: Si True, elige el primer tema automáticamente (útil para demos)
    """
    print("\n" + "🗞️ " * 20)
    print("       NEWSMIND – PIPELINE EDITORIAL")
    print("🗞️ " * 20 + "\n")

    # ---- PASO 1: Buscar tendencias ----
    print("📡 PASO 1: Buscando tendencias informativas...\n")
    topics = run_trend_scout(location=location)

    # ---- PASO 2: Seleccionar tema ----
    print("\n" + "-"*50)
    print("📋 PASO 2: Selección de tema")
    print("-"*50)

    if auto_select:
        # Modo automático: elige el tema de mayor urgencia
        topic_data = sorted(topics, key=lambda x: x["urgencia"] == "alta", reverse=True)[0]
        print(f"→ Tema seleccionado automáticamente: {topic_data['tema']}")
    else:
        # Modo interactivo: el usuario elige
        print("\nTemas disponibles:")
        for i, t in enumerate(topics, 1):
            urgencia_emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}.get(t["urgencia"], "⚪")
            print(f"  {i}. {urgencia_emoji} {t['tema']}")
            print(f"     Ángulo: {t['angulo']}\n")

        while True:
            try:
                choice = int(input("Elige un número (1-5): ")) - 1
                if 0 <= choice < len(topics):
                    topic_data = topics[choice]
                    break
                print("❌ Número fuera de rango, inténtalo de nuevo")
            except ValueError:
                print("❌ Introduce un número válido")

    # ---- PASO 3: Generar artículo ----
    print(f"\n✍️  PASO 3: Generando artículo...\n")
    print(f"Tema: {topic_data['tema']}")
    print(f"Estilo: {topic_data['estilo_recomendado']}\n")

    article = generate_article(
        topic=topic_data["tema"],
        style=topic_data.get("estilo_recomendado", "informativo")
    )

    # ---- PASO 4: Mostrar y guardar ----
    print("📰 PASO 4: Artículo generado:\n")
    display_article(article)

    filepath = save_article(article)

    print(f"\n✅ Pipeline completado. Artículo guardado en: {filepath}")
    return article


if __name__ == "__main__":
    # Puedes cambiar la localización aquí
    run_editorial_pipeline(location="Madrid", auto_select=False)