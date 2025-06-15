from __future__ import annotations

from ..entity.pdf_document import MergerError, PDFMerger, validate_paths


def merge_documents(
    input_paths: list[str],
    output_path: str,
    *,
    merger: PDFMerger,
) -> bool:
    """Validate inputs and delegate PDF merging."""
    validate_paths(input_paths, output_path)
    try:
        merger.merge(input_paths, output_path)
    except MergerError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise MergerError(str(exc)) from exc
    return True
