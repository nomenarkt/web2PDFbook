from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from ...logger import get_logger
from ..entity.renderer import RendererError

logger = get_logger(__name__)


DEFAULT_STYLE = """
@page { margin: 1cm; }
body { font-family: system-ui, sans-serif; }
"""


class PlaywrightRenderer:
    """Render pages using Playwright."""

    def __init__(
        self,
        *,
        launch_args: list[str] | None = None,
        css_path: str | None = None,
        viewport_width: int = 1280,
        viewport_height: int = 800,
    ) -> None:
        self.launch_args = launch_args or []
        self.css_path = css_path
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    async def render(self, url: str, output_path: str, timeout: int) -> None:
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
                    viewport={
                        "width": self.viewport_width,
                        "height": self.viewport_height,
                    },
                )
                page = await context.new_page()
                await page.goto(url, timeout=timeout)
                await page.wait_for_load_state("networkidle")
                await page.emulate_media(media="screen")
                await page.add_style_tag(content=DEFAULT_STYLE)
                if self.css_path:
                    css_file = str(Path(self.css_path).resolve())
                    await page.add_style_tag(path=css_file)
                await page.pdf(path=output_path)
                await browser.close()
        except Exception as exc:  # noqa: BLE001
            if parsed.scheme == "file":
                logger.warning("Chromium blocked file access: %s", exc)
            raise RendererError(str(exc)) from exc
