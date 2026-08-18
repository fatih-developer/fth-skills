#!/usr/bin/env python3
"""Check staleness of a handoff document against current repo state."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from session_transfer_lib import parse_handoff_metadata


def get_file_modified_time(path: Path) -> datetime | None:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime)
    except Exception:
        return None


def get_git_commits_after(path: Path) -> list[str]:
    try:
        since = datetime.fromtimestamp(path.stat().st_mtime).isoformat()
        result = subprocess.run(
            ["git", "log", "--oneline", f"--since={since}", "-10"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


def get_git_status() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


def referenced_files_missing(path: Path) -> list[str]:
    missing: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return missing
    root = path.parent
    while root != root.parent and not (root / ".git").exists():
        root = root.parent
    for match in __import__("re").findall(r"`([^`]+)`", content):
        if "/" not in match and "\\" not in match:
            continue
        if match.endswith(".md") and "handoff" in match.replace("\\", "/"):
            continue
        candidate = root / match
        if match.startswith(".") and not candidate.exists():
            continue
        if any(part in match for part in ("src/", "skills/", "scripts/", "app/", "lib/")):
            if not candidate.exists() and not (Path.cwd() / match).exists():
                missing.append(match)
    return missing


def assess_staleness(
    path: Path,
    file_mtime: datetime | None,
    commits: list[str],
    status_files: list[str],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    now = datetime.now()

    if file_mtime is None:
        return "UNKNOWN", ["Could not determine file modification time"]

    age = now - file_mtime
    reasons.append(f"Handoff created: {file_mtime.strftime('%Y-%m-%d %H:%M')} ({_format_delta(age)})")
    meta = {}
    try:
        meta = parse_handoff_metadata(path.read_text(encoding="utf-8"))
    except Exception:
        meta = {}
    if meta.get("commit"):
        reasons.append(f"Handoff commit: {meta['commit']}")
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
    if delta < timedelta(hours=1):
        mins = int(delta.total_seconds() / 60)
        return f"{mins} minute{'s' if mins != 1 else ''} ago"
    if delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = int(delta.total_seconds() / 86400)
    return f"{days} day{'s' if days != 1 else ''} ago"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check staleness of a handoff document.")
    parser.add_argument("file", help="Path to handoff file")
    args = parser.parse_args(argv)

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

    missing = referenced_files_missing(path)
    if missing:
        print("  Missing referenced files:")
        for item in missing[:10]:
            print(f"    - {item}")

    print()
    if level == "FRESH":
        print("[OK] Safe to resume — reconcile Next Recommended Action, then continue")
    elif level == "SLIGHTLY_STALE":
        print("[INFO] Review changes, then resume from Next Recommended Action")
    elif level == "STALE":
        print("[WARN] Verify context carefully before resuming — do not trust the handoff blindly")
    elif level == "VERY_STALE":
        print("[WARN] Consider creating a fresh handoff after reconciling repo state")
    return 0


if __name__ == "__main__":
    sys.exit(main())
