from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from ...logger import get_logger
from ..entity.renderer import RendererError

logger = get_logger(__name__)


class PlaywrightRenderer:
    """Render pages using Playwright."""

    def __init__(self, *, launch_args: list[str] | None = None) -> None:
        self.launch_args = launch_args or []

    async def render(
        self, url: str, output_path: str, timeout: int, *, style: str | None = None
    ) -> None:
        parsed = urlparse(url)
        args = list(self.launch_args)
        if parsed.scheme == "file":
            if "--allow-file-access-from-files" not in args:
                args.append("--allow-file-access-from-files")
            file_path = Path(parsed.path).resolve()
            url = file_path.as_uri()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(args=args)
                context = await browser.new_context(
                    ignore_https_errors=True,
                    viewport={"width": 1280, "height": 800},
                )
                page = await context.new_page()
                await page.goto(url, timeout=timeout)
                await page.wait_for_load_state("networkidle")
                if style:
                    await page.add_style_tag(content=style)
                    try:
                        await page.evaluate("async () => await document.fonts.ready")
                    except Exception:  # noqa: BLE001
                        pass
                await page.pdf(
                    path=output_path,
                    margin={
                        "top": "0.5in",
                        "bottom": "0.5in",
                        "left": "0.5in",
                        "right": "0.5in",
                    },
                    scale=1.0,
                    print_background=True,
                )
                await browser.close()
        except Exception as exc:  # noqa: BLE001
            if parsed.scheme == "file":
                logger.warning("Chromium blocked file access: %s", exc)
            raise RendererError(str(exc)) from exc
