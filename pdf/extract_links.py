#!/usr/bin/env python3
"""
extract_links.py - Extract clickable URLs from PDF files
Usage: python3 extract_links.py file.pdf [file2.pdf ...]
"""

import fitz  # PyMuPDF
import sys
import os
import csv
import requests
from urllib.parse import urlparse


# Known URL shortening domains (often used in phishing)
URL_SHORTENERS = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 'tiny.cc', 'ow.ly',
    't.co', 'is.gd', 'cutt.ly', 'adf.ly', 'buff.ly', 'rebrand.ly'
}


def expand_url(url):
    """Expand shortened URL to final destination"""
    try:
        response = requests.get(
            url,
            timeout=8,
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        return response.url
    except Exception:
        return "[expand-error]"


def extract_domain(url):
    """Extract domain from URL"""
    try:
        return urlparse(url).netloc.lower()
    except:
        return "[invalid-domain]"


def analyze_pdf(filepath, writer):
    """Extract all clickable links from a single PDF"""
    try:
        doc = fitz.open(filepath)
        print(f"📄 Processing: {filepath} ({doc.page_count} pages)")

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            links = page.get_links()

            for link in links:
                if link['kind'] == fitz.LINK_URI:  # Only external web links
                    url = link['uri']
                    domain = extract_domain(url)
                    is_shortened = "Yes" if domain in URL_SHORTENERS else ""
                    final_url = expand_url(url) if is_shortened else ""

                    writer.writerow([
                        filepath,
                        page_num + 1,
                        url,
                        domain,
                        is_shortened,
                        final_url
                    ])
                    print(f"   → Page {page_num + 1}: {url}")

        doc.close()

    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")


def main():
    if len(sys.argv) < 2:
        print(f"\n📌 Usage: {sys.argv[0]} file.pdf [file2.pdf ...]")
        print("💡 Example: python3 extract_links.py *.pdf\n")
        sys.exit(1)

    output_csv = "links_report.csv"
    write_header = not os.path.exists(output_csv)

    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "File", "Page", "URL", "Domain", "Shortened?", "Final URL"
            ])

        for arg in sys.argv[1:]:
            if os.path.isfile(arg) and arg.lower().endswith('.pdf'):
                analyze_pdf(arg, writer)
            elif os.path.isdir(arg):
                for root, _, files in os.walk(arg):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            filepath = os.path.join(root, file)
                            analyze_pdf(filepath, writer)

    print(f"\n✅ Report saved: {output_csv}")


if __name__ == "__main__":
    main()
