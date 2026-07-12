"""Normalize and score Strategy 1 complaints (playbook Steps 2-3).

§11 Phase B: complaints require citeable http(s) source_url (no seed examples).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

CATEGORIES = ("UX", "performance", "cost", "support", "other")
FREQUENCY_LEVELS = ("Daily", "Weekly", "Monthly", "Occasional")
IMPACT_LEVELS = ("High", "Medium", "Low")
SOLVABILITY_LEVELS = ("High", "Medium", "Low")

_FREQ_SCORE = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Occasional": 0}
_IMPACT_SCORE = {"High": 3, "Medium": 2, "Low": 1}
_SOLVE_SCORE = {"High": 3, "Medium": 2, "Low": 1}


def is_http_url(value: str) -> bool:
    raw = (value or "").strip()
    try:
        parsed = urlparse(raw)
    except Exception:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def require_http_url(value: str, *, field: str) -> str:
    raw = (value or "").strip()
    if not is_http_url(raw):
        raise ValueError(f"{field} must be an http(s) URL (got {raw!r})")
    return raw


def _norm_choice(value: str, allowed: tuple, default: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return default
    lower_map = {a.lower(): a for a in allowed}
    if raw.lower() in lower_map:
        return lower_map[raw.lower()]
    if raw.lower() in ("ux", "user experience", "usability"):
        return "UX"
    return default


def normalize_complaint(
    text: str,
    *,
    source_url: str,
    source: str = "online",
    category: str = "other",
    frequency: str = "Weekly",
    impact: str = "Medium",
    solvability: str = "Medium",
) -> Dict[str, Any]:
    url = require_http_url(source_url, field="complaint source_url")
    complaint = {
        "text": (text or "").strip(),
        "source": (source or "online").strip() or "online",
        "source_url": url,
        "category": _norm_choice(category, CATEGORIES, "other"),
        "frequency": _norm_choice(frequency, FREQUENCY_LEVELS, "Weekly"),
        "impact": _norm_choice(impact, IMPACT_LEVELS, "Medium"),
        "solvability": _norm_choice(solvability, SOLVABILITY_LEVELS, "Medium"),
    }
    if not complaint["text"]:
        raise ValueError("complaint text must be non-empty")
    complaint["score"] = score_complaint(complaint)
    return complaint


def score_complaint(complaint: Dict[str, Any]) -> int:
    """Higher = more frequent + painful + solvable (playbook prioritization)."""
    return (
        _FREQ_SCORE.get(complaint.get("frequency", ""), 0)
        + _IMPACT_SCORE.get(complaint.get("impact", ""), 0)
        + _SOLVE_SCORE.get(complaint.get("solvability", ""), 0)
    )


def parse_inputs_payload(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate non-interactive inputs JSON (URL-cited).

    Expected shape:
    {
      "businesses": [
        {
          "name": "...",
          "success_url": "https://...",
          "category": "optional",
          "complaints": [
            {"text": "...", "source_url": "https://...", "source": "...",
             "category": "...", "frequency": "...", "impact": "...",
             "solvability": "..."}
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
        success_url = require_http_url(
            str(item.get("success_url") or item.get("business_url") or ""),
            field=f"business '{name}' success_url",
        )
        complaints_raw = item.get("complaints") or []
        if not isinstance(complaints_raw, list) or not complaints_raw:
            raise ValueError(f"business '{name}' needs at least one complaint")
        complaints: List[Dict[str, Any]] = []
        for c in complaints_raw:
            if not isinstance(c, dict):
                raise ValueError(
                    f"business '{name}': each complaint must be an object with "
                    "text + source_url (strings alone are not allowed)"
                )
            text = str(c.get("text") or c.get("complaint") or "").strip()
            source_url = str(c.get("source_url") or c.get("url") or "").strip()
            if not text:
                continue
            complaints.append(
                normalize_complaint(
                    text,
                    source_url=source_url,
                    source=str(c.get("source") or "online"),
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
                "success_url": success_url,
                "complaints": sorted(complaints, key=lambda x: x["score"], reverse=True),
            }
        )
    if not results:
        raise ValueError("no valid businesses parsed from inputs")
    return results


def interactive_collect_businesses() -> List[Dict[str, Any]]:
    """CLI: enter online-discovered businesses + URL-cited complaints (no seed list)."""
    print(
        "\nOnline discovery mode (no seed_businesses.json).\n"
        "For each successful business: name + success evidence URL, then complaints "
        "each with a source URL (review, news, forum, app store, etc.).\n"
    )
    chosen: List[Dict[str, Any]] = []
    while True:
        name = input("Successful business name (Enter to finish): ").strip()
        if not name:
            break
        success_url = input("  Success evidence URL (https://...): ").strip()
        try:
            success_url = require_http_url(success_url, field="success_url")
        except ValueError as exc:
            print(f"  Error: {exc}")
            continue
        cat = input("  Category [optional]: ").strip()
        biz = {
            "id": None,
            "name": name,
            "category": cat,
            "success_url": success_url,
        }
        try:
            complaints = interactive_collect_complaints(biz)
        except ValueError as exc:
            print(f"  Error: {exc}")
            continue
        biz["complaints"] = complaints
        chosen.append(biz)

    if not chosen:
        raise ValueError("No businesses collected")
    return chosen


def interactive_collect_complaints(business: Dict[str, Any]) -> List[Dict[str, Any]]:
    """CLI: paste URL-cited complaints for one business."""
    print(f"\n--- Complaints for: {business.get('name')} ---")
    print("Each complaint needs text + http(s) source_url.\n")
    complaints: List[Dict[str, Any]] = []
    while True:
        text = input("Complaint text (Enter to finish): ").strip()
        if not text:
            break
        source_url = input("  Source URL (https://...): ").strip()
        source = input("  Source label [online]: ").strip() or "online"
        category = (
            input(
                "  Category [UX/performance/cost/support/other] (default other): "
            ).strip()
            or "other"
        )
        frequency = (
            input(
                "  Frequency [Daily/Weekly/Monthly/Occasional] (default Weekly): "
            ).strip()
            or "Weekly"
        )
        impact = input("  Impact [High/Medium/Low] (default Medium): ").strip() or "Medium"
        solvability = (
            input("  Solvability [High/Medium/Low] (default Medium): ").strip() or "Medium"
        )
        try:
            complaints.append(
                normalize_complaint(
                    text,
                    source_url=source_url,
                    source=source,
                    category=category,
                    frequency=frequency,
                    impact=impact,
                    solvability=solvability,
                )
            )
        except ValueError as exc:
            print(f"  Skipped: {exc}")

    if not complaints:
        raise ValueError(f"No complaints collected for {business.get('name')}")
    return sorted(complaints, key=lambda x: x["score"], reverse=True)
