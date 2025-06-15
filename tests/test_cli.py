import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from unittest.mock import AsyncMock, patch  # noqa: E402

import pytest  # noqa: E402

from cli import main, parse_args  # noqa: E402


def test_parse_args_valid():
    args = parse_args(["https://example.com", "out.pdf", "--timeout", "2000"])
    assert args.url == "https://example.com"
    assert args.output == "out.pdf"
    assert args.timeout == 2000


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["https://example.com"],
    ],
)
def test_parse_args_missing(argv):
    with pytest.raises(SystemExit):
        parse_args(argv)


@pytest.mark.asyncio
@patch("cli.run", new_callable=AsyncMock)
def test_main_invokes_runner(mock_run, tmp_path):
    out = tmp_path / "book.pdf"
    argv = ["https://example.com", str(out), "--timeout", "2000"]
    assert main(argv) == 0
    mock_run.assert_awaited_once_with("https://example.com", str(out), timeout=2000)
