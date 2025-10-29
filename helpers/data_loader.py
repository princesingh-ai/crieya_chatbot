import pandas as pd
import glob
import os

def load_excel_data(folder_path: str = "data/raw_data") -> list[str]:
    """Loads and returns text data from all Excel files in the specified folder."""
    texts = []
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

    if not excel_files:
        print(f"No Excel files found in : {folder_path}")
        return []
    
    for file in excel_files:
        print(f"Loading file: {os.path.basename(file)}")
        df = pd.read_excel(file)

        for i, row in df.iterrows():
            row_text = " ".join([str(cell) for cell in row if pd.notnull(cell)])
            texts.append(row_text)
    print(f"loaded {len(excel_files)} Excel files, total {len(texts)} text entries.")
    return texts

def save_to_text(texts: list[str], output_path: str = "./data/loaded_data/data.txt") -> None:
    """Saves the list of texts to a single text file."""
    full_text = "\n".join(texts)
    os.makedirs(os.path.dirname(output_path), exist_ok= True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Saved combined data to {output_path}")