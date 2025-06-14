from __future__ import annotations

from collections import deque
from typing import List, Set
from urllib.parse import urljoin, urlparse
import os

import requests
from bs4 import BeautifulSoup


NON_HTML_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', '.pdf',
    '.zip', '.tar', '.gz', '.mp4', '.mp3', '.woff', '.woff2'
}


def _is_html_url(url: str) -> bool:
    """Return True if URL points to an HTML page based on its extension."""
    path = urlparse(url).path
    if not path or path.endswith('/'):
        return True
    ext = os.path.splitext(path)[1]
    return ext.lower() in {'', '.html', '.htm'}


def get_all_links(base_url: str) -> List[str]:
    """Crawl ``base_url`` and return all internal HTML links.

    Args:
        base_url: The starting URL of the documentation site.

    Returns:
        A sorted list of unique URLs belonging to the same domain as ``base_url``.
    """
    parsed_base = urlparse(base_url)
    domain = parsed_base.netloc
    scheme = parsed_base.scheme

    visited: Set[str] = set()
    queue: deque[str] = deque([base_url])

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except requests.RequestException:
            continue

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            if href.startswith('#'):
                continue
            next_url = urljoin(current_url, href)
            parsed = urlparse(next_url)
            if parsed.scheme not in {'http', 'https'}:
                continue
            if parsed.netloc != domain:
                continue
            if not _is_html_url(next_url):
                continue
            if next_url not in visited and next_url not in queue:
                queue.append(next_url)

    return sorted(visited)
