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
- Extend `build_rag.py` to implement your RAG logic using libraries like LangChain, LlamaIndex, etc.

---

For any questions or improvements, feel free to contribute or open an issue.
