import os
import json
import shutil
from tqdm import tqdm
from typing import List
from rag.schema import MantisTicket
from rag.chunkers import chunk_text
from rag.utils import setup_logger, ensure_dirs

logger = setup_logger("ingest")

def load_json_files(raw_dir: str = "data/raw") -> List[str]:
    # Devuelve la lista de archivos .json a procesar
    files = [f for f in os.listdir(raw_dir) if f.endswith(".json")]
    return files

def process_tickets(raw_dir: str = "data/raw", output_dir: str = "data/processed", processed_raw_dir: str = "data/processed_raw"):
    """
    Lee archivos JSON desde data/raw/,
    Los valida, los convierte en chunks y exporta a data/processed/tickets_processed.jsonl.
    Luego mueve los archivos procesados a data/processed_raw/.
    """
    ensure_dirs()
    os.makedirs(processed_raw_dir, exist_ok=True)

    files = load_json_files(raw_dir)
    if not files:
        logger.info("No hay nuevos archivos para procesar en data/raw/")
        return

    logger.info(f"{len(files)} archivos encontrados para procesar.")
    output_path = os.path.join(output_dir, "tickets_processed.jsonl")

    with open(output_path, "a", encoding="utf-8") as out:  # modo append por si ya existe
        for file in tqdm(files, desc="Procesando archivos"):
            path = os.path.join(raw_dir, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        data = [data]  # convertir a lista si es un solo ticket

                for item in data:
                    try:
                        ticket = MantisTicket(**item)
                        text = ticket.canonical_text()
                        chunks = chunk_text(text)
                        for idx, ch in enumerate(chunks):
                            record = {
                                "ticket_id": ticket.id,
                                "chunk_id": idx,
                                "content": ch["content"],
                                "start_word": ch["start_word"],
                                "end_word": ch["end_word"],
                                "project": ticket.project.get("name") if ticket.project else None,
                                "category": ticket.category.get("name") if ticket.category else None,
                                "status": ticket.status.get("name") if ticket.status else None,
                                "created_at": str(ticket.created_at) if ticket.created_at else None,
                            }
                            out.write(json.dumps(record, ensure_ascii=False) + "\n")

                    except Exception as e:
                        logger.warning(f"Ticket inválido dentro de {file}: {e}")

                # Mover archivo procesado a processed_raw/
                shutil.move(path, os.path.join(processed_raw_dir, file))
                logger.info(f"Archivo {file} procesado y movido a {processed_raw_dir}/")

            except Exception as e:
                logger.error(f"Error procesando {file}: {e}")

    logger.info(f"Todos los archivos fueron procesados y exportados a {output_path}")
    return output_path


def main():
    """
    Punto de entrada principal del proceso de ingesta.
    """
    process_tickets()


if __name__ == "__main__":
    main()

