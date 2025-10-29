import nltk
from nltk.tokenize import sent_tokenize
import os

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def chunk_text(input_path="data/loaded_data/data.txt", output_folder="data/chunked_data/chunked_texts.txt"):

    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return []

    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sentences = sent_tokenize(text)

    chunks = []
    for i in range(len(sentences)-1):
        chunk = sentences[i] + " " + sentences[i + 1]
        chunks.append(chunk)

        os.makedirs(os.path.dirname(output_folder), exist_ok=True)

    with open(output_folder, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks, 1):
            f.write(f"Chunk {idx}:\n{chunk}\n\n")

        print(f"Created {len(chunks)} chunks and saved to {output_folder}")
        return chunks
