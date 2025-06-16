from __future__ import annotations

from typing import Protocol
from urllib.parse import urlparse


class RendererError(Exception):
    """Raised when rendering a web page to PDF fails."""


class Renderer(Protocol):
    async def render(
        self, url: str, output_path: str, timeout: int, *, style: str | None = None
    ) -> None:
        """Render ``url`` into ``output_path`` as PDF."""


def validate_params(url: str, output_path: str, timeout: int) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https", "file"}:
        raise RendererError("URL must start with http, https, or file")
    if not output_path.lower().endswith(".pdf"):
        raise RendererError("output_path must be a .pdf file")
    if timeout <= 1000:
        raise RendererError("timeout must be greater than 1000 ms")
