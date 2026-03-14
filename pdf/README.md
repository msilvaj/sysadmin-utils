# 📄 PDF Link Extractor

Extracts **clickable hyperlinks** from PDF files, including **embedded
annotations** (not just visible text).\
Ideal for **security analysis**, **document auditing**, or **sysadmin
automation workflows**.

------------------------------------------------------------------------

## 🚀 Features

-   ✅ Extracts real clickable links (**PDF URI annotations**)
-   🔍 Detects common **URL shorteners** (`bit.ly`, `goo.gl`, `t.co`,
    etc.)
-   🔗 Expands shortened URLs to reveal the **final destination**
-   📊 Exports results to **CSV for analysis**
-   🐍 Works on **Linux, WSL2, macOS, and Windows**

------------------------------------------------------------------------

## ⚡ Quick Start

### 1. Clone the repository

``` bash
git clone https://github.com/msilvaj/sysadmin-utils.git
cd sysadmin-utils/pdf
```

### 2. Create and activate a virtual environment

``` bash
python3 -m venv env
source env/bin/activate
```

**Windows (PowerShell):**

``` bash
env\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install pymupdf requests
```

### 4. Run the extractor

Single file:

``` bash
python extract_links.py example.pdf
```

Multiple files:

``` bash
python extract_links.py *.pdf
```

------------------------------------------------------------------------

## 📦 Output

Results are saved to:

    links_report.csv

The script **appends results**, so you can run it multiple times without
losing previous data.

------------------------------------------------------------------------

## 📋 Requirements

-   **Python 3.7+**

### Python libraries

  Library            Purpose
  ------------------ -----------------------------------------
  `PyMuPDF (fitz)`   Extract links and annotations from PDFs
  `requests`         Expand shortened URLs

Install them with:

``` bash
pip install pymupdf requests
```

💡 **Tip:** Always use a **virtual environment** to avoid dependency
conflicts.

------------------------------------------------------------------------

## 🧪 Usage

### Extract links from a single PDF

``` bash
python extract_links.py document.pdf
```

### Extract links from multiple PDFs

``` bash
python extract_links.py *.pdf
```

### Scan an entire folder (recursive)

``` bash
python extract_links.py ../../reports/
```

------------------------------------------------------------------------

## 📊 Example CSV Output

    File, Page, URL, Domain, Shortened?, Final URL
    doc.pdf, 1, https://bit.ly/xyz123, bit.ly, Yes, https://malware.com

------------------------------------------------------------------------

## 🔎 Use Cases

### 🔐 Security Analysis

Analyze suspicious PDFs received via email to detect hidden or malicious
links.

### 📑 Documentation Auditing

Verify all external links referenced in documentation or reports.

### ⚙️ Automation / Sysadmin Workflows

Integrate the tool into **automation pipelines** or **PDF analysis
scripts**.

Example using **WSL2 on Windows**:

``` bash
cd /mnt/c/Users/YourName/Downloads
python /home/user/sysadmin-utils/pdf/extract_links.py *.pdf
```

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome!

Feel free to:

-   Open an **issue**
-   Submit a **pull request**
-   Suggest improvements or new features

### Future ideas

-   VirusTotal integration
-   Domain risk scoring
-   Simple GUI interface

------------------------------------------------------------------------

## 📜 License

This project is part of the **sysadmin-utils** toolkit.
