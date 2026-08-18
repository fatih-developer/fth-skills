#!/usr/bin/env python3
"""RESUME: select the handoff to load without scanning every historical file."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from session_transfer_lib import (
    DetectionSignals,
    detect_existing_agent_dirs,
    recover_indexes,
    select_handoff,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select the session-transfer handoff to resume.")
    parser.add_argument("--workspace", default=".", help="Project root (default: current directory)")
    parser.add_argument("--agent", default=None, help="Explicit current agent/runtime")
    parser.add_argument("--topic", default=None, help="Prefer a matching unfinished topic")
    parser.add_argument(
        "--recover",
        action="store_true",
        help="Rebuild indexes from JSONL/handoff files if navigation is missing.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve()
    signals = DetectionSignals(
        env=dict(os.environ),
        explicit_instruction=args.agent,
        existing_agent_dirs=detect_existing_agent_dirs(workspace),
    )

    global_index = workspace / ".session-transfer" / "INDEX.md"
    if args.recover or not global_index.is_file():
        report = recover_indexes(workspace)
        print(report.message)

    try:
        selection = select_handoff(workspace, signals=signals, topic=args.topic)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"Selected: {selection.handoff_repo_path}")
    print(f"Source agent: {selection.source_agent}")
    print(f"Cross-agent: {'yes' if selection.cross_agent else 'no'}")
    print(f"Reason: {selection.reason}")
    print("Read the selected handoff, then reconcile with git/repo state before continuing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
