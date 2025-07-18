import functools
import http.server
import socketserver
import threading
from unittest.mock import Mock, patch

import requests

from web2pdfbook.crawler.usecase.extract_links import extract_links


class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: D401  -- silence server logs
        pass


def run_server(directory, port=0):
    handler = functools.partial(SilentHandler, directory=directory)
    httpd = socketserver.TCPServer(("localhost", port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd, httpd.server_address[1]


def test_extract_links_unit():
    html_index = (
        '<a href="/page1.html">1</a><a href="/page2.html">2</a>'
        '<a href="/page">4</a><a href="/image.png">img</a>'
    )
    html_page1 = '<a href="/page2.html">2</a>'
    html_page2 = '<a href="#anchor">A</a><a href="/page3.html">3</a>'
    html_page3 = ""
    html_page_no_ext = ""

    responses = {
        "https://example.com/": Mock(
            status_code=200, text=html_index, headers={"Content-Type": "text/html"}
        ),
        "https://example.com/page1.html": Mock(
            status_code=200, text=html_page1, headers={"Content-Type": "text/html"}
        ),
        "https://example.com/page2.html": Mock(
            status_code=200, text=html_page2, headers={"Content-Type": "text/html"}
        ),
        "https://example.com/page3.html": Mock(
            status_code=200, text=html_page3, headers={"Content-Type": "text/html"}
        ),
        "https://example.com/page": Mock(
            status_code=200,
            text=html_page_no_ext,
            headers={"Content-Type": "text/html"},
        ),
        "https://example.com/image.png": Mock(
            status_code=200, text="", headers={"Content-Type": "image/png"}
        ),
    }

    def fake_get(url, *args, **kwargs):
        resp = responses[url]
        return resp

    with patch(
        "web2pdfbook.crawler.usecase.extract_links.requests.get", side_effect=fake_get
    ):
        result = extract_links("https://example.com/")

    assert result.links == [
        "https://example.com/",
        "https://example.com/page",
        "https://example.com/page1.html",
        "https://example.com/page2.html",
        "https://example.com/page3.html",
    ]


def test_extract_links_skips_errors():
    responses = {
        "https://example.com/": Mock(
            status_code=200,
            text='<a href="/bad.html">bad</a>',
            headers={"Content-Type": "text/html"},
        ),
    }

    def fake_get(url, *args, **kwargs):
        if url.endswith("bad.html"):
            raise requests.RequestException
        return responses[url]

    with patch(
        "web2pdfbook.crawler.usecase.extract_links.requests.get", side_effect=fake_get
    ):
        result = extract_links("https://example.com/")

    assert result.links == ["https://example.com/"]


def test_extract_links_integration(tmp_path):
    (tmp_path / "index.html").write_text(
        '<a href="/page1.html">1</a><a href="/page2.html">2</a>'
        '<a href="/page">4</a><a href="/image.png">img</a>'
    )
    (tmp_path / "page1.html").write_text('<a href="/page2.html">2</a>')
    (tmp_path / "page2.html").write_text(
        '<a href="#top">top</a><a href="/page3.html">3</a>'
    )
    (tmp_path / "page3.html").write_text("")
    (tmp_path / "page").write_text("")
    (tmp_path / "image.png").write_bytes(b"")

    server, port = run_server(str(tmp_path))
    base_url = f"http://localhost:{port}/"
    try:
        result = extract_links(base_url)
    finally:
        server.shutdown()
        server.server_close()

    assert result.links == [
        base_url,
        f"http://localhost:{port}/page1.html",
        f"http://localhost:{port}/page2.html",
        f"http://localhost:{port}/page3.html",
    ]
