import pandas as pd
from pathlib import Path
from helpers.data_loader import load_excel
from src.chunker import chunk_text
from helpers.utils import load_config
from helpers.utils import input_path, chunks_path, config


target_columns = config["chunking"]["target_columns"]
window_size = int(config["chunking"]["window_size"])


def process_excel(input_path=input_path):
    # Load data
    df = load_excel(input_path)
    file_name = input_path.name
    chunk_rows = []
    chunk_id_global = 0

    # Process each row
    for _, row in df.iterrows():
        for target_col in target_columns:
            text = str(row[target_col]).strip()
            chunks = chunk_text(text, window_size)

            for chunk_id, chunk in enumerate(chunks):
                if target_col == "Title":
                    chunk = "Title: " + chunk

                chunk_rows.append(
                    {
                        "file_name": file_name,
                        "id": row.get("ID", None),
                        "column_name": target_col,
                        "chunk_text": chunk,
                        "chunk_id": chunk_id_global,
                    }
                )
                chunk_id_global += 1     

    # Save results
    pd.DataFrame(chunk_rows).to_csv(chunks_path, index=False)

    print(f"✅ Saved {len(chunk_rows)} chunks to {chunks_path}")


if __name__ == "__main__":
    process_excel()
