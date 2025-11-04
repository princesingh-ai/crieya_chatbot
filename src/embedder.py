import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from tqdm import tqdm
from helpers.utils import load_config, get_project_root

# Load configurations and Paths
config = load_config()
project_root = get_project_root()
paths = config["paths"]
embedding_conf = config["embedding"]

input_path = project_root / paths["output_dir"] / paths["chunks_file"]
output_dir = project_root / paths["output_dir"]
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / embedding_conf["output_file"]
# Model settings
text_column = embedding_conf["text_column"]
model_name = embedding_conf["model_name"]
batch_size = embedding_conf.get("batch_size")

# Select GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer, model
print(f"Loading model: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
model.eval()

# Load chunked data
df = pd.read_excel(input_path) if str(input_path).endswith(".xlsx") else pd.read_csv(input_path)
texts = df[text_column].astype(str).tolist()
chunk_ids = df["chunk_id"].tolist()
print(f"Loaded {len(texts)} texts from {input_path.name}")

# Mean pooling : converts token level embeddings -> one sentence level embeddings
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )

# This: Tokenizes the text, Runs it through the transformer, Applies mean_pooing(), Normalizes the result, and Returns embeddings as numpy arrays
def encode(texts):
    if isinstance(texts, str):
        texts = [texts]
        
    encoded_input = tokenizer(
        texts, padding=True, truncation=True, return_tensors="pt", max_length=512).to(device)
    
    with torch.no_grad():
        model_output = model(**encoded_input, return_dict=True)
    
    emb = mean_pooling(model_output, encoded_input["attention_mask"])
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    return emb.cpu().numpy()

# Encode all chunks in batches
all_embeddings = []
for i in tqdm(range(0, len(texts), batch_size), desc="Embedding chunks"):
    batch_texts = texts[i : i + batch_size]
    batch_embs = encode(batch_texts)
    all_embeddings.append(batch_embs)

# combines all batches and saves it
embeddings = np.vstack(all_embeddings)
print(f"✅ Generated embeddings shape: {embeddings.shape}")

emb_df = pd.DataFrame({
    "chunk_id" : chunk_ids,
    "embedding" : [",".join(map(str, emb)) for emb in embeddings],
})

emb_df.to_csv(output_file, index=False)
print(f"✅ Embeddings saved to: {output_file}")