import os
from bs4 import BeautifulSoup
from scraper.config import HTML_DIR, PROCESSED_DIR

os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_text_from_html():
    for filename in os.listdir(HTML_DIR):
        if filename.lower().endswith('.html'):
            html_path = os.path.join(HTML_DIR, filename)
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
            out_path = os.path.join(PROCESSED_DIR, filename + '.txt')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)

if __name__ == "__main__":
    extract_text_from_html()
