"""
Interactive Nigeria official / open data portal picker (Strategy 5–style UX).

Numbered list, comma-separated multi-select, optional open in Chrome/default browser.
URLs are entry points; verify current pages on the live sites over time.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from browser_links import open_urls_in_browser

# (short label, https URL) — NBS + open data catalogs (curated; CBN/finance/OAGF/NBS home omitted by design)
DEFAULT_PORTALS: List[Tuple[str, str]] = [
    ("National Bureau of Statistics (NBS) — eLibrary (reports)", "https://www.nigerianstat.gov.ng/elibrary/"),
    ("National Bureau of Statistics (NBS) — Microdata Catalog", "https://microdata.nigerianstat.gov.ng/index.php/home"),
    ("Open Data for Africa — Nigeria", "https://nigeria.opendataforafrica.org/"),
    ("Open Data for Africa — Nigeria foreign trade", "https://nigeriaforeigntrade.opendataforafrica.org/"),
]


def _parse_indices(selection: str, n: int) -> List[int]:
    """Parse '1,3,5' or '1, 2' into 0-based indices; ignore invalid/out-of-range."""
    out: List[int] = []
    seen: set[int] = set()
    for part in selection.split(","):
        part = part.strip()
        if not part.isdigit():
            continue
        idx = int(part) - 1
        if 0 <= idx < n and idx not in seen:
            seen.add(idx)
            out.append(idx)
    return out


def run_portal_selection_interactive(portals: Sequence[Tuple[str, str]] | None = None) -> List[str]:
    """
    Prompt user to pick portals (like Strategy 5 news source selection).
    Optionally opens selected URLs in the browser.
    Returns the list of selected https URLs (for callers that want to log or merge).
    """
    items = list(portals) if portals is not None else list(DEFAULT_PORTALS)
    n = len(items)

    print("\n" + "=" * 60)
    print("STEP 1: Select Nigeria official / open data portals")
    print("=" * 60)
    print("\nINSTRUCTIONS:")
    print("  • Each number below is one official entry-point URL.")
    print("  • Type the numbers you want, separated by commas (no spaces required). Examples: 1   or   1,3   or   2,4,5")
    print("  • Press Enter at 'Selection:' to submit. You need at least one valid number.")
    print("  • Next you will be asked whether to open those URLs in your browser.")
    print("\nAvailable entry points (bookmark these; verify pages if a link moves):")
    for i, (label, url) in enumerate(items, 1):
        print(f"  {i}. {label}")
        print(f"     {url}")

    print("\nTip: Use eLibrary for published reports; Microdata for datasets; Open Data for Africa")
    print("for indicators and trade — then open the specific report or table before Step 2.")
    print("\nEnter your selection now:")

    selection = input("Selection: ").strip()
    indices = _parse_indices(selection, n)
    if not indices:
        print("\nNo valid selection.")
        print("INSTRUCTIONS: Re-run the script and type at least one number from 1 to", n, "at 'Selection:'.")
        print("Example: 1  or  1,2")
        return []

    selected: List[Tuple[str, str]] = [items[i] for i in indices]
    selected_urls = [url for _, url in selected]

    print(f"\n✓ Selected {len(selected)} portal(s):")
    for label, url in selected:
        print(f"  - {label}")
        print(f"    {url}")

    choice = input(
        "\nOpen selected portal(s) in Chrome/default browser now? (y/n, default=y): "
    ).strip().lower()
    if choice in ("", "y", "yes"):
        print("\nOpening selected portal(s) in your default browser...")
        print("(Use the open tabs to find the exact table or figure; Step 2 will capture or paste text.)")
        open_urls_in_browser(selected_urls)
    else:
        print("\nBrowser open skipped. Step 2 can still auto-fetch each URL or you can paste manually.")

    return selected_urls
