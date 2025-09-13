"""Stage 2 — Chunking & metadata

Reads `data/processed/documents.jsonl` and emits `data/chunks/chunks.jsonl` with
overlapping chunks and metadata per chunk.
"""

import json
from pathlib import Path
import uuid


# Try to import chunking config and data paths, fallback to defaults if not found
try:
    import sys
    import importlib.util
    config_path = Path(__file__).resolve().parents[1] / 'config.py'
    spec = importlib.util.spec_from_file_location('config', str(config_path))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    CHUNK_SIZE = getattr(config, 'CHUNK_SIZE', 2000)
    CHUNK_OVERLAP = getattr(config, 'CHUNK_OVERLAP', 200)
    DATA_DIR = Path(getattr(config, 'DATA_DIR', Path(__file__).resolve().parents[1] / 'data'))
    PROCESSED_DIR = Path(getattr(config, 'PROCESSED_DIR', DATA_DIR / 'processed'))
except Exception:
    CHUNK_SIZE = 2000
    CHUNK_OVERLAP = 200
    DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
    PROCESSED_DIR = DATA_DIR / 'processed'


INPUT = PROCESSED_DIR / 'documents.jsonl'
OUT_DIR = DATA_DIR / 'chunks'
OUT_DIR.mkdir(parents=True, exist_ok=True)



def split_text(text: str, max_chars: int = None, overlap: int = None):
    # naive split on chars; replace with sentence-aware splitter if needed
    if max_chars is None:
        max_chars = CHUNK_SIZE
    if overlap is None:
        overlap = CHUNK_OVERLAP
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + max_chars, L)
        chunks.append(text[start:end])
        start = end - overlap if end < L else end
    return chunks


def run():
    if not INPUT.exists():
        print('Input not found:', INPUT)
        return
    out_path = OUT_DIR / 'chunks.jsonl'
    with out_path.open('w', encoding='utf8') as fout:
        for line in INPUT.read_text(encoding='utf8').splitlines():
            doc = json.loads(line)
            chunks = split_text(doc['text'])
            for i, c in enumerate(chunks):
                chunk_id = f"{doc['id']}_{i}_{uuid.uuid4().hex[:6]}"
                payload = {
                    'chunk_id': chunk_id,
                    'text': c,
                    'metadata': {**doc['metadata'], 'parent_id': doc['id'], 'chunk_index': i}
                }
                fout.write(json.dumps(payload, ensure_ascii=False) + '\n')
    print('Wrote', out_path)


if __name__ == '__main__':
    run()
