import re
import os
import pandas as pd
from io import StringIO
from fuzzywuzzy import process
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging
logging.basicConfig(filename="logs/ocr_debug.log", level=logging.INFO)

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_tables_from_markdown(md_text):
    table_blocks = re.findall(r'(\|.+\|\n\|[-| ]+\|(?:\n\|.+\|)+)', md_text)
    tables = []
    for block in table_blocks:
        try:
            clean_block = block.replace('\n', '\n')
            df = pd.read_csv(StringIO(clean_block), sep='|', engine='python')
            df = df.dropna(axis=1, how='all')
            df.columns = [c.strip() for c in df.columns]
            df = df[1:]  # Drop header if repeated
            tables.append(df)
        except Exception:
            continue
    return tables

def normalize_table_structure(df):
    try:
        df.columns = [str(c).strip() if c else f"col_{i}" for i, c in enumerate(df.columns)]
        df = df.dropna(how="all")
        df.fillna("", inplace=True)
    except Exception as e:
        logging.warning(f"Normalization failed: {e}")
    return df

def fuzzy_match_column(table, target):
    best_col, score = process.extractOne(target, table.columns)
    return best_col if score > 70 else None


def search_tables_for_range(tables, column_name, value):
    matching_rows = []
    for table in tables:
        if column_name in table.columns:
            try:
                table[column_name] = pd.to_numeric(table[column_name], errors='coerce')
                rows = table[(table[column_name] >= value - 2) & (table[column_name] <= value + 2)]
                matching_rows.append(rows)
            except:
                continue
    return pd.concat(matching_rows) if matching_rows else None

def embed_table_rows(tables):
    texts, metadata = [], []
    for i, table in enumerate(tables):
        for _, row in table.iterrows():
            row_text = " | ".join(str(val) for val in row.values)
            texts.append(row_text)
            metadata.append({"table_idx": i})
    embeddings = model.encode(texts)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, texts, metadata

def semantic_table_search(query, index, texts, metadata, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    results = [texts[i] for i in I[0]]
    return results