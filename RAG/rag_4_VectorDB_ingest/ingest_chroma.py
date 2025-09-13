"""Stage 4 — Vector DB ingestion (ChromaDB)

Reads embeddings and metadata, upserts into a ChromaDB collection in data/chroma_db/.
"""
import json
from pathlib import Path
import numpy as np
import chromadb
from chromadb.config import Settings

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / 'data'
EMB_DIR = DATA_DIR / 'embeddings'
CHROMA_DIR = DATA_DIR / 'chroma_db'
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

def run():
    npz = np.load(EMB_DIR / 'embeddings.npz', allow_pickle=True)
    ids = list(npz['ids'])
    vectors = npz['embeddings']
    meta_path = EMB_DIR / 'metadata.jsonl'
    metas = [json.loads(l) for l in meta_path.read_text(encoding='utf8').splitlines()]
    metadict = {m['chunk_id']: m['metadata'] for m in metas}

    client = chromadb.Client(Settings(persist_directory=str(CHROMA_DIR)))
    collection = client.get_or_create_collection('worldfallsguidelines')
    # Chroma expects str ids and dict metadata
    collection.add(
        ids=[str(i) for i in ids],
        embeddings=vectors.tolist(),
        metadatas=[metadict.get(i, {}) for i in ids],
    )
    client.persist()
    print('Upserted', len(ids), 'vectors to ChromaDB at', CHROMA_DIR)

if __name__ == '__main__':
    run()
