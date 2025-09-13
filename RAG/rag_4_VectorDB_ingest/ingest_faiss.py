"""Stage 4 — Vector DB ingestion (FAISS)

Reads embeddings and metadata, builds a FAISS index, and saves it to disk in data/vector_index/.
"""
import json
from pathlib import Path
import numpy as np
import faiss

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / 'data'
EMB_DIR = DATA_DIR / 'embeddings'
INDEX_DIR = DATA_DIR / 'vector_index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)


def run():
    npz = np.load(EMB_DIR / 'embeddings.npz', allow_pickle=True)
    ids = list(npz['ids'])
    vectors = npz['embeddings']
    dim = vectors.shape[1]
    # Build FAISS index (L2 or cosine)
    index = faiss.IndexFlatL2(dim)
    index.add(vectors.astype(np.float32))
    faiss.write_index(index, str(INDEX_DIR / 'faiss_index.faiss'))
    # Save mapping from FAISS index to chunk_id and metadata
    meta_path = EMB_DIR / 'metadata.jsonl'
    metas = [json.loads(l) for l in meta_path.read_text(encoding='utf8').splitlines()]
    with (INDEX_DIR / 'faiss_metadata.jsonl').open('w', encoding='utf8') as fout:
        for i, chunk_id in enumerate(ids):
            meta = next((m['metadata'] for m in metas if m['chunk_id'] == chunk_id), {})
            fout.write(json.dumps({'faiss_idx': i, 'chunk_id': chunk_id, 'metadata': meta}, ensure_ascii=False) + '\n')
    print('Saved FAISS index and metadata to', INDEX_DIR)


if __name__ == '__main__':
    run()
