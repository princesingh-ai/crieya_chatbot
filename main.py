import pandas as pd
from pathlib import Path
from helpers.data_loader import load_excel
from src.chunker import chunk_text
from helpers.utils import load_config

# Load configuration
config = load_config()
config_paths = config["paths"]
chunk_config = config["chunking"]
output_config = config["output"]

input_path = Path(config_paths["input_file"])
output_dir = Path(config_paths["output_dir"])
target_columns = chunk_config["target_columns"]
window_size = int(chunk_config["window_size"])


def process_excel(input_path=input_path):
    # Load data
    df = load_excel(input_path)
    file_name = input_path.name
    chunk_rows = []

    # Process each row
    for _, row in df.iterrows():
        for target_col in target_columns:
            text = str(row[target_col]).strip()
            chunks = chunk_text(text, window_size)

            for chunk_id, chunk in enumerate(chunks):
                chunk_rows.append(
                    {
                        "file_name": file_name,
                        "id": row.get("ID", None),
                        "column_name": target_col,
                        "chunk_text": chunk,
                        "chunk_id": chunk_id,
                    }
                )

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / output_config["chunks_file"]
    pd.DataFrame(chunk_rows).to_csv(output_file, index=False)

    print(f"✅ Saved {len(chunk_rows)} chunks to {output_dir / output_config['chunks_file']}")

if __name__ == "__main__":
    process_excel()