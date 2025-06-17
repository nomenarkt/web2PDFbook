from __future__ import annotations

import os
import tempfile
from typing import Awaitable, Callable
from urllib.parse import urlparse

from PyPDF2 import PdfMerger

from ..crawler import extract_index_links
from ..crawler.entity.crawl_result import CrawlResult
from ..logger import get_logger

LinkExtractor = Callable[[str], CrawlResult]
RendererFunc = Callable[[str, str, int], Awaitable[bool]]

logger = get_logger(__name__)


async def run(urls: list[str], output_file: str, timeout: int, use_index: bool = False):
    """Render multiple URLs and merge them into a single PDF output."""
    rendered_pdfs: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, url in enumerate(urls):
            dest = os.path.join(tmpdir, f"page{idx}.pdf")
            try:
                from ..renderer.adapter.playwright_renderer import Renderer

                await Renderer().render(url, dest, timeout=timeout)
                rendered_pdfs.append(dest)
            except Exception as e:
                logger.warning("Failed to render %s: %s", url, e)

        if not rendered_pdfs:
            raise RuntimeError("no valid PDFs generated")

        merger = PdfMerger()
        for path in rendered_pdfs:
            merger.append(path)
        merger.write(output_file)
        merger.close()

    logger.info("written %s", output_file)
    return output_file
