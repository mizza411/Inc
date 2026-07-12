"""Build Strategy 1 Prompt 1a / 1b payload text from structured run data."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

STRATEGY_DIR = Path(__file__).resolve().parent


def read_prompt_template(name: str) -> str:
    path = STRATEGY_DIR / name
    if not path.exists():
        return f"(missing template: {name})\n"
    return path.read_text(encoding="utf-8").strip() + "\n"


def build_material_block(businesses: List[Dict[str, Any]]) -> str:
    lines: List[str] = [
        "Strategy 1 material (successful businesses + recurring complaints):",
        "",
    ]
    for b in businesses:
        lines.append(f"## Target successful business: {b['name']}")
        if b.get("category"):
            lines.append(f"Category: {b['category']}")
        lines.append("Complaints (highest score first):")
        for i, c in enumerate(b.get("complaints") or [], 1):
            lines.append(
                f"  {i}. [{c.get('category')}] {c.get('text')} "
                f"(freq={c.get('frequency')}, impact={c.get('impact')}, "
                f"solvability={c.get('solvability')}, score={c.get('score')}, "
                f"source={c.get('source')})"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_prompt_1a_payload(businesses: List[Dict[str, Any]]) -> str:
    template = read_prompt_template("chatgpt_prompt_1a.txt")
    material = build_material_block(businesses)
    return (
        f"{template}\n"
        f"{'=' * 60}\n"
        f"PASTED / STRUCTURED INPUT\n"
        f"{'=' * 60}\n\n"
        f"{material}"
    )


def build_prompt_1b_scaffold(businesses: List[Dict[str, Any]]) -> str:
    """Scaffold reminding lead columns; full tabulation is done in ChatGPT/agent."""
    template = read_prompt_template("chatgpt_prompt_1b.txt")
    rows: List[str] = [
        template,
        "",
        "Rows to expand (one per high-priority complaint; fill remaining columns in Prompt 1b):",
        "",
    ]
    for b in businesses:
        for c in b.get("complaints") or []:
            rows.append(
                f"- Target: {b['name']} | Complaint: {c.get('text')} | "
                f"Category: {c.get('category')} | Frequency: {c.get('frequency')} | "
                f"Impact: {c.get('impact')} | Solvability: {c.get('solvability')}"
            )
    rows.append("")
    return "\n".join(rows)
