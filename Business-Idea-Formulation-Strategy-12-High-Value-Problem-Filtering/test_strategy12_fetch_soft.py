#!/usr/bin/env python3
"""Phase 4 smoke: optional strategy_12_run soft-fail; default skipped."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUN_DIR = REPO / "agent-business-idea-runs"


class TestStrategy12FetchSoft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(RUN_DIR))
        import agent_strategy_run as asr  # noqa: E402

        cls.asr = asr

    def test_default_argparse_skips_strategy12(self):
        args = self.asr.build_parser().parse_args([])
        self.assertFalse(args.with_strategy12)

    def test_run_strategy12_noninteractive_fixture_ok(self):
        result = self.asr.run_strategy12_noninteractive(timeout_sec=60)
        self.assertEqual(
            result.get("status"),
            "ok",
            msg=str(result),
        )
        self.assertEqual(result.get("selected_indices"), [0])
        self.assertTrue(result.get("ranked_preview"))
        self.assertIn("Mode B", result.get("note") or "")

    def test_missing_inputs_soft_status(self):
        result = self.asr.run_strategy12_noninteractive(
            inputs_path=str(REPO / "does_not_exist_strategy12.json"),
            timeout_sec=10,
        )
        self.assertEqual(result.get("status"), "no_inputs_file")


if __name__ == "__main__":
    unittest.main()
