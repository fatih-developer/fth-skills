#!/usr/bin/env python3
"""Show status of, and optionally install, the skills of this ecosystem.

This file is generated from scripts/templates/ecosystem/install_all.py by
scripts/build_ecosystems.py. Edit the template, not the copies.

Dry-run by default: it prints the install commands and changes nothing.

Examples:
    python install_all.py --list
    python install_all.py --status
    python install_all.py --workflow api-design           # print commands for one workflow
    python install_all.py --workflow api-design --missing-only --execute
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_SLUG = "fatih-developer/fth-skills"
HERE = Path(__file__).resolve().parent
WORKFLOWS = HERE.parent / "references" / "workflows.json"

# Folders where hosts commonly install skills, relative to the project and to $HOME.
PROJECT_DIRS = [".claude/skills", ".agents/skills", ".agent/skills", ".codex/skills", ".opencode/skills", ".cursor/skills", "skills"]
HOME_DIRS = [".claude/skills", ".agents/skills", ".codex/skills", ".config/opencode/skills"]


def load() -> dict:
    return json.loads(WORKFLOWS.read_text(encoding="utf-8"))


def search_dirs(extra: list[str]) -> list[Path]:
    cwd = Path.cwd()
    home = Path.home()
    dirs = [Path(p).expanduser() for p in extra]
    dirs += [cwd / d for d in PROJECT_DIRS] + [home / d for d in HOME_DIRS]
    # The folder this ecosystem skill was installed into holds its siblings.
    dirs.append(HERE.parent.parent)
    seen, result = set(), []
    for d in dirs:
        key = str(d.resolve()) if d.exists() else str(d)
        if key not in seen:
            seen.add(key)
            result.append(d)
    return result


def installed_at(skill: str, dirs: list[Path]) -> Path | None:
    for d in dirs:
        candidate = d / skill / "SKILL.md"
        if candidate.is_file():
            return candidate.parent
    return None


def selected_skills(data: dict, workflow: str | None) -> list[str]:
    if not workflow:
        names = [data["ecosystem"], *data["members"]]
    else:
        match = [w for w in data["workflows"] if w["id"] == workflow]
        if not match:
            ids = ", ".join(w["id"] for w in data["workflows"])
            sys.exit(f"Unknown workflow '{workflow}'. Available: {ids}")
        names = [s["skill"] for s in match[0]["steps"]]
    deprecated = set(data.get("deprecated", {}))
    ordered = []
    for n in names:
        if n not in deprecated and n not in ordered:
            ordered.append(n)
    return ordered


def command(skill: str) -> list[str]:
    return ["npx", "skills", "add", REPO_SLUG, "--skill", skill]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="List workflows and member skills")
    parser.add_argument("--status", action="store_true", help="Show which skills are installed")
    parser.add_argument("--workflow", help="Limit to the skills used by one workflow id")
    parser.add_argument("--missing-only", action="store_true", help="Only act on skills that are not installed")
    parser.add_argument("--skills-dir", action="append", default=[], help="Extra folder to search for installed skills")
    parser.add_argument("--execute", action="store_true", help="Run the install commands (default: print only)")
    args = parser.parse_args()

    data = load()
    if args.list:
        print(f"{data['ecosystem']} — {data['title']}")
        for w in data["workflows"]:
            print(f"  {w['id']}: {w['title']} -> " + ", ".join(s["skill"] for s in w["steps"]))
        return 0

    dirs = search_dirs(args.skills_dir)
    skills = selected_skills(data, args.workflow)
    status = {s: installed_at(s, dirs) for s in skills}

    if args.status:
        for s in skills:
            where = status[s]
            print(f"{'installed' if where else 'missing  '}  {s}" + (f"  ({where})" if where else ""))
        missing = [s for s in skills if not status[s]]
        print(f"\n{len(skills) - len(missing)}/{len(skills)} installed.")
        return 0

    targets = [s for s in skills if not (args.missing_only and status[s])]
    if not targets:
        print("Nothing to install.")
        return 0

    if not args.execute:
        print("Dry run. Re-run with --execute (after the user agrees) to install:")
        for s in targets:
            print("  " + " ".join(command(s)))
        return 0

    npx = shutil.which("npx")
    if not npx:
        sys.exit("npx was not found. Install Node.js, or run the printed commands in another shell.")
    failed = []
    for s in targets:
        print(f"Installing {s} ...", flush=True)
        result = subprocess.run([npx, *command(s)[1:]], env=os.environ.copy())
        if result.returncode != 0:
            failed.append(s)
    if failed:
        print("Failed: " + ", ".join(failed))
        return 1
    print(f"Installed {len(targets)} skill(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
