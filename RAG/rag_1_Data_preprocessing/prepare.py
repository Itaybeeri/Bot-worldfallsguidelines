"""Stage 1 — Data preprocessing

Normalize scraped files under ../data/ into cleaned text documents
with metadata and write them to ../data/processed/ (JSONL).
"""


import json
from pathlib import Path

import os
from config import DATA_DIR, PROCESSED_DIR

import pdfplumber


# Always resolve output to the RAG/data/processed directory
rag_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
output_dir = rag_dir / 'data' / 'processed'
output_dir.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [page.extract_text() or '' for page in pdf.pages]
        return '\n'.join(pages)
    except Exception as e:
        print(f"Failed to extract text from PDF {pdf_path}: {e}")
        return ''

def preprocess_document(path: Path) -> dict:
    """Return a dict with keys: id, title, text, metadata"""
    if path.suffix.lower() == '.pdf':
        text = extract_text_from_pdf(path)
    else:
        text = path.read_text(encoding='utf8', errors='ignore')
    # Very small example normalizations — replace with robust cleaning
    clean = ' '.join(line.strip() for line in text.splitlines() if line.strip())
    doc_id = path.stem
    metadata = {
        'source_path': str(path.relative_to(Path(DATA_DIR))),
        'file_name': path.name,
    }
    return {'id': doc_id, 'title': path.stem, 'text': clean, 'metadata': metadata}

def run_once():
    # Load forbidden and captcha file lists
    forbidden_path = Path(DATA_DIR) / 'forbidden_files.txt'
    captcha_path = Path(DATA_DIR) / 'captcha_files.txt'
    forbidden_files = set()
    captcha_files = set()
    if forbidden_path.exists():
        with open(forbidden_path, encoding='utf8') as f:
            for line in f:
                fname = line.split('\t')[0].strip()
                if fname:
                    forbidden_files.add(fname)
    if captcha_path.exists():
        with open(captcha_path, encoding='utf8') as f:
            for line in f:
                fname = line.split('\t')[0].strip()
                if fname:
                    captcha_files.add(fname)

    # Recursively find all .txt and .pdf files in DATA_DIR and subfolders
    all_files = list(Path(DATA_DIR).rglob('*.txt')) + list(Path(DATA_DIR).rglob('*.pdf'))
    # Exclude forbidden_files.txt and captcha_files.txt themselves
    skip_names = {'forbidden_files.txt', 'captcha_files.txt'}
    if not all_files:
        print('No .txt or .pdf files found in', DATA_DIR)
        return
    out_path = output_dir / 'documents.jsonl'
    with out_path.open('w', encoding='utf8') as fout:
        for p in all_files:
            if p.name in forbidden_files or p.name in captcha_files or p.name in skip_names:
                print(f"Skipping forbidden/captcha file: {p.name}")
                continue
            doc = preprocess_document(p)
            fout.write(json.dumps(doc, ensure_ascii=False) + '\n')
    print('Wrote', out_path)


if __name__ == '__main__':
    run_once()
