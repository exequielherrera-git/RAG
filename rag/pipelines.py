import logging
from rag.ingest import main as ingest_main
from rag.store_faiss import build_faiss_index
from rag.generator import TicketAnswerGenerator

logger = logging.getLogger(__name__)

def build_index():
    """
    Orquesta la construcción completa del índice:
    1. Ingesta y procesamiento de tickets JSON
    2. Generación de embeddings
    3. Creación/actualización del índice FAISS
    """
    logger.info("Iniciando construcción del índice...")
    ingest_main()              # Procesa los JSON en data/raw/
    build_faiss_index()        # Crea o actualiza el índice FAISS
    logger.info("Índice construido exitosamente.")


def answer_query(query: str):
    """
    Ejecuta el flujo completo de recuperación y generación:
    - Busca los chunks relevantes
    - Genera una respuesta natural
    """
    logger.info(f"Consultando RAG con: {query}")
    generator = TicketAnswerGenerator()
    answer = generator.generate_answer(query)
    logger.info("Respuesta generada.")
    return answer


if __name__ == "__main__":
    # Ejemplo rápido para probar
    q = input("Ingresá tu pregunta: ")
    print(answer_query(q))
