#!/usr/bin/env python3
"""Generate agents/openai.yaml for all skills missing it."""

import re
from pathlib import Path

SKILLS_ROOT = Path("skills")

SKILL_DISPLAY_NAMES = {
    "access-policy-designer": "Access Policy Designer",
    "accessibility-enforcer": "Accessibility Enforcer",
    "api-mock-designer": "API Mock Designer",
    "api-observability-planner": "API Observability Planner",
    "app-store-reviewer": "App Store Reviewer",
    "auth-flow-designer": "Auth Flow Designer",
    "breaking-change-detector": "Breaking Change Detector",
    "changelog-generator": "Changelog Generator",
    "contract-first-designer": "Contract-First Designer",
    "crash-analyst": "Crash Analyst",
    "data-lineage-tracer": "Data Lineage Tracer",
    "data-masker": "Data Masker",
    "deep-link-architect": "Deep Link Architect",
    "index-advisor": "Index Advisor",
    "migration-strategist": "Migration Strategist",
    "mobile-perf-auditor": "Mobile Perf Auditor",
    "mobile-security-auditor": "Mobile Security Auditor",
    "offline-sync-designer": "Offline Sync Designer",
    "onboarding-designer": "Onboarding Designer",
    "protocol-selector": "Protocol Selector",
    "push-notification-planner": "Push Notification Planner",
    "query-budget-enforcer": "Query Budget Enforcer",
    "query-explainer": "Query Explainer",
    "rate-limit-strategist": "Rate Limit Strategist",
    "release-orchestrator": "Release Orchestrator",
    "schema-architect": "Schema Architect",
    "schema-diff-analyzer": "Schema Diff Analyzer",
    "sdk-scaffolder": "SDK Scaffolder",
    "seed-data-generator": "Seed Data Generator",
    "task-decomposer": "Task Decomposer",
    "webhook-architect": "Webhook Architect",
}


def extract_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    # Extract from YAML frontmatter
    m = re.search(r'^---\s*\n.*?description:\s*(.+?)(?:\n\S|\n---)', text, re.DOTALL)
    if m:
        desc = m.group(1).strip().replace('\n', ' ')
        # Truncate to ~120 chars for yaml short_description
        if len(desc) > 120:
            desc = desc[:117].rsplit(' ', 1)[0] + '...'
        return desc
    return "A specialized skill for AI agents."


def make_yaml(display_name: str, short_description: str, default_prompt: str) -> str:
    return f'''interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
  default_prompt: "{default_prompt}"

policy:
  allow_implicit_invocation: true
'''


created = 0
for skill_dir in sorted(SKILLS_ROOT.iterdir()):
    if not skill_dir.is_dir():
        continue
    name = skill_dir.name
    if name not in SKILL_DISPLAY_NAMES:
        continue

    agents_dir = skill_dir / "agents"
    yaml_path = agents_dir / "openai.yaml"

    if yaml_path.exists():
        print(f"[SKIP] {name} already has openai.yaml")
        continue

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"[WARN] {name} missing SKILL.md")
        continue

    desc = extract_description(skill_md)
    display = SKILL_DISPLAY_NAMES[name]
    default_prompt = f"Use ${name} to help with this task."

    agents_dir.mkdir(exist_ok=True)
    yaml_path.write_text(make_yaml(display, desc, default_prompt), encoding="utf-8")
    print(f"[OK]   Created {yaml_path}")
    created += 1

print(f"\nDone. Created {created} openai.yaml files.")
