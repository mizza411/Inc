"""AUTO-NAR-10 — copy-paste ask openers (never send)."""

from __future__ import annotations

from typing import Any, Literal

Mode = Literal["s3", "s4", "both"]

_S3_OPENERS = [
    "Hey — quick one: what’s the most annoying / expensive problem in your work or side hustle right now?",
    "I’m collecting real business problems (not pitching). What’s broken or slow for you weekly?",
    "If a simple digital tool could remove one headache for you, what would it fix?",
]

_S4_OPENERS = [
    "Hi — I’m learning what owners struggle with. What’s the hardest ops problem this week?",
    "No sales pitch: what takes too much time or money to run your business day-to-day?",
    "Would you mind a 5-minute questionnaire on business challenges? Totally optional.",
]


def generate_openers(cfg: dict[str, Any], mode: Mode = "both") -> str:
    blocks: list[str] = []
    if mode in ("s3", "both"):
        blocks.append("=== Strategy 3 (network) — copy/paste; you send ===")
        blocks.append(cfg["prompts"]["s3"])
        blocks.extend(f"- {line}" for line in _S3_OPENERS)
    if mode in ("s4", "both"):
        if blocks:
            blocks.append("")
        blocks.append("=== Strategy 4 (business owners) — copy/paste; you send ===")
        blocks.append(cfg["prompts"]["s4"])
        blocks.extend(f"- {line}" for line in _S4_OPENERS)
    blocks.append("")
    blocks.append("(Automation never sends these. MAN-NAR-05 stays with you.)")
    return "\n".join(blocks)
