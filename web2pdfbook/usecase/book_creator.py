from __future__ import annotations

import os
import tempfile
from typing import Awaitable, Callable
from urllib.parse import urlparse

from ..crawler.entity.crawl_result import CrawlResult
from ..crawler import extract_index_links
from ..logger import get_logger

LinkExtractor = Callable[[str], CrawlResult]
RendererFunc = Callable[[str, str, int], Awaitable[bool]]
MergeFunc = Callable[[list[str], str], bool]

logger = get_logger(__name__)


async def create_book(
    base_url: str,
    output_file: str,
    timeout: int,
    *,
    link_extractor: LinkExtractor,
    index_extractor: LinkExtractor = extract_index_links,
    renderer: RendererFunc,
    merger: MergeFunc,
    use_index_links: bool = False,
) -> str:
    """Create a PDF book from ``base_url`` and save to ``output_file``."""
    parsed = urlparse(base_url)
    if parsed.scheme == "file":
        links = [base_url]
    else:
        if use_index_links:
            result = index_extractor(base_url)
            logger.info("Used index-based link extraction")
        else:
            result = link_extractor(base_url)
            logger.info("Used full-site link extraction")
        links = result.links

    pdf_paths: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, link in enumerate(links):
            dest = os.path.join(tmpdir, f"page{idx}.pdf")
            await renderer(link, dest, timeout)
            pdf_paths.append(dest)
        merger(pdf_paths, output_file)

    logger.info("written %s", output_file)
    return output_file
