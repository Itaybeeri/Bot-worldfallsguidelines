def scrape_url(url, filename_hint=None):
    """Scrape a single URL and save the text and PDFs found."""
    global current_url
    html = get_html_with_browser(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(soup)
    if text.strip():
        current_url = url
        # Use the page title as filename if no hint is provided
        if filename_hint:
            fname = filename_hint
        else:
            title_tag = soup.find('title')
            if title_tag and title_tag.text.strip():
                title = title_tag.text.strip()
            else:
                title = "scraped_single"
            # Sanitize title for filename
            import re
            fname = re.sub(r'[^\w\-_\. ]', '_', title)[:80] + ".txt"
        save_text(fname, text)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            pdf_url = urljoin(url, href)
            save_pdf(pdf_url)

import os
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
try:
    # When run as a package (python -m rag_0_Scraper.scraper)
    from config import WEBSITE_URL, DATA_DIR as CONFIG_DATA_DIR, PDF_DIR as CONFIG_PDF_DIR, HTML_DIR as CONFIG_HTML_DIR
except Exception:
    # Fallback when running the script directly (python rag_0_Scraper/scraper.py)
    import importlib.util
    import sys
    import pathlib
    # Add the parent RAG directory to sys.path
    sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
    from config import WEBSITE_URL, DATA_DIR as CONFIG_DATA_DIR, PDF_DIR as CONFIG_PDF_DIR, HTML_DIR as CONFIG_HTML_DIR
BASE_URL = WEBSITE_URL.rstrip('/') + '/'
SECTIONS = [
    "guidelines",
    "risk-assessment",
    "implementation",
    "editorial-%26-reports"
]

DATA_DIR = CONFIG_DATA_DIR
# Use configured HTML/PDF directories if provided
PDF_DIR = CONFIG_PDF_DIR if CONFIG_PDF_DIR else os.path.join(DATA_DIR, "browser_pdf")
TEXT_DIR = CONFIG_HTML_DIR if CONFIG_HTML_DIR else os.path.join(DATA_DIR, "browser_text")
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def get_html_with_browser(url):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        return html
    except Exception as e:
        print(f"❌ Browser failed to fetch {url}: {e}")
        return None
    finally:
        driver.quit()

scraped_count = 0
forbidden_count = 0
captcha_count = 0
other_skipped_count = 0
forbidden_urls = []  # list of (filename, url)
captcha_urls = []    # list of (filename, url)
other_skipped_urls = []   # list of (filename, url)

def save_text(filename, content):
    global scraped_count, forbidden_count, captcha_count, other_skipped_count, forbidden_urls, captcha_urls, other_skipped_urls, current_url
    # Do not save if content is a 403 Forbidden page, Access Denied, or CAPTCHA page
    forbidden_signatures = ["403 Forbidden", "Error 403", "<title>403", "<h1>403", "Access Denied", "access denied"]
    captcha_signatures = ["verify you are human", "enable javascript and cookies to continue", "captcha"]
    content_lower = content.lower()
    if any(sig.lower() in content_lower for sig in forbidden_signatures):
        print(f"⛔ Skipped saving {filename} (forbidden detected)")
        forbidden_count += 1
        forbidden_urls.append((filename, current_url))
        return
    if any(sig.lower() in content_lower for sig in captcha_signatures):
        print(f"⛔ Skipped saving {filename} (captcha detected)")
        captcha_count += 1
        captcha_urls.append((filename, current_url))
        return
    # Optionally, add more checks for other types
    if len(content_lower.strip()) < 20:
        preview = content_lower.strip().replace('\n', ' ')[:60]
        print(f"⛔ Skipped saving {filename} (other/empty). Preview: '{preview}'")
        other_skipped_count += 1
        other_skipped_urls.append((filename, current_url))
        return
    filepath = os.path.join(TEXT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved text: {filepath}")
    scraped_count += 1

def save_pdf(url):
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(PDF_DIR, filename)
    try:
        import requests
        resp = requests.get(url, stream=True, timeout=20)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        print(f"📄 Saved PDF: {filepath}")
    except Exception as e:
        print(f"❌ Failed to download PDF {url}: {e}")

def clean_text(soup):
    for tag in soup(["script", "style", "header", "footer", "nav", "form"]):
        tag.extract()
    text = soup.get_text(separator="\n", strip=True)
    return text

def crawl_section_with_browser(url, idx):
    external_idx = 1
    print(f"\n➡️ [Browser] Crawling section: {url}")
    global current_url
    # Scrape the section page itself
    scrape_url(url, filename_hint=f"section_{idx}.txt")
    # Now find and scrape external links
    html = get_html_with_browser(url)
    if not html:
        return
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and not href.lower().endswith(".pdf") and not href.startswith(BASE_URL):
            print(f"🌐 [Browser] Found external link: {href}")
            save_external_html_with_browser(href, idx, external_idx)
            external_idx += 1

def single_scrape(url):
    print(f"\n➡️ [Browser] Single scrape: {url}")
    scrape_url(url, filename_hint="single_scrape.txt")

def save_external_html_with_browser(url, idx, ext_idx):
    global current_url
    html = get_html_with_browser(url)
    if not html:
        print(f"❌ [Browser] Skipping external link (no HTML): {url}")
        return
    try:
        soup = BeautifulSoup(html, "html.parser")
        text = clean_text(soup)
        if text.strip():
            # Use the page title as filename
            title_tag = soup.find('title')
            if title_tag and title_tag.text.strip():
                title = title_tag.text.strip()
            else:
                title = f"external_{idx}_{ext_idx}"
            import re
            filename = re.sub(r'[^\w\-_\. ]', '_', title)[:80] + ".txt"
            current_url = url
            save_text(filename, text)
        # Download any PDFs found on the external page
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                pdf_url = urljoin(url, href)
                save_pdf(pdf_url)
    except Exception as e:
        print(f"❌ [Browser] Error processing external HTML {url}: {e}")

if __name__ == "__main__":
    # To run the full crawl using the configured SECTIONS list (recommended):
    if SECTIONS:
        for i, section in enumerate(SECTIONS, start=1):
            section_url = urljoin(BASE_URL, section)
            crawl_section_with_browser(section_url, i)
    else:
        # No sections configured — crawl the main BASE_URL once and exit.
        print("No SECTIONS configured — crawling the main BASE_URL only")
        crawl_section_with_browser(BASE_URL, 1)
    # To run a single scrape, uncomment and provide a URL:
    # single_scrape("https://doi.org/10.1002/mdc3.13860")
    print("\n--- Scraping Statistics ---")
    print(f"Scraped successfully: {scraped_count}")
    print(f"Forbidden/blocked: {forbidden_count}")
    if forbidden_urls:
        print("  Blocked files (filenames):")
        for fname in forbidden_urls:
            print(f"    {fname}")
    print(f"CAPTCHA/verification: {captcha_count}")
    if captcha_urls:
        print("  CAPTCHA files (filenames):")
        for fname in captcha_urls:
            print(f"    {fname}")
    print(f"Other/empty: {other_skipped_count}")

    # Write summary files for each type
    if forbidden_urls:
        with open(os.path.join(DATA_DIR, "forbidden_files.txt"), "w", encoding="utf-8") as f:
            for fname, url in forbidden_urls:
                f.write(f"{fname}\t{url}\n")
    if captcha_urls:
        with open(os.path.join(DATA_DIR, "captcha_files.txt"), "w", encoding="utf-8") as f:
            for fname, url in captcha_urls:
                f.write(f"{fname}\t{url}\n")
    if other_skipped_urls:
        with open(os.path.join(DATA_DIR, "other_skipped_files.txt"), "w", encoding="utf-8") as f:
            for fname, url in other_skipped_urls:
                f.write(f"{fname}\t{url}\n")
