#!/usr/bin/env python3
"""Fix unquoted double quotes inside description values in SKILL.md frontmatter."""

import re
from pathlib import Path

SKILLS_ROOT = Path("skills")
QUOTE = chr(34)  # "

for skill_dir in sorted(SKILLS_ROOT.iterdir()):
    if not skill_dir.is_dir():
        continue
    md = skill_dir / "SKILL.md"
    if not md.exists():
        continue

    text = md.read_text(encoding="utf-8")
    original = text

    # Find the frontmatter block (between --- markers)
    match = re.match(r'---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        continue

    frontmatter = match.group(1)
    if QUOTE not in frontmatter:
        continue

    # Check if it's in a description value (not wrapped in quotes)
    desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
    if not desc_match:
        continue

    desc_value = desc_match.group(1)
    if QUOTE not in desc_value:
        continue

    # Replace inner double quotes with single quotes in description
    new_desc_value = desc_value.replace(QUOTE, "'")
    new_frontmatter = frontmatter[:desc_match.start(1)] + new_desc_value + frontmatter[desc_match.end(1):]
    new_text = text[:match.start(1)] + new_frontmatter + text[match.end(1):]

    md.write_text(new_text, encoding="utf-8")
    print(f"[FIXED] {skill_dir.name}")
    print(f"  Before: ...{desc_value[:80]}...")
    print(f"  After:  ...{new_desc_value[:80]}...")

print("\nDone.")
