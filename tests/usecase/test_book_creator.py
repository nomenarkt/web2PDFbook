import asyncio
from unittest.mock import AsyncMock, Mock

from web2pdfbook.usecase import create_book


def test_create_book_orchestrates(tmp_path):
    extractor = Mock()
    extractor.return_value.links = ["https://a", "https://b"]
    renderer = AsyncMock()
    merger = Mock()

    output = tmp_path / "book.pdf"

    result = asyncio.run(
        create_book(
            "https://base",
            str(output),
            1234,
            link_extractor=extractor,
            renderer=renderer,
            merger=merger,
        )
    )

    assert result == str(output)
    extractor.assert_called_once_with("https://base")
    assert renderer.await_count == 2
    merger.assert_called_once()
    args = merger.call_args.args
    assert args[1] == str(output)
    assert len(args[0]) == 2
    for path in args[0]:
        assert path.endswith(".pdf")
