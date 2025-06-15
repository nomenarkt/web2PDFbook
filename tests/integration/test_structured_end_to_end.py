import asyncio
import functools
import http.server
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

import pytest
from PyPDF2 import PdfReader

from web2pdfbook.crawler.usecase.extract_index_links import extract_index_links
from web2pdfbook.crawler.usecase.extract_links import extract_links
from web2pdfbook.merger import PyPDF2Merger, merge_documents
from web2pdfbook.renderer import PlaywrightRenderer, render_to_pdf
from web2pdfbook.usecase import create_book

ROOT = Path(__file__).resolve().parents[2]


class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: D401
        pass


def run_server(directory: str, port: int = 0):
    handler = functools.partial(SilentHandler, directory=directory)
    httpd = socketserver.TCPServer(("localhost", port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd, httpd.server_address[1]


# Reuse helper from other integration tests

def is_url_accessible(url: str) -> bool:
    try:
        import requests

        resp = requests.get(url, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def _ensure_playwright_installed() -> bool:
    try:
        import playwright  # noqa: F401
    except Exception:
        return False
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


@pytest.fixture(scope="session", autouse=True)
def playwright_setup():
    if not _ensure_playwright_installed():
        pytest.skip("Playwright not available")


@pytest.mark.integration
def test_structured_documentation_end_to_end(tmp_path):
    site_dir = ROOT / "tests" / "fixtures" / "structured_site"
    server, port = run_server(str(site_dir))
    base_url = f"http://localhost:{port}/"

    if not is_url_accessible(base_url):
        server.shutdown()
        server.server_close()
        pytest.skip("Test URL is not accessible")

    output = tmp_path / "structured.pdf"

    try:
        result = extract_index_links(base_url)
        print("Extracted links:", result.links)
        assert len(result.links) == 12

        renderer = PlaywrightRenderer()

        async def render_page(u: str, dest: str, t: int) -> bool:
            return await render_to_pdf(u, dest, timeout=t, renderer=renderer)

        def merge_pdfs(paths: list[str], dest: str) -> bool:
            return merge_documents(paths, dest, merger=PyPDF2Merger())

        asyncio.run(
            create_book(
                base_url,
                str(output),
                20000,
                link_extractor=extract_links,
                index_extractor=extract_index_links,
                renderer=render_page,
                merger=merge_pdfs,
                use_index_links=True,
            )
        )
    finally:
        server.shutdown()
        server.server_close()

    assert output.exists()
    assert output.stat().st_size > 100 * 1024
    reader = PdfReader(str(output))
    assert len(reader.pages) == len(result.links)

