#!/usr/bin/env python3
"""Phase 2 smoke: agent prompt requires Strategy 12 Mode A + Mode B (not overlay-only)."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROMPT = REPO / "prompts" / "agent_formulation_run.txt"

# Stable markers — keep in sync with prompts/agent_formulation_run.txt + task.md §13 Phase 2
MARKERS = (
    "Strategy 12 (GUEMF",
    "Mode A (standalone)",
    "Mode B (overlay)",
    "BOTH Mode A and Mode B",
    "primary strategy trace includes S12",
)


class TestStrategy12PromptDualMode(unittest.TestCase):
    def test_prompt_has_dual_mode_markers(self):
        self.assertTrue(PROMPT.is_file(), f"missing {PROMPT}")
        text = PROMPT.read_text(encoding="utf-8")
        missing = [m for m in MARKERS if m not in text]
        self.assertFalse(
            missing,
            msg="agent_formulation_run.txt missing Strategy 12 dual-mode markers: "
            + ", ".join(missing),
        )
        # Include list still has 12
        self.assertRegex(text, r"include strategies[^;]*\b12\b")
        # Guard against regressing to overlay-only wording as the sole GUEMF instruction
        self.assertNotIn(
            "GUEMF-style scoring (Growing/Urgent/Expensive/Mandatory/Frequent) where relevant",
            text,
        )


if __name__ == "__main__":
    unittest.main()
