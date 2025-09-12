# Configuration parameters for the RAG project

import os

WEBSITE_URL = "https://worldfallsguidelines.com"

# Make DATA_DIR an absolute path sibling to the `scraper` package directory
# so the `data/` folder lives at the repository root (RAG/data), not inside
# the `scraper/` package when scripts are executed from within that package.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
# Where downloaded PDFs are stored by the scraper
PDF_DIR = os.path.join(DATA_DIR, "browser_pdf")
# Where downloaded/saved HTML/browser text files are stored
HTML_DIR = os.path.join(DATA_DIR, "browser_text")
# Processed/plain-text output directory used by processing steps
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")