"""
Strategy 15: optional browser opening for explicit http(s) URLs (e.g. source_url).

Phase A.1: modular helpers only — no dependency on nigeria_national_open_data.py.
Phase A.2 will wire CLI --open-links to collect_source_urls_from_raw_records + open_urls_in_browser.
"""

from __future__ import annotations

import os
import re
import webbrowser
from typing import Any, Dict, List, Sequence

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def is_http_url(value: str) -> bool:
    s = (value or "").strip()
    return bool(s) and bool(_URL_RE.match(s))


def collect_source_urls_from_raw_records(records: Sequence[Dict[str, Any]]) -> List[str]:
    """
    Collect http(s) URLs from each record's optional `source_url` field.
    Dedupes while preserving first-seen order.
    """
    seen: set[str] = set()
    out: List[str] = []
    for raw in records:
        if not isinstance(raw, dict):
            continue
        url = raw.get("source_url", "") or ""
        url = str(url).strip()
        if not is_http_url(url):
            continue
        if url in seen:
            continue
        seen.add(url)
        out.append(url)
    return out


def open_in_chrome_or_default(url: str) -> bool:
    """
    Open URL in Chrome on Windows if installed, else default browser.
    Returns True if open was attempted without raising.
    """
    try:
        browser = None
        if os.name == "nt":
            for path in (
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ):
                if os.path.exists(path):
                    browser = webbrowser.get(f'"{path}" %s')
                    break
        if browser is None:
            browser = webbrowser.get()
        browser.open(url)
        print(f"\n✓ Opened in browser: {url}")
        return True
    except Exception as exc:
        print(f"\n⚠ Could not open browser for URL ({exc}). Open manually: {url}")
        return False


def open_urls_in_browser(urls: Sequence[str]) -> None:
    """
    Open each URL in order; fail-soft per URL (does not raise).
    """
    for u in urls:
        open_in_chrome_or_default(u.strip())
