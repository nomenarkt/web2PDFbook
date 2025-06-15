from __future__ import annotations

import os
import tempfile
from typing import Awaitable, Callable

from ..crawler.entity.crawl_result import CrawlResult
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
    renderer: RendererFunc,
    merger: MergeFunc,
) -> str:
    """Create a PDF book from ``base_url`` and save to ``output_file``."""
    result = link_extractor(base_url)
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
