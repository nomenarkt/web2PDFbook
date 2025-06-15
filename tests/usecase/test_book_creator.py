import asyncio
from unittest.mock import AsyncMock, Mock

from web2pdfbook.usecase import create_book


def test_create_book_orchestrates(tmp_path):
    extractor = Mock()
    extractor.return_value.links = ["https://a", "https://b"]
    index_extractor = Mock()
    renderer = AsyncMock()
    merger = Mock()

    output = tmp_path / "book.pdf"

    result = asyncio.run(
        create_book(
            "https://base",
            str(output),
            1234,
            link_extractor=extractor,
            index_extractor=index_extractor,
            renderer=renderer,
            merger=merger,
        )
    )

    assert result == str(output)
    extractor.assert_called_once_with("https://base")
    index_extractor.assert_not_called()
    assert renderer.await_count == 2
    merger.assert_called_once()
    args = merger.call_args.args
    assert args[1] == str(output)
    assert len(args[0]) == 2
    for path in args[0]:
        assert path.endswith(".pdf")


def test_create_book_file_scheme(tmp_path):
    extractor = Mock()
    index_extractor = Mock()
    renderer = AsyncMock()
    merger = Mock()

    html = tmp_path / "page.html"
    html.write_text("<p>hi</p>")
    url = html.as_uri()

    output = tmp_path / "out.pdf"

    asyncio.run(
        create_book(
            url,
            str(output),
            1234,
            link_extractor=extractor,
            index_extractor=index_extractor,
            renderer=renderer,
            merger=merger,
        )
    )

    extractor.assert_not_called()
    index_extractor.assert_not_called()
    renderer.assert_awaited_once()
    merger.assert_called_once()
    args = merger.call_args.args
    assert len(args[0]) == 1


def test_create_book_uses_index_extractor(tmp_path):
    extractor = Mock()
    index_extractor = Mock()
    index_extractor.return_value.links = ["https://a"]
    renderer = AsyncMock()
    merger = Mock()

    output = tmp_path / "book.pdf"

    asyncio.run(
        create_book(
            "https://base",
            str(output),
            500,
            link_extractor=extractor,
            index_extractor=index_extractor,
            renderer=renderer,
            merger=merger,
            use_index_links=True,
        )
    )

    index_extractor.assert_called_once_with("https://base")
    extractor.assert_not_called()
    renderer.assert_awaited_once()
