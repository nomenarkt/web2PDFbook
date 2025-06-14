# Web2PDFBook – Architecture & Tech Stack

## 1. System Overview

Web2PDFBook is a modular Python CLI application that converts an entire documentation website into a structured PDF book. It follows Clean Architecture principles, enabling testing, reuse, and future extension into a web-based interface.

---

## 2. Component Architecture

### 📦 Modules

1. **CLI Interface (`cli.py`)**

   * Parses user arguments
   * Kicks off the crawl-render-merge pipeline

2. **Crawler (`crawler.py`)**

   * Inputs: Base URL
   * Outputs: Ordered list of valid internal documentation URLs
   * Technologies: `requests`, `BeautifulSoup4`, `urllib.parse`

3. **Renderer (`renderer.py`)**

   * Inputs: List of URLs
   * Outputs: Rendered PDF files (one per URL)
   * Backends:

     * **Playwright** (default)
     * **PDFmyURL API** (optional, with API key)
   * Technologies: `playwright`, `asyncio`, `aiohttp`, `os`

4. **Merger (`merger.py`)**

   * Inputs: List of PDF file paths
   * Output: Final merged PDF
   * Technology: `PyPDF2`

5. **Logger (`logger.py`)**

   * Unified logging with verbosity levels and timestamps

6. **Cache (`cache.py`)** *(optional)*

   * Stores already-rendered PDFs and visited URLs
   * Format: JSON or SQLite

7. **Tests (`tests/`)**

   * Unit + integration tests
   * Tooling: `pytest`, `playwright`, `tox`

---

## 3. Tech Stack

### 🚀 Core Tools

| Purpose      | Tool                                            |
| ------------ | ----------------------------------------------- |
| Language     | Python 3.11+                                    |
| Crawling     | `requests`, `BeautifulSoup4`                    |
| Rendering    | `playwright` (headless Chromium)                |
| Merging PDFs | `PyPDF2`                                        |
| CLI UX       | `argparse`, `rich` (optional for formatting)    |
| Testing      | `pytest`, `tox`, `playwright/test`              |
| Packaging    | `setuptools`, `taskfile`, `Makefile` (optional) |

### 📦 Optional APIs

* `PDFmyURL` or `Urlbox` (if not using Playwright)

---

## 4. Directory Structure

```bash
web2pdfbook/
├── cli.py
├── crawler.py
├── renderer.py
├── merger.py
├── logger.py
├── cache.py
├── config.py
├── utils.py
├── tests/
│   ├── test_crawler.py
│   ├── test_renderer.py
│   ├── test_merger.py
│   └── fixtures/
├── requirements.txt
├── README.md
└── main.py
```

---

## 5. System Flow Diagram

```plaintext
[User CLI Input]
      ↓
[cli.py] → [crawler.py] → [renderer.py] → [merger.py]
                             ↓                ↓
                        [PDFs Folder] → Final Book Output
```

---

## 6. Design Principles

* Clean Architecture (isolate logic, reusable modules)
* Fail-safe by default (log errors, skip failed pages)
* TDD: test each unit and full flow
* Modular and extensible

---

## 7. Next Steps

* Scaffold project structure and virtualenv
* Implement basic `main.py` pipeline: crawl → render → merge
* Add sample test and logging utility

---

**End of Document**
