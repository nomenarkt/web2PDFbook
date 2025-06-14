from __future__ import annotations


def ensure_pdf_extension(path: str) -> str:
    """Return ``path`` with a ``.pdf`` extension if missing."""
    if not path.lower().endswith(".pdf"):
        return f"{path}.pdf"
    return path
