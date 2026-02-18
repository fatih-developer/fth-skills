#!/usr/bin/env python3
"""Validate curated skills in this repository."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
PATH_REF_RE = re.compile(r"(?:references|templates|scripts|assets|agents)/[A-Za-z0-9._/-]+")


@dataclass
class SkillIssue:
    skill: str
    message: str


def parse_frontmatter(skill_md_path: Path) -> dict[str, str]:
    text = skill_md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimiter '---'.")

    end_index = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = idx
            break
    if end_index is None:
        raise ValueError("SKILL.md frontmatter must end with delimiter '---'.")

    parsed: dict[str, str] = {}
    for line in lines[1:end_index]:
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            raise ValueError(f"Invalid frontmatter line: '{line}'.")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Invalid frontmatter key in line: '{line}'.")
        if not value:
            raise ValueError(f"Frontmatter key '{key}' must have a non-empty value.")

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1].strip()
        parsed[key] = value

    return parsed


def extract_referenced_paths(skill_md_path: Path) -> set[str]:
    text = skill_md_path.read_text(encoding="utf-8")
    matches = set()
    for match in PATH_REF_RE.finditer(text):
        raw = match.group(0).rstrip("`.,:;)]}\"'")
        matches.add(raw)
    return matches


def validate_skill_dir(skill_dir: Path) -> list[SkillIssue]:
    issues: list[SkillIssue] = []
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        issues.append(SkillIssue(skill_name, "Missing SKILL.md"))
        return issues

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as err:
        issues.append(SkillIssue(skill_name, str(err)))
        return issues

    missing = REQUIRED_FRONTMATTER_KEYS - set(frontmatter.keys())
    if missing:
        issues.append(SkillIssue(skill_name, f"Missing required frontmatter keys: {sorted(missing)}"))

    extra = set(frontmatter.keys()) - REQUIRED_FRONTMATTER_KEYS
    if extra:
        issues.append(SkillIssue(skill_name, f"Unexpected frontmatter keys: {sorted(extra)}"))

    declared_name = frontmatter.get("name", "")
    if declared_name and declared_name != skill_name:
        issues.append(
            SkillIssue(
                skill_name,
                f"Frontmatter name '{declared_name}' does not match folder name '{skill_name}'",
            )
        )

    if not frontmatter.get("description", "").strip():
        issues.append(SkillIssue(skill_name, "Frontmatter 'description' must be non-empty"))

    agents_dir = skill_dir / "agents"
    if agents_dir.exists() and not (agents_dir / "openai.yaml").exists():
        issues.append(SkillIssue(skill_name, "agents/ exists but agents/openai.yaml is missing"))

    for rel_path in sorted(extract_referenced_paths(skill_md)):
        if not (skill_dir / rel_path).exists():
            issues.append(SkillIssue(skill_name, f"Referenced path not found: {rel_path}"))

    return issues


def list_skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted([p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")], key=lambda p: p.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all curated skills in this repository.")
    parser.add_argument(
        "--root",
        default="skills/.curated",
        help="Skill root directory to validate (default: skills/.curated)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    root = (repo_root / args.root).resolve()

    skill_dirs = list_skill_dirs(root)
    if not skill_dirs:
        print(f"No skill directories found under: {root}")
        return 1

    all_issues: list[SkillIssue] = []
    for skill_dir in skill_dirs:
        all_issues.extend(validate_skill_dir(skill_dir))

    if all_issues:
        print("Validation failed:\n")
        for issue in all_issues:
            print(f"- [{issue.skill}] {issue.message}")
        print(f"\nTotal issues: {len(all_issues)}")
        return 1

    print(f"Validation passed for {len(skill_dirs)} skill(s) under {root}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
