from __future__ import annotations

import os
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from ..entity.crawl_result import CrawlResult


def _is_html_url(url: str) -> bool:
    """Return True if URL points to an HTML page based on its extension."""
    path = urlparse(url).path
    if not path or path.endswith("/"):
        return True
    ext = os.path.splitext(path)[1]
    return ext.lower() in {"", ".html", ".htm"}


def extract_links(base_url: str) -> CrawlResult:
    """Crawl ``base_url`` and return internal HTML links."""
    parsed_base = urlparse(base_url)
    domain = parsed_base.netloc

    visited: set[str] = set()
    queue: deque[str] = deque([base_url])

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue

        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except requests.RequestException:
            continue

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            continue

        visited.add(current_url)

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            if not isinstance(tag, Tag):
                continue
            href = str(tag["href"])
            if href.startswith("#"):
                continue
            next_url = urljoin(current_url, href)
            parsed = urlparse(next_url)
            if parsed.scheme not in {"http", "https"}:
                continue
            if parsed.netloc != domain:
                continue
            if not _is_html_url(next_url):
                continue
            if next_url not in visited and next_url not in queue:
                queue.append(next_url)

    return CrawlResult(sorted(visited))
