# PowerShell script to set up and run the RAG pipeline

python -m venv .venv

# Install requirements
python.exe -m pip install -r requirements.txt

# Run the pipeline steps
python.exe scraper/scraper.py
python.exe scraper/process_pdf.py
python.exe scraper/process_html.py
python.exe build_rag.py
