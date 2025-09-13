"""Stage 4 — Vector DB Ingest

Reads embeddings and metadata, ingests into a vector database (ChromaDB or FAISS).
Configurable via config.py. Output is a persistent vector DB for chatbot retrieval.
"""
import json
from pathlib import Path
import numpy as np

# Try to import config for paths and vector DB params, fallback to defaults if not found
try:
    import sys
    import importlib.util
    config_path = Path(__file__).resolve().parents[1] / 'config.py'
    spec = importlib.util.spec_from_file_location('config', str(config_path))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    DATA_DIR = Path(getattr(config, 'DATA_DIR', Path(__file__).resolve().parents[1] / 'data'))
    EMB_DIR = DATA_DIR / 'embeddings'
    VECTORDB_DIR = DATA_DIR / getattr(config, 'VECTORDB_DIR', 'vectordb')
    VECTORDB_TYPE = getattr(config, 'VECTORDB_TYPE', 'chroma')  # 'chroma' or 'faiss'
    VECTORDB_COLLECTION = getattr(config, 'VECTORDB_COLLECTION', 'worldfalls')
except Exception:
    DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
    EMB_DIR = DATA_DIR / 'embeddings'
    VECTORDB_DIR = DATA_DIR / 'vectordb'
    VECTORDB_TYPE = 'chroma'
    VECTORDB_COLLECTION = 'worldfalls'

EMB_PATH = EMB_DIR / 'embeddings.npz'
META_PATH = EMB_DIR / 'metadata.jsonl'
VECTORDB_DIR.mkdir(parents=True, exist_ok=True)

# Import ChromaDB only
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

def load_embeddings():
    arr = np.load(EMB_PATH, allow_pickle=True)
    ids = arr['ids']
    embs = arr['embeddings']
    return ids, embs

def load_metadata():
    with open(META_PATH, encoding='utf8') as f:
        return [json.loads(line) for line in f]

def ingest_chroma(ids, embs, metadata):
    if chromadb is None:
        raise ImportError('chromadb not installed. Please install chromadb to use this backend.')
    client = chromadb.PersistentClient(path=str(VECTORDB_DIR), settings=Settings(allow_reset=True))
    if VECTORDB_COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(VECTORDB_COLLECTION)
    collection = client.get_or_create_collection(VECTORDB_COLLECTION)
    # Chroma expects lists
    collection.add(
        ids=[str(i) for i in ids],
        embeddings=embs.tolist(),
        metadatas=[m['metadata'] for m in metadata],
        documents=None
    )
    print(f'Ingested {len(ids)} embeddings into ChromaDB at {VECTORDB_DIR}')



def run():
    ids, embs = load_embeddings()
    metadata = load_metadata()
    ingest_chroma(ids, embs, metadata)

if __name__ == '__main__':
    run()
