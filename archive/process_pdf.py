import os
import fitz  # PyMuPDF
from scraper.config import PDF_DIR, PROCESSED_DIR

os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_text_from_pdfs():
    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(PDF_DIR, filename)
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            out_path = os.path.join(PROCESSED_DIR, filename + '.txt')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)

if __name__ == "__main__":
    extract_text_from_pdfs()
