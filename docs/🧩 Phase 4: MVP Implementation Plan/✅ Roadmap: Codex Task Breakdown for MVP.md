We'll structure implementation into 4 self-contained Codex Tasks:
| Step | Module        | Codex Task                                  |
| ---- | ------------- | ------------------------------------------- |
| 1️⃣  | `crawler.py`  | Extract all internal doc URLs from base URL |
| 2️⃣  | `renderer.py` | Render each URL to PDF (via Playwright)     |
| 3️⃣  | `merger.py`   | Merge all PDFs into one final PDF book      |
| 4️⃣  | `main.py`     | Orchestrate full pipeline via CLI           |

Let's proceed with the first one:
💻 Codex Task:  
`get_all_links()` function  

📁 Layer:  
crawler.py  

🎯 Objective:  
Extract all valid internal documentation page URLs from a given base URL.

🧩 Specs:
- **Input:**  
  - `base_url: str` (e.g., "https://docs.telegram-mini-apps.com/")
- **Validation Rules:**  
  - Only follow links with the same domain
  - Skip non-HTML, external, anchor-only, and duplicate links
  - Respect `robots.txt` if present (optional for MVP)

- **Logic Flow:**  
  1. Start from `base_url`
  2. Use `requests.get()` to fetch HTML content
  3. Use `BeautifulSoup` to parse `<a href="">`
  4. Normalize each href with `urljoin`
  5. Deduplicate and filter to same domain
  6. Return a list of sorted URLs

- **Authorization:**  
  - Not required

- **Response Format:**  
  - `List[str]` of valid internal URLs

🧪 Tests:
- ✅ Unit test with a local mock HTML file
- ✅ Integration test against a test server with 3–5 pages
- ❌ Skip broken link retries for MVP

📦 Follow:  
- Pure function design: `get_all_links(base_url) -> list[str]`
- No logging or I/O in this layer — that belongs in `logger.py` or `main.py`
