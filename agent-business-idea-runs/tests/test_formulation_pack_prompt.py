#!/usr/bin/env python3
"""§14 Phase 1 smoke: Pass 2 pack prompt has required card/schema markers."""
from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACK = REPO / "prompts" / "agent_formulation_pack.txt"
DISCOVER = REPO / "prompts" / "agent_formulation_run.txt"

# Keep in sync with prompts/agent_formulation_pack.txt + FORMULATION_PASS_CONTRACT.md
MARKERS = (
    "Pass 2",
    "Regulatory",
    "Competitors / alternatives",
    "Incomplete Pass 2",
    "MVP cost",
    "exactly once",
    "FORMULATION_PASS_CONTRACT.md",
    "do not invent fake competitor",
)


class TestFormulationPackPrompt(unittest.TestCase):
    def test_pack_prompt_exists_with_markers(self):
        self.assertTrue(PACK.is_file(), f"missing {PACK}")
        text = PACK.read_text(encoding="utf-8")
        missing = [m for m in MARKERS if m not in text]
        self.assertFalse(
            missing,
            msg="agent_formulation_pack.txt missing markers: " + ", ".join(missing),
        )

    def test_discover_defers_docx_to_pass2(self):
        text = DISCOVER.read_text(encoding="utf-8")
        self.assertIn("Pass 1 Discover", text)
        self.assertIn("agent_formulation_pack.txt", text)
        self.assertIn("_PENDING_PASS_2_PACK_", text)
        # Docx convert is Pass 2's job — Discover must not instruct one-shot convert as its finale
        self.assertNotIn("then convert/open the Word file exactly once as the final automated step", text)

    def test_discover_prompt_untouched_exists(self):
        """Discover file remains the Hub default path."""
        self.assertTrue(DISCOVER.is_file(), f"missing {DISCOVER}")
        text = DISCOVER.read_text(encoding="utf-8")
        self.assertGreater(len(text), 500)
        self.assertIn("include strategies", text)


if __name__ == "__main__":
    unittest.main()
