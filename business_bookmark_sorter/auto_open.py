"""Open the current bookmark URL once per item (BB-TIMED-1 Phase 3).

Never bulk-opens the queue — one URL for the item currently shown.
"""

from __future__ import annotations

from typing import Callable, Optional, Set

OpenUrl = Callable[[str], None]


class LinkAutoOpener:
    """Debounced opener: each item id opens at most once until reset."""

    def __init__(self, open_url: Optional[OpenUrl] = None) -> None:
        self._open_url: OpenUrl = open_url or _default_open
        self._opened_ids: Set[str] = set()

    def reset(self) -> None:
        self._opened_ids.clear()

    def maybe_open(
        self,
        *,
        item_id: str,
        url: str,
        enabled: bool,
    ) -> bool:
        """Open url if enabled and not yet opened for this id. Returns True if opened."""
        if not enabled:
            return False
        uid = (item_id or "").strip()
        href = (url or "").strip()
        if not uid or not href:
            return False
        if uid in self._opened_ids:
            return False
        self._opened_ids.add(uid)
        self._open_url(href)
        return True


def _default_open(url: str) -> None:
    import webbrowser

    webbrowser.open(url)
