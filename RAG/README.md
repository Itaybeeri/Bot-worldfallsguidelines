# World Falls Guidelines RAG Pipeline

This folder contains everything needed to build the knowledge base (vector database) for the World Falls Guidelines chatbot. You only need to run this pipeline once, or whenever the source data changes. It builds a local vector database on your computer that the chatbot will use to answer questions.

---

## How to Run (One-Time Setup)

### Easiest: Run the full pipeline with one command

If you're on Windows, you can run the entire process automatically:

```powershell
./run_all.ps1
```

This script will create a virtual environment, install all requirements, and run every stage in order. When it finishes, your local vector database will be ready in the `data/` folder.

### Manual: Run each stage yourself

If you prefer, you can run each step manually:

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run each stage in order:**
   - Scrape the website and download all PDFs:
     ```sh
     python scraper.py
     ```
   - Process the downloaded PDFs:
     ```sh
     python process_pdf.py
     ```
   - Process the downloaded HTML files:
     ```sh
     python process_html.py
     ```
   - Build the RAG pipeline (chunking, embeddings, vector DB):
     ```sh
     python build_rag.py
     ```

You do not need to run these steps again unless you want to update the knowledge base with new data.

---

## What does each step do?

1. **Scraping** (`scraper.py`)

   - Downloads all HTML and PDF content from the official World Falls Guidelines website.
   - Saves raw files in the `data/` folder (HTML in `browser_text/`, PDFs in `browser_pdf/`).

2. **PDF Processing** (`process_pdf.py`)

   - Extracts and normalizes text from all downloaded PDF files.
   - Adds metadata (source path, file name) to each document.

3. **HTML Processing** (`process_html.py`)

   - Extracts and cleans text from all downloaded HTML files.
   - Adds metadata for each document.

4. **RAG Pipeline Build** (`build_rag.py`)
   - Chunks the processed documents into smaller pieces.
   - Generates embeddings for each chunk.
   - Ingests all chunks and embeddings into a local vector database (ChromaDB or FAISS).

---

## Notes

- All configuration (such as website URL and data paths) is set in `config.py`.
- The scripts are modular; you can run each step independently if needed.
- This folder does **not** contain the chatbot code—see the main project or `ChatBot/README.md` for that.

---

_For any questions or improvements, feel free to contribute or open an issue._
