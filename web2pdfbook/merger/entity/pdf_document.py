from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol


class MergerError(Exception):
    """Raised when merging PDF files fails."""


class PDFMerger(Protocol):
    def merge(self, input_paths: list[str], output_path: str) -> None:
        """Merge ``input_paths`` into ``output_path``."""


@dataclass(slots=True)
class PDFDocument:
    path: str


def validate_paths(input_paths: list[str], output_path: str) -> None:
    if not input_paths:
        raise MergerError("no input PDFs provided")
    if not output_path.lower().endswith(".pdf"):
        raise MergerError("output_path must be a .pdf file")
    for path in input_paths:
        if not os.path.isfile(path):
            raise MergerError(f"{path} does not exist")
        try:
            with open(path, "rb") as f:
                header = f.read(4)
            if header != b"%PDF":
                raise MergerError(f"{path} is not a PDF file")
        except OSError as exc:  # noqa: BLE001
            raise MergerError(str(exc)) from exc
