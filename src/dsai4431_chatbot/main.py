"""Command-line entry point for DSAI4431 Chatbot."""

from __future__ import annotations

import argparse

from dsai4431_chatbot import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dsai4431-chatbot",
        description="DSAI4431 Chatbot",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="message to send to the bot (interactive prompt when omitted)",
    )
    return parser


def reply(message: str) -> str:
    """Return the bot's answer to a single message."""
    if not message.strip():
        return "Please say something."
    return f"echo: {message}"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = " ".join(args.message)

    if text:
        print(reply(text))
        return 0

    try:
        while True:
            line = input("you> ")
            if line.strip().lower() in {"exit", "quit"}:
                break
            print(f"bot> {reply(line)}")
    except (EOFError, KeyboardInterrupt):
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
