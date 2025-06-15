# web2PDFbook

[![Python CI](https://github.com/OWNER/web2PDFbook/actions/workflows/python-ci.yml/badge.svg)](https://github.com/OWNER/web2PDFbook/actions/workflows/python-ci.yml)

![Coverage](https://raw.githubusercontent.com/OWNER/web2PDFbook/main/coverage.svg)

## 🧠 What it does

web2PDFbook crawls a website and compiles its pages into a single PDF. It is useful for archiving or offline reading.

## ⚙️ How to install

Install from PyPI:

```bash
pip install web2pdfbook
```

To test a pre-release from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple web2pdfbook
```

## 🔄 How it works

1. **Link crawling** – `crawler.extract_links()` retrieves all internal HTML links starting from the base URL.
2. **PDF rendering** – `renderer.render_to_pdf()` uses Playwright to save each page as a PDF.
3. **Merging** – `merger.merge_documents()` merges the PDFs into a single document.

Generate a book via the CLI:

```bash
web2pdfbook --help
web2pdfbook https://example.com output.pdf --timeout 20000 --use-index
```

* `--timeout` – render timeout in milliseconds.
* `--use-index` – only crawl links from index pages.

## ✅ How to test

Install dependencies first:

```bash
pip install -r requirements.txt
```

```bash
python -m coverage run -m pytest -q
python -m coverage report
```

## 📦 How to release

Install packaging dependencies:

```bash
pip install -r dev-requirements.txt
```

Build and upload the distribution (defaults to TestPyPI):

```bash
./release/publish.sh
```

This script runs `python -m build` and uploads with `twine`. Set `REPOSITORY_URL` to publish elsewhere.

The repository contains a `.pypirc` template with placeholder credentials for
TestPyPI and PyPI. Fill in your tokens (or copy it to `~/.pypirc`) so `twine`
can authenticate during the upload.
