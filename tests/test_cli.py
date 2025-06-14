import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pytest

from cli import parse_args


def test_parse_args_valid():
    args = parse_args(["https://example.com", "out.pdf", "--timeout", "2000"])
    assert args.url == "https://example.com"
    assert args.output == "out.pdf"
    assert args.timeout == 2000


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["https://example.com"],
    ],
)
def test_parse_args_missing(argv):
    with pytest.raises(SystemExit):
        parse_args(argv)

