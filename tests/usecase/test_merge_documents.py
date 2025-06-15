import sys
from pathlib import Path

import pytest
from PyPDF2 import PdfReader, PdfWriter

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from merger import MergerError, PyPDF2Merger, merge_documents  # noqa: E402


def create_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with path.open("wb") as f:
        writer.write(f)


def test_merge_documents_success(tmp_path):
    pdf1 = tmp_path / "1.pdf"
    pdf2 = tmp_path / "2.pdf"
    create_pdf(pdf1)
    create_pdf(pdf2)

    output = tmp_path / "out.pdf"
    merger = PyPDF2Merger()
    assert merge_documents([str(pdf1), str(pdf2)], str(output), merger=merger) is True

    reader = PdfReader(str(output))
    assert len(reader.pages) == 2


@pytest.mark.parametrize(
    "inputs,output,exc",
    [
        ([], "out.pdf", MergerError),
        (["missing.pdf"], "out.pdf", MergerError),
        (["file.txt"], "out.pdf", MergerError),
        (["1.pdf"], "out.txt", MergerError),
    ],
)
def test_merge_documents_invalid(tmp_path, inputs, output, exc):
    for inp in inputs:
        if inp.endswith(".pdf") and inp != "missing.pdf":
            create_pdf(tmp_path / inp)
        else:
            (tmp_path / inp).write_text("not pdf")
    inputs = [str(tmp_path / inp) for inp in inputs]
    output = str(tmp_path / output)
    merger = PyPDF2Merger()
    with pytest.raises(exc):
        merge_documents(inputs, output, merger=merger)
