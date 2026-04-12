#!/usr/bin/env python3
"""Validate a handoff document for completeness, quality, and security."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|apikey|secret[_-]?key)", re.I), "API key pattern"),
    (re.compile(r"(?i)(password|passwd|pwd)", re.I), "Password pattern"),
    (re.compile(r"(?i)(bearer|token|auth[_-]?token)", re.I), "Auth token pattern"),
    (re.compile(r"(?i)(aws[_-]?access[_-]?key|aws[_-]?secret)", re.I), "AWS credential pattern"),
    (re.compile(r"(?i)(ghp_|github_pat_)", re.I), "GitHub token pattern"),
    (re.compile(r"sk-[a-zA-Z0-9]{20,}", re.I), "OpenAI API key pattern"),
]

REQUIRED_SECTIONS = [
    "Current State Summary",
    "Immediate Next Steps",
    "Important Context",
    "Decisions Made",
]


def check_secrets(content: str) -> list[str]:
    """Check for potential secrets in content."""
    found: list[str] = []
    for pattern, name in SECRET_PATTERNS:
        if pattern.search(content):
            found.append(name)
    return found


def check_todos(content: str) -> int:
    """Count remaining TODO placeholders."""
    return len(re.findall(r"\[TODO[:\s]", content))


def check_sections(content: str) -> list[str]:
    """Check for required sections."""
    missing: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing.append(section)
    return missing


def calculate_score(content: str) -> int:
    """Calculate quality score 0-100."""
    score = 100

    # Deduct for TODOs
    todos = check_todos(content)
    score -= min(todos * 10, 40)

    # Deduct for missing sections
    missing = check_sections(content)
    score -= len(missing) * 15

    # Deduct for secrets (major issue)
    secrets = check_secrets(content)
    if secrets:
        score -= 50

    return max(0, min(100, score))


def validate_handoff(path: Path) -> tuple[int, list[str], list[str], list[str]]:
    """Validate handoff file. Returns (score, secrets, missing_sections, todos)."""
    if not path.exists():
        raise FileNotFoundError(f"Handoff not found: {path}")

    content = path.read_text(encoding="utf-8")
    secrets = check_secrets(content)
    missing_sections = check_sections(content)
    todos = check_todos(content)
    score = calculate_score(content)

    return score, secrets, missing_sections, todos


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a handoff document.")
    parser.add_argument("file", help="Path to handoff file to validate")
    args = parser.parse_args()

    path = Path(args.file).resolve()
    try:
        score, secrets, missing, todos = validate_handoff(path)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1

    print(f"Handoff: {path.name}")
    print(f"Score: {score}/100")

    if secrets:
        print(f"\n[FAIL] Secrets detected:")
        for s in secrets:
            print(f"  - {s}")
    else:
        print("[OK] No secrets detected")

    if missing:
        print(f"\n[WARN] Missing sections:")
        for s in missing:
            print(f"  - {s}")

    if todos > 0:
        print(f"\n[WARN] {todos} TODO placeholder(s) remaining")

    if score < 70:
        print(f"\n[FAIL] Score below 70 — do not finalize without improvements.")
        return 1
    elif secrets:
        print(f"\n[FAIL] Secrets detected — remove before finalizing.")
        return 1
    else:
        print(f"\n[PASS] Handoff is ready to use.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
