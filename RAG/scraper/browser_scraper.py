from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

# Output folder
DATA_DIR = "data/browser_html"
os.makedirs(DATA_DIR, exist_ok=True)

def save_html(url, idx):
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load (increase if needed)
        html = driver.page_source
        filename = os.path.join(DATA_DIR, f'browser_{idx}.html')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Saved browser HTML: {filename}")
    except Exception as e:
        print(f"❌ Failed to fetch with browser: {url}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage: replace with your target URLs
    urls = [
        "https://www.godaddy.com/websites/website-builder?isc=pwugc&utm_source=wsb&utm_medium=applications&utm_campaign=en-ca_corp_applications_base"
    ]
    for i, url in enumerate(urls, 1):
        save_html(url, i)
