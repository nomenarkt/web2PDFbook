import logging
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from logger import get_logger  # noqa: E402


def test_get_logger_reuses_instance():
    logger1 = get_logger("sample")
    logger2 = get_logger("sample")
    assert logger1 is logger2
    assert logger1.handlers
    assert isinstance(logger1.handlers[0], logging.Handler)
