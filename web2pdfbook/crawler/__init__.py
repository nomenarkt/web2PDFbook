from __future__ import annotations

from .entity.crawl_result import CrawlResult
from .usecase.extract_index_links import extract_index_links
from .usecase.extract_links import extract_links


def get_all_links(base_url: str) -> list[str]:
    """Backward-compatible wrapper for link extraction."""
    return extract_links(base_url).links


__all__ = ["CrawlResult", "extract_links", "extract_index_links", "get_all_links"]
