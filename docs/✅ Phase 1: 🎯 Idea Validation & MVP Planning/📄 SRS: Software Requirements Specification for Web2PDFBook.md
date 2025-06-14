# Software Requirements Specification (SRS)

## Project Title: Web2PDFBook

**Version**: 1.0
**Author**: The Architect GPT
**Date**: 2025-06-12

---

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to define the software requirements for **Web2PDFBook**, a command-line tool designed to convert an entire documentation website into a structured, single-file PDF book.

### 1.2 Scope

Web2PDFBook will:

* Accept a base URL
* Crawl all reachable internal pages
* Render each HTML page to a PDF file
* Merge all PDFs into a single book, ordered by structure
* Offer a configurable CLI interface for flexible usage

### 1.3 Definitions

* **Base URL**: Starting page of documentation site.
* **Renderer**: Module that converts URLs to PDF.
* **Crawler**: Module that discovers all valid HTML links.
* **TOC**: Table of Contents based on page order.

---

## 2. Overall Description

### 2.1 Product Perspective

The tool is a standalone CLI application. Future extensions may include a web frontend or integration with GitHub Actions.

### 2.2 Product Functions

* Crawl site from root URL
* Parse navigation order or sitemap (if available)
* Use headless browser (Playwright) or rendering API (PDFmyURL)
* Store intermediate PDFs
* Merge into one book with TOC-like ordering
* Output result to user-defined path

### 2.3 User Classes and Characteristics

* Developers: Need offline access to docs
* PMs / Legal: Need PDF snapshot for compliance
* Educators: Want printable technical material

---

## 3. Specific Requirements

### 3.1 Functional Requirements

* **FR1**: System shall accept a base URL as input
* **FR2**: System shall crawl all internal documentation links
* **FR3**: System shall filter for valid HTML pages
* **FR4**: System shall render each page into an individual PDF
* **FR5**: System shall merge all PDFs into a single output file
* **FR6**: System shall support CLI configuration for output file, delay, and verbosity

### 3.2 Non-Functional Requirements

* **NFR1**: Must complete a 50-page site under 5 minutes
* **NFR2**: Must run on Python 3.9+ and Linux/macOS/Windows
* **NFR3**: Should be modular, allowing pluggable renderer backends
* **NFR4**: Should use caching to avoid re-fetching URLs
* **NFR5**: Logging must be clear, timestamped, and optionally verbose

### 3.3 Constraints

* Internet access required
* Respect target site's robots.txt
* Rate limit API calls to avoid bans

### 3.4 Assumptions and Dependencies

* Docs site is static (non-JS rendered pages)
* Playwright or external PDF API must be installed/configured

---

## 4. External Interfaces

### 4.1 Command-Line Interface

Example:

```bash
python web2pdfbook.py \
  --url https://docs.telegram-mini-apps.com/ \
  --output ./telegram-book.pdf \
  --method playwright \
  --delay 1.0
```

### 4.2 Modules

* `crawler.py`: Crawl and return valid URLs
* `renderer.py`: Render URLs to PDF (headless or API)
* `merger.py`: Combine PDFs
* `cli.py`: Argument parsing and job orchestration
* `tests/`: Unit and integration tests

---

## 5. Future Enhancements

* GUI/Web-based dashboard
* Support login-protected sites
* Output in EPUB/Markdown
* Auto-publish to GitHub or S3
* Multilingual site support

---

## 6. Appendices

* Tools: Playwright, PyPDF2, requests, BeautifulSoup
* Standards: PEP8, Clean Architecture, TDD

---

**End of Document**
