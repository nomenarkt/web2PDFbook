import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest  # noqa: E402

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from renderer import RendererError, render_to_pdf  # noqa: E402


@patch("renderer.async_playwright")
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
    assert asyncio.run(render_to_pdf(url, str(dest), timeout=timeout)) is True
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
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf(url, str(dest), timeout=timeout))


@patch("renderer.async_playwright")
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
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf("https://example.com", str(dest)))


@pytest.mark.skip("requires network and browser")
def test_render_to_pdf_integration(tmp_path):
    output = tmp_path / "page.pdf"
    url = "https://docs.telegram-mini-apps.com"
    assert asyncio.run(render_to_pdf(url, str(output), timeout=20000)) is True
    assert output.exists() and output.stat().st_size > 0
