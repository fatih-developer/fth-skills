#!/usr/bin/env python3
"""Check staleness of a handoff document."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_file_modified_time(path: Path) -> datetime | None:
    """Get when file was last modified."""
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime)
    except Exception:
        return None


def get_git_commits_after(path: Path) -> list[str]:
    """Get git commits since handoff was modified."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", f"--since={datetime.fromtimestamp(path.stat().st_mtime).isoformat()}", "-10"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
    except Exception:
        pass
    return []


def get_git_status() -> list[str]:
    """Get modified files in git status."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
    except Exception:
        pass
    return []


def assess_staleness(
    path: Path,
    file_mtime: datetime | None,
    commits: list[str],
    status_files: list[str],
) -> tuple[str, list[str]]:
    """Assess staleness level and return (level, reasons)."""
    reasons: list[str] = []
    now = datetime.now()

    if file_mtime is None:
        return "UNKNOWN", ["Could not determine file modification time"]

    age = now - file_mtime
    reasons.append(f"Handoff created: {file_mtime.strftime('%Y-%m-%d %H:%M')} ({_format_delta(age)})")

    if commits:
        reasons.append(f"Git commits since: {len(commits)}")
    if status_files:
        reasons.append(f"Files modified locally: {len(status_files)}")

    if age > timedelta(days=7):
        return "VERY_STALE", reasons

    if age > timedelta(days=2) or len(commits) > 10 or len(status_files) > 15:
        return "STALE", reasons

    if age > timedelta(hours=12) or commits or status_files:
        return "SLIGHTLY_STALE", reasons

    return "FRESH", reasons


def _format_delta(delta: timedelta) -> str:
    """Format timedelta as human readable string."""
    if delta < timedelta(hours=1):
        mins = int(delta.total_seconds() / 60)
        return f"{mins} minute{'s' if mins != 1 else ''} ago"
    if delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = int(delta.total_seconds() / 86400)
    return f"{days} day{'s' if days != 1 else ''} ago"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check staleness of a handoff document.")
    parser.add_argument("file", help="Path to handoff file")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    if not path.exists():
        print(f"[ERROR] Handoff not found: {path}")
        return 1

    file_mtime = get_file_modified_time(path)
    commits = get_git_commits_after(path)
    status_files = get_git_status()

    level, reasons = assess_staleness(path, file_mtime, commits, status_files)

    print(f"Handoff: {path.name}")
    print(f"Staleness: {level}")
    for reason in reasons:
        print(f"  {reason}")

    print()
    if level == "FRESH":
        print("[OK] Safe to resume — minimal changes since handoff")
    elif level == "SLIGHTLY_STALE":
        print("[INFO] Review changes, then resume")
    elif level == "STALE":
        print("[WARN] Verify context carefully before resuming")
    elif level == "VERY_STALE":
        print("[WARN] Consider creating a fresh handoff")

    return 0


if __name__ == "__main__":
    sys.exit(main())
