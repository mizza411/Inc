"""Suggest Inc destination from URL, title, and folder path."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def load_routes(config: Dict[str, Any]) -> Dict[str, Any]:
    return config.get("destinations", {})


def suggest_destination(entry: Dict[str, Any], config: Dict[str, Any]) -> Tuple[str, str]:
    """
    Return (destination_id, reason).
    destination_id is a key in config.destinations.
    """
    destinations = config.get("destinations", {})
    default = "other"
    if entry.get("type") == "folder":
        return default, "Bookmark folder — review in Chrome first (suggested Other)"

    haystack = " ".join(
        [
            entry.get("title") or "",
            entry.get("url") or "",
            entry.get("folder_path") or "",
        ]
    ).lower()

    best_id = default
    best_score = 0
    best_kw = ""

    for rule in config.get("keyword_rules", []):
        dest = rule.get("destination", default)
        if dest not in destinations:
            continue
        for kw in rule.get("keywords", []):
            k = kw.lower()
            if k and k in haystack:
                score = len(k)
                if score > best_score:
                    best_score = score
                    best_id = dest
                    best_kw = kw

    if best_score:
        label = destinations.get(best_id, {}).get("label", best_id)
        return best_id, f"Keyword '{best_kw}' → {label}"

    return default, "No keyword match — suggested Other (not forced into a pillar)"
