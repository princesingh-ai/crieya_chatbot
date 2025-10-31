import pandas as pd
from pathlib import Path


def load_excel(file_path):
    """Load excel and clean text fields."""
    path = Path(file_path)

    df = pd.read_excel(path).fillna("")

    print(f"Loaded: {path.name}")
    print(f"Rows: {len(df)} , Columns: {list(df.columns)}")
    return df
