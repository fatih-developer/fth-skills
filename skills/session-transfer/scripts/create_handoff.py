#!/usr/bin/env python3
"""CREATE: write an immutable timestamped handoff and update indexes."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from session_transfer_lib import (
    DetectionSignals,
    collect_git_info,
    collect_modified_files,
    create_handoff,
    detect_existing_agent_dirs,
    normalize_status,
    normalize_trigger,
)


def _parse_now(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create an immutable session-transfer handoff and update indexes."
    )
    parser.add_argument("topic", help="Short topic or slug (e.g. dashboard-ui)")
    parser.add_argument(
        "--workspace",
        default=".",
        help="Project root (default: current directory)",
    )
    parser.add_argument(
        "--agent",
        default=None,
        help="Explicit agent/runtime (codex, claude, opencode). Overrides weaker signals.",
    )
    parser.add_argument("--status", default="in-progress", help="completed|in-progress|partial|blocked|interrupted")
    parser.add_argument(
        "--trigger",
        default="manual",
        help="manual|goal-completion|substantial-work|context-pressure|agent-transfer|interrupted",
    )
    parser.add_argument("--goal-status", dest="goal_status", default=None)
    parser.add_argument("--branch", default=None, help="Git branch if already known")
    parser.add_argument("--commit", default=None, help="Git commit if already known")
    parser.add_argument("--source-model", dest="source_model", default=None)
    parser.add_argument("--objective", default=None)
    parser.add_argument("--current-state", dest="current_state", default=None)
    parser.add_argument("--work-completed", dest="work_completed", default=None)
    parser.add_argument("--next-action", dest="next_action", default=None)
    parser.add_argument("--remaining-work", dest="remaining_work", default=None)
    parser.add_argument("--resume-instructions", dest="resume_instructions", default=None)
    parser.add_argument("--continues-from", dest="continues_from", default=None, help="previous_session id")
    parser.add_argument("--resumed-from", dest="resumed_from", default=None, help="Repo-relative prior handoff path")
    parser.add_argument("--now", default=None, help="ISO timestamp for tests / deterministic names")
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Do not inspect git; only persist fields that were provided.",
    )
    parser.add_argument(
        "--print-full",
        action="store_true",
        help="Also print the handoff body (off by default).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve()
    git_info = {} if args.no_git else collect_git_info(workspace)
    if args.branch:
        git_info["branch"] = args.branch
    if args.commit:
        git_info["commit"] = args.commit

    files_changed = None if args.no_git else collect_modified_files(workspace)

    signals = DetectionSignals(
        env=dict(__import__("os").environ),
        explicit_instruction=args.agent,
        existing_agent_dirs=detect_existing_agent_dirs(workspace),
    )

    result = create_handoff(
        workspace,
        topic=args.topic,
        status=normalize_status(args.status),
        trigger=normalize_trigger(args.trigger),
        signals=signals,
        now=_parse_now(args.now),
        git_info=git_info,
        objective=args.objective,
        current_state=args.current_state,
        work_completed=args.work_completed,
        files_changed=files_changed,
        remaining_work=args.remaining_work,
        next_recommended_action=args.next_action,
        resume_instructions=args.resume_instructions,
        previous_session=args.continues_from,
        resumed_from=args.resumed_from,
        source_model=args.source_model,
        goal_status=args.goal_status,
    )

    sys.stdout.write(result.confirmation)
    if args.print_full:
        sys.stdout.write("\n")
        sys.stdout.write(result.handoff_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
