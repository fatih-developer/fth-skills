#!/usr/bin/env python3
"""Publish public skills from this repository to ClawHub.

The source of truth for public skills is skills.sh.json. By default this script
only prints the commands it would run. Pass --execute to publish.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
INDEX_PATH = REPO_ROOT / "skills.sh.json"
EXCLUDED_SKILLS = {"eachlabs-kling-generator"}
DEFAULT_CHANGELOG = "Initial ClawHub release"


@dataclass(frozen=True)
class SkillEntry:
    slug: str
    path: Path


def display_command(args: list[str]) -> str:
    return shlex.join(args)


def load_indexed_skills() -> list[str]:
    if not INDEX_PATH.exists():
        raise RuntimeError(f"Missing public skill index: {INDEX_PATH}")

    try:
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise RuntimeError(f"Invalid JSON in {INDEX_PATH}: {err}") from err

    groupings = index.get("groupings")
    if not isinstance(groupings, list):
        raise RuntimeError(f"{INDEX_PATH} must contain a 'groupings' array")

    skills: list[str] = []
    for group in groupings:
        if not isinstance(group, dict):
            raise RuntimeError("Each skills.sh.json grouping must be an object")
        group_skills = group.get("skills")
        if not isinstance(group_skills, list):
            title = group.get("title", "<untitled>")
            raise RuntimeError(f"Grouping {title!r} must contain a 'skills' array")
        for skill in group_skills:
            if not isinstance(skill, str) or not skill:
                raise RuntimeError(f"Invalid skill entry in skills.sh.json: {skill!r}")
            skills.append(skill)

    return skills


def validate_public_skills(indexed_skills: list[str]) -> list[SkillEntry]:
    duplicates = sorted({skill for skill in indexed_skills if indexed_skills.count(skill) > 1})
    if duplicates:
        raise RuntimeError(f"Duplicate skill(s) in skills.sh.json: {', '.join(duplicates)}")

    if not SKILLS_ROOT.exists():
        raise RuntimeError(f"Missing skills directory: {SKILLS_ROOT}")

    public_dirs = sorted(
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and path.name not in EXCLUDED_SKILLS
    )
    missing_from_index = sorted(set(public_dirs) - set(indexed_skills))
    unknown_in_index = sorted(set(indexed_skills) - set(public_dirs))

    if missing_from_index:
        raise RuntimeError(
            "Skill folder(s) missing from skills.sh.json: " + ", ".join(missing_from_index)
        )
    if unknown_in_index:
        raise RuntimeError(
            "skills.sh.json references unknown skill folder(s): " + ", ".join(unknown_in_index)
        )

    entries: list[SkillEntry] = []
    for slug in indexed_skills:
        skill_dir = SKILLS_ROOT / slug
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            raise RuntimeError(f"Missing SKILL.md for indexed skill: {slug}")
        entries.append(SkillEntry(slug=slug, path=skill_dir))

    return entries


def build_publish_command(
    clawhub_cmd: list[str],
    entry: SkillEntry,
    version: str,
    tags: str,
    changelog: str,
) -> list[str]:
    return [
        *clawhub_cmd,
        "publish",
        str(entry.path),
        "--slug",
        entry.slug,
        "--name",
        entry.slug,
        "--version",
        version,
        "--changelog",
        changelog,
        "--tags",
        tags,
    ]


def build_inspect_command(clawhub_cmd: list[str], slug: str) -> list[str]:
    return [*clawhub_cmd, "inspect", slug]


def run_command(args: list[str]) -> None:
    print(f"[RUN] {display_command(args)}")
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or publish public fth-skills entries to ClawHub."
    )
    parser.add_argument(
        "--skill",
        action="append",
        help="Publish only the named skill. Can be passed more than once.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run ClawHub publish and inspect commands. Default is dry-run.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the public skill list and exit without printing publish commands.",
    )
    parser.add_argument("--version", default="1.0.0", help="Version to publish.")
    parser.add_argument("--tags", default="latest", help="Comma-separated ClawHub tags.")
    parser.add_argument(
        "--changelog",
        default=DEFAULT_CHANGELOG,
        help="Changelog text for ClawHub publish.",
    )
    parser.add_argument(
        "--clawhub-cmd",
        default="npx clawhub",
        help="Command used to invoke ClawHub. Default: 'npx clawhub'.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        indexed_skills = load_indexed_skills()
        entries = validate_public_skills(indexed_skills)
        by_slug = {entry.slug: entry for entry in entries}

        if args.skill:
            unknown = sorted(set(args.skill) - set(by_slug))
            if unknown:
                raise RuntimeError("Requested skill(s) are not public: " + ", ".join(unknown))
            entries = [by_slug[slug] for slug in args.skill]

        print(f"[OK] Public ClawHub skill list validated: {len(entries)} skill(s).")

        if args.check_only:
            return 0

        clawhub_cmd = shlex.split(args.clawhub_cmd)
        if not clawhub_cmd:
            raise RuntimeError("--clawhub-cmd cannot be empty")

        for entry in entries:
            publish_cmd = build_publish_command(
                clawhub_cmd=clawhub_cmd,
                entry=entry,
                version=args.version,
                tags=args.tags,
                changelog=args.changelog,
            )
            inspect_cmd = build_inspect_command(clawhub_cmd, entry.slug)

            if args.execute:
                run_command(publish_cmd)
                run_command(inspect_cmd)
            else:
                print(f"[DRY-RUN] {display_command(publish_cmd)}")
                print(f"[DRY-RUN] {display_command(inspect_cmd)}")

        if not args.execute:
            print("\nDry-run only. Pass --execute to publish to ClawHub.")

        return 0
    except subprocess.CalledProcessError as err:
        print(f"[FAIL] Command exited with status {err.returncode}", file=sys.stderr)
        return err.returncode
    except RuntimeError as err:
        print(f"[FAIL] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
