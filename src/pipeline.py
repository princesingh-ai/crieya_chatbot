from helpers.data_loader import load_excel_data, save_to_text
from src.chunker import chunk_text

texts = load_excel_data("data/raw_data")
save_to_text(texts)

chunk_text("data/loaded_data/data.txt", "data/chunked_data/chunked_texts.txt")