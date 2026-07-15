#!/usr/bin/env python3
"""§14 Phase 3 smoke: idea_card_schema good/bad fixtures + CLI exit codes."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MOD = REPO / "agent-business-idea-runs" / "idea_card_schema.py"
GOOD = REPO / "agent-business-idea-runs" / "fixtures" / "idea_cards_good.md"
BAD = REPO / "agent-business-idea-runs" / "fixtures" / "idea_cards_bad.md"


class TestIdeaCardSchema(unittest.TestCase):
    def test_module_import_validate_good(self):
        sys.path.insert(0, str(MOD.parent))
        import idea_card_schema as ics  # noqa: E402

        report = ics.validate_path(GOOD)
        self.assertTrue(report.ok, ics.format_report(report, show_optional=True))
        self.assertEqual(len(report.ideas), 2)

    def test_validate_bad_missing_required(self):
        sys.path.insert(0, str(MOD.parent))
        import idea_card_schema as ics  # noqa: E402

        report = ics.validate_path(BAD)
        self.assertFalse(report.ok)
        self.assertEqual(len(report.ideas), 2)
        # Idea 1 missing Target + Regulatory (among others)
        miss0 = set(report.ideas[0].missing_required)
        self.assertIn("Target", miss0)
        self.assertIn("Regulatory", miss0)
        # Idea 2 missing Regulatory + Competitors
        miss1 = set(report.ideas[1].missing_required)
        self.assertIn("Regulatory", miss1)
        self.assertTrue(
            any(m.startswith("Competitors") for m in miss1),
            msg=miss1,
        )

    def test_cli_exit_codes(self):
        good = subprocess.run(
            [sys.executable, str(MOD), str(GOOD)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
        bad = subprocess.run(
            [sys.executable, str(MOD), str(BAD)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)

    def test_not_wired_into_agent_strategy_run(self):
        runner = (REPO / "agent-business-idea-runs" / "agent_strategy_run.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("idea_card_schema", runner)


if __name__ == "__main__":
    unittest.main()
