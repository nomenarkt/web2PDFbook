from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Web2PDFBook CLI")
    parser.add_argument("url", help="Base documentation URL")
    parser.add_argument("output", help="Destination PDF file")
    parser.add_argument(
        "--timeout",
        type=int,
        default=15000,
        help="Render timeout in milliseconds",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


if __name__ == "__main__":  # pragma: no cover - manual invocation only
    args = parse_args()
    print(f"URL: {args.url} -> {args.output} (timeout={args.timeout})")
