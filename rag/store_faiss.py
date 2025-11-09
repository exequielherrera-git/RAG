import os
import json
import numpy as np
import faiss
from rag.embeddings import Embedder
from rag.utils import setup_logger, ensure_dirs

logger = setup_logger("faiss_store")

def build_faiss_index(
    processed_path: str = "data/processed/tickets_processed.jsonl",
    index_dir: str = "index/faiss"
):
    """
    Lee los chunks procesados, genera embeddings y crea el índice FAISS.
    """
    ensure_dirs()
    os.makedirs(index_dir, exist_ok=True)

    if not os.path.exists(processed_path):
        logger.error(f"No se encontró el archivo {processed_path}.")
        return

    # Leer todos los chunks
    texts, metadatas = [], []
    logger.info(f"Leyendo chunks desde {processed_path}...")
    with open(processed_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            texts.append(record["content"])
            metadatas.append({
                "ticket_id": record["ticket_id"],
                "chunk_id": record["chunk_id"],
                "content": record["content"], 
                "project": record.get("project"),
                "category": record.get("category"),
                "status": record.get("status"),
                "created_at": record.get("created_at")
            })

    if not texts:
        logger.warning("No se encontraron chunks para procesar.")
        return

    # Crear embeddings
    embedder = Embedder()
    logger.info(f"Generando embeddings para {len(texts)} chunks...")
    embeddings = embedder.encode(texts).astype("float32")

    dim = embeddings.shape[1]
    logger.info(f"Creando índice FAISS (dim={dim})...")
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)  # type: ignore

    # Guardar índice y metadatos
    faiss.write_index(index, os.path.join(index_dir, "tickets.index"))
    np.save(os.path.join(index_dir, "metadatas.npy"), np.array(metadatas, dtype=object))

    # Guardar los embeddings como .npy
    np.save(os.path.join(index_dir, "embeddings.npy"), embeddings)
    
    logger.info(f"Índice FAISS creado y guardado en {index_dir}")
    logger.info(f"Cantidad de vectores indexados: {index.ntotal}")
    logger.info(f"Embeddings guardados en {index_dir}/embeddings.npy")
    return index


if __name__ == "__main__":
    build_faiss_index()