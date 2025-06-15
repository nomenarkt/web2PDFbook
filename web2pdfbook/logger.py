from __future__ import annotations

import logging
from logging import Logger

from rich.logging import RichHandler


def get_logger(name: str) -> Logger:
    """Return a configured logger with rich output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, show_time=False)
        formatter = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
