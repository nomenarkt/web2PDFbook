from __future__ import annotations

from .adapter.pypdf2_merger import PyPDF2Merger
from .entity.pdf_document import MergerError, PDFDocument, PDFMerger
from .usecase.merge_documents import merge_documents

__all__ = [
    "PDFDocument",
    "PDFMerger",
    "MergerError",
    "PyPDF2Merger",
    "merge_documents",
]
