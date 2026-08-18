#!/usr/bin/env python3
"""Validate a handoff document for completeness, quality, and security."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|apikey|secret[_-]?key)"), "API key pattern"),
    (re.compile(r"(?i)(password|passwd|pwd)"), "Password pattern"),
    (re.compile(r"(?i)(bearer|token|auth[_-]?token)"), "Auth token pattern"),
    (re.compile(r"(?i)(aws[_-]?access[_-]?key|aws[_-]?secret)"), "AWS credential pattern"),
    (re.compile(r"(?i)(ghp_|github_pat_)"), "GitHub token pattern"),
    (re.compile(r"sk-[a-zA-Z0-9]{20,}"), "OpenAI API key pattern"),
]

# New names first; older CREATE scaffolds remain valid.
REQUIRED_SECTION_ALIASES = [
    ("Current State", ("Current State", "Current State Summary")),
    ("Next Recommended Action", ("Next Recommended Action", "Immediate Next Steps")),
    ("Resume Instructions", ("Resume Instructions", "Important Context")),
    ("Architecture & Decisions", ("Architecture & Decisions", "Decisions Made")),
]


def check_secrets(content: str) -> list[str]:
    found: list[str] = []
    for pattern, name in SECRET_PATTERNS:
        if pattern.search(content):
            found.append(name)
    return found


def check_todos(content: str) -> int:
    return len(re.findall(r"\[TODO[:\s]", content))


def check_sections(content: str) -> list[str]:
    missing: list[str] = []
    for canonical, aliases in REQUIRED_SECTION_ALIASES:
        if not any(alias in content for alias in aliases):
            missing.append(canonical)
    return missing


def calculate_score(content: str) -> int:
    score = 100
    score -= min(check_todos(content) * 10, 40)
    score -= len(check_sections(content)) * 15
    if check_secrets(content):
        score -= 50
    return max(0, min(100, score))


def validate_handoff(path: Path) -> tuple[int, list[str], list[str], int]:
    if not path.exists():
        raise FileNotFoundError(f"Handoff not found: {path}")
    content = path.read_text(encoding="utf-8")
    secrets = check_secrets(content)
    missing_sections = check_sections(content)
    todos = check_todos(content)
    return calculate_score(content), secrets, missing_sections, todos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a handoff document.")
    parser.add_argument("file", help="Path to handoff file to validate")
    args = parser.parse_args(argv)

    path = Path(args.file).resolve()
    try:
        score, secrets, missing, todos = validate_handoff(path)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1

    print(f"Handoff: {path.name}")
    print(f"Score: {score}/100")

    if secrets:
        print("\n[FAIL] Secrets detected:")
        for item in secrets:
            print(f"  - {item}")
    else:
        print("[OK] No secrets detected")

    if missing:
        print("\n[WARN] Missing sections:")
        for item in missing:
            print(f"  - {item}")

    if todos > 0:
        print(f"\n[WARN] {todos} TODO placeholder(s) remaining")

    if score < 70:
        print("\n[FAIL] Score below 70 — do not finalize without improvements.")
        return 1
    if secrets:
        print("\n[FAIL] Secrets detected — remove before finalizing.")
        return 1
    print("\n[PASS] Handoff is ready to use.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
