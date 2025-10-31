import pandas as pd
from pathlib import Path

def load_excel(file_path: str) -> pd.DataFrame:
    """Load excel and clean text fields."""
    path = Path(file_path)
    if not path.exists():
        raise FileExistsError(f"File not found: {path}")
    
    df = pd.read_excel(path)
    df = df.fillna("").applymap(lambda x: str(x).replace("\n", " ").strip())

    print(f"Loaded: {path.name}")
    print(f"Rows: {len(df)} , Columns: {list(df.columns)}")
    return df