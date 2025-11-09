from sentence_transformers import SentenceTransformer
import numpy as np
from rag.utils import setup_logger

logger = setup_logger("embeddings")

class Embedder:
    """
    Crea embeddings (vectores numéricos) a partir de texto.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f"Cargando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size: int = 32):
        """
        Convierte uno o varios textos en embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # normaliza para búsquedas más precisas
        )
        return np.array(embeddings)
