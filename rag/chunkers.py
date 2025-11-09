from typing import List, Dict

def chunk_text(text: str, max_words: int = 300, overlap: int = 50) -> List[Dict]:
    """
    Divide el texto en fragmentos ("chunks") con solapamiento para preservar contexto.
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    start = 0
    total_words = len(words)

    while start < total_words:
        end = min(start + max_words, total_words)
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "content": chunk_text,
            "start_word": start,
            "end_word": end
        })

        # Avanzar con solapamiento (para no cortar frases importantes)
        start += max_words - overlap

        if start >= total_words:
            break

    return chunks
