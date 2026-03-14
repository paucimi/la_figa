from google.adk.agents import SequentialAgent, ParallelAgent
from agents.trend_scout import trend_scout_agent
from agents.content_writer import content_writer_agent
from agents.rag_recommender import rag_recommender_agent
from agents.reader_chatbot import reader_chatbot_agent
from agents.social_publisher import social_publisher_agent


def build_editorial_pipeline():
    """
    Pipeline principal de La Figa.
    Flujo: Trend Scout → Content Writer → [RAG + Social] en paralelo
    """

    # Fase 2: RAG y Social en paralelo (no dependen entre sí)
    fase_publicacion = ParallelAgent(
        name="fase_publicacion",
        description="Recomienda contenido y genera posts simultáneamente",
        sub_agents=[
            rag_recommender_agent(),
            social_publisher_agent(),
        ]
    )

    # Pipeline completo secuencial
    pipeline = SequentialAgent(
        name="la_figa_pipeline",
        description="Pipeline editorial completo de La Figa",
        sub_agents=[
            trend_scout_agent(),
            content_writer_agent(),
            fase_publicacion,
        ]
    )

    return pipeline


def build_chatbot():
    """Pipeline independiente para el chatbot de lectores."""
    return reader_chatbot_agent()


if __name__ == "__main__":
    # Puedes cambiar la localización aquí
    run_editorial_pipeline(location="Madrid", auto_select=False)
