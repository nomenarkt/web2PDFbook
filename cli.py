from __future__ import annotations

import argparse
import asyncio

from config import load_config
from book_creator import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Web2PDFBook CLI")
    parser.add_argument("url", help="Base documentation URL")
    parser.add_argument("output", help="Destination PDF file")
    parser.add_argument(
        "--timeout",
        type=int,
        default=load_config().timeout,
        help="Render timeout in milliseconds",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    asyncio.run(run(args.url, args.output, timeout=args.timeout))
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    raise SystemExit(main())
