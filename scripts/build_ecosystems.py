#!/usr/bin/env python3
"""Build every ecosystem-derived artifact from skills/ecosystem-*/references/workflows.json.

The workflow maps are the single source of truth. This script renders:

* the catalog, workflow, and router blocks inside each ecosystem SKILL.md
* the "🔗 Next Steps & Handoffs" block inside every member skill
* the ecosystem index inside the hub and planner skills
* the shared installer script and handoff contract inside each ecosystem skill
* the groupings in skills.sh.json
* the skill catalog and counts in README.md

Usage:
    python scripts/build_ecosystems.py           # write changes
    python scripts/build_ecosystems.py --check   # exit 1 if anything is out of date
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
TEMPLATES = REPO / "scripts" / "templates" / "ecosystem"
REPO_SLUG = "fatih-developer/fth-skills"

# Display order of ecosystems in the README, skills.sh.json, and indexes.
ORDER = [
    "ecosystem-orchestration",
    "ecosystem-reasoning",
    "ecosystem-api",
    "ecosystem-database",
    "ecosystem-mobile",
    "ecosystem-web",
    "ecosystem-product",
    "ecosystem-security",
]
# Skills that embed the cross-ecosystem index.
INDEX_HOSTS = ["ecosystem-orchestration", "task-decomposer", "parallel-planner"]
GEN_NOTE = "generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand"
HANDOFF_HEADING = "## 🔗 Next Steps & Handoffs"


# --------------------------------------------------------------------------- loading


def load_ecosystems() -> dict[str, dict]:
    ecos = {}
    for path in sorted(SKILLS.glob("ecosystem-*/references/workflows.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        ecos[data["ecosystem"]] = data
    missing = [e for e in ORDER if e not in ecos]
    extra = [e for e in ecos if e not in ORDER]
    if missing or extra:
        raise SystemExit(f"ORDER mismatch: missing={missing} extra={extra}")
    return {e: ecos[e] for e in ORDER}


def short_description(skill: str) -> str:
    data = yaml.safe_load((SKILLS / skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    return data["interface"]["short_description"].strip()


def owner_map(ecos: dict[str, dict]) -> dict[str, str]:
    owners = {}
    for eco, data in ecos.items():
        for member in data["members"]:
            owners[member] = eco
    return owners


# --------------------------------------------------------------------------- helpers


def block(name: str, body: str) -> str:
    return f"<!-- BEGIN GENERATED: {name} ({GEN_NOTE}) -->\n{body.rstrip()}\n<!-- END GENERATED: {name} -->"


def replace_block(text: str, name: str, body: str, path: Path) -> str:
    pattern = re.compile(
        rf"<!-- BEGIN GENERATED: {re.escape(name)}\b.*?-->.*?<!-- END GENERATED: {re.escape(name)} -->",
        re.S,
    )
    if not pattern.search(text):
        raise SystemExit(f"{path}: missing generated block markers for '{name}'")
    return pattern.sub(lambda _: block(name, body), text, count=1)


def skill_ref(name: str) -> str:
    return f"`@{name}`"


def step_label(step: dict) -> str:
    label = skill_ref(step["skill"])
    if step.get("optional"):
        label += " *(optional)*"
    return label


def stages(steps: list[dict]) -> list[list[int]]:
    """Group consecutive steps that share a parallel_group into one stage."""
    result: list[list[int]] = []
    for i, step in enumerate(steps):
        group = step.get("parallel_group")
        if result and group and steps[result[-1][0]].get("parallel_group") == group:
            result[-1].append(i)
        else:
            result.append([i])
    return result


# --------------------------------------------------------------------------- ecosystem SKILL.md blocks


def render_catalog(eco: str, data: dict) -> str:
    deprecated = data.get("deprecated", {})
    lines = [
        f"**Domain:** {data['title']} — {data['summary']}",
        "",
        f"**Philosophy:** {data['philosophy']}",
        "",
        "| Skill | Role | Handoff artifact |",
        "|---|---|---|",
    ]
    for name, member in data["members"].items():
        role = member["role"]
        if name in deprecated:
            role = f"Deprecated alias — use {skill_ref(deprecated[name])}."
        artifact = f"`{member['artifact']}`" if member.get("artifact") else "inline handoff block"
        lines.append(f"| {skill_ref(name)} | {role} | {artifact} |")
    return "\n".join(lines)


def render_workflows(eco: str, data: dict) -> str:
    out = []
    for n, wf in enumerate(data["workflows"], 1):
        out.append(f"### {n}. {wf['title']} (`{wf['id']}`)")
        out.append("")
        out.append("**When:** " + "; ".join(f"“{w}”" for w in wf["when"]))
        out.append("")
        out.append("| # | Skill | Does | Done when | Condition | Parallel group |")
        out.append("|---|---|---|---|---|---|")
        for i, step in enumerate(wf["steps"], 1):
            cond = step.get("condition", "—")
            group = f"`{step['parallel_group']}`" if step.get("parallel_group") else "—"
            out.append(f"| {i} | {step_label(step)} | {step['do']} | {step['done_when']} | {cond} | {group} |")
        out.append("")
    if data.get("handoffs"):
        out.append("### Direct handoffs")
        out.append("")
        for h in data["handoffs"]:
            out.append(f"- {skill_ref(h['from'])} → {skill_ref(h['to'])}: {h['when']}.")
        out.append("")
    if data.get("gates"):
        out.append("### Gate precedence")
        out.append("")
        out.append(
            "Run **at most one** clarification gate per request, choosing the first one whose condition holds. "
            "A gate that another gate already satisfied must be skipped. `@checkpoint-guardian` is not a "
            "clarification gate; it always applies before irreversible actions."
        )
        out.append("")
        for i, g in enumerate(data["gates"], 1):
            out.append(f"{i}. {skill_ref(g['skill'])} — {g['applies']}.")
        out.append("")
    return "\n".join(out)


ROUTER = """\
Follow this protocol whenever this ecosystem is invoked.

1. **Match.** Compare the request with each workflow's *When* phrases. Pick one workflow, or route straight to a single member skill when the request is narrow. If two workflows fit equally, ask one question to choose. If the request belongs to another domain, use the ecosystem index in `@ecosystem-orchestration`.
2. **Preflight.** Find out which step skills are installed: check the skills your host lists, or run `python <skill-dir>/scripts/install_all.py --status --workflow <id>` (`<skill-dir>` is the folder containing this `SKILL.md`). Show a short plan: step, skill, installed or missing, condition, expected artifact.
3. **Missing skills never block.** Offer once: (a) install them — `install_all.py --workflow <id>` prints the commands and only runs them with `--execute` after the user agrees; or (b) continue in fallback mode — perform the step yourself using its *Does* and *Done when* columns and label that output `fallback`.
4. **Conditions.** Skip optional steps whose condition does not hold, and say which steps you skipped and why.
5. **Execute.** Run steps in order. Steps that share a parallel group are independent and may run concurrently (`@parallel-planner`). Pass artifacts as described in `references/handoff-contract.md`. Check each step's *Done when* before moving on.
6. **Gates.** Before any destructive, irreversible, or production-impacting action, stop at `@checkpoint-guardian`, or ask for explicit confirmation when it is not installed.
7. **Failures.** When a step misses its *Done when*, hand off to `@error-recovery`. Without it, retry once with a changed approach, then report the blocker with evidence instead of guessing.
8. **State.** Keep a run log (workflow id, step, status, artifact). Record it with `@memory-ledger` when installed, and write a `@session-transfer` handoff if the run will continue in another session.
9. **Finish.** Summarize artifacts, skipped steps, open risks, and the most relevant next workflow.

**Skip this protocol** when the user names one specific skill (invoke it directly) or asks a quick factual question that needs no workflow."""


def render_index(ecos: dict[str, dict]) -> str:
    lines = [
        "| Ecosystem | Domain | Use for | Workflows |",
        "|---|---|---|---|",
    ]
    for eco, data in ecos.items():
        wfs = ", ".join(f"`{w['id']}`" for w in data["workflows"])
        lines.append(f"| {skill_ref(eco)} | {data['title']} | {data['summary']} | {wfs} |")
    lines.append("")
    lines.append(
        "Pick the ecosystem whose domain matches the request and follow its workflow map. If the ecosystem skill is "
        "not installed, use the workflow ids above as the plan skeleton and run each member skill directly, or install "
        f"it with `npx skills add {REPO_SLUG} --skill <ecosystem>` after the user agrees. Never invent skills that are not listed."
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------- member handoffs


def render_handoffs(skill: str, ecos: dict[str, dict], owners: dict[str, str]) -> str:
    eco = owners[skill]
    data = ecos[eco]
    member = data["members"][skill]
    lines = [f"**Ecosystem:** {skill_ref(eco)} — {data['title']}."]

    wf_lines = []
    for e, d in ecos.items():
        for wf in d["workflows"]:
            steps = wf["steps"]
            stage_list = stages(steps)
            for si, stage in enumerate(stage_list):
                for idx in stage:
                    if steps[idx]["skill"] != skill:
                        continue
                    where = f"step {idx + 1} of {len(steps)}"
                    if e != eco:
                        where += f", via {skill_ref(e)}"
                    if si + 1 < len(stage_list):
                        nxt = stage_list[si + 1]
                        targets = ", ".join(step_label(steps[j]) for j in nxt)
                        if len(nxt) > 1:
                            targets += " (can run in parallel)"
                        follow = f"next → {targets}"
                    else:
                        follow = "last step → once it passes, complete the workflow and report the outcome"
                    wf_lines.append(f"- **{wf['title']}** (`{wf['id']}`, {where}): {follow}.")
    if wf_lines:
        lines += ["", "**Workflows:**"] + wf_lines

    direct = [h for d in ecos.values() for h in d.get("handoffs", []) if h["from"] == skill]
    direct += [{"to": h["to"], "when": h["when"]} for h in member.get("handoffs", [])]
    if direct:
        lines += ["", "**Direct handoffs:**"]
        lines += [f"- {skill_ref(h['to'])} — {h['when']}." for h in direct]

    artifact = member.get("artifact")
    target = f"`{artifact}`" if artifact else "an inline *Handoff* block in your reply"
    lines += [
        "",
        f"**Handoff contract:** pass results to the next skill through {target} with the fields `skill`, "
        f"`workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of {skill_ref(eco)}). If a next skill is not installed, continue with its step from the "
        f"ecosystem map, or install it with `npx skills add {REPO_SLUG} --skill <name>` after the user agrees.",
    ]
    return "\n".join(lines)


def apply_handoff_section(text: str, body: str) -> str:
    section = f"{HANDOFF_HEADING}\n\n{block('handoffs', body)}\n"
    # Replace an existing handoff section (heading up to the next H2 or EOF).
    pattern = re.compile(r"^## 🔗 Next Steps(?: & Handoffs)?[^\n]*\n.*?(?=^## |\Z)", re.S | re.M)
    if pattern.search(text):
        return pattern.sub(lambda _: section + "\n", text, count=1).rstrip() + "\n"
    return text.rstrip() + "\n\n" + section


# --------------------------------------------------------------------------- registry and README


def render_groupings(ecos: dict[str, dict]) -> list[dict]:
    groups = [{"title": "Ecosystem Hubs", "skills": list(ecos)}]
    deprecated = []
    for eco, data in ecos.items():
        dep = data.get("deprecated", {})
        deprecated += list(dep)
        groups.append({"title": data["title"], "skills": sorted(m for m in data["members"] if m not in dep)})
    if deprecated:
        groups.append({"title": "Deprecated Aliases", "skills": sorted(deprecated)})
    return groups


def md_row(name: str) -> str:
    return f"| **{name}** | `--skill {name}` | {short_description(name)} |"


def render_readme_catalog(ecos: dict[str, dict]) -> str:
    out = []
    deprecated = {}
    for eco, data in ecos.items():
        dep = data.get("deprecated", {})
        deprecated.update(dep)
        members = [m for m in data["members"] if m not in dep]
        out.append(f"### {data['title']} ({len(members)} + hub)")
        out.append("")
        out.append(f"_{data['summary']}_ Workflows: " + ", ".join(f"`{w['id']}`" for w in data["workflows"]) + ".")
        out.append("")
        out.append("| Skill | Install | Description |")
        out.append("|---|---|---|")
        out.append(md_row(eco))
        out += [md_row(m) for m in members]
        out.append("")
    if deprecated:
        out.append("### Deprecated aliases")
        out.append("")
        out.append("Kept so existing installs keep working. They route to the canonical skill and never trigger implicitly.")
        out.append("")
        out.append("| Alias | Use instead |")
        out.append("|---|---|")
        out += [f"| `{a}` | `{t}` |" for a, t in sorted(deprecated.items())]
    return "\n".join(out)


def public_count(ecos: dict[str, dict]) -> int:
    deprecated = {a for d in ecos.values() for a in d.get("deprecated", {})}
    return len([p for p in SKILLS.iterdir() if (p / "SKILL.md").exists() and p.name not in deprecated])


# --------------------------------------------------------------------------- build


def build() -> dict[Path, str]:
    ecos = load_ecosystems()
    owners = owner_map(ecos)
    deprecated = {a for d in ecos.values() for a in d.get("deprecated", {})}
    outputs: dict[Path, str] = {}

    def current(path: Path) -> str:
        return outputs.get(path) or path.read_text(encoding="utf-8")

    installer = (TEMPLATES / "install_all.py").read_text(encoding="utf-8")
    contract = (TEMPLATES / "handoff-contract.md").read_text(encoding="utf-8")
    index = render_index(ecos)

    for eco, data in ecos.items():
        path = SKILLS / eco / "SKILL.md"
        text = current(path)
        text = replace_block(text, "ecosystem-catalog", render_catalog(eco, data), path)
        text = replace_block(text, "ecosystem-workflows", render_workflows(eco, data), path)
        text = replace_block(text, "ecosystem-router", ROUTER, path)
        outputs[path] = text
        outputs[SKILLS / eco / "scripts" / "install_all.py"] = installer
        outputs[SKILLS / eco / "references" / "handoff-contract.md"] = contract

    for host in INDEX_HOSTS:
        path = SKILLS / host / "SKILL.md"
        outputs[path] = replace_block(current(path), "ecosystem-index", index, path)

    for skill, eco in owners.items():
        if skill in deprecated:
            continue
        path = SKILLS / skill / "SKILL.md"
        outputs[path] = apply_handoff_section(current(path), render_handoffs(skill, ecos, owners))

    registry_path = REPO / "skills.sh.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["groupings"] = render_groupings(ecos)
    outputs[registry_path] = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"

    readme_path = REPO / "README.md"
    readme = replace_block(current(readme_path), "skill-catalog", render_readme_catalog(ecos), readme_path)
    count = public_count(ecos)
    readme = re.sub(r"skills-\d+%20Public", f"skills-{count}%20Public", readme)
    readme = re.sub(r"Skills: \d+\]", f"Skills: {count}]", readme)
    readme = re.sub(r"Available Skills \(\d+ Public\)", f"Available Skills ({count} Public)", readme)
    outputs[readme_path] = readme
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Report out-of-date files and exit 1 instead of writing")
    args = parser.parse_args()

    stale = []
    for path, content in build().items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == content:
            continue
        stale.append(path)
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    rel = [str(p.relative_to(REPO)) for p in stale]
    if args.check:
        if rel:
            print("Out of date (run: python scripts/build_ecosystems.py):")
            print("\n".join(f"  {r}" for r in rel))
            return 1
        print("Ecosystem artifacts are up to date.")
        return 0
    print(f"Updated {len(rel)} file(s)." + ("".join(f"\n  {r}" for r in rel) if rel else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
