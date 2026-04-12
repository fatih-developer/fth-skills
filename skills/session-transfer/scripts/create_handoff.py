#!/usr/bin/env python3
"""Generate a new handoff document with smart scaffolding."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def get_git_info() -> dict[str, str]:
    """Get current git branch, commit, and project root."""
    import subprocess

    info: dict[str, str] = {
        "branch": "unknown",
        "commit": "unknown",
        "root": str(Path.cwd()),
    }

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            info["branch"] = result.stdout.strip()
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            info["commit"] = result.stdout.strip()
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            info["root"] = result.stdout.strip()
    except Exception:
        pass

    return info


def get_recent_commits(count: int = 5) -> list[str]:
    """Get recent commit messages."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{count}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
    except Exception:
        pass
    return []


def get_modified_files() -> list[str]:
    """Get list of modified files."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            files = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    # Get filename (skip status chars)
                    parts = line.strip().split(" ", 1)
                    if len(parts) > 1:
                        files.append(parts[1].strip())
            return files
    except Exception:
        pass
    return []


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text


def generate_handoff_content(
    slug: str,
    continues_from: str | None,
    git_info: dict[str, str],
    recent_commits: list[str],
    modified_files: list[str],
) -> str:
    """Generate handoff document content."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    chain_section = ""
    if continues_from:
        chain_section = f"\n## Handoff Chain\n\n- Continues from: {continues_from}\n"

    modified_section = ""
    if modified_files:
        files_table = "\n".join(
            f"| {f} | Modified | — |" for f in modified_files[:20]
        )
        modified_section = f"\n### Files Modified\n\n| File | Changes | Rationale |\n|------|---------|-----------|\n{files_table}\n"

    commits_section = ""
    if recent_commits:
        commits_list = "\n".join(f"- {c}" for c in recent_commits)
        commits_section = f"\n### Recent Commits\n\n{commits_list}\n"

    return f"""# Handoff: {slug.replace('-', ' ').title()}

## Session Metadata

- Created: {timestamp}
- Project: {git_info['root']}
- Branch: {git_info['branch']}
- Commit: {git_info['commit']}
- Session duration: [APPROX_DURATION]

## Current State Summary

[TODO: Write 1-2 paragraphs describing what is happening right now, current status, and where things left off]

## Codebase Understanding

### Architecture Overview

[TODO: Describe the key architectural insights — how the system is structured, main components, data flow]

### Critical Files

| File | Purpose | Relevance |
|------|---------|-----------|
| [path/to/file] | [what this file does] | [why it matters] |

### Key Patterns Discovered

[TODO: Document important patterns, conventions, or idioms the next agent should follow]

## Work Completed

### Tasks Finished

- [TODO: List completed tasks with brief descriptions]

{modified_section}### Decisions Made

| Decision | Options Considered | Rationale |
|----------|-------------------|-----------|
| [Decision made] | [X, Y, Z] | [Why X was chosen] |

{commits_section}
## Pending Work

### Immediate Next Steps

1. [TODO: Most critical next action — what to do first]
2. [Second priority]
3. [Third priority]

### Blockers/Open Questions

- [ ] Blocker: [description] — Needs: [what's required to unblock]
- [ ] Question: [unclear aspect] — Suggested: [potential resolution]

### Deferred Items

- [TODO: Item 1 (deferred because: [reason])]

## Context for Resuming Agent

### Important Context

[TODO: Critical information the next agent MUST know — this is the most important section]

### Assumptions Made

- Assumption 1: [what was assumed to be true]
- Assumption 2: [another assumption]

### Potential Gotchas

- [TODO: Things that might trip up a new agent — edge cases, quirks, non-obvious behavior]

## Environment State

### Tools/Services Used

- [TODO: Tool/Service: relevant configuration or state]

### Active Processes

- [TODO: Any background processes, dev servers, watchers that may be running]

### Environment Variables

- [TODO: Key env vars that matter — DO NOT include secrets/values, just names]

## Related Resources

- [TODO: Link to relevant documentation, related file paths, external resources]

{chain_section}
---

## Validation Required

Before finalizing, run:

```bash
python skills/session-transfer/scripts/validate_handoff.py <this-file>
```

Score must be 70+ and no secrets detected.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a new handoff document with smart scaffolding.")
    parser.add_argument("slug", help="Short slug for this task (e.g., implementing-auth)")
    parser.add_argument(
        "--continues-from",
        dest="continues_from",
        default=None,
        help="Previous handoff file to link from (e.g., 2024-01-15-auth.md)",
    )
    args = parser.parse_args()

    git_info = get_git_info()
    recent_commits = get_recent_commits()
    modified_files = get_modified_files()

    filename_ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    safe_slug = slugify(args.slug)
    output_name = f"{filename_ts}-{safe_slug}.md"

    handoffs_dir = Path.cwd() / ".claude" / "handoffs"
    handoffs_dir.mkdir(parents=True, exist_ok=True)

    output_path = handoffs_dir / output_name

    content = generate_handoff_content(
        slug=safe_slug,
        continues_from=args.continues_from,
        git_info=git_info,
        recent_commits=recent_commits,
        modified_files=modified_files,
    )

    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] Created handoff: {output_path}")
    print(f"  Branch: {git_info['branch']}")
    print(f"  Commit: {git_info['commit']}")
    if modified_files:
        print(f"  Modified files: {len(modified_files)}")
    if args.continues_from:
        print(f"  Continues from: {args.continues_from}")
    print(f"\nOpen and fill in the TODO sections, then validate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
