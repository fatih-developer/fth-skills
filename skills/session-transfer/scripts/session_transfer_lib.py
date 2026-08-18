#!/usr/bin/env python3
"""Portable session-transfer helpers: detect, create, resume, index, recover."""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


AGENT_DIR_MAP: dict[str, str] = {
    "codex": ".codex",
    "claude": ".claude",
    "opencode": ".opencode",
    "unknown": ".agent",
}

KNOWN_AGENT_DIRS: tuple[str, ...] = (".codex", ".claude", ".opencode", ".agent")

STATUSES: frozenset[str] = frozenset(
    {"completed", "in-progress", "partial", "blocked", "interrupted"}
)
TRIGGERS: frozenset[str] = frozenset(
    {
        "manual",
        "goal-completion",
        "substantial-work",
        "context-pressure",
        "agent-transfer",
        "interrupted",
    }
)
UNFINISHED_STATUSES: frozenset[str] = frozenset(
    {"in-progress", "partial", "blocked", "interrupted"}
)
JSONL_FIELDS: frozenset[str] = frozenset(
    {
        "id",
        "created",
        "agent",
        "topic",
        "status",
        "trigger",
        "branch",
        "commit",
        "file",
        "previous_session",
        "resumed_from",
        "goal_status",
    }
)
METADATA_FIELDS: tuple[str, ...] = (
    "session_id",
    "created",
    "source_agent",
    "source_model",
    "trigger",
    "status",
    "goal_status",
    "topic",
    "working_directory",
    "branch",
    "commit",
    "previous_session",
    "resumed_from",
)

ENV_HINTS: dict[str, tuple[str, ...]] = {
    "codex": ("CODEX_HOME", "CODEX_SANDBOX", "CODEX_SESSION", "CODEX"),
    "claude": ("CLAUDECODE", "CLAUDE_CODE", "CLAUDE_CODE_SSE_PORT"),
    "opencode": ("OPENCODE", "OPENCODE_DIR", "OPENCODE_SESSION"),
}

SUBSTANTIAL_CATEGORIES: frozenset[str] = frozenset(
    {
        "feature",
        "module",
        "architecture",
        "schema",
        "migration",
        "api",
        "auth",
        "security",
        "deploy",
        "infra",
    }
)

LEGACY_TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}-\d{6})(?:-|$)")
NEW_TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}-\d{4})(?:-(\d+))?$")

_NOT_RECORDED = "Not recorded."


@dataclass(frozen=True)
class DetectionSignals:
    """Injectable runtime signals. Existing dirs never select an agent alone."""

    env: Mapping[str, str] = field(default_factory=dict)
    execution_context: str | None = None
    explicit_instruction: str | None = None
    self_identified: str | None = None
    existing_agent_dirs: Sequence[str] = ()


@dataclass(frozen=True)
class AgentIdentity:
    name: str
    directory: str

    @property
    def repo_dir(self) -> str:
        return self.directory


@dataclass
class HandoffRecord:
    id: str
    created: str
    agent: str
    file: str
    topic: str | None = None
    status: str | None = None
    trigger: str | None = None
    branch: str | None = None
    commit: str | None = None
    previous_session: str | None = None
    resumed_from: str | None = None
    goal_status: str | None = None
    next_action: str | None = None
    repo_path: str | None = None

    def to_jsonl(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key in (
            "id",
            "created",
            "agent",
            "topic",
            "status",
            "trigger",
            "branch",
            "commit",
            "file",
            "previous_session",
            "resumed_from",
            "goal_status",
        ):
            value = getattr(self, key)
            if value is not None and value != "":
                payload[key] = value
        return payload


@dataclass
class CreateResult:
    identity: AgentIdentity
    record: HandoffRecord
    handoff_path: Path
    agent_index_path: Path
    jsonl_path: Path
    global_index_path: Path
    confirmation: str


@dataclass
class ResumeSelection:
    handoff_repo_path: str
    source_agent: str
    cross_agent: bool
    reason: str
    files_read: tuple[str, ...]
    record: HandoffRecord | None = None


@dataclass
class RecoveryReport:
    rebuilt_global: bool
    rebuilt_agents: tuple[str, ...]
    handoffs_preserved: int
    deleted_handoffs: int
    message: str


@dataclass
class WorkSignals:
    files_changed: int = 0
    categories: Sequence[str] = ()
    multi_phase: bool = False
    build_test_debug: bool = False
    large_context: bool = False
    continuation_requires_state: bool = False
    critical_one_file: bool = False
    trivial_copy_or_format: bool = False
    isolated_low_impact: bool = False


@dataclass
class AutoCreateSignals:
    substantial: bool
    already_handed_off_this_boundary: bool = False
    context_pressure: bool = False
    agent_changing: bool = False
    interrupted: bool = False
    explicit_checkpoint: bool = False
    user_requested: bool = False


class FileAccessLog:
    def __init__(self) -> None:
        self.reads: list[str] = []
        self.writes: list[str] = []

    def _norm(self, rel: str) -> str:
        return rel.replace("\\", "/")

    def record_read(self, rel: str) -> None:
        self.reads.append(self._norm(rel))

    def record_write(self, rel: str) -> None:
        self.writes.append(self._norm(rel))

    def handoff_bodies_read(self) -> list[str]:
        out: list[str] = []
        for rel in self.reads:
            if "/handoffs/" in rel and rel.endswith(".md") and not rel.endswith("INDEX.md"):
                out.append(rel)
        return out


def normalize_agent(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower().replace(" ", "-").replace("_", "-")
    aliases = {
        "codex": "codex",
        "openai-codex": "codex",
        "claude": "claude",
        "claude-code": "claude",
        "anthropic": "claude",
        "opencode": "opencode",
        "open-code": "opencode",
        "unknown": "unknown",
        "agent": "unknown",
        ".agent": "unknown",
    }
    if key in aliases:
        return aliases[key]
    if key in AGENT_DIR_MAP:
        return key
    return None


def agent_identity(name: str) -> AgentIdentity:
    resolved = normalize_agent(name) or "unknown"
    return AgentIdentity(name=resolved, directory=AGENT_DIR_MAP[resolved])


def _truthy_env(env: Mapping[str, str], key: str) -> bool:
    if key not in env:
        return False
    value = str(env[key]).strip()
    if value == "":
        return False
    return value.lower() not in {"0", "false", "no"}


def infer_agent_from_env(env: Mapping[str, str]) -> str | None:
    hits: list[str] = []
    for agent, keys in ENV_HINTS.items():
        if any(_truthy_env(env, key) for key in keys):
            hits.append(agent)
    if len(hits) == 1:
        return hits[0]
    return None


def infer_agent_from_existing_dirs(dirs: Sequence[str]) -> str | None:
    """Weak signal only. Never used as the sole selector."""
    known = []
    for item in dirs:
        name = item.strip().replace("\\", "/").rstrip("/")
        if not name.startswith("."):
            name = f".{name}"
        if name in {".codex", ".claude", ".opencode"}:
            known.append(name)
    unique = list(dict.fromkeys(known))
    if len(unique) != 1:
        return None
    mapping = {".codex": "codex", ".claude": "claude", ".opencode": "opencode"}
    return mapping[unique[0]]


def detect_agent(signals: DetectionSignals | None = None) -> AgentIdentity:
    """Priority: env → execution/config → explicit → self-id → never dirs-alone → .agent."""
    sig = signals or DetectionSignals()

    env_agent = infer_agent_from_env(sig.env)
    if env_agent:
        return agent_identity(env_agent)

    for candidate in (
        sig.execution_context,
        sig.explicit_instruction,
        sig.self_identified,
    ):
        resolved = normalize_agent(candidate)
        if resolved:
            return agent_identity(resolved)

    # Existing dirs are a supporting signal only and must not select alone.
    _ = infer_agent_from_existing_dirs(sig.existing_agent_dirs)
    return agent_identity("unknown")


def detect_existing_agent_dirs(workspace: Path) -> list[str]:
    found: list[str] = []
    for name in KNOWN_AGENT_DIRS:
        if (workspace / name).is_dir():
            found.append(name)
    return found


def detect_agent_from_workspace(
    workspace: Path,
    *,
    env: Mapping[str, str] | None = None,
    execution_context: str | None = None,
    explicit_instruction: str | None = None,
    self_identified: str | None = None,
) -> AgentIdentity:
    return detect_agent(
        DetectionSignals(
            env=env if env is not None else os.environ,
            execution_context=execution_context,
            explicit_instruction=explicit_instruction,
            self_identified=self_identified,
            existing_agent_dirs=detect_existing_agent_dirs(workspace),
        )
    )


def format_timestamp_id(now: datetime) -> str:
    return now.strftime("%Y-%m-%d-%H%M")


def allocate_handoff_stem(handoffs_dir: Path, now: datetime) -> str:
    """Immutable names: never overwrite; deterministic -N suffix on collision."""
    base = format_timestamp_id(now)
    candidate = base
    suffix = 2
    while (handoffs_dir / f"{candidate}.md").exists():
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def compact_metadata(fields: Mapping[str, Any]) -> dict[str, Any]:
    """Keep known values only. Never invent missing repo/agent fields."""
    out: dict[str, Any] = {}
    for key in METADATA_FIELDS:
        if key not in fields:
            continue
        value = fields[key]
        if value is None or value == "" or value == "unknown":
            continue
        out[key] = value
    return out


def render_metadata_yaml(fields: Mapping[str, Any]) -> str:
    compact = compact_metadata(fields)
    lines = ["```yaml"]
    for key in METADATA_FIELDS:
        if key in compact:
            lines.append(f"{key}: {compact[key]}")
    lines.append("```")
    return "\n".join(lines)


def _section(title: str, body: str | None) -> str:
    text = (body or "").strip() or _NOT_RECORDED
    return f"## {title}\n\n{text}\n"


def render_handoff_markdown(
    *,
    metadata: Mapping[str, Any],
    objective: str | None = None,
    current_state: str | None = None,
    work_completed: str | None = None,
    files_changed: Sequence[str] | None = None,
    architecture_decisions: str | None = None,
    database_changes: str | None = None,
    api_changes: str | None = None,
    frontend_changes: str | None = None,
    commands_executed: str | None = None,
    verification: str | None = None,
    issues_risks: str | None = None,
    remaining_work: str | None = None,
    next_recommended_action: str | None = None,
    resume_instructions: str | None = None,
) -> str:
    files_body = None
    if files_changed:
        files_body = "\n".join(f"- {path}" for path in files_changed)
    parts = [
        "# Session Handoff\n",
        "## Metadata\n",
        render_metadata_yaml(metadata),
        "",
        _section("Objective", objective),
        _section("Current State", current_state),
        _section("Work Completed", work_completed),
        _section("Files Changed", files_body),
        _section("Architecture & Decisions", architecture_decisions),
        _section("Database Changes", database_changes),
        _section("API Changes", api_changes),
        _section("Frontend Changes", frontend_changes),
        _section("Commands Executed", commands_executed),
        _section("Verification", verification),
        _section("Issues / Risks", issues_risks),
        _section("Remaining Work", remaining_work),
        _section("Next Recommended Action", next_recommended_action),
        _section("Resume Instructions", resume_instructions),
    ]
    return "\n".join(parts).rstrip() + "\n"


def parse_handoff_metadata(content: str) -> dict[str, str]:
    match = re.search(r"```yaml\n(.*?)```", content, re.DOTALL)
    block = match.group(1) if match else ""
    parsed: dict[str, str] = {}
    source = block or content
    for line in source.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in METADATA_FIELDS or key in {"id", "agent", "file"}:
            if value:
                parsed[key] = value
    next_match = re.search(
        r"## Next Recommended Action\n\n(.+?)(?:\n## |\Z)", content, re.DOTALL
    )
    if next_match:
        parsed["next_action"] = next_match.group(1).strip()
    return parsed


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def append_jsonl(path: Path, record: HandoffRecord, access: FileAccessLog | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record.to_jsonl(), ensure_ascii=True, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    if access:
        access.record_write(_rel(path, path.parents[1] if path.name == "handoffs.jsonl" else path.parent))


def read_jsonl(path: Path, access: FileAccessLog | None = None) -> list[HandoffRecord]:
    if not path.exists():
        return []
    if access:
        access.record_read(path.as_posix())
    records: list[HandoffRecord] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        records.append(_record_from_mapping(data))
    return records


def _record_from_mapping(data: Mapping[str, Any]) -> HandoffRecord:
    return HandoffRecord(
        id=str(data.get("id") or data.get("session_id") or ""),
        created=str(data.get("created") or ""),
        agent=str(data.get("agent") or data.get("source_agent") or "unknown"),
        file=str(data.get("file") or ""),
        topic=data.get("topic"),
        status=data.get("status"),
        trigger=data.get("trigger"),
        branch=data.get("branch"),
        commit=data.get("commit"),
        previous_session=data.get("previous_session"),
        resumed_from=data.get("resumed_from"),
        goal_status=data.get("goal_status"),
        next_action=data.get("next_action"),
        repo_path=data.get("repo_path"),
    )


def _display_time(created: str) -> str:
    if not created:
        return ""
    if "T" in created:
        return created.replace("T", " ")[:16]
    return created[:16]


def render_agent_index(agent_name: str, records: Sequence[HandoffRecord], now: datetime) -> str:
    title = {
        "codex": "Codex Session Index",
        "claude": "Claude Session Index",
        "opencode": "OpenCode Session Index",
    }.get(agent_name, "Agent Session Index")
    current = _latest_record(records)
    lines = [
        f"# {title}",
        "",
        f"Last updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Current Session",
        "",
    ]
    if current:
        lines.extend(
            [
                f"- Handoff: `{current.file}`",
                f"- Topic: {current.topic or '—'}",
                f"- Status: {current.status or '—'}",
                f"- Branch: {current.branch or '—'}",
                f"- Next Action: {current.next_action or '—'}",
            ]
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Recent Sessions",
            "",
            "| Date | Session | Topic | Status | Branch |",
            "|---|---|---|---|---|",
        ]
    )
    for rec in reversed(sort_records(records)[-10:]):
        lines.append(
            f"| {_display_time(rec.created) or rec.id} | `{rec.id}` | {rec.topic or '—'} | {rec.status or '—'} | {rec.branch or '—'} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_global_index(records: Sequence[HandoffRecord], now: datetime) -> str:
    current = _recommended_record(records)
    lines = [
        "# Session Transfer Index",
        "",
        f"Last updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Current / Recommended",
        "",
    ]
    if current:
        lines.extend(
            [
                f"- Handoff: `{current.repo_path or current.file}`",
                f"- Source agent: {current.agent}",
                f"- Topic: {current.topic or '—'}",
                f"- Status: {current.status or '—'}",
                f"- Branch: {current.branch or '—'}",
                f"- Next recommended action: {current.next_action or '—'}",
            ]
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Recent Cross-Agent Handoffs",
            "",
            "| Date | Agent | Session | Topic | Status | Branch |",
            "|---|---|---|---|---|---|",
        ]
    )
    for rec in reversed(sort_records(records)[-12:]):
        lines.append(
            f"| {_display_time(rec.created) or rec.id} | {rec.agent} | `{rec.id}` | {rec.topic or '—'} | {rec.status or '—'} | {rec.branch or '—'} |"
        )
    lines.append("")
    return "\n".join(lines)


def _parse_created(value: str | None) -> datetime:
    text = (value or "").strip()
    if not text:
        return datetime.min.replace(tzinfo=timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def sort_records(records: Sequence[HandoffRecord]) -> list[HandoffRecord]:
    """Oldest → newest by created timestamp, then id. Independent of agent-dir order."""
    return sorted(records, key=lambda rec: (_parse_created(rec.created), rec.id or ""))


def _latest_record(records: Sequence[HandoffRecord]) -> HandoffRecord | None:
    if not records:
        return None
    return sort_records(records)[-1]


def _recommended_record(records: Sequence[HandoffRecord]) -> HandoffRecord | None:
    if not records:
        return None
    unfinished = [r for r in records if (r.status or "") in UNFINISHED_STATUSES]
    if unfinished:
        return _latest_record(unfinished)
    return _latest_record(records)


def parse_global_index(content: str) -> dict[str, str] | None:
    if "## Current / Recommended" not in content or "- Handoff:" not in content:
        return None
    fields: dict[str, str] = {}
    mapping = {
        "handoff": "Handoff",
        "source_agent": "Source agent",
        "topic": "Topic",
        "status": "Status",
        "branch": "Branch",
        "next_action": "Next recommended action",
    }
    for dest, label in mapping.items():
        match = re.search(rf"- {re.escape(label)}:\s*(.+)", content)
        if match:
            fields[dest] = match.group(1).strip().strip("`")
    if not fields.get("handoff") or fields.get("handoff") == "None":
        return None
    return fields


def parse_agent_index(content: str) -> dict[str, str] | None:
    if "## Current Session" not in content or "- Handoff:" not in content:
        return None
    fields: dict[str, str] = {}
    for dest, label in (
        ("handoff", "Handoff"),
        ("topic", "Topic"),
        ("status", "Status"),
        ("branch", "Branch"),
        ("next_action", "Next Action"),
    ):
        match = re.search(rf"- {re.escape(label)}:\s*(.+)", content)
        if match:
            fields[dest] = match.group(1).strip().strip("`")
    if not fields.get("handoff"):
        return None
    return fields


def collect_git_info(workspace: Path | None = None) -> dict[str, str]:
    cwd = str(workspace) if workspace else None
    info: dict[str, str] = {}

    def _run(args: list[str]) -> str | None:
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=cwd,
            )
        except Exception:
            return None
        if result.returncode != 0:
            return None
        value = result.stdout.strip()
        return value or None

    branch = _run(["git", "branch", "--show-current"])
    commit = _run(["git", "rev-parse", "--short", "HEAD"])
    root = _run(["git", "rev-parse", "--show-toplevel"])
    if branch:
        info["branch"] = branch
    if commit:
        info["commit"] = commit
    if root:
        info["working_directory"] = root
    return info


def collect_modified_files(workspace: Path | None = None) -> list[str]:
    cwd = str(workspace) if workspace else None
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd,
        )
    except Exception:
        return []
    if result.returncode != 0:
        return []
    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        files.append(line[3:].strip() if len(line) > 3 else line.strip())
    return files


def format_create_confirmation(status: str, handoff_rel: str) -> str:
    return (
        "Session handoff created.\n"
        f"Status: {status}\n"
        f"Handoff: {handoff_rel}\n"
        "Global index updated: .session-transfer/INDEX.md\n"
    )


def _read_text(path: Path, workspace: Path, access: FileAccessLog | None) -> str:
    if access:
        access.record_read(_rel(path, workspace))
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str, workspace: Path, access: FileAccessLog | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if access:
        access.record_write(_rel(path, workspace))


def _load_agent_records(workspace: Path, identity: AgentIdentity, access: FileAccessLog | None) -> list[HandoffRecord]:
    jsonl = workspace / identity.directory / "handoffs.jsonl"
    records = []
    if jsonl.exists():
        if access:
            access.record_read(_rel(jsonl, workspace))
        records = read_jsonl(jsonl)
        for rec in records:
            if not rec.repo_path and rec.file:
                rec.repo_path = f"{identity.directory}/{rec.file.lstrip('/')}"
    return records


def _load_all_jsonl_records(workspace: Path, access: FileAccessLog | None) -> list[HandoffRecord]:
    records: list[HandoffRecord] = []
    for directory in KNOWN_AGENT_DIRS:
        jsonl = workspace / directory / "handoffs.jsonl"
        if not jsonl.exists():
            continue
        if access:
            access.record_read(_rel(jsonl, workspace))
        for rec in read_jsonl(jsonl):
            if not rec.agent or rec.agent == "unknown":
                rec.agent = _agent_from_dir(directory)
            if not rec.repo_path and rec.file:
                rec.repo_path = f"{directory}/{rec.file.lstrip('/')}"
            records.append(rec)
    return sort_records(records)


def _agent_from_dir(directory: str) -> str:
    for name, mapped in AGENT_DIR_MAP.items():
        if mapped == directory:
            return name
    return "unknown"


def create_handoff(
    workspace: Path,
    *,
    topic: str,
    status: str = "in-progress",
    trigger: str = "manual",
    signals: DetectionSignals | None = None,
    now: datetime | None = None,
    git_info: Mapping[str, str] | None = None,
    objective: str | None = None,
    current_state: str | None = None,
    work_completed: str | None = None,
    files_changed: Sequence[str] | None = None,
    architecture_decisions: str | None = None,
    database_changes: str | None = None,
    api_changes: str | None = None,
    frontend_changes: str | None = None,
    commands_executed: str | None = None,
    verification: str | None = None,
    issues_risks: str | None = None,
    remaining_work: str | None = None,
    next_recommended_action: str | None = None,
    resume_instructions: str | None = None,
    previous_session: str | None = None,
    resumed_from: str | None = None,
    source_model: str | None = None,
    goal_status: str | None = None,
    working_directory: str | None = None,
    access: FileAccessLog | None = None,
) -> CreateResult:
    if status not in STATUSES:
        raise ValueError(f"Invalid status '{status}'. Use one of: {sorted(STATUSES)}")
    if trigger not in TRIGGERS:
        raise ValueError(f"Invalid trigger '{trigger}'. Use one of: {sorted(TRIGGERS)}")

    root = Path(workspace)
    when = now or datetime.now().astimezone()
    identity = detect_agent(signals)
    agent_dir = root / identity.directory
    handoffs_dir = agent_dir / "handoffs"
    handoffs_dir.mkdir(parents=True, exist_ok=True)

    stem = allocate_handoff_stem(handoffs_dir, when)
    handoff_path = handoffs_dir / f"{stem}.md"
    if handoff_path.exists():
        raise FileExistsError(f"Refusing to overwrite handoff: {handoff_path}")

    created_iso = when.isoformat(timespec="seconds")
    git = dict(git_info or {})
    branch = git.get("branch")
    commit = git.get("commit")
    workdir = working_directory or git.get("working_directory")

    metadata = compact_metadata(
        {
            "session_id": stem,
            "created": created_iso,
            "source_agent": identity.name,
            "source_model": source_model,
            "trigger": trigger,
            "status": status,
            "goal_status": goal_status,
            "topic": topic,
            "working_directory": workdir,
            "branch": branch,
            "commit": commit,
            "previous_session": previous_session,
            "resumed_from": resumed_from,
        }
    )

    body = render_handoff_markdown(
        metadata=metadata,
        objective=objective or topic,
        current_state=current_state,
        work_completed=work_completed,
        files_changed=files_changed,
        architecture_decisions=architecture_decisions,
        database_changes=database_changes,
        api_changes=api_changes,
        frontend_changes=frontend_changes,
        commands_executed=commands_executed,
        verification=verification,
        issues_risks=issues_risks,
        remaining_work=remaining_work,
        next_recommended_action=next_recommended_action,
        resume_instructions=resume_instructions,
    )
    _write_text(handoff_path, body, root, access)

    relative_file = f"handoffs/{stem}.md"
    repo_path = f"{identity.directory}/{relative_file}"
    record = HandoffRecord(
        id=stem,
        created=created_iso,
        agent=identity.name,
        file=relative_file,
        topic=topic,
        status=status,
        trigger=trigger,
        branch=branch,
        commit=commit,
        previous_session=previous_session,
        resumed_from=resumed_from,
        goal_status=goal_status,
        next_action=next_recommended_action,
        repo_path=repo_path,
    )

    jsonl_path = agent_dir / "handoffs.jsonl"
    existing = _load_agent_records(root, identity, access)
    existing.append(record)
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_jsonl(), ensure_ascii=True, separators=(",", ":")) + "\n")
    if access:
        access.record_write(_rel(jsonl_path, root))

    agent_index_path = agent_dir / "INDEX.md"
    _write_text(agent_index_path, render_agent_index(identity.name, existing, when), root, access)

    all_records = _load_all_jsonl_records(root, access)
    matched = False
    for rec in all_records:
        if rec.id == record.id and rec.agent == record.agent:
            rec.next_action = record.next_action
            rec.repo_path = record.repo_path
            matched = True
            break
    if not matched:
        all_records.append(record)
    global_index_path = root / ".session-transfer" / "INDEX.md"
    _write_text(global_index_path, render_global_index(all_records, when), root, access)

    confirmation = format_create_confirmation(status, repo_path)
    return CreateResult(
        identity=identity,
        record=record,
        handoff_path=handoff_path,
        agent_index_path=agent_index_path,
        jsonl_path=jsonl_path,
        global_index_path=global_index_path,
        confirmation=confirmation,
    )


def _safe_read(workspace: Path, rel: str, access: FileAccessLog | None) -> str | None:
    path = workspace / rel
    if not path.is_file():
        return None
    return _read_text(path, workspace, access)


def _record_from_index_fields(
    fields: Mapping[str, str],
    *,
    default_agent: str | None = None,
) -> HandoffRecord:
    handoff = fields.get("handoff") or ""
    agent = normalize_agent(fields.get("source_agent") or fields.get("agent") or default_agent) or "unknown"
    if handoff.startswith(".codex/"):
        agent = "codex"
    elif handoff.startswith(".claude/"):
        agent = "claude"
    elif handoff.startswith(".opencode/"):
        agent = "opencode"
    elif handoff.startswith(".agent/"):
        agent = "unknown"
    session = Path(handoff.replace("\\", "/")).stem
    file_rel = handoff
    if "/" in handoff and not handoff.startswith("handoffs/"):
        parts = handoff.split("/", 1)
        if parts[0].startswith("."):
            file_rel = parts[1] if len(parts) > 1 else handoff
    repo_path = handoff if handoff.startswith(".") else f"{AGENT_DIR_MAP[agent]}/{handoff.lstrip('/')}"
    return HandoffRecord(
        id=session,
        created="",
        agent=agent,
        file=file_rel if file_rel.startswith("handoffs/") else f"handoffs/{Path(handoff).name}",
        topic=None if fields.get("topic") in {None, "—"} else fields.get("topic"),
        status=None if fields.get("status") in {None, "—"} else fields.get("status"),
        branch=None if fields.get("branch") in {None, "—"} else fields.get("branch"),
        next_action=None if fields.get("next_action") in {None, "—"} else fields.get("next_action"),
        repo_path=repo_path,
    )


def _topic_matches(record: HandoffRecord, topic: str | None) -> bool:
    if not topic:
        return True
    needle = topic.lower()
    hay = f"{record.topic or ''} {record.id}".lower()
    return needle in hay


def _is_unfinished(record: HandoffRecord) -> bool:
    return (record.status or "") in UNFINISHED_STATUSES


def select_handoff(
    workspace: Path,
    *,
    signals: DetectionSignals | None = None,
    topic: str | None = None,
    access: FileAccessLog | None = None,
) -> ResumeSelection:
    """Prefer global index, then current-agent unfinished, then cross-agent.

    Does not open historical handoff bodies when indexes/JSONL suffice.
    """
    root = Path(workspace)
    identity = detect_agent(signals)
    log = access or FileAccessLog()

    global_rel = ".session-transfer/INDEX.md"
    global_path = root / global_rel
    global_fields = None
    if global_path.is_file():
        content = _read_text(global_path, root, log)
        global_fields = parse_global_index(content)

    current_unfinished: HandoffRecord | None = None
    recommended: HandoffRecord | None = None

    if global_fields:
        recommended = _record_from_index_fields(global_fields)
        if recommended.agent == identity.name and _is_unfinished(recommended) and _topic_matches(recommended, topic):
            current_unfinished = recommended

    if current_unfinished is None:
        agent_index = root / identity.directory / "INDEX.md"
        if agent_index.is_file():
            parsed = parse_agent_index(_read_text(agent_index, root, log))
            if parsed:
                rec = _record_from_index_fields(parsed, default_agent=identity.name)
                rec.repo_path = f"{identity.directory}/{rec.file}"
                if _is_unfinished(rec) and _topic_matches(rec, topic):
                    current_unfinished = rec

    if current_unfinished is None and (global_fields is None or topic):
        records = _load_all_jsonl_records(root, log)
        agent_unfinished = [
            r
            for r in records
            if r.agent == identity.name and _is_unfinished(r) and _topic_matches(r, topic)
        ]
        if agent_unfinished:
            current_unfinished = _latest_record(agent_unfinished)
        elif recommended is None:
            compatible = [r for r in records if _topic_matches(r, topic)]
            unfinished = [r for r in compatible if _is_unfinished(r)]
            recommended = _latest_record(unfinished or compatible or records)

    if current_unfinished is not None:
        selected = current_unfinished
        reason = "current-agent unfinished"
    elif recommended is not None and _topic_matches(recommended, topic):
        selected = recommended
        reason = "global recommended" if recommended.agent == identity.name else "cross-agent"
    else:
        records = _load_all_jsonl_records(root, log)
        if not records:
            records = _discover_handoff_files(root, log)
        compatible = [r for r in records if _topic_matches(r, topic)]
        unfinished = [r for r in compatible if _is_unfinished(r)]
        pool = unfinished or compatible
        if not pool:
            raise FileNotFoundError("No handoff available to resume.")
        selected = _latest_record(pool)
        if selected is None:
            raise FileNotFoundError("No handoff available to resume.")
        reason = "jsonl/metadata fallback" if selected.agent == identity.name else "cross-agent"

    cross = selected.agent != identity.name
    if cross and reason == "global recommended":
        reason = "cross-agent"
    path = selected.repo_path or f"{AGENT_DIR_MAP.get(selected.agent, '.agent')}/{selected.file}"
    return ResumeSelection(
        handoff_repo_path=path,
        source_agent=selected.agent,
        cross_agent=cross,
        reason=reason,
        files_read=tuple(log.reads),
        record=selected,
    )


def _discover_handoff_files(workspace: Path, access: FileAccessLog | None) -> list[HandoffRecord]:
    records: list[HandoffRecord] = []
    for directory in KNOWN_AGENT_DIRS:
        handoffs = workspace / directory / "handoffs"
        if not handoffs.is_dir():
            continue
        for path in sorted(handoffs.glob("*.md")):
            content = _read_text(path, workspace, access)
            meta = parse_handoff_metadata(content)
            agent = normalize_agent(meta.get("source_agent")) or _agent_from_dir(directory)
            rec = HandoffRecord(
                id=meta.get("session_id") or path.stem,
                created=meta.get("created") or "",
                agent=agent,
                file=f"handoffs/{path.name}",
                topic=meta.get("topic"),
                status=meta.get("status"),
                trigger=meta.get("trigger"),
                branch=meta.get("branch"),
                commit=meta.get("commit"),
                previous_session=meta.get("previous_session"),
                resumed_from=meta.get("resumed_from"),
                goal_status=meta.get("goal_status"),
                next_action=meta.get("next_action"),
                repo_path=f"{directory}/handoffs/{path.name}",
            )
            records.append(rec)
    return sort_records(records)


def recover_indexes(
    workspace: Path,
    *,
    now: datetime | None = None,
    access: FileAccessLog | None = None,
) -> RecoveryReport:
    """Rebuild navigation from JSONL / handoff files. Never delete timestamped handoffs."""
    root = Path(workspace)
    when = now or datetime.now().astimezone()
    log = access or FileAccessLog()
    preserved = 0
    rebuilt_agents: list[str] = []
    all_verified: list[HandoffRecord] = []

    for directory in KNOWN_AGENT_DIRS:
        handoffs_dir = root / directory / "handoffs"
        files = list(handoffs_dir.glob("*.md")) if handoffs_dir.is_dir() else []
        preserved += len(files)
        jsonl_path = root / directory / "handoffs.jsonl"
        records = read_jsonl(jsonl_path, None)
        if jsonl_path.exists() and log:
            log.record_read(_rel(jsonl_path, root))

        file_index = {path.name: path for path in files}
        verified: list[HandoffRecord] = []
        seen_files: set[str] = set()
        for rec in records:
            name = Path(rec.file).name if rec.file else f"{rec.id}.md"
            if name in file_index:
                rec.file = f"handoffs/{name}"
                rec.repo_path = f"{directory}/handoffs/{name}"
                rec.agent = rec.agent or _agent_from_dir(directory)
                content = _read_text(file_index[name], root, log)
                meta = parse_handoff_metadata(content)
                if meta.get("next_action"):
                    rec.next_action = meta["next_action"]
                if not rec.created and meta.get("created"):
                    rec.created = meta["created"]
                if not rec.status and meta.get("status"):
                    rec.status = meta["status"]
                if not rec.topic and meta.get("topic"):
                    rec.topic = meta["topic"]
                verified.append(rec)
                seen_files.add(name)

        for name, path in file_index.items():
            if name in seen_files:
                continue
            content = _read_text(path, root, log)
            meta = parse_handoff_metadata(content)
            verified.append(
                HandoffRecord(
                    id=meta.get("session_id") or path.stem,
                    created=meta.get("created") or "",
                    agent=_agent_from_dir(directory),
                    file=f"handoffs/{name}",
                    topic=meta.get("topic"),
                    status=meta.get("status"),
                    trigger=meta.get("trigger"),
                    branch=meta.get("branch"),
                    commit=meta.get("commit"),
                    previous_session=meta.get("previous_session"),
                    resumed_from=meta.get("resumed_from"),
                    goal_status=meta.get("goal_status"),
                    next_action=meta.get("next_action"),
                    repo_path=f"{directory}/handoffs/{name}",
                )
            )

        verified = sort_records(verified)
        if verified or files:
            identity_name = _agent_from_dir(directory)
            _write_text(root / directory / "INDEX.md", render_agent_index(identity_name, verified, when), root, log)
            rebuilt_jsonl = "\n".join(
                json.dumps(rec.to_jsonl(), ensure_ascii=True, separators=(",", ":")) for rec in verified
            )
            if rebuilt_jsonl:
                rebuilt_jsonl += "\n"
            _write_text(jsonl_path, rebuilt_jsonl, root, log)
            rebuilt_agents.append(directory)
        all_verified.extend(verified)

    _write_text(
        root / ".session-transfer" / "INDEX.md",
        render_global_index(sort_records(all_verified), when),
        root,
        log,
    )
    return RecoveryReport(
        rebuilt_global=True,
        rebuilt_agents=tuple(rebuilt_agents),
        handoffs_preserved=preserved,
        deleted_handoffs=0,
        message=f"Rebuilt navigation from {preserved} handoff file(s). No timestamped handoffs deleted.",
    )


def is_substantial_work(work: WorkSignals) -> bool:
    if work.trivial_copy_or_format or work.isolated_low_impact:
        if (
            work.files_changed <= 1
            and not work.categories
            and not work.critical_one_file
            and not work.multi_phase
            and not work.build_test_debug
            and not work.large_context
            and not work.continuation_requires_state
        ):
            return False
    if work.files_changed >= 5:
        return True
    if any(cat.lower() in SUBSTANTIAL_CATEGORIES for cat in work.categories):
        return True
    if work.critical_one_file:
        return True
    if work.multi_phase or work.build_test_debug or work.large_context:
        return True
    if work.continuation_requires_state:
        return True
    return False


def should_auto_create(signals: AutoCreateSignals) -> bool:
    if signals.user_requested or signals.explicit_checkpoint:
        return True
    if signals.context_pressure or signals.agent_changing or signals.interrupted:
        return True
    if signals.substantial and not signals.already_handed_off_this_boundary:
        return True
    return False


def context_pressure_handoff(
    *,
    remaining_context_low: bool | None = None,
    session_long: bool = False,
    complexity_high: bool = False,
) -> dict[str, str] | None:
    """Portable rule: persist before reliable completion is threatened. No hardcoded %."""
    threatened = False
    if remaining_context_low is True:
        threatened = True
    elif remaining_context_low is None and session_long and complexity_high:
        threatened = True
    if not threatened:
        return None
    return {"trigger": "context-pressure", "status": "in-progress"}


def goal_close_requires_create(*, meaningful_work: bool) -> bool:
    return meaningful_work


def goal_may_close(
    *,
    meaningful_work: bool,
    handoff_persisted: bool,
    indexes_updated: bool,
) -> bool:
    if not meaningful_work:
        return True
    return handoff_persisted and indexes_updated


def normalize_status(value: str) -> str:
    key = value.strip().lower().replace(" ", "-")
    aliases = {
        "complete": "completed",
        "done": "completed",
        "wip": "in-progress",
        "in_progress": "in-progress",
        "progress": "in-progress",
        "abort": "interrupted",
        "aborted": "interrupted",
    }
    resolved = aliases.get(key, key)
    if resolved not in STATUSES:
        raise ValueError(f"Invalid status '{value}'")
    return resolved


def normalize_trigger(value: str) -> str:
    key = value.strip().lower().replace(" ", "-").replace("_", "-")
    if key not in TRIGGERS:
        raise ValueError(f"Invalid trigger '{value}'")
    return key


def list_handoff_records(workspace: Path) -> list[HandoffRecord]:
    records = _load_all_jsonl_records(workspace, None)
    if records:
        known = {r.repo_path for r in records}
        for extra in _discover_handoff_files(workspace, None):
            if extra.repo_path not in known:
                records.append(extra)
        return records
    return _discover_handoff_files(workspace, None)


def find_legacy_and_new_handoffs(workspace: Path) -> list[Path]:
    found: list[Path] = []
    for directory in KNOWN_AGENT_DIRS:
        handoffs = workspace / directory / "handoffs"
        if handoffs.is_dir():
            found.extend(sorted(handoffs.glob("*.md")))
    return found
