import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from tqdm import tqdm
import faiss
import json
from helpers.utils import config, chunks_path, output_dir, mapping_path

# Model settings
embedding_config = config["embedding"]
text_column = embedding_config["text_column"]
model_name = embedding_config["model_name"]
batch_size = int(embedding_config.get("batch_size"))

# retrieval settings 
retrieval = config["retrieval"]
k = retrieval["top_k"]

# Select GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer, model
print(f"Loading model: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
model.eval()

# Load chunked data
df = pd.read_csv(chunks_path)
texts = df[text_column].astype(str).tolist()
chunk_ids = df["chunk_id"].tolist()
print(f"✅ Loaded {len(texts)} texts from {chunks_path.name}")


# Mean pooling : converts token level embeddings -> one sentence level embeddings
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# This: Tokenizes the text, Runs it through the transformer, Applies mean_pooing(), and Returns embeddings as numpy arrays
def tokenize(texts):
    tokenized_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512).to(device)

    with torch.no_grad():
        model_output = model(**tokenized_input, return_dict=True)

    emb = mean_pooling(model_output, tokenized_input["attention_mask"])
    return emb.cpu().numpy()

print("\nGenerating embeddings...")
embeddings = []
for i in tqdm(range(0, len(texts), batch_size)):
    batch_texts = texts[i:i + batch_size]
    batch_embeddings = tokenize(batch_texts)
    embeddings.extend(batch_embeddings)

embeddings = np.array(embeddings).astype("float32")
print(f"✅ Generated embeddings with shape: {embeddings.shape}")

vector_size = embeddings.shape[1]
faiss_index = faiss.IndexFlatIP(vector_size)
faiss_index.add(embeddings)
print(f"✅ FAISS index created with {faiss_index.ntotal} vectors.")

faiss_index_path = output_dir / "embeddings.index"
faiss.write_index(faiss_index, str(faiss_index_path))
print(f"✅ FAISS index saved to: {faiss_index_path}")

index_to_chunk_id = {i: cid for i, cid in enumerate(chunk_ids)}
with open(mapping_path, "w") as f:
    json.dump(index_to_chunk_id, f)

print(f"✅ Chunk id mapping created successfully")
print(f"✅ Chunk id mapping save to: {mapping_path}")

def search(query, k):
    query_emb = tokenize([query])
    query_emb = np.array(query_emb)
    distances, indices = faiss_index.search(query_emb, k)

    results = []
    for rank, idx in enumerate(indices[0]):
        chunk_id = index_to_chunk_id[idx]
        chunk_row = df.loc[df["chunk_id"] == chunk_id]
        chunk_text = chunk_row["chunk_text"].values[0] if not chunk_row.empty else "[Missing chunk]"
        results.append({
            "rank": rank + 1,
            "chunk_id": chunk_id,
            "score": float(distances[0][rank]),
            "text": chunk_text
        })
    return results

if __name__ == "__main__":
    print("\nType your query (or 'exit' to quit):")
    while True:
        query = input("\nQuery: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Exiting retriever.")
            break

        top_results = search(query, k)
        print(f"\nTop {len(top_results)} results for: {query}\n")
        for r in top_results:
            print(f"Rank {r['rank']} | Chunk ID: {r['chunk_id']} | Score: {r['score']:.4f}")
            print(r["text"][:400], "...\n")