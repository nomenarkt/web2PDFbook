from __future__ import annotations

import argparse
import asyncio

from .usecase import book_creator
from .config import load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Web2PDFBook CLI")
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Base documentation URLs followed by the destination PDF file",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=load_config().timeout,
        help="Render timeout in milliseconds",
    )
    parser.add_argument(
        "--use-index",
        action="store_true",
        help="Use navigation index to find pages",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if len(args.inputs) < 2:
        parser.error("must provide at least one URL and an output file")
    args.urls = args.inputs[:-1]
    args.output = args.inputs[-1]
    del args.inputs
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    asyncio.run(
        book_creator.run(
            args.urls,
            args.output,
            timeout=args.timeout,
            use_index=args.use_index,
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    raise SystemExit(main())
