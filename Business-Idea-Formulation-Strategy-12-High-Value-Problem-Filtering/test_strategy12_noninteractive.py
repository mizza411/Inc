#!/usr/bin/env python3
"""Strategy 12 Phase 1 smoke: scoring helpers + non-interactive CLI (no input())."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
if str(STRATEGY_DIR) not in sys.path:
    sys.path.insert(0, str(STRATEGY_DIR))

from guemf_scoring import (  # noqa: E402
    CRITERIA,
    apply_cli_scores,
    cli_scores_to_agent_guemf,
    high_value_indices,
    normalize_cli_scores,
    rank_problems,
    require_complete_cli_scores,
)


class TestGuemfScoring(unittest.TestCase):
    def test_normalize_and_total(self):
        scores = normalize_cli_scores(
            {"Growing": 1, "urgent": "yes", "e": 1, "Mandatory": 0, "Frequent": True}
        )
        self.assertEqual(scores["Growing"], 1)
        self.assertEqual(scores["Urgent"], 1)
        self.assertEqual(scores["Expensive to Solve"], 1)
        self.assertEqual(scores["Mandatory"], 0)
        self.assertEqual(scores["Frequent"], 1)
        p = {"description": "x"}
        apply_cli_scores(p, scores)
        self.assertEqual(p["total_score"], 4)

    def test_require_complete_rejects_missing(self):
        with self.assertRaises(ValueError):
            require_complete_cli_scores({"Growing": 1, "Urgent": 1})

    def test_rank_and_high_value(self):
        problems = [
            apply_cli_scores(
                {"description": "low"},
                {c: 0 for c in CRITERIA},
            ),
            apply_cli_scores(
                {"description": "high"},
                {c: 1 for c in CRITERIA},
            ),
        ]
        ranked = rank_problems(problems)
        self.assertEqual(ranked[0]["description"], "high")
        self.assertEqual(high_value_indices(problems, min_score=4), [1])

    def test_agent_band_bridge(self):
        guemf = cli_scores_to_agent_guemf({c: 1 for c in CRITERIA})
        self.assertEqual(guemf["composite"], 25)
        self.assertEqual(guemf["Growing"], 5)


class TestNonInteractiveCli(unittest.TestCase):
    def test_fixture_run(self):
        fixture = STRATEGY_DIR / "fixtures" / "sample_inputs.json"
        self.assertTrue(fixture.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "summary.json"
            prompts = Path(tmp) / "prompts.txt"
            # Write prompts beside cwd by chdir into tmp; also pass --output
            cmd = [
                sys.executable,
                str(STRATEGY_DIR / "problem_filter.py"),
                "--non-interactive",
                "--inputs",
                str(fixture),
                "--output",
                str(out),
            ]
            proc = subprocess.run(
                cmd,
                cwd=str(Path(tmp)),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONIOENCODING": "utf-8"},
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )
            self.assertTrue(out.is_file())
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["strategy"], 12)
            self.assertEqual(data["mode"], "non-interactive")
            self.assertEqual(len(data["problems"]), 3)
            scores = [p["total_score"] for p in data["problems"]]
            self.assertEqual(scores, [5, 3, 0])
            # min_score 4 → only first problem
            self.assertEqual(data["selected_indices"], [0])
            ranked = data["ranked_preview"]
            self.assertEqual(ranked[0]["total_score"], 5)
            # prompts file created in cwd (tmp)
            prompt_file = Path(tmp) / "chatgpt_strategy12_prompts.txt"
            self.assertTrue(prompt_file.is_file())
            self.assertIn("High-value problem", prompt_file.read_text(encoding="utf-8"))

    def test_missing_inputs_flag_exits_2(self):
        proc = subprocess.run(
            [sys.executable, str(STRATEGY_DIR / "problem_filter.py"), "--non-interactive"],
            cwd=str(STRATEGY_DIR),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(proc.returncode, 2)

    def test_interactive_import_still_works(self):
        import problem_filter as pf

        self.assertTrue(callable(pf.HighValueProblemFilter))
        self.assertTrue(callable(pf.main))
        runner = pf.HighValueProblemFilter(auto_open=False)
        self.assertEqual(runner.problems, [])


if __name__ == "__main__":
    unittest.main()
