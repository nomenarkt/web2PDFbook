import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from utils import ensure_pdf_extension


def test_ensure_pdf_extension():
    assert ensure_pdf_extension("file") == "file.pdf"
    assert ensure_pdf_extension("doc.PDF") == "doc.PDF"
