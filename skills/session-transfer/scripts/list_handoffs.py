#!/usr/bin/env python3
"""List available handoff documents across agent directories."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from session_transfer_lib import list_handoff_records


def format_results(records) -> str:
    if not records:
        return "No handoff documents found.\n"

    lines = ["Found handoff documents:\n"]
    for rec in records:
        when = rec.created[:16].replace("T", " ") if rec.created else "unknown date"
        title = rec.topic or rec.id
        path = rec.repo_path or rec.file
        status = rec.status or "—"
        agent = rec.agent or "—"
        lines.append(f"  {when}  [{agent}] {title} ({status})")
        lines.append(f"           {path}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List available handoff documents.")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to search for handoffs (default: current directory)",
    )
    args = parser.parse_args(argv)
    records = list_handoff_records(Path(args.path).resolve())
    print(format_results(records))
    return 0


if __name__ == "__main__":
    sys.exit(main())
