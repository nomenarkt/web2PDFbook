import asyncio
from unittest.mock import AsyncMock, patch

from web2pdfbook.book_creator import run


@patch("web2pdfbook.book_creator.merge_documents")
@patch("web2pdfbook.book_creator.render_to_pdf", new_callable=AsyncMock)
@patch("web2pdfbook.book_creator.extract_links")
def test_run_orchestrates(mock_extract, mock_render, mock_merge, tmp_path):
    mock_extract.return_value.links = ["https://a", "https://b"]
    out = tmp_path / "book.pdf"
    asyncio.run(run("https://base", str(out), 1234))
    mock_extract.assert_called_once_with("https://base")
    assert mock_render.await_count == 2
    mock_merge.assert_called_once()
    assert mock_merge.call_args.args[1] == str(out)
