# web2PDFbook

[![Python CI](https://github.com/OWNER/web2PDFbook/actions/workflows/python-ci.yml/badge.svg)](https://github.com/OWNER/web2PDFbook/actions/workflows/python-ci.yml)

![Coverage](./coverage.svg)

## 🧠 What it does

web2PDFbook crawls a website and compiles its pages into a single PDF. It is useful for archiving or offline reading.

## ⚙️ How to install

```bash
git clone https://github.com/OWNER/web2PDFbook.git
cd web2PDFbook
pip install -r requirements.txt
```

## 🔄 How it works

1. **Link crawling** – `crawler.get_all_links()` retrieves all internal HTML links starting from the base URL.
2. **PDF rendering** – `renderer.render_to_pdf()` uses Playwright to save each page as a PDF.
3. **Merging** – `merger.merge_pdfs()` merges the PDFs into a single document.

Generate a book via the CLI:

```bash
python -m web2pdfbook.cli https://example.com output.pdf --timeout 20000
```

## ✅ How to test

```bash
python -m coverage run -m pytest -q
python -m coverage report
```
