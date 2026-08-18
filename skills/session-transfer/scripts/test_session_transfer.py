#!/usr/bin/env python3
"""Drive shipped session-transfer helpers and CREATE CLI (scenarios A–I)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
CREATE_CLI = SCRIPTS_DIR / "create_handoff.py"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from session_transfer_lib import (  # noqa: E402
    JSONL_FIELDS,
    AutoCreateSignals,
    DetectionSignals,
    FileAccessLog,
    WorkSignals,
    context_pressure_handoff,
    create_handoff,
    goal_close_requires_create,
    goal_may_close,
    is_substantial_work,
    recover_indexes,
    select_handoff,
    should_auto_create,
)


NOW = datetime(2026, 8, 18, 17, 4, tzinfo=timezone.utc)
CODEX_SIG = DetectionSignals(env={"CODEX_HOME": "1"}, existing_agent_dirs=[".codex", ".claude", ".opencode"])
CLAUDE_SIG = DetectionSignals(env={"CLAUDECODE": "1"}, existing_agent_dirs=[".codex", ".claude", ".opencode"])
NONE_SIG = DetectionSignals(env={}, existing_agent_dirs=[".codex", ".claude", ".opencode"])


def _workspace(tmp: str) -> Path:
    root = Path(tmp)
    for name in (".codex", ".claude", ".opencode"):
        (root / name).mkdir(exist_ok=True)
    return root


def _plant_historical(root: Path, agent_dir: str, stem: str, body: str = "historical-only") -> Path:
    path = root / agent_dir / "handoffs" / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# Old\n\n{body}\n", encoding="utf-8")
    return path


class SessionTransferTests(unittest.TestCase):
    def test_a_i_detection_ignores_existing_dirs(self) -> None:
        """A/B/I: env/context wins; existing .codex/.claude/.opencode never select alone."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            unique = "UNIQUE-BODY-TOKEN-DO-NOT-INDEX"

            codex = create_handoff(
                root,
                topic="dashboard-ui",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=NOW,
                git_info={"branch": "main"},
                work_completed=unique,
                next_recommended_action="Complete filtering integration",
            )
            self.assertTrue(str(codex.handoff_path).replace("\\", "/").endswith(".codex/handoffs/2026-08-18-1704.md"))
            self.assertTrue((root / ".codex" / "INDEX.md").is_file())
            self.assertTrue((root / ".codex" / "handoffs.jsonl").is_file())
            self.assertTrue((root / ".session-transfer" / "INDEX.md").is_file())

            claude = create_handoff(
                root,
                topic="auth-api",
                status="completed",
                trigger="goal-completion",
                signals=CLAUDE_SIG,
                now=datetime(2026, 8, 18, 18, 30, tzinfo=timezone.utc),
                git_info={"branch": "main"},
            )
            self.assertTrue(str(claude.handoff_path).replace("\\", "/").endswith(".claude/handoffs/2026-08-18-1830.md"))

            unknown = create_handoff(
                root,
                topic="notes",
                status="partial",
                trigger="manual",
                signals=NONE_SIG,
                now=datetime(2026, 8, 18, 19, 15, tzinfo=timezone.utc),
            )
            self.assertTrue(str(unknown.handoff_path).replace("\\", "/").endswith(".agent/handoffs/2026-08-18-1915.md"))

    def test_b_create_artifacts_are_compact(self) -> None:
        """B: one CREATE writes four artifacts; indexes stay compact."""
        unique = "FULL-HANDOFF-BODY-SHOULD-NOT-APPEAR-IN-INDEX"
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            result = create_handoff(
                root,
                topic="dashboard-ui",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=NOW,
                git_info={"branch": "main", "commit": "abc1234"},
                work_completed=unique,
                next_recommended_action="Complete filtering integration",
            )
            global_index = (root / ".session-transfer" / "INDEX.md").read_text(encoding="utf-8")
            agent_index = (root / ".codex" / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn("Current / Recommended", global_index)
            self.assertIn(".codex/handoffs/2026-08-18-1704.md", global_index)
            self.assertIn("Complete filtering integration", global_index)
            self.assertNotIn(unique, global_index)
            self.assertNotIn(unique, agent_index)
            self.assertIn("handoffs/2026-08-18-1704.md", agent_index)
            self.assertTrue(result.handoff_path.is_file())
            self.assertIn("session_id: 2026-08-18-1704", result.handoff_path.read_text(encoding="utf-8"))

    def test_c_second_create_does_not_overwrite(self) -> None:
        """C: collision gets a deterministic suffix; first file is unchanged."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            first = create_handoff(
                root,
                topic="one",
                status="in-progress",
                trigger="manual",
                signals=CODEX_SIG,
                now=NOW,
                objective="first-unique-marker",
            )
            original = first.handoff_path.read_text(encoding="utf-8")
            second = create_handoff(
                root,
                topic="two",
                status="in-progress",
                trigger="manual",
                signals=CODEX_SIG,
                now=NOW,
                objective="second-unique-marker",
            )
            self.assertEqual(first.handoff_path.name, "2026-08-18-1704.md")
            self.assertEqual(second.handoff_path.name, "2026-08-18-1704-2.md")
            self.assertTrue(first.handoff_path.is_file())
            self.assertTrue(second.handoff_path.is_file())
            self.assertEqual(first.handoff_path.read_text(encoding="utf-8"), original)
            self.assertIn("first-unique-marker", original)
            self.assertNotIn("second-unique-marker", original)
            self.assertIn("second-unique-marker", second.handoff_path.read_text(encoding="utf-8"))

    def test_d_jsonl_compact_known_fields_only(self) -> None:
        """JSONL: one compact object per handoff; omit unknown fields."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            create_handoff(
                root,
                topic="dashboard-ui",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=NOW,
            )
            create_handoff(
                root,
                topic="follow-up",
                status="completed",
                trigger="manual",
                signals=CODEX_SIG,
                now=datetime(2026, 8, 18, 17, 9, tzinfo=timezone.utc),
                git_info={"branch": "feat/billing"},
                previous_session="2026-08-18-1704",
                resumed_from=".codex/handoffs/2026-08-18-1704.md",
            )
            lines = (root / ".codex" / "handoffs.jsonl").read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)
            first = json.loads(lines[0])
            second = json.loads(lines[1])
            self.assertTrue(set(first).issubset(JSONL_FIELDS))
            self.assertTrue(set(second).issubset(JSONL_FIELDS))
            self.assertNotIn("branch", first)
            self.assertNotIn("commit", first)
            self.assertEqual(first["file"], "handoffs/2026-08-18-1704.md")
            self.assertEqual(second["branch"], "feat/billing")
            self.assertEqual(second["previous_session"], "2026-08-18-1704")
            self.assertEqual(second["resumed_from"], ".codex/handoffs/2026-08-18-1704.md")

    def test_e_resume_selection_does_not_open_history(self) -> None:
        """C/E: current-agent unfinished from global index; Claude falls back cross-agent."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            create_handoff(
                root,
                topic="dashboard-ui",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=NOW,
                git_info={"branch": "main"},
                next_recommended_action="Complete filtering integration",
            )
            extras = [
                _plant_historical(root, ".codex", "2026-08-01-0900", "OLD-A"),
                _plant_historical(root, ".codex", "2026-08-02-1000", "OLD-B"),
                _plant_historical(root, ".claude", "2026-08-03-1100", "OLD-C"),
            ]

            log_codex = FileAccessLog()
            selected = select_handoff(root, signals=CODEX_SIG, access=log_codex)
            self.assertEqual(selected.handoff_repo_path, ".codex/handoffs/2026-08-18-1704.md")
            self.assertFalse(selected.cross_agent)
            self.assertEqual(log_codex.handoff_bodies_read(), [])
            for extra in extras:
                self.assertNotIn(extra.as_posix().replace("\\", "/"), [r.replace("\\", "/") for r in log_codex.reads])
                rel = extra.relative_to(root).as_posix()
                self.assertNotIn(rel, log_codex.reads)

            log_claude = FileAccessLog()
            cross = select_handoff(root, signals=CLAUDE_SIG, access=log_claude)
            self.assertEqual(cross.handoff_repo_path, ".codex/handoffs/2026-08-18-1704.md")
            self.assertTrue(cross.cross_agent)
            self.assertEqual(log_claude.handoff_bodies_read(), [])

    def test_f_policy_substantial_trivial_pressure_goal(self) -> None:
        """F/G/D: substantial vs trivial, context-pressure mapping, /goal requires CREATE."""
        self.assertTrue(is_substantial_work(WorkSignals(files_changed=5)))
        self.assertTrue(is_substantial_work(WorkSignals(files_changed=1, categories=["schema"])))
        self.assertTrue(is_substantial_work(WorkSignals(files_changed=1, categories=["api"])))
        self.assertTrue(is_substantial_work(WorkSignals(files_changed=1, categories=["auth"])))
        self.assertFalse(
            is_substantial_work(WorkSignals(files_changed=1, trivial_copy_or_format=True))
        )
        self.assertFalse(
            should_auto_create(
                AutoCreateSignals(substantial=False, already_handed_off_this_boundary=False)
            )
        )
        self.assertTrue(should_auto_create(AutoCreateSignals(substantial=True)))
        self.assertFalse(
            should_auto_create(AutoCreateSignals(substantial=True, already_handed_off_this_boundary=True))
        )
        self.assertTrue(
            should_auto_create(
                AutoCreateSignals(
                    substantial=True,
                    already_handed_off_this_boundary=True,
                    context_pressure=True,
                )
            )
        )
        pressure = context_pressure_handoff(remaining_context_low=True)
        self.assertEqual(pressure, {"trigger": "context-pressure", "status": "in-progress"})
        self.assertTrue(goal_close_requires_create(meaningful_work=True))
        self.assertFalse(
            goal_may_close(meaningful_work=True, handoff_persisted=False, indexes_updated=False)
        )
        self.assertTrue(
            goal_may_close(meaningful_work=True, handoff_persisted=True, indexes_updated=True)
        )

        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            pressure_create = create_handoff(
                root,
                topic="billing",
                status="in-progress",
                trigger="context-pressure",
                signals=CODEX_SIG,
                now=NOW,
            )
            self.assertEqual(pressure_create.record.trigger, "context-pressure")
            self.assertEqual(pressure_create.record.status, "in-progress")
            blocked = create_handoff(
                root,
                topic="billing",
                status="blocked",
                trigger="goal-completion",
                goal_status="blocked",
                signals=CODEX_SIG,
                now=datetime(2026, 8, 18, 17, 20, tzinfo=timezone.utc),
                remaining_work="Need the API token from the user",
            )
            body = blocked.handoff_path.read_text(encoding="utf-8")
            self.assertIn("status: blocked", body)
            self.assertIn("Need the API token from the user", body)

    def test_g_recover_index_without_deleting_handoffs(self) -> None:
        """H: missing/corrupt global index rebuilds from JSONL; files stay."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            created = create_handoff(
                root,
                topic="dashboard-ui",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=NOW,
                git_info={"branch": "main"},
                next_recommended_action="Complete filtering integration",
            )
            extra = _plant_historical(root, ".codex", "2026-08-01-0900", "KEEP-ME")
            extra_text = extra.read_text(encoding="utf-8")
            handoff_text = created.handoff_path.read_text(encoding="utf-8")
            global_index = root / ".session-transfer" / "INDEX.md"
            global_index.write_text("CORRUPT INDEX\n", encoding="utf-8")

            report = recover_indexes(root, now=NOW)
            self.assertEqual(report.deleted_handoffs, 0)
            self.assertTrue(created.handoff_path.is_file())
            self.assertTrue(extra.is_file())
            self.assertEqual(created.handoff_path.read_text(encoding="utf-8"), handoff_text)
            self.assertEqual(extra.read_text(encoding="utf-8"), extra_text)
            rebuilt = global_index.read_text(encoding="utf-8")
            self.assertIn("Current / Recommended", rebuilt)
            self.assertIn(".codex/handoffs/2026-08-18-1704.md", rebuilt)
            self.assertIn("Complete filtering integration", rebuilt)
            self.assertIn("KEEP-ME", extra.read_text(encoding="utf-8"))

    def test_recommended_latest_by_created_not_dir_order(self) -> None:
        """Mixed-agent unfinished: newest created wins, not KNOWN_AGENT_DIRS JSONL order."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            create_handoff(
                root,
                topic="legacy-claude",
                status="in-progress",
                trigger="substantial-work",
                signals=CLAUDE_SIG,
                now=datetime(2026, 8, 18, 17, 4, tzinfo=timezone.utc),
                next_recommended_action="Finish Claude-side work",
            )
            create_handoff(
                root,
                topic="newer-codex",
                status="in-progress",
                trigger="substantial-work",
                signals=CODEX_SIG,
                now=datetime(2026, 8, 18, 18, 30, tzinfo=timezone.utc),
                next_recommended_action="Continue Codex filtering",
            )
            index = (root / ".session-transfer" / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn(".codex/handoffs/2026-08-18-1830.md", index.split("## Recent")[0])
            self.assertNotIn(".claude/handoffs/2026-08-18-1704.md", index.split("## Recent")[0])
            self.assertIn("Continue Codex filtering", index.split("## Recent")[0])

            unknown = select_handoff(root, signals=NONE_SIG)
            self.assertEqual(unknown.handoff_repo_path, ".codex/handoffs/2026-08-18-1830.md")

            (root / ".session-transfer" / "INDEX.md").unlink()
            from_jsonl = select_handoff(root, signals=NONE_SIG)
            self.assertEqual(from_jsonl.handoff_repo_path, ".codex/handoffs/2026-08-18-1830.md")

    def test_skill_docs_cover_required_topics(self) -> None:
        text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for needle in (
            "CREATE",
            "RESUME",
            "automatic",
            "/goal",
            ".session-transfer/INDEX.md",
            "INDEX.md",
            "handoffs.jsonl",
            "YYYY-MM-DD-HHmm",
            "cross-agent",
            "context-pressure",
            "Fallback",
            "Use session-transfer to create a handoff.",
            "Use session-transfer to resume the latest session.",
            "Use session-transfer to resume the latest unfinished billing work.",
            "session-transfer runs as the terminal persistence step",
            ".codex",
            ".claude",
            ".opencode",
            ".agent",
        ):
            self.assertIn(needle, text)


def _clean_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        upper = key.upper()
        if upper.startswith(("CODEX", "CLAUDE", "OPENCODE")):
            env.pop(key, None)
    env["CODEX_HOME"] = "1"
    return env


class CreateCliTests(unittest.TestCase):
    def test_cli_confirmation_is_concise(self) -> None:
        """Shipped CREATE entry point: concise confirmation + four artifacts."""
        with tempfile.TemporaryDirectory() as tmp:
            root = _workspace(tmp)
            cmd = [
                sys.executable,
                str(CREATE_CLI),
                "dashboard-ui",
                "--workspace",
                str(root),
                "--agent",
                "codex",
                "--status",
                "completed",
                "--trigger",
                "goal-completion",
                "--branch",
                "feat/billing",
                "--next-action",
                "Ship the filter",
                "--objective",
                "Finish dashboard filtering",
                "--no-git",
                "--now",
                "2026-08-18T17:09:00+00:00",
            ]
            env = _clean_env()
            first = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            out = first.stdout
            self.assertIn("Session handoff created.", out)
            self.assertIn("Status: completed", out)
            self.assertIn("Handoff: .codex/handoffs/2026-08-18-1709.md", out)
            self.assertIn("Global index updated: .session-transfer/INDEX.md", out)
            self.assertNotIn("## Work Completed", out)
            self.assertNotIn("Finish dashboard filtering", out)

            handoff = root / ".codex" / "handoffs" / "2026-08-18-1709.md"
            self.assertTrue(handoff.is_file())
            self.assertTrue((root / ".codex" / "INDEX.md").is_file())
            self.assertTrue((root / ".codex" / "handoffs.jsonl").is_file())
            self.assertTrue((root / ".session-transfer" / "INDEX.md").is_file())
            meta = handoff.read_text(encoding="utf-8")
            self.assertIn("status: completed", meta)
            self.assertIn("branch: feat/billing", meta)
            self.assertIn("topic: dashboard-ui", meta)

            second_cmd = cmd[:-1] + ["2026-08-18T17:10:00+00:00"]
            second = subprocess.run(second_cmd, capture_output=True, text=True, env=env, check=False)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("Handoff: .codex/handoffs/2026-08-18-1710.md", second.stdout)
            self.assertTrue(handoff.is_file())
            self.assertTrue((root / ".codex" / "handoffs" / "2026-08-18-1710.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
