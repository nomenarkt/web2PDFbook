from __future__ import annotations

from PyPDF2 import PdfMerger

from ..entity.pdf_document import MergerError


class PyPDF2Merger:
    """Merge PDFs using PyPDF2."""

    def merge(self, input_paths: list[str], output_path: str) -> None:
        merger = PdfMerger()
        try:
            for path in input_paths:
                merger.append(path)
            with open(output_path, "wb") as f:
                merger.write(f)
        except Exception as exc:  # noqa: BLE001
            raise MergerError(str(exc)) from exc
        finally:
            merger.close()
