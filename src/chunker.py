import nltk
from nltk.tokenize import sent_tokenize
from helpers.utils import load_config, get_project_root, config, cache_dir


nltk.data.path.append(str(cache_dir))
nltk.download("punkt_tab", download_dir=cache_dir)


def chunk_text(text: str, window_size: int = config["chunking"]["window_size"]) -> list[str]:
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
