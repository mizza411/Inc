"""
Per-portal catalog search suggestions for Strategy 15 Step 2.

These are dataset / indicator keywords for publisher search boxes—not “business idea” queries.
Selection copies one term to the clipboard (via cursor_copy_helper) so you avoid retyping.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    from cursor_copy_helper import copy_to_clipboard
except ImportError:
    copy_to_clipboard = None  # type: ignore[misc, assignment]


def _match_key(url: str) -> Optional[str]:
    u = (url or "").lower().rstrip("/")
    if "microdata.nigerianstat.gov.ng" in u:
        return "microdata"
    if "elibrary" in u and "nigerianstat" in u:
        return "elibrary"
    if "nigeriaforeigntrade.opendataforafrica.org" in u:
        return "odfa_trade"
    if "nigeria.opendataforafrica.org" in u:
        return "odfa_ng"
    return None


# Keywords tuned for catalog search boxes (verify on live sites over time).
_TERMS: dict[str, List[str]] = {
    "elibrary": [
        "consumer price index",
        "GDP",
        "labour force",
        "foreign trade",
        "demographic",
        "national accounts",
        "inflation",
        "agriculture",
    ],
    "microdata": [
        "food price",
        "kerosene",
        "premium motor spirit",
        "transport fare",
        "telecoms",
        "liquefied petroleum gas",
        "foreign trade",
        "CPI",
        "labour force",
    ],
    "odfa_ng": [
        "GDP",
        "inflation",
        "population",
        "trade",
        "unemployment",
        "agriculture",
        "health",
        "education",
    ],
    "odfa_trade": [
        "import",
        "export",
        "trade partner",
        "foreign trade",
        "HS",
        "commodity",
    ],
}


def get_search_terms_for_portal_url(url: str) -> List[str]:
    key = _match_key(url)
    if not key:
        return []
    return list(_TERMS.get(key, []))


def offer_catalog_search_term_menu(terms: List[str]) -> Optional[str]:
    """
    Print numbered search-term presets; copy selection to clipboard.
    Returns the chosen search phrase for audit (also when clipboard fails), or None if skipped.
    """
    if not terms:
        return None

    print("\n  Catalog search terms (for this site's search box):")
    print("  Pick a number to copy that phrase to the clipboard — paste with Ctrl+V in the portal search.")
    for i, t in enumerate(terms, 1):
        print(f"    {i:2}) {t}")
    other_idx = len(terms) + 1
    print(f"    {other_idx:2}) Other — type your own search phrase (then copied)")
    print(f"    {0:2}) Skip — do not copy a preset")

    phrase: Optional[str] = None
    while True:
        raw = input("  Search-term menu (number, or Enter=skip): ").strip()
        if raw == "":
            print("  Skipped preset search term.")
            return None
        if not raw.isdigit():
            print("  Enter a number, or Enter alone to skip.")
            continue
        choice = int(raw)
        if choice == 0:
            print("  Skipped preset search term.")
            return None
        if 1 <= choice <= len(terms):
            phrase = terms[choice - 1]
            break
        if choice == other_idx:
            phrase = input("  Type custom search phrase: ").strip()
            if not phrase:
                print("  Empty — try again or Enter to skip.")
                continue
            break
        print(f"  Enter 0–{other_idx}.")

    assert phrase is not None

    if copy_to_clipboard is None:
        print(f"\n  ⚠ Clipboard helper unavailable. Copy this manually:\n  {phrase}\n")
        return phrase

    if copy_to_clipboard(phrase):
        print(f"\n  ✓ Copied to clipboard: {phrase!r}")
        print("  Paste into the portal search field (Ctrl+V), open the dataset/report, then paste excerpt below.")
    else:
        print(f"\n  ⚠ Clipboard copy failed. Copy manually: {phrase!r}")

    return phrase
