#!/usr/bin/env python3
"""Pure GUEMF scoring helpers for Strategy 12 (no I/O, no input()).

CLI interactive path uses 0/1 per criterion (sum 0–5).
Agent markdown uses 1–5 per criterion (composite max 25) — see cli_bit_to_agent_band.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence

CRITERIA: List[str] = [
    "Growing",
    "Urgent",
    "Expensive to Solve",
    "Mandatory",
    "Frequent",
]

# Short aliases accepted in JSON inputs (normalized to CRITERIA names).
CRITERIA_ALIASES: Dict[str, str] = {
    "growing": "Growing",
    "g": "Growing",
    "urgent": "Urgent",
    "u": "Urgent",
    "expensive": "Expensive to Solve",
    "expensive to solve": "Expensive to Solve",
    "e": "Expensive to Solve",
    "mandatory": "Mandatory",
    "m": "Mandatory",
    "frequent": "Frequent",
    "f": "Frequent",
}


def canonical_criterion(name: str) -> Optional[str]:
    key = (name or "").strip()
    if key in CRITERIA:
        return key
    return CRITERIA_ALIASES.get(key.lower())


def yn_to_bit(answer: str) -> int:
    """Interactive Y/N → 0/1."""
    return 1 if (answer or "").strip().lower() in ("y", "yes", "1", "true") else 0


def normalize_cli_scores(raw: Mapping[str, Any]) -> Dict[str, int]:
    """
    Normalize a criteria_scores mapping to full CRITERIA → 0|1.
    Missing keys default to 0. Values may be int/bool/str.
    """
    out: Dict[str, int] = {c: 0 for c in CRITERIA}
    for k, v in (raw or {}).items():
        crit = canonical_criterion(str(k))
        if not crit:
            continue
        if isinstance(v, bool):
            out[crit] = 1 if v else 0
        elif isinstance(v, (int, float)):
            # Treat 1–5 agent-style as strong if >=4, else if exactly 0/1 use bit.
            iv = int(v)
            if iv in (0, 1):
                out[crit] = iv
            else:
                out[crit] = 1 if iv >= 4 else 0
        else:
            out[crit] = yn_to_bit(str(v))
    return out


def total_from_scores(scores: Mapping[str, int]) -> int:
    return sum(int(scores.get(c, 0)) for c in CRITERIA)


def apply_cli_scores(
    problem: MutableMapping[str, Any], scores: Mapping[str, Any]
) -> MutableMapping[str, Any]:
    """Mutate problem with normalized criteria_scores + total_score (0–5)."""
    normalized = normalize_cli_scores(scores)
    problem["criteria_scores"] = normalized
    problem["total_score"] = total_from_scores(normalized)
    return problem


def require_complete_cli_scores(raw: Mapping[str, Any]) -> Dict[str, int]:
    """
    Non-interactive: every criterion must be present (aliases OK).
    Raises ValueError if any criterion missing — do not invent Y/N.
    """
    found: Dict[str, Any] = {}
    for k, v in (raw or {}).items():
        crit = canonical_criterion(str(k))
        if crit:
            found[crit] = v
    missing = [c for c in CRITERIA if c not in found]
    if missing:
        raise ValueError(
            "criteria_scores missing required keys (no invented Y/N): "
            + ", ".join(missing)
        )
    return normalize_cli_scores(found)


def rank_problems(
    problems: Sequence[Mapping[str, Any]],
    *,
    score_key: str = "total_score",
) -> List[Dict[str, Any]]:
    """Return new list sorted by score descending (copies as dicts)."""
    return sorted(
        (dict(p) for p in problems),
        key=lambda x: int(x.get(score_key) or 0),
        reverse=True,
    )


def high_value_indices(
    problems: Sequence[Mapping[str, Any]],
    *,
    min_score: int = 4,
) -> List[int]:
    """Original indices of problems with total_score >= min_score."""
    return [
        i
        for i, p in enumerate(problems)
        if int(p.get("total_score") or 0) >= min_score
    ]


def cli_bit_to_agent_band(bit: int) -> int:
    """
    Documented bridge CLI 0/1 → agent 1–5 band (mid of weak/strong).
    0 → 2, 1 → 5 (conservative strong yes).
    """
    return 5 if int(bit) else 2


def cli_scores_to_agent_guemf(scores: Mapping[str, int]) -> Dict[str, int]:
    """Map CLI criteria_scores to agent-style 1–5 GUEMF dict + composite."""
    guemf = {c: cli_bit_to_agent_band(int(scores.get(c, 0))) for c in CRITERIA}
    guemf["composite"] = sum(guemf[c] for c in CRITERIA)
    return guemf


def problems_list_from_payload(payload: Any) -> List[Any]:
    """Accept {\"problems\": [...]} or a bare list."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, Mapping) and isinstance(payload.get("problems"), list):
        return list(payload["problems"])
    raise ValueError(
        "Inputs JSON must be a list of problems or an object with a 'problems' array."
    )
