#!/usr/bin/env python3
"""List available handoff documents in a project."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


def list_handoffs(path: Path) -> list[tuple[Path, datetime | None, str]]:
    """Find all .md handoff files in .claude/handoffs/."""
    handoffs_dir = path / ".claude" / "handoffs"
    if not handoffs_dir.exists():
        return []

    results: list[tuple[Path, datetime | None, str]] = []
    for f in sorted(handoffs_dir.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8")
            # Extract title from first H1
            title = f.stem  # default to filename
            for line in content.split("\n")[:10]:
                if line.startswith("# Handoff:"):
                    title = line.replace("# Handoff:", "").strip()
                    break

            # Try to extract date from filename (YYYY-MM-DD-HHMMSS-slug.md)
            ts = None
            m = _TS_RE.match(f.stem)
            if m:
                try:
                    ts = datetime.strptime(m.group(1), "%Y-%m-%d-%H%M%S")
                except ValueError:
                    pass

            results.append((f, ts, title))
        except Exception:
            results.append((f, None, f.stem))

    return results


_TS_RE = __import__("re").compile(r"^(\d{4}-\d{2}-\d{2}-\d{6})-")


def format_results(results: list[tuple[Path, datetime | None, str]]) -> str:
    if not results:
        return "No handoff documents found.\n"

    lines = ["Found handoff documents:\n"]
    for f, ts, title in results:
        ts_str = ts.strftime("%Y-%m-%d %H:%M") if ts else "unknown date"
        lines.append(f"  {ts_str}  {title}")
        lines.append(f"           {f}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="List available handoff documents.")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to search for handoffs (default: current directory)",
    )
    args = parser.parse_args()

    search_path = Path(args.path).resolve()
    results = list_handoffs(search_path)
    print(format_results(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
