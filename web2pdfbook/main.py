from __future__ import annotations

import asyncio

from .cli_runner import run
from .cli import parse_args

if __name__ == "__main__":  # pragma: no cover - manual invocation only
    args = parse_args()
    asyncio.run(run(args.urls, args.output, timeout=args.timeout))
