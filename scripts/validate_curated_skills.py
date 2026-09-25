#!/usr/bin/env python3
"""Validate curated skills in this repository.

Checks every skill folder for the rules that skills.sh discovery, the ecosystem
router, and agents rely on. Exit code 1 means at least one error.

Usage:
    python scripts/validate_curated_skills.py
    python scripts/validate_curated_skills.py --root skills/.experimental
"""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
MAX_DESCRIPTION = 1024
MAX_SHORT_DESCRIPTION = 150
MAX_SKILL_LINES = 500
TRIGGER_RE = re.compile(r"\b(use when|use for|use only when|use it when|use this skill|trigger|triggers|invoke|kullan|tetikle)\b", re.I)
# A relative path inside the skill folder; not preceded by a path character (so ".agents/x" is ignored).
PATH_REF_RE = re.compile(r"(?<![\w./~-])((?:references|templates|scripts|assets|agents|examples|evals)/[A-Za-z0-9._/-]+)")
SKILL_REF_RE = re.compile(r"`@([a-z0-9]+(?:-[a-z0-9]+)+)`")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
ORPHAN_DIRS = ("references", "templates", "examples", "assets")
HANDOFF_MARKER = "<!-- BEGIN GENERATED: handoffs"


@dataclass
class Issue:
    skill: str
    message: str


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' frontmatter delimiter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter must end with a '---' delimiter")
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as err:
        raise ValueError(f"frontmatter is not valid YAML: {str(err).splitlines()[0]}") from err
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def nested_fences(text: str) -> int:
    """Count fence-opening lines that appear inside an already open fence of the same length."""
    open_fence = None
    bad = 0
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if not m:
            continue
        fence, info = m.group(1), m.group(2).strip()
        if open_fence is None:
            open_fence = fence
        elif fence[0] == open_fence[0] and len(fence) >= len(open_fence):
            if info:
                bad += 1
            else:
                open_fence = None
    return bad + (1 if open_fence else 0)


def tracked_files() -> set[str] | None:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return set(out.splitlines())


def load_ecosystems() -> dict[str, dict]:
    ecos = {}
    for path in sorted((REPO / "skills").glob("ecosystem-*/references/workflows.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        ecos[data["ecosystem"]] = data
    return ecos


def validate_skill(skill_dir: Path, all_names: set[str], aliases: set[str], tracked: set[str] | None) -> list[Issue]:
    name = skill_dir.name
    issues: list[Issue] = []

    def err(msg: str) -> None:
        issues.append(Issue(name, msg))

    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    try:
        fm = parse_frontmatter(text)
    except ValueError as e:
        err(str(e))
        return issues

    keys = set(fm)
    if REQUIRED_FRONTMATTER_KEYS - keys:
        err(f"missing frontmatter keys: {sorted(REQUIRED_FRONTMATTER_KEYS - keys)}")
    if keys - REQUIRED_FRONTMATTER_KEYS:
        err(f"unexpected frontmatter keys: {sorted(keys - REQUIRED_FRONTMATTER_KEYS)}")
    if fm.get("name") != name:
        err(f"frontmatter name '{fm.get('name')}' does not match folder name")
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        err("description must be a non-empty string")
    else:
        if len(desc) > MAX_DESCRIPTION:
            err(f"description is {len(desc)} characters (max {MAX_DESCRIPTION})")
        if not TRIGGER_RE.search(desc):
            err("description must say when to use the skill (e.g. 'Use when ...')")

    lines = text.count("\n") + 1
    if lines > MAX_SKILL_LINES:
        err(f"SKILL.md has {lines} lines (max {MAX_SKILL_LINES}); move detail into references/")

    if nested_fences(text):
        err("nested or unclosed code fence; use a longer outer fence (````) around blocks that contain ``` fences")

    # agents/openai.yaml
    yaml_path = skill_dir / "agents" / "openai.yaml"
    yaml_text = ""
    if not yaml_path.exists():
        err("missing agents/openai.yaml (required for skills.sh discovery)")
    else:
        yaml_text = yaml_path.read_text(encoding="utf-8")
        try:
            data = yaml.safe_load(yaml_text) or {}
        except yaml.YAMLError as e:
            err(f"agents/openai.yaml is not valid YAML: {str(e).splitlines()[0]}")
            data = {}
        iface = data.get("interface") or {}
        for key in ("display_name", "short_description", "default_prompt"):
            if not iface.get(key):
                err(f"agents/openai.yaml missing interface.{key}")
        short = str(iface.get("short_description", "")).strip()
        if short.endswith(("...", "…")):
            err("agents/openai.yaml short_description is truncated ('...')")
        if len(short) > MAX_SHORT_DESCRIPTION:
            err(f"agents/openai.yaml short_description is {len(short)} characters (max {MAX_SHORT_DESCRIPTION})")
        if f"${name}" not in str(iface.get("default_prompt", "")):
            err(f"agents/openai.yaml default_prompt must mention ${name}")
        policy = data.get("policy") or {}
        if not isinstance(policy.get("allow_implicit_invocation"), bool):
            err("agents/openai.yaml policy.allow_implicit_invocation must be true or false")
        if name in aliases and policy.get("allow_implicit_invocation") is not False:
            err("deprecated alias must set allow_implicit_invocation: false")
        for key in ("icon_small", "icon_large"):
            icon = iface.get(key)
            if icon and not (skill_dir / icon).exists():
                err(f"agents/openai.yaml {key} not found: {icon}")

    # Referenced local paths
    for match in sorted(set(PATH_REF_RE.findall(text))):
        rel = match.rstrip("`.,:;)]}\"'")
        if not (skill_dir / rel).exists():
            err(f"referenced path not found: {rel}")

    # Referenced skills
    for ref in sorted(set(SKILL_REF_RE.findall(text))):
        if ref not in all_names:
            err(f"references unknown skill @{ref}")

    # Orphan supporting files
    corpus = text + "\n" + yaml_text
    for sub in ORPHAN_DIRS:
        base = skill_dir / sub
        if not base.is_dir():
            continue
        for f in sorted(p for p in base.rglob("*") if p.is_file()):
            rel = f.relative_to(skill_dir).as_posix()
            if f.name not in corpus and rel not in corpus:
                err(f"orphan file not referenced from SKILL.md: {rel}")

    # Evals
    evals = skill_dir / "evals"
    if evals.is_dir():
        for f in sorted(p for p in evals.iterdir() if p.is_file()):
            if f.suffix != ".json":
                err(f"evals must be JSON: evals/{f.name}")
                continue
            try:
                json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                err(f"evals/{f.name} is not valid JSON: {e}")

    # Handoff section
    if not name.startswith("ecosystem-") and name not in aliases and HANDOFF_MARKER not in text:
        err("missing generated '🔗 Next Steps & Handoffs' section (run scripts/build_ecosystems.py)")

    # Committed bytecode
    if tracked is not None:
        prefix = skill_dir.relative_to(REPO).as_posix() + "/"
        for f in tracked:
            if f.startswith(prefix) and ("__pycache__/" in f or f.endswith(".pyc")):
                err(f"compiled Python file is committed: {f}")
    return issues


def validate_repo(skill_dirs: list[Path], ecos: dict[str, dict]) -> list[Issue]:
    issues: list[Issue] = []
    names = {d.name for d in skill_dirs}

    # Ecosystem membership: every skill belongs to exactly one ecosystem.
    owners = Counter(m for data in ecos.values() for m in data["members"])
    for n in sorted(names):
        if n.startswith("ecosystem-"):
            if n not in ecos:
                issues.append(Issue(n, "ecosystem skill has no references/workflows.json"))
            continue
        if owners[n] == 0:
            issues.append(Issue(n, "not a member of any ecosystem workflows.json"))
        elif owners[n] > 1:
            issues.append(Issue(n, "member of more than one ecosystem"))
    for eco, data in ecos.items():
        refs = set(data["members"])
        for wf in data["workflows"]:
            refs |= {s["skill"] for s in wf["steps"]}
        for h in data.get("handoffs", []):
            refs |= {h["from"], h["to"]}
        for m in data["members"].values():
            refs |= {h["to"] for h in m.get("handoffs", [])}
        for r in sorted(refs - names):
            issues.append(Issue(eco, f"workflows.json references unknown skill '{r}'"))
        ids = [w["id"] for w in data["workflows"]]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            issues.append(Issue(eco, f"duplicate workflow id '{dup}'"))

    # skills.sh.json registration
    registry = json.loads((REPO / "skills.sh.json").read_text(encoding="utf-8"))
    listed = Counter(s for g in registry.get("groupings", []) for s in g["skills"])
    for n in sorted(names):
        if listed[n] != 1:
            issues.append(Issue(n, f"listed {listed[n]} time(s) in skills.sh.json (expected 1)"))
    for n in sorted(set(listed) - names):
        issues.append(Issue(n, "listed in skills.sh.json but the folder does not exist"))

    # README catalog
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    for n in sorted(names):
        if f"**{n}**" not in readme and f"`{n}`" not in readme:
            issues.append(Issue(n, "missing from README catalog"))

    # Generated artifacts in sync
    try:
        import build_ecosystems

        for path, content in build_ecosystems.build().items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                issues.append(Issue("build", f"out of date: {path.relative_to(REPO)} (run python scripts/build_ecosystems.py)"))
    except SystemExit as e:
        issues.append(Issue("build", f"build_ecosystems failed: {e}"))
    return issues


def list_skill_dirs(root: Path) -> list[Path]:
    dirs = []
    for skill_md in root.rglob("SKILL.md"):
        parent = skill_md.parent
        if not any(part.startswith(".") for part in parent.relative_to(root).parts):
            dirs.append(parent)
    return sorted(dirs, key=lambda p: p.name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all curated skills in this repository.")
    parser.add_argument("--root", default="skills", help="Skill root directory to validate (default: skills)")
    args = parser.parse_args()

    root = (REPO / args.root).resolve()
    skill_dirs = list_skill_dirs(root)
    if not skill_dirs:
        print(f"No skill directories found under: {root}")
        return 1

    ecos = load_ecosystems()
    aliases = {a for d in ecos.values() for a in d.get("deprecated", {})}
    all_names = {p.name for p in list_skill_dirs(REPO / "skills")} | {d.name for d in skill_dirs}
    tracked = tracked_files()

    issues: list[Issue] = []
    for d in skill_dirs:
        issues += validate_skill(d, all_names, aliases, tracked)
    if root == (REPO / "skills").resolve():
        issues += validate_repo(skill_dirs, ecos)

    if issues:
        print(f"Errors ({len(issues)}):\n")
        for i in issues:
            print(f"  [FAIL] [{i.skill}] {i.message}")
        print(f"\nValidation FAILED — {len(issues)} error(s).")
        return 1
    print(f"Validation PASSED for {len(skill_dirs)} skill(s) under {root}.")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.exit(main())
