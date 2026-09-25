"""Tests for the repository tooling: validator, ecosystem builder, and installer."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import build_ecosystems  # noqa: E402
import validate_curated_skills as v  # noqa: E402


class FrontmatterTests(unittest.TestCase):
    def test_rejects_unescaped_single_quotes(self):
        # The exact bug that broke project-analyzer on skills.sh.
        text = "---\nname: x\ndescription: 'Use when phrases like 'analyze' occur.'\n---\n"
        with self.assertRaises(ValueError):
            v.parse_frontmatter(text)

    def test_accepts_double_quoted_with_apostrophes(self):
        text = '---\nname: x\ndescription: "Use when the user\'s project needs it."\n---\n'
        self.assertEqual(v.parse_frontmatter(text)["name"], "x")


class FenceTests(unittest.TestCase):
    def test_detects_nested_fence(self):
        text = "```markdown\n# Report\n```json\n{}\n```\n```\n"
        self.assertGreater(v.nested_fences(text), 0)

    def test_accepts_longer_outer_fence(self):
        text = "````markdown\n# Report\n```json\n{}\n```\n````\n"
        self.assertEqual(v.nested_fences(text), 0)

    def test_detects_unclosed_fence(self):
        self.assertGreater(v.nested_fences("```bash\necho hi\n"), 0)


class RepositoryTests(unittest.TestCase):
    def test_validator_passes(self):
        result = subprocess.run([sys.executable, "scripts/validate_curated_skills.py"], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout[-3000:])

    def test_generated_artifacts_are_current(self):
        stale = [str(p) for p, c in build_ecosystems.build().items() if not p.exists() or p.read_text(encoding="utf-8") != c]
        self.assertEqual(stale, [], "run python scripts/build_ecosystems.py")

    def test_every_workflow_step_has_do_and_done_when(self):
        for eco, data in build_ecosystems.load_ecosystems().items():
            for wf in data["workflows"]:
                for step in wf["steps"]:
                    self.assertTrue(step.get("do") and step.get("done_when"), f"{eco}/{wf['id']}/{step['skill']}")

    def test_handoff_next_step_skips_parallel_siblings(self):
        steps = [{"skill": "a"}, {"skill": "b", "parallel_group": "g"}, {"skill": "c", "parallel_group": "g"}, {"skill": "d"}]
        self.assertEqual(build_ecosystems.stages(steps), [[0], [1, 2], [3]])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        skills = self.tmp / ".claude" / "skills"
        skills.mkdir(parents=True)
        shutil.copytree(REPO / "skills" / "ecosystem-api", skills / "ecosystem-api")
        shutil.copytree(REPO / "skills" / "auth-flow-designer", skills / "auth-flow-designer")
        self.script = skills / "ecosystem-api" / "scripts" / "install_all.py"
        self.env = {**os.environ, "HOME": str(self.tmp)}

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_installer(self, *args):
        return subprocess.run([sys.executable, str(self.script), *args], cwd=self.tmp, env=self.env, capture_output=True, text=True)

    def test_status_reports_missing(self):
        out = self.run_installer("--status", "--workflow", "api-security-scale").stdout
        self.assertIn("installed  auth-flow-designer", out)
        self.assertIn("missing    rate-limit-strategist", out)

    def test_default_is_dry_run(self):
        out = self.run_installer("--workflow", "api-security-scale", "--missing-only").stdout
        self.assertIn("Dry run", out)
        self.assertIn("npx skills add fatih-developer/fth-skills --skill rate-limit-strategist", out)
        self.assertNotIn("auth-flow-designer", out)

    def test_unknown_workflow_fails(self):
        self.assertNotEqual(self.run_installer("--workflow", "nope").returncode, 0)

    def test_installers_match_template(self):
        template = (REPO / "scripts" / "templates" / "ecosystem" / "install_all.py").read_text(encoding="utf-8")
        for path in (REPO / "skills").glob("ecosystem-*/scripts/install_all.py"):
            self.assertEqual(path.read_text(encoding="utf-8"), template, str(path))


class RegistryTests(unittest.TestCase):
    def test_registry_lists_each_skill_once(self):
        registry = json.loads((REPO / "skills.sh.json").read_text(encoding="utf-8"))
        listed = [s for g in registry["groupings"] for s in g["skills"]]
        folders = sorted(p.name for p in (REPO / "skills").iterdir() if (p / "SKILL.md").exists())
        self.assertEqual(sorted(listed), folders)


if __name__ == "__main__":
    unittest.main()
