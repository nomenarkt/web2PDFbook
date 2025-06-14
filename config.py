from __future__ import annotations

from dataclasses import dataclass
import os

# Utility configuration helpers

DEFAULT_TIMEOUT = 15000


@dataclass(slots=True)
class Config:
    """Application configuration loaded from environment variables."""

    timeout: int = DEFAULT_TIMEOUT


def load_config() -> Config:
    """Load configuration from environment variables."""
    timeout = int(os.environ.get("WEB2PDFBOOK_TIMEOUT", DEFAULT_TIMEOUT))
    return Config(timeout=timeout)
