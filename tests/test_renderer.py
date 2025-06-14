import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from renderer import RendererError, render_to_pdf


@patch("renderer.async_playwright")
def test_render_to_pdf_unit(mock_playwright, tmp_path):
    page = AsyncMock()
    context = AsyncMock(new_page=AsyncMock(return_value=page))
    browser = AsyncMock(new_context=AsyncMock(return_value=context))
    browser_type = AsyncMock(launch=AsyncMock(return_value=browser))
    mock_playwright_cm = AsyncMock()
    mock_playwright_cm.__aenter__.return_value = MagicMock(chromium=browser_type)
    mock_playwright.return_value = mock_playwright_cm

    output = tmp_path / "test.pdf"
    assert asyncio.run(render_to_pdf("https://example.com", str(output))) is True
    page.goto.assert_called_with("https://example.com", timeout=15000)
    page.wait_for_load_state.assert_called_with("networkidle")
    page.pdf.assert_called_with(path=str(output))


def test_render_to_pdf_invalid(tmp_path):
    output = tmp_path / "test.pdf"
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf("ftp://example.com", str(output)))
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf("https://example.com", "out.txt"))
    with pytest.raises(RendererError):
        asyncio.run(render_to_pdf("https://example.com", str(output), timeout=500))


def test_render_to_pdf_integration(tmp_path):
    output = tmp_path / "page.pdf"
    url = "https://docs.telegram-mini-apps.com"  # small static page
    assert asyncio.run(render_to_pdf(url, str(output), timeout=20000)) is True
    assert output.exists() and output.stat().st_size > 0
