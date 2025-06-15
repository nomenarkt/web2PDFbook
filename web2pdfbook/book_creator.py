from __future__ import annotations

from .crawler import extract_links
from .merger import PyPDF2Merger, merge_documents
from .renderer import PlaywrightRenderer, render_to_pdf
from .usecase import create_book


async def run(url: str, output: str, timeout: int = 15000) -> str:
    """Crawl ``url`` and produce a merged PDF at ``output``."""
    renderer = PlaywrightRenderer()

    async def render_page(u: str, dest: str, t: int) -> bool:
        return await render_to_pdf(u, dest, timeout=t, renderer=renderer)

    def merge_pdfs(paths: list[str], dest: str) -> bool:
        return merge_documents(paths, dest, merger=PyPDF2Merger())

    return await create_book(
        url,
        output,
        timeout,
        link_extractor=extract_links,
        renderer=render_page,
        merger=merge_pdfs,
    )
