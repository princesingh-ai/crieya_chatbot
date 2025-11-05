import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from helpers.utils import config, input_path

collection_name = "problem_statement_chunks"

# Model settings

embedding_config = config["embedding"]
text_column = embedding_config["text_column"]
model_name = embedding_config["model_name"]
batch_size = int(embedding_config.get("batch_size"))

# Select GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer, model
print(f"Loading model: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
model.eval()

# Load chunked data
df = pd.read_csv(input_path)
texts = df[text_column].astype(str).tolist()
chunk_ids = df["chunk_id"].tolist()
print(f"Loaded {len(texts)} texts from {input_path.name}")


# Mean pooling : converts token level embeddings -> one sentence level embeddings
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# This: Tokenizes the text, Runs it through the transformer, Applies mean_pooing(), Normalizes the result, and Returns embeddings as numpy arrays
def encode(texts):
    tokenized_input = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512).to(device)

    with torch.no_grad():
        model_output = model(**tokenized_input, return_dict=True)

    emb = mean_pooling(model_output, tokenized_input["attention_mask"])
    return emb.cpu().numpy()


# Qdrant Setup
client = QdrantClient(path=str(project_root / "qdrant_db"))  # Local qdrant store
dim = model.config.hidden_size

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
)

print("Generating embeddings and uploding to Qdrant....")

for i in tqdm(range(0, len(texts), batch_size), desc="Embedding to Qdrant"):
    batch_texts = texts[i : i + batch_size]
    batch_ids = chunk_ids[i : i + batch_size]
    batch_embs = encode(batch_texts)

    points = [
        PointStruct(id=int(cid), vector=vec.tolist(), payload={"chunk_id": int(cid), "text": text})
        for cid, vec, text in zip(batch_ids, batch_embs, batch_texts)
    ]

    client.upsert(collection_name=collection_name, points=points)
print(f"✅ Successfully stored {len(texts)} embeddings in Qdrant ({collection_name})")
