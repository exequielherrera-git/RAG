import logging
import os

def setup_logger(name: str = "rag"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def ensure_dirs():
    # Crea las carpetas necesarias para que el sistema funcione
    for path in ["data/raw", "data/processed", "index/faiss"]:
        os.makedirs(path, exist_ok=True)