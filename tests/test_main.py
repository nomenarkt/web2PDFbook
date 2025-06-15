import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from web2pdfbook.book_creator import run


@patch("web2pdfbook.book_creator.merge_documents")
@patch("web2pdfbook.book_creator.create_book", new_callable=AsyncMock)
def test_run_orchestrates(mock_create, mock_merge, tmp_path):
    mock_create.side_effect = lambda url, dest, timeout, **kwargs: dest
    out = tmp_path / "book.pdf"
    asyncio.run(run(["https://a", "https://b"], str(out), 1234))
    assert mock_create.await_count == 2
    mock_merge.assert_called_once()
    args = mock_merge.call_args.args
    assert args[1] == str(out)
    assert len(args[0]) == 2


@patch("web2pdfbook.book_creator.logger")
@patch("web2pdfbook.book_creator.merge_documents")
@patch("web2pdfbook.book_creator.create_book", new_callable=AsyncMock)
def test_run_partial_failures(mock_create, mock_merge, mock_logger, tmp_path):
    async def succeed(url, dest, timeout, **kwargs):
        return dest

    mock_create.side_effect = [Exception("boom"), succeed]
    out = tmp_path / "book.pdf"
    asyncio.run(run(["bad", "good"], str(out), 1234))
    mock_logger.warning.assert_called_once()
    args = mock_merge.call_args.args
    assert len(args[0]) == 1


@patch(
    "web2pdfbook.book_creator.create_book",
    new_callable=AsyncMock,
    side_effect=Exception("boom"),
)
def test_run_all_fail(mock_create, tmp_path):
    out = tmp_path / "book.pdf"
    with pytest.raises(RuntimeError):
        asyncio.run(run(["bad"], str(out), 1234))
