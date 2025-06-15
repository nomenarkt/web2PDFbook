from web2pdfbook.utils import ensure_pdf_extension


def test_ensure_pdf_extension():
    assert ensure_pdf_extension("file") == "file.pdf"
    assert ensure_pdf_extension("doc.PDF") == "doc.PDF"
