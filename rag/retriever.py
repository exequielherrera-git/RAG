import os
import numpy as np
import faiss
from typing import List, Tuple, Dict
from rag.embeddings import Embedder
from rag.utils import setup_logger

logger = setup_logger("retriever")

class TicketRetriever:
    """
    Recuperador semántico basado en FAISS.
    """
    def __init__(
        self,
        index_path: str = "index/faiss/tickets.index",
        metadata_path: str = "index/faiss/metadatas.npy",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"No se encontró el índice FAISS en {index_path}")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"No se encontró el archivo de metadatos en {metadata_path}")

        logger.info("Cargando índice FAISS y metadatos...")
        self.index = faiss.read_index(index_path)
        self.metadatas = np.load(metadata_path, allow_pickle=True)
        self.embedder = Embedder(model_name)

        logger.info(f"Índice cargado: {self.index.ntotal} vectores disponibles.")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Busca los chunks más similares a la consulta.
        Retorna una lista de resultados con score y metadatos.
        """
        logger.info(f"Buscando: '{query}'")

        # Generar embedding del texto de consulta
        query_vec = self.embedder.encode(query).astype("float32")

        # Hacer búsqueda FAISS
        distances, indices = self.index.search(query_vec, top_k)
        indices = indices.flatten()
        distances = distances.flatten()

        results = []
        for idx, score in zip(indices, distances):
            if idx < len(self.metadatas):
                meta = self.metadatas[idx]  # <- FIX: ya es un dict
                meta["score"] = float(score)
                results.append(meta)

        logger.info(f"Se recuperaron {len(results)} resultados.")

        return results

if __name__ == "__main__":
    retriever = TicketRetriever()
    query = input("Escribí tu consulta: ")
    results = retriever.search(query, top_k=3)

    print("\n🔍 Resultados más similares:")
    for i, r in enumerate(results, start=1):
        print(f"\n#{i} [Ticket {r['ticket_id']}] (score={r['score']:.3f})")
        print(f"Proyecto: {r['project']} | Categoría: {r['category']}")
        print(f"Status: {r['status']} | Creado: {r['created_at']}")
