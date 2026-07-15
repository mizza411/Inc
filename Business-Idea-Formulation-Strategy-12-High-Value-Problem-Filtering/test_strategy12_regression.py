#!/usr/bin/env python3
"""Strategy 12 Phase 3 regression bundle: smokes + runner registration untouched."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
REPO = STRATEGY_DIR.parent


class TestStrategy12Regression(unittest.TestCase):
    def test_run_all_registers_strategy_12(self):
        sys.path.insert(0, str(REPO))
        import run_all_strategies as ras  # noqa: E402

        self.assertIn(12, ras.STRATEGY_SCRIPTS)
        script = ras.STRATEGY_SCRIPTS[12]
        self.assertEqual(script.name, "problem_filter.py")
        self.assertTrue(script.is_file(), f"missing {script}")
        self.assertIn(12, ras.STRATEGY_META)
        self.assertIn("High-Value", ras.STRATEGY_META[12]["name"])
        # Neighbor strategies still registered (anti-break sample)
        for n in (1, 5, 6, 7, 9, 11, 13, 14, 15):
            self.assertIn(n, ras.STRATEGY_SCRIPTS, msg=f"STRATEGY_SCRIPTS missing {n}")
        for retired in (8, 10):
            self.assertNotIn(retired, ras.STRATEGY_SCRIPTS)

    def test_prompt_and_ni_smokes_pass(self):
        files = [
            STRATEGY_DIR / "test_strategy12_noninteractive.py",
            STRATEGY_DIR / "test_strategy12_prompt_dual_mode.py",
            STRATEGY_DIR / "test_strategy12_fetch_soft.py",
        ]
        for f in files:
            self.assertTrue(f.is_file(), f"missing {f}")
        cmd = [sys.executable, "-m", "pytest", *[str(f) for f in files], "-q", "--tb=line"]
        proc = subprocess.run(
            cmd,
            cwd=str(REPO),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(
            proc.returncode,
            0,
            msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
        )


if __name__ == "__main__":
    # Prefer pytest if available for this file alone
    raise SystemExit(unittest.main(verbosity=2))
