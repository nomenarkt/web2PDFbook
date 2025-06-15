from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CrawlResult:
    """Result of a crawl containing discovered links."""

    links: list[str]
