import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt", quiet=True)

def chunk_text(text: str, window_size: int = 2) -> list[str]:
    """Chunk text into overlapping windows of sentences."""
    sentences = sent_tokenize(text)
    chunks = []

    if not sentences:
        return chunks
    
    for i in range(len(sentences) - window_size + 1):
        chunk = " ".join(sentences[i : i + window_size])
        chunks.append(chunk.strip())

    if not chunks and sentences:
        chunks.append(sentences[0])
    
    return chunks