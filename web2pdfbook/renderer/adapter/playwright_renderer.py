from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from ...logger import get_logger
from ..entity.renderer import RendererError

logger = get_logger(__name__)


FONT_URL = "https://fonts.googleapis.com/css2?family=Inter&display=swap"

DEFAULT_STYLE = """
@page { margin: 0.75cm 1cm 1cm 0.75cm; }
@media print {
  body {
    margin: 0 auto;
    padding: 0;
    max-width: 100%;
    font-size: 12pt;
    -webkit-font-smoothing: antialiased;
  }

  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
  }

  h1,
  h2,
  h3,
  p,
  ul,
  ol,
  section {
    page-break-inside: avoid;
  }

  h1,
  h2,
  .doc-section,
  section {
    page-break-before: always;
    break-before: page;
    padding-top: 1.5em;
  }

  section,
  article,
  pre {
    page-break-inside: avoid;
  }

  * {
    font-family: 'Inter', sans-serif !important;
  }

  code,
  pre {
    font-family: 'JetBrains Mono', monospace;
  }
}
"""

SUPPRESS_STYLE = """
@media print {
  .header,
  .menu,
  .edit-page,
  .footer,
  .timestamp,
  .search,
  .command-bar,
  nav,
  .feedback {
    display: none !important;
  }
}
"""


class PlaywrightRenderer:
    """Render pages using Playwright."""

    def __init__(
        self,
        *,
        launch_args: list[str] | None = None,
        css_path: str | None = None,
        viewport_width: int = 1024,
        viewport_height: int = 1366,
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
                await page.add_style_tag(url=FONT_URL)
                await page.add_style_tag(content=DEFAULT_STYLE)
                await page.add_style_tag(content=SUPPRESS_STYLE)
                if self.css_path:
                    css_file = str(Path(self.css_path).resolve())
                    await page.add_style_tag(path=css_file)
                await page.pdf(path=output_path)
                await browser.close()
        except Exception as exc:  # noqa: BLE001
            if parsed.scheme == "file":
                logger.warning("Chromium blocked file access: %s", exc)
            raise RendererError(str(exc)) from exc
