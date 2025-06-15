from __future__ import annotations

import os
import tempfile

from crawler import extract_links
from logger import get_logger
from merger import merge_pdfs
from renderer import PlaywrightRenderer, render_to_pdf

logger = get_logger(__name__)


async def run(url: str, output: str, timeout: int = 15000) -> str:
    """Crawl ``url`` and produce a merged PDF at ``output``."""
    result = extract_links(url)
    links = result.links
    renderer = PlaywrightRenderer()
    pdf_paths: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, link in enumerate(links):
            dest = os.path.join(tmpdir, f"page{idx}.pdf")
            await render_to_pdf(link, dest, timeout=timeout, renderer=renderer)
            pdf_paths.append(dest)
        merge_pdfs(pdf_paths, output)
    logger.info("written %s", output)
    return output
