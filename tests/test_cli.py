from unittest.mock import AsyncMock, patch

import pytest

from web2pdfbook.cli import main, parse_args


def test_parse_args_valid():
    args = parse_args(["https://example.com", "out.pdf", "--timeout", "2000"])
    assert args.urls == ["https://example.com"]
    assert args.output == "out.pdf"
    assert args.timeout == 2000
    assert args.use_index is False


def test_parse_args_multiple():
    args = parse_args(
        ["https://a.com", "https://b.com", "book.pdf", "--timeout", "1500"]
    )
    assert args.urls == ["https://a.com", "https://b.com"]
    assert args.output == "book.pdf"
    assert args.timeout == 1500
    assert args.use_index is False


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


def test_parse_args_use_index():
    args = parse_args(
        [
            "https://example.com",
            "out.pdf",
            "--timeout",
            "2000",
            "--use-index",
        ]
    )
    assert args.use_index is True


@pytest.mark.asyncio
@patch("web2pdfbook.cli.run", new_callable=AsyncMock)
def test_main_invokes_runner(mock_run, tmp_path):
    out = tmp_path / "book.pdf"
    argv = ["https://example.com", str(out), "--timeout", "2000", "--use-index"]
    assert main(argv) == 0
    mock_run.assert_awaited_once_with(
        ["https://example.com"], str(out), timeout=2000, use_index=True
    )
