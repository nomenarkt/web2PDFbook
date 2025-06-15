from __future__ import annotations

import asyncio
import sys

from .book_creator import run

if __name__ == "__main__":  # pragma: no cover - manual invocation only
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python main.py <url> <output> [timeout]")
    url = sys.argv[1]
    output = sys.argv[2]
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 15000
    asyncio.run(run(url, output, timeout))
