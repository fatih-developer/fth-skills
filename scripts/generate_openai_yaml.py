#!/usr/bin/env python3
"""Create agents/openai.yaml for skills that do not have one yet.

The generated file is a starting point: display_name comes from the folder name,
short_description from the first sentence of the SKILL.md description (never
truncated). If that sentence is longer than the validator allows, the script
says so and you must shorten it by hand.

Usage:
    python scripts/generate_openai_yaml.py            # all skills missing the file
    python scripts/generate_openai_yaml.py my-skill   # one skill
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
MAX_SHORT = 150
ACRONYMS = {"api", "sdk", "db", "geo", "ugc", "ui", "ux", "b2b", "md"}


def display_name(folder: str) -> str:
    return " ".join(w.upper() if w in ACRONYMS else w.capitalize() for w in folder.split("-"))


def description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    return str(yaml.safe_load(text[4:end])["description"]).strip()


def first_sentence(text: str) -> str:
    match = re.match(r"(.+?[.!?])(\s|$)", text)
    return (match.group(1) if match else text).strip()


def render(name: str, short: str) -> str:
    q = lambda s: json.dumps(s, ensure_ascii=False)  # noqa: E731 - valid YAML double-quoted string
    return (
        "interface:\n"
        f"  display_name: {q(display_name(name))}\n"
        f"  short_description: {q(short)}\n"
        f"  default_prompt: {q(f'Use ${name} to help with this task.')}\n"
        "\n"
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )


def main() -> int:
    targets = sys.argv[1:] or sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").exists())
    created = 0
    for name in targets:
        skill_dir = SKILLS / name
        path = skill_dir / "agents" / "openai.yaml"
        if path.exists():
            continue
        short = first_sentence(description(skill_dir / "SKILL.md"))
        path.parent.mkdir(exist_ok=True)
        path.write_text(render(name, short), encoding="utf-8")
        created += 1
        print(f"[OK]   {path.relative_to(REPO)}")
        if len(short) > MAX_SHORT:
            print(f"[EDIT] short_description is {len(short)} characters; shorten it to {MAX_SHORT} or fewer.")
        print("[EDIT] Replace the generic default_prompt with one that describes the task.")
    print(f"Created {created} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
