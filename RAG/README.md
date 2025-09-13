# RAG vector pipeline (staged)

**Note:** This folder is only for building and updating the vector database (ChromaDB or FAISS) from your data. It does not contain any chatbot or LLM code. To build a chatbot or run LLM queries, use a separate folder/project that queries the vector DB built here.

## Pipeline Stages

- **0. Scraping (`rag_0_Scraper`)**

  - `scraper.py` downloads all HTML and PDF content from worldfallsguidelines.com using Selenium and undetected-chromedriver.
  - All raw files are saved in the `data/` folder (HTML in `browser_text/`, PDFs in `browser_pdf/`).
  - No files are modified or deleted; only new files are added.

- **1. Data Preprocessing (`rag_1_Data_preprocessing`)**

  - `prepare.py` recursively scans all `.txt` and `.pdf` files in the `data/` folder and subfolders.
  - For `.txt` files: reads and normalizes the text.
  - For `.pdf` files: extracts text using `pdfplumber` and normalizes it.
  - Adds metadata (source path, file name) to each document.
  - Outputs a single `documents.jsonl` file in `data/processed/`, containing one JSON object per document.

- `2_Chunking` — chunker.py
- `3_Embeddings` — embed.py
- `4_VectorDB_ingest` — ingest_qdrant.py
- `5_Index_tuning` — notes
- `6_Retrieval` — retriever.py
- `7_RAG_integration` — run_rag.py
- `8_Monitoring` — notes

## Using ChromaDB as your vector DB

- Embeddings and metadata are ingested into ChromaDB with `4_VectorDB_ingest/ingest_chroma.py`.
- The vector DB and all metadata are stored in `data/chroma_db/` (local folder, safe to delete/rebuild).
- Retrieval is done with `6_Retrieval/chroma_retriever.py`.

To install all dependencies:

```sh
pip install -r requirements.txt
```

To ingest into ChromaDB:

```sh
python rag/4_VectorDB_ingest/ingest_chroma.py
```

To retrieve (example):

```sh
python rag/6_Retrieval/chroma_retriever.py
```

# RAG Project for worldfallsguidelines.com

This project implements a Retrieval-Augmented Generation (RAG) pipeline that scrapes all data (HTML and publications) from [worldfallsguidelines.com](https://worldfallsguidelines.com), processes the data, and prepares it for use in a RAG system.

## Project Structure

- `config.py` — Stores all configuration parameters (website URL, data paths, etc.)
- `scraper.py` — Downloads all HTML and PDF content from the website
- `process_pdf.py` — Extracts text from downloaded PDFs
- `process_html.py` — Extracts and cleans text from HTML files
- `build_rag.py` — Placeholder for building the RAG pipeline using processed data
- `requirements.txt` — Python dependencies
- `data/` — Folder containing all downloaded and processed data

## Setup Instructions

1. **Clone the repository** (if needed):

   ```sh
   git clone <repo-url>
   cd RAG
   ```

2. **Create a Python virtual environment:**

   ```sh
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # On Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the pipeline:**
   - Scrape the website:
     ```sh
     python scraper.py
     ```
   - Process PDFs:
     ```sh
     python process_pdf.py
     ```
   - Process HTML files:
     ```sh
     python process_html.py
     ```
   - Build the RAG pipeline:
     ```sh
     python build_rag.py
     ```

## Notes

- All parameters (such as the website URL and data paths) are set in `config.py`.
- The scripts are modular; you can run each step independently from the terminal.
- **Chatbot/LLM logic is not included here.**

  ***

For any questions or improvements, feel free to contribute or open an issue.
