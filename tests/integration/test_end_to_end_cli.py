import os
import subprocess
import sys
from pathlib import Path

import requests

import pytest
from PyPDF2 import PdfReader

ROOT = Path(__file__).resolve().parents[2]


def is_url_accessible(url: str) -> bool:
    try:
        resp = requests.get(url, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def _ensure_playwright_installed() -> bool:
    try:
        import playwright  # noqa: F401
    except Exception:
        return False
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "playwright",
            "install",
            "chromium",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


@pytest.fixture(scope="session", autouse=True)
def playwright_setup():
    if not _ensure_playwright_installed():
        pytest.skip("Playwright not available")


@pytest.mark.integration
def test_end_to_end_success():
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "output.pdf"
    if output.exists():
        output.unlink()

    url = "https://httpbin.org/html"
    if not is_url_accessible(url):
        pytest.skip("Test URL is not accessible")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            url,
            str(output),
            "--timeout",
            "30000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert output.stat().st_size > 10 * 1024
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1
    output.unlink()


@pytest.mark.integration
def test_end_to_end_broken_url():
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "bad.pdf"
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            "https://example.com/404",
            str(output),
            "--timeout",
            "15000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode != 0
    assert (
        "not found" in result.stderr.lower()
        or "no input pdfs provided" in result.stderr.lower()
        or "no valid pdfs generated" in result.stderr.lower()
    ), f"Unexpected error: {result.stderr}"


@pytest.mark.integration
def test_output_pdf_validity():
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "valid.pdf"
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            "https://httpbin.org/html",
            str(output),
            "--timeout",
            "15000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1
    output.unlink()


@pytest.mark.integration
def test_end_to_end_multiple_urls():
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "multi.pdf"
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            "https://httpbin.org/html",
            "https://httpbin.org/html",
            str(output),
            "--timeout",
            "15000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 2
    output.unlink()


@pytest.mark.integration
def test_end_to_end_mixed_urls():
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "mixed.pdf"
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            "https://httpbin.org/html",
            "https://example.com/404",
            str(output),
            "--timeout",
            "15000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1
    output.unlink()


@pytest.mark.integration
def test_end_to_end_file_url(tmp_path):
    env = os.environ.copy()
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "local.pdf"
    if output.exists():
        output.unlink()

    html = tmp_path / "sample.html"
    html.write_text(Path(ROOT / "tests" / "fixtures" / "sample.html").read_text())
    url = html.as_uri()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "web2pdfbook.cli",
            url,
            str(output),
            "--timeout",
            "15000",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert output.stat().st_size > 10 * 1024
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1
    output.unlink()
