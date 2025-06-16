import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PyPDF2 import PdfReader

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
def test_render_to_pdf_unit_no_style(mock_playwright, tmp_path, url, output, timeout):
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
    page.add_style_tag.assert_not_called()
    page.pdf.assert_called_with(
        path=str(dest),
        margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"},
        scale=1.0,
        print_background=True,
    )


@patch("web2pdfbook.renderer.adapter.playwright_renderer.async_playwright")
def test_render_to_pdf_unit_with_style(mock_playwright, tmp_path):
    page = AsyncMock()
    context = AsyncMock(new_page=AsyncMock(return_value=page))
    browser = AsyncMock(new_context=AsyncMock(return_value=context))
    browser_type = AsyncMock(launch=AsyncMock(return_value=browser))
    mock_playwright_cm = AsyncMock()
    mock_playwright_cm.__aenter__.return_value = MagicMock(chromium=browser_type)
    mock_playwright.return_value = mock_playwright_cm

    dest = tmp_path / "styled.pdf"
    renderer = PlaywrightRenderer()
    style = "body { color: red; }"
    assert (
        asyncio.run(
            render_to_pdf(
                "https://example.com",
                str(dest),
                timeout=15000,
                renderer=renderer,
                style=style,
            )
        )
        is True
    )
    page.add_style_tag.assert_called_with(content=style)
    page.pdf.assert_called_with(
        path=str(dest),
        margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"},
        scale=1.0,
        print_background=True,
    )


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


def is_url_accessible(url: str) -> bool:
    try:
        import requests

        resp = requests.get(url, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def _ensure_playwright_installed() -> bool:
    try:
        import playwright  # noqa: F401
    except Exception:
        return False
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


@pytest.fixture(scope="session", autouse=True)
def playwright_setup():
    if not _ensure_playwright_installed():
        pytest.skip("Playwright not available")


@pytest.mark.integration
def test_render_to_pdf_real_url_consistency(tmp_path):
    url = "https://httpbin.org/html"
    if not is_url_accessible(url):
        pytest.skip("Test URL is not accessible")

    out1 = tmp_path / "run1.pdf"
    out2 = tmp_path / "run2.pdf"
    renderer = PlaywrightRenderer()

    assert (
        asyncio.run(render_to_pdf(url, str(out1), timeout=20000, renderer=renderer))
        is True
    )
    size1 = out1.stat().st_size
    reader1 = PdfReader(str(out1))
    pages1 = len(reader1.pages)

    assert (
        asyncio.run(render_to_pdf(url, str(out2), timeout=20000, renderer=renderer))
        is True
    )
    size2 = out2.stat().st_size
    reader2 = PdfReader(str(out2))
    pages2 = len(reader2.pages)

    assert pages1 == pages2 >= 1
    assert size1 == size2


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
