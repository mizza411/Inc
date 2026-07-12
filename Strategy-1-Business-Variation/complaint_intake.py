"""Normalize and score Strategy 1 complaints (playbook Steps 2-3)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

CATEGORIES = ("UX", "performance", "cost", "support", "other")
FREQUENCY_LEVELS = ("Daily", "Weekly", "Monthly", "Occasional")
IMPACT_LEVELS = ("High", "Medium", "Low")
SOLVABILITY_LEVELS = ("High", "Medium", "Low")

_FREQ_SCORE = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Occasional": 0}
_IMPACT_SCORE = {"High": 3, "Medium": 2, "Low": 1}
_SOLVE_SCORE = {"High": 3, "Medium": 2, "Low": 1}


def _norm_choice(value: str, allowed: tuple, default: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return default
    lower_map = {a.lower(): a for a in allowed}
    # Accept UX as UX; performance aliases
    if raw.lower() in lower_map:
        return lower_map[raw.lower()]
    if raw.lower() in ("ux", "user experience", "usability"):
        return "UX"
    return default


def normalize_complaint(
    text: str,
    *,
    source: str = "manual",
    category: str = "other",
    frequency: str = "Weekly",
    impact: str = "Medium",
    solvability: str = "Medium",
) -> Dict[str, Any]:
    complaint = {
        "text": (text or "").strip(),
        "source": (source or "manual").strip() or "manual",
        "category": _norm_choice(category, CATEGORIES, "other"),
        "frequency": _norm_choice(frequency, FREQUENCY_LEVELS, "Weekly"),
        "impact": _norm_choice(impact, IMPACT_LEVELS, "Medium"),
        "solvability": _norm_choice(solvability, SOLVABILITY_LEVELS, "Medium"),
    }
    complaint["score"] = score_complaint(complaint)
    return complaint


def score_complaint(complaint: Dict[str, Any]) -> int:
    """Higher = more frequent + painful + solvable (playbook prioritization)."""
    return (
        _FREQ_SCORE.get(complaint.get("frequency", ""), 0)
        + _IMPACT_SCORE.get(complaint.get("impact", ""), 0)
        + _SOLVE_SCORE.get(complaint.get("solvability", ""), 0)
    )


def complaints_from_seed_examples(
    business: Dict[str, Any],
    *,
    default_frequency: str = "Weekly",
    default_impact: str = "Medium",
    default_solvability: str = "Medium",
) -> List[Dict[str, Any]]:
    """Build complaint records from seed example_complaints strings."""
    out: List[Dict[str, Any]] = []
    for text in business.get("example_complaints") or []:
        if not str(text).strip():
            continue
        out.append(
            normalize_complaint(
                str(text),
                source="seed_example",
                category="other",
                frequency=default_frequency,
                impact=default_impact,
                solvability=default_solvability,
            )
        )
    return out


def parse_inputs_payload(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate non-interactive inputs JSON.

    Expected shape:
    {
      "businesses": [
        {
          "name": "...",
          "id": "optional",
          "complaints": [
            {"text": "...", "source": "...", "category": "...",
             "frequency": "...", "impact": "...", "solvability": "..."}
          ]
        }
      ]
    }
    """
    raw = data.get("businesses")
    if not isinstance(raw, list) or not raw:
        raise ValueError("inputs JSON must include a non-empty 'businesses' list")

    results: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            raise ValueError("each business requires a non-empty 'name'")
        complaints_raw = item.get("complaints") or []
        if not isinstance(complaints_raw, list) or not complaints_raw:
            raise ValueError(f"business '{name}' needs at least one complaint")
        complaints: List[Dict[str, Any]] = []
        for c in complaints_raw:
            if isinstance(c, str):
                complaints.append(normalize_complaint(c, source="inputs"))
            elif isinstance(c, dict):
                text = str(c.get("text") or c.get("complaint") or "").strip()
                if not text:
                    continue
                complaints.append(
                    normalize_complaint(
                        text,
                        source=str(c.get("source") or "inputs"),
                        category=str(c.get("category") or "other"),
                        frequency=str(c.get("frequency") or "Weekly"),
                        impact=str(c.get("impact") or "Medium"),
                        solvability=str(c.get("solvability") or "Medium"),
                    )
                )
        if not complaints:
            raise ValueError(f"business '{name}' has no usable complaints")
        results.append(
            {
                "id": item.get("id"),
                "name": name,
                "category": item.get("category") or "",
                "complaints": sorted(complaints, key=lambda x: x["score"], reverse=True),
            }
        )
    if not results:
        raise ValueError("no valid businesses parsed from inputs")
    return results


def interactive_pick_businesses(seeds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """CLI: pick seed indices and/or enter custom business names."""
    print("\nSeed businesses:")
    for i, b in enumerate(seeds, 1):
        print(f"  {i}. {b.get('name')} ({b.get('category', '')})")
    print("  C. Custom business name(s)")

    sel = input(
        "\nSelect seeds (comma numbers), 'C' for custom, or both "
        "(e.g. 1,3 or 1,C) [default=1]: "
    ).strip() or "1"

    chosen: List[Dict[str, Any]] = []
    want_custom = False
    for part in sel.split(","):
        token = part.strip()
        if not token:
            continue
        if token.upper() == "C":
            want_custom = True
            continue
        try:
            idx = int(token) - 1
        except ValueError:
            print(f"  Skipping invalid token: {token}")
            continue
        if 0 <= idx < len(seeds):
            chosen.append(dict(seeds[idx]))
        else:
            print(f"  Skipping out-of-range: {token}")

    if want_custom or not chosen:
        while True:
            name = input("Custom successful business name (Enter to finish): ").strip()
            if not name:
                break
            cat = input("  Category [optional]: ").strip()
            chosen.append({"id": None, "name": name, "category": cat, "example_complaints": []})

    if not chosen:
        raise ValueError("No businesses selected")
    return chosen


def interactive_collect_complaints(business: Dict[str, Any]) -> List[Dict[str, Any]]:
    """CLI: paste complaints for one business; offer seed examples if present."""
    print(f"\n--- Complaints for: {business.get('name')} ---")
    examples = business.get("example_complaints") or []
    complaints: List[Dict[str, Any]] = []

    if examples:
        use = input(
            f"Load {len(examples)} seed example complaints? [Y/n]: "
        ).strip().lower()
        if use in ("", "y", "yes"):
            complaints.extend(complaints_from_seed_examples(business))
            print(f"  Loaded {len(complaints)} seed examples (you can add more).")

    print(
        "Enter complaints (blank description ends).\n"
        "For each: text, then optional source/category/frequency/impact/solvability.\n"
    )
    while True:
        text = input("Complaint text (Enter to finish): ").strip()
        if not text:
            break
        source = input("  Source [manual]: ").strip() or "manual"
        category = input(
            "  Category [UX/performance/cost/support/other] (default other): "
        ).strip() or "other"
        frequency = input(
            "  Frequency [Daily/Weekly/Monthly/Occasional] (default Weekly): "
        ).strip() or "Weekly"
        impact = input("  Impact [High/Medium/Low] (default Medium): ").strip() or "Medium"
        solvability = (
            input("  Solvability [High/Medium/Low] (default Medium): ").strip() or "Medium"
        )
        complaints.append(
            normalize_complaint(
                text,
                source=source,
                category=category,
                frequency=frequency,
                impact=impact,
                solvability=solvability,
            )
        )

    if not complaints:
        raise ValueError(f"No complaints collected for {business.get('name')}")
    return sorted(complaints, key=lambda x: x["score"], reverse=True)
