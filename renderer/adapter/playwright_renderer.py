from __future__ import annotations

from playwright.async_api import async_playwright

from ..entity.renderer import Renderer, RendererError


class PlaywrightRenderer:
    """Render pages using Playwright."""

    async def render(self, url: str, output_path: str, timeout: int) -> None:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                context = await browser.new_context(ignore_https_errors=True)
                page = await context.new_page()
                await page.goto(url, timeout=timeout)
                await page.wait_for_load_state("networkidle")
                await page.pdf(path=output_path)
                await browser.close()
        except Exception as exc:  # noqa: BLE001
            raise RendererError(str(exc)) from exc
