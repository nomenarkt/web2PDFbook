from unittest.mock import Mock, patch
import threading
import http.server
import socketserver
import sys
import functools
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from crawler import get_all_links


class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: D401  -- silence server logs
        pass


def run_server(directory, port=0):
    handler = functools.partial(SilentHandler, directory=directory)
    httpd = socketserver.TCPServer(('localhost', port), handler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd, httpd.server_address[1]


def test_get_all_links_unit():
    html_index = (
        '<a href="/page1.html">1</a><a href="/page2.html">2</a>'
        '<a href="/page">4</a>'
    )
    html_page1 = '<a href="/page2.html">2</a>'
    html_page2 = '<a href="#anchor">A</a><a href="/page3.html">3</a>'
    html_page3 = ''
    html_page_no_ext = ''

    responses = {
        'https://example.com/': Mock(
            status_code=200,
            text=html_index,
            headers={'Content-Type': 'text/html'}
        ),
        'https://example.com/page1.html': Mock(
            status_code=200,
            text=html_page1,
            headers={'Content-Type': 'text/html'}
        ),
        'https://example.com/page2.html': Mock(
            status_code=200,
            text=html_page2,
            headers={'Content-Type': 'text/html'}
        ),
        'https://example.com/page3.html': Mock(
            status_code=200,
            text=html_page3,
            headers={'Content-Type': 'text/html'}
        ),
        'https://example.com/page': Mock(
            status_code=200,
            text=html_page_no_ext,
            headers={'Content-Type': 'text/html'}
        ),
    }

    def fake_get(url, *args, **kwargs):
        return responses[url]

    with patch('crawler.requests.get', side_effect=fake_get):
        result = get_all_links('https://example.com/')

    assert result == [
        'https://example.com/',
        'https://example.com/page',
        'https://example.com/page1.html',
        'https://example.com/page2.html',
        'https://example.com/page3.html',
    ]


def test_get_all_links_integration(tmp_path):
    (tmp_path / 'index.html').write_text(
        '<a href="/page1.html">1</a><a href="/page2.html">2</a><a href="/page">4</a>'
    )
    (tmp_path / 'page1.html').write_text('<a href="/page2.html">2</a>')
    (tmp_path / 'page2.html').write_text(
        '<a href="#top">top</a><a href="/page3.html">3</a>'
    )
    (tmp_path / 'page3.html').write_text('')
    (tmp_path / 'page').write_text('')

    server, port = run_server(str(tmp_path))
    base_url = f'http://localhost:{port}/'
    try:
        result = get_all_links(base_url)
    finally:
        server.shutdown()
        server.server_close()

    assert result == [
        base_url,
        f'http://localhost:{port}/page',
        f'http://localhost:{port}/page1.html',
        f'http://localhost:{port}/page2.html',
        f'http://localhost:{port}/page3.html',
    ]
