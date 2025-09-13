# Configuration parameters for the RAG project

import os

# -------------------
# 0 scraper parameters
# -------------------
WEBSITE_URL = "https://worldfallsguidelines.com"
# Make DATA_DIR relative to the folder containing this config.py (i.e., the RAG folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
# Where downloaded PDFs are stored by the scraper
PDF_DIR = os.path.join(DATA_DIR, "browser_pdf")
# Where downloaded/saved HTML/browser text files are stored
HTML_DIR = os.path.join(DATA_DIR, "browser_text")

# -------------------
# 1 Data preprocessing parameters
# -------------------
# Processed/plain-text output directory used by processing steps
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# -------------------
# 2 Chunking parameters
# -------------------
# Number of characters per chunk
CHUNK_SIZE = 2000
# Number of overlapping characters between chunks
CHUNK_OVERLAP = 200

# -------------------
# 3 Embeddings parameters
# -------------------
# Name of the sentence-transformers model to use for embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Batch size for embedding generation (tune for your GPU/CPU)
EMBEDDING_BATCH_SIZE = 32

# -------------------
# 4 Vector DB ingest parameters
# -------------------
# Type of vector DB to use (currently only 'chroma' is supported)
VECTORDB_TYPE = 'chroma'
# Directory for persistent vector DB storage
VECTORDB_DIR = 'vectordb'
# Collection name (for ChromaDB)
VECTORDB_COLLECTION = 'worldfalls'
