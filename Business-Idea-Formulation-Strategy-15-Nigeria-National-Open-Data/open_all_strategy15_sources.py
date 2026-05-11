#!/usr/bin/env python3
"""
Open every Strategy 15 default portal URL in the browser (same list as portal_menu.DEFAULT_PORTALS).

Run from this folder:
  python open_all_strategy15_sources.py

Uses browser_links.open_urls_in_browser (Chrome on Windows if installed, else default browser).
"""

from __future__ import annotations

from browser_links import open_urls_in_browser
from portal_menu import DEFAULT_PORTALS


def main() -> None:
    urls = [url for _, url in DEFAULT_PORTALS]
    print(f"Opening {len(urls)} portal URL(s) from portal_menu.DEFAULT_PORTALS:\n")
    for i, (label, url) in enumerate(DEFAULT_PORTALS, 1):
        print(f"  {i}. {label}")
        print(f"     {url}")
    print()
    open_urls_in_browser(urls)
    print("\nDone.")


if __name__ == "__main__":
    main()
