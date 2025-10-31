import pandas as pd
from pathlib import Path
from helpers.data_loader import load_excel
from src.chunker import chunk_text
from helpers.utils import load_config

def process_excel(config_path: str = "config.yaml"):
    # --- Load configuration ---
    config = load_config(config_path)
    print("\nDEBUG CONFIG:", config, "\n")

    paths = config["paths"]
    chunk_config = config["chunking"]      # ✅ FIXED
    output_config = config["output"]       # ✅ FIXED

    # --- Extract parameters ---
    input_path = Path(paths["input_file"])
    output_dir = Path(paths["output_dir"])
    target_col = chunk_config["target_column"]
    window_size = int(chunk_config["window_size"])

    # --- Load data ---
    df = load_excel(input_path)
    file_name = input_path.name

    metadata_rows, chunk_rows = [], []

    # --- Process each row ---
    for _, row in df.iterrows():
        text = str(row.get(target_col, "")).strip()
        if not text:
            continue

        chunks = chunk_text(text, window_size)
        for chunk_id, chunk in enumerate(chunks):
            metadata_rows.append({
                "file_name": file_name,
                "id": row.get("ID", None),
                "column_name": target_col,
                "chunk_id": chunk_id,
            })
            chunk_rows.append({
                "file_name": file_name,
                "id": row.get("ID", None),
                "chunk_text": chunk,
                "chunk_id": chunk_id,
            })

    # --- Save results ---
    output_dir.mkdir(parents=True, exist_ok=True)  # ✅ FIXED
    pd.DataFrame(metadata_rows).to_csv(output_dir / output_config["metadata_file"], index=False)
    pd.DataFrame(chunk_rows).to_csv(output_dir / output_config["chunks_file"], index=False)  # ✅ FIXED

    print(f"✅ Saved {len(chunk_rows)} chunks to {output_dir / output_config['chunks_file']}")
    print(f"✅ Saved metadata to {output_dir / output_config['metadata_file']}")

if __name__ == "__main__":
    process_excel()