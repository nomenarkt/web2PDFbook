from __future__ import annotations

import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from ..entity.crawl_result import CrawlResult
from .extract_links import _is_html_url, extract_links


def _fetch_html(url: str) -> str | None:
    """Fetch ``url`` and return text if HTML, else ``None``."""
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    if "text/html" not in resp.headers.get("Content-Type", ""):
        return None
    return resp.text


def extract_index_links(base_url: str) -> CrawlResult:
    """Extract navigation links from ``base_url``."""
    html = _fetch_html(base_url)
    if not html:
        return extract_links(base_url)

    parsed_base = urlparse(base_url)
    domain = parsed_base.netloc
    soup = BeautifulSoup(html, "html.parser")

    sitemap_link = soup.find("link", rel="sitemap")
    links: list[str] = []

    if isinstance(sitemap_link, Tag) and sitemap_link.has_attr("href"):
        sitemap_url = urljoin(base_url, str(sitemap_link["href"]))
        try:
            resp = requests.get(sitemap_url)
            resp.raise_for_status()
        except requests.RequestException:
            pass
        else:
            root = ET.fromstring(resp.text)
            for loc in root.iterfind(".//loc"):
                url = urljoin(sitemap_url, loc.text.strip())
                parsed = urlparse(url)
                if parsed.scheme not in {"http", "https"}:
                    continue
                if parsed.netloc != domain:
                    continue
                if not _is_html_url(url):
                    continue
                if url not in links:
                    links.append(url)
    else:
        selectors = "nav, #sidebar, .sphinxsidebar, [role=navigation]"
        for container in soup.select(selectors):
            for tag in container.find_all("a", href=True):
                if not isinstance(tag, Tag):
                    continue
                href = str(tag["href"])
                if href.startswith("#"):
                    continue
                url = urljoin(base_url, href)
                parsed = urlparse(url)
                if parsed.scheme not in {"http", "https"}:
                    continue
                if parsed.netloc != domain:
                    continue
                if not _is_html_url(url):
                    continue
                if url not in links:
                    links.append(url)

    if not links:
        return extract_links(base_url)

    return CrawlResult(links)
