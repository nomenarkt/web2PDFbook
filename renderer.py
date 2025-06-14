"""Utilities for rendering web pages to PDF using Playwright."""

from __future__ import annotations

import asyncio
from urllib.parse import urlparse

from playwright.async_api import async_playwright


class RendererError(Exception):
    """Raised when rendering a web page to PDF fails."""

    pass


async def render_to_pdf(url: str, output_path: str, timeout: int = 15000) -> bool:
    """Render ``url`` into a PDF file.

    Args:
        url: HTTP/HTTPS URL to visit.
        output_path: Destination PDF path. Must end with ``.pdf``.
        timeout: Navigation timeout in milliseconds. Must be greater than 1000.

    Returns:
        ``True`` when the PDF was successfully written.

    Raises:
        RendererError: If arguments are invalid or rendering fails.
    """

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise RendererError("URL must start with http or https")
    if not output_path.lower().endswith(".pdf"):
        raise RendererError("output_path must be a .pdf file")
    if timeout <= 1000:
        raise RendererError("timeout must be greater than 1000 ms")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(ignore_https_errors=True)
            page = await context.new_page()
            await page.goto(url, timeout=timeout)
            await page.wait_for_load_state("networkidle")
            await page.pdf(path=output_path)
            await browser.close()
    except Exception as exc:  # noqa: BLE001 -- convert to RendererError
        raise RendererError(str(exc)) from exc

    return True
