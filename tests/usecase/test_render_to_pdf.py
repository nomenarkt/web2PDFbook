import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web2pdfbook.renderer import PlaywrightRenderer, RendererError
from web2pdfbook.renderer.entity.renderer import validate_params
from web2pdfbook.renderer.usecase.render_to_pdf import render_to_pdf


@patch("web2pdfbook.renderer.adapter.playwright_renderer.async_playwright")
@pytest.mark.parametrize(
    "url,output,timeout",
    [
        ("https://example.com", "out.pdf", 15000),
    ],
)
def test_render_to_pdf_unit(mock_playwright, tmp_path, url, output, timeout):
    page = AsyncMock()
    context = AsyncMock(new_page=AsyncMock(return_value=page))
    browser = AsyncMock(new_context=AsyncMock(return_value=context))
    browser_type = AsyncMock(launch=AsyncMock(return_value=browser))
    mock_playwright_cm = AsyncMock()
    mock_playwright_cm.__aenter__.return_value = MagicMock(chromium=browser_type)
    mock_playwright.return_value = mock_playwright_cm

    dest = tmp_path / output
    renderer = PlaywrightRenderer()
    assert (
        asyncio.run(render_to_pdf(url, str(dest), timeout=timeout, renderer=renderer))
        is True
    )
    page.goto.assert_called_with(url, timeout=timeout)
    page.wait_for_load_state.assert_called_with("networkidle")
    page.pdf.assert_called_with(path=str(dest))


@pytest.mark.parametrize(
    "url,output,timeout",
    [
        ("ftp://example.com", "out.pdf", 15000),
        ("https://example.com", "out.txt", 15000),
        ("https://example.com", "out.pdf", 500),
    ],
)
def test_render_to_pdf_invalid_params(tmp_path, url, output, timeout):
    dest = tmp_path / output
    renderer = PlaywrightRenderer()
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf(url, str(dest), timeout=timeout, renderer=renderer))


@patch("web2pdfbook.renderer.adapter.playwright_renderer.async_playwright")
@pytest.mark.parametrize(
    "side_effect",
    [Exception("404"), TimeoutError("timeout")],
)
def test_render_to_pdf_errors(mock_playwright, tmp_path, side_effect):
    page = AsyncMock(goto=AsyncMock(side_effect=side_effect))
    context = AsyncMock(new_page=AsyncMock(return_value=page))
    browser = AsyncMock(new_context=AsyncMock(return_value=context))
    browser_type = AsyncMock(launch=AsyncMock(return_value=browser))
    mock_playwright_cm = AsyncMock()
    mock_playwright_cm.__aenter__.return_value = MagicMock(chromium=browser_type)
    mock_playwright.return_value = mock_playwright_cm

    dest = tmp_path / "out.pdf"
    renderer = PlaywrightRenderer()
    with pytest.raises(RendererError):
        asyncio.run(
            render_to_pdf(
                "https://example.com", str(dest), timeout=15000, renderer=renderer
            )
        )


class FailingRenderer:
    async def render(
        self, url: str, output_path: str, timeout: int, *, style: str | None = None
    ) -> None:
        raise RuntimeError("boom")


def test_render_to_pdf_wraps_errors(tmp_path):
    dest = tmp_path / "out.pdf"
    with pytest.raises(RendererError):
        asyncio.run(
            render_to_pdf(
                "https://example.com",
                str(dest),
                timeout=1500,
                renderer=FailingRenderer(),
            )
        )


def test_validate_params_accepts_file_url(tmp_path):
    html = tmp_path / "index.html"
    html.write_text("<p>ok</p>")
    file_url = html.as_uri()
    validate_params(file_url, str(tmp_path / "out.pdf"), 1501)


@pytest.mark.skip("requires network and browser")
def test_render_to_pdf_integration(tmp_path):
    output = tmp_path / "page.pdf"
    url = "https://docs.telegram-mini-apps.com"
    renderer = PlaywrightRenderer()
    assert (
        asyncio.run(render_to_pdf(url, str(output), timeout=20000, renderer=renderer))
        is True
    )
    assert output.exists() and output.stat().st_size > 0
