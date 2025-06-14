from __future__ import annotations

from typing import Iterable

from PyPDF2 import PdfMerger


class MergerError(Exception):
    """Raised when merging PDF files fails."""

    pass


def merge_pdfs(input_paths: Iterable[str], output_path: str) -> bool:
    """Merge multiple PDF files into a single output file.

    Args:
        input_paths: Iterable of paths to existing PDF files.
        output_path: Destination path ending with ``.pdf``.

    Returns:
        ``True`` if merging was successful.

    Raises:
        MergerError: If arguments are invalid or merging fails.
    """

    paths = list(input_paths)
    if not paths:
        raise MergerError("no input PDFs provided")
    if not output_path.lower().endswith(".pdf"):
        raise MergerError("output_path must be a .pdf file")

    merger = PdfMerger()
    try:
        for path in paths:
            merger.append(path)
        with open(output_path, "wb") as f:
            merger.write(f)
    except Exception as exc:  # noqa: BLE001 -- convert to MergerError
        raise MergerError(str(exc)) from exc
    finally:
        merger.close()

    return True
