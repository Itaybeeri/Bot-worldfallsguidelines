"""Stage 3 — Embedding generation

Reads `data/chunks/chunks.jsonl`, produces a numpy .npz with embeddings and a
metadata JSONL for mapping ids -> metadata. By default this uses sentence-transformers
local model if available. Replace with OpenAI calls if desired.
"""

import json
from pathlib import Path
import numpy as np

# Try to import config for paths and model, fallback to defaults if not found
try:
    import sys
    import importlib.util
    config_path = Path(__file__).resolve().parents[1] / 'config.py'
    spec = importlib.util.spec_from_file_location('config', str(config_path))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    DATA_DIR = Path(getattr(config, 'DATA_DIR', Path(__file__).resolve().parents[1] / 'data'))
    CHUNKS_DIR = DATA_DIR / 'chunks'
    EMB_DIR = DATA_DIR / 'embeddings'
    MODEL_NAME = getattr(config, 'EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    BATCH_SIZE = getattr(config, 'EMBEDDING_BATCH_SIZE', 32)
except Exception:
    DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
    CHUNKS_DIR = DATA_DIR / 'chunks'
    EMB_DIR = DATA_DIR / 'embeddings'
    MODEL_NAME = 'all-MiniLM-L6-v2'
    BATCH_SIZE = 32

INPUT = CHUNKS_DIR / 'chunks.jsonl'
EMB_DIR.mkdir(parents=True, exist_ok=True)

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


def load_chunks():
    if not INPUT.exists():
        print('No chunks at', INPUT)
        return []
    return [json.loads(l) for l in INPUT.read_text(encoding='utf8').splitlines()]




def embed_chunks(chunks, model_name=None, batch_size=None):
    texts = [c['text'] for c in chunks]
    if SentenceTransformer is None:
        raise RuntimeError('sentence-transformers not installed; please install it to run local embeddings')
    if model_name is None:
        model_name = MODEL_NAME
    if batch_size is None:
        batch_size = BATCH_SIZE
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=batch_size)
    return embeddings




def run():
    chunks = load_chunks()
    if not chunks:
        return
    embs = embed_chunks(chunks)
    ids = [c['chunk_id'] for c in chunks]
    np.savez_compressed(EMB_DIR / 'embeddings.npz', ids=ids, embeddings=embs)
    # write metadata mapping (include chunk text for RAG retrieval)
    meta_path = EMB_DIR / 'metadata.jsonl'
    with meta_path.open('w', encoding='utf8') as fout:
        for c in chunks:
            out = {
                'chunk_id': c['chunk_id'],
                'metadata': {**c['metadata'], 'text': c['text']}
            }
            fout.write(json.dumps(out, ensure_ascii=False) + '\n')
    print('Saved embeddings to', EMB_DIR)


if __name__ == '__main__':
    run()
