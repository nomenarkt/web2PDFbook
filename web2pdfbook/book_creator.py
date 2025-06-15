from __future__ import annotations

import os
import tempfile
from typing import Iterable

from .crawler import extract_links
from .logger import get_logger
from .merger import PyPDF2Merger, merge_documents
from .renderer import PlaywrightRenderer, render_to_pdf
from .usecase import create_book

logger = get_logger(__name__)


async def run(urls: Iterable[str], output: str, timeout: int = 15000) -> str:
    """Crawl ``urls`` and produce a merged PDF at ``output``."""
    renderer = PlaywrightRenderer()

    async def render_page(u: str, dest: str, t: int) -> bool:
        return await render_to_pdf(u, dest, timeout=t, renderer=renderer)

    def merge_pdfs(paths: list[str], dest: str) -> bool:
        return merge_documents(paths, dest, merger=PyPDF2Merger())

    pdf_paths: list[str] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, url in enumerate(urls):
            dest = os.path.join(tmpdir, f"site{idx}.pdf")
            try:
                await create_book(
                    url,
                    dest,
                    timeout,
                    link_extractor=extract_links,
                    renderer=render_page,
                    merger=merge_pdfs,
                )
                pdf_paths.append(dest)
            except Exception as exc:  # noqa: BLE001
                logger.warning("failed to process %s: %s", url, exc)

        if not pdf_paths:
            raise RuntimeError("no valid PDFs generated")

        merge_pdfs(pdf_paths, output)

    logger.info("written %s", output)
    return output
