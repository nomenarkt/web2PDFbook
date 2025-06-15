import logging

from web2pdfbook.logger import get_logger


def test_get_logger_reuses_instance():
    logger1 = get_logger("sample")
    logger2 = get_logger("sample")
    assert logger1 is logger2
    assert logger1.handlers
    assert isinstance(logger1.handlers[0], logging.Handler)
