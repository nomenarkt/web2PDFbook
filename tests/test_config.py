import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from config import load_config  # noqa: E402


def test_load_config_env(monkeypatch):
    monkeypatch.setenv("WEB2PDFBOOK_TIMEOUT", "9999")
    cfg = load_config()
    assert cfg.timeout == 9999
