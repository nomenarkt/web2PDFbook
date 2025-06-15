import os
import subprocess
import sys
from pathlib import Path

import pytest
from PyPDF2 import PdfReader

ROOT = Path(__file__).resolve().parents[2]


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
    )
    return result.returncode == 0


@pytest.fixture(scope="session", autouse=True)
def playwright_setup():
    if not _ensure_playwright_installed():
        pytest.skip("Playwright not available")


@pytest.fixture(scope="session")
def cli_package(tmp_path_factory):
    pkg_root = tmp_path_factory.mktemp("pkg")
    pkg_dir = pkg_root / "web2pdfbook"
    pkg_dir.mkdir()
    init = pkg_dir / "__init__.py"
    init.write_text(
        "import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.parent))"
    )
    cli_stub = pkg_dir / "cli.py"
    cli_stub.write_text(
        "from cli import build_parser, parse_args, main\n\nif __name__ == '__main__':\n    import sys\n    raise SystemExit(main(sys.argv[1:]))\n"
    )
    return pkg_root


@pytest.mark.integration
def test_end_to_end_success(cli_package):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cli_package)
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    output = docs_dir / "output.pdf"
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
    assert output.exists()
    assert output.stat().st_size > 10 * 1024
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1
    output.unlink()


@pytest.mark.integration
def test_end_to_end_broken_url(cli_package):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cli_package)
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
    assert "not found" in result.stderr.lower()


@pytest.mark.integration
def test_output_pdf_validity(cli_package):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cli_package)
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
