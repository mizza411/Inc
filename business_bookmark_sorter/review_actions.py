"""Apply review decisions to queue items (JSON-first workflow)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from business_bookmark_sorter.actions_log import log_action
from business_bookmark_sorter.queue_store import load_queue, save_queue


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_item(queue: Dict[str, Any], item_id: str) -> Optional[Dict[str, Any]]:
    for item in queue.get("items", []):
        if item.get("id") == item_id:
            return item
    return None


def update_item(queue: Dict[str, Any], item_id: str, **fields: Any) -> Optional[Dict[str, Any]]:
    for item in queue.get("items", []):
        if item.get("id") == item_id:
            item.update(fields)
            save_queue(queue)
            return item
    return None


def revert_filed(item_id: str) -> bool:
    """Undo a failed export — return item to pending."""
    queue = load_queue()
    item = find_item(queue, item_id)
    if not item or item.get("status") != "filed":
        return False
    update_item(
        queue,
        item_id,
        status="pending",
        filed_destination=None,
        filed_links_file=None,
        filed_at=None,
        exported_at=None,
        exported_path=None,
    )
    return True


def resolve_file_destination(
    item: Optional[Dict[str, Any]],
    config: Dict[str, Any],
) -> str:
    """BB-LINKS-UX-1 / R1: default dest = suggested → other (no Assign picker).

    If the item is already filed, prefer ``filed_destination``. Never returns
    ``stay_in_chrome``. Falls back to ``other`` when suggest is missing/invalid.
    """
    destinations = config.get("destinations", {}) or {}

    def _ok(dest_id: str | None) -> bool:
        if not dest_id or dest_id == "stay_in_chrome":
            return False
        meta = destinations.get(dest_id)
        if not meta:
            return False
        if meta.get("assignable", True) is False and dest_id != "other":
            return False
        return True

    candidates: list[str | None] = []
    if item:
        if item.get("status") == "filed":
            candidates.append(item.get("filed_destination"))
        candidates.append(item.get("suggested_destination"))
        candidates.append(item.get("filed_destination"))
    candidates.append("other")

    for cand in candidates:
        if _ok(cand):
            assert cand is not None
            return cand
    # Last resort if config has no "other"
    for key, meta in destinations.items():
        if key != "stay_in_chrome" and meta.get("assignable", True) is not False:
            return key
    return "other"


def mark_exported(item_id: str, md_path: Path) -> None:
    queue = load_queue()
    update_item(
        queue,
        item_id,
        exported_at=_now(),
        exported_path=str(md_path.resolve()),
    )


def apply_mark_filed(
    item_id: str,
    destination_id: str,
    config: Dict[str, Any],
) -> Tuple[bool, str]:
    """Record filing decision in queue.json (markdown via file_workflow / export-md)."""
    if destination_id == "stay_in_chrome":
        return False, "Use Stay in Chrome instead"

    dest = config.get("destinations", {}).get(destination_id, {})
    if not dest:
        return False, f"Unknown destination: {destination_id}"

    queue = load_queue()
    item = find_item(queue, item_id)
    if not item:
        return False, f"Item not found: {item_id}"

    master = config.get("export", {}).get(
        "master_links_file",
        "business_bookmark_sorter/Business Links.md",
    )
    update_item(
        queue,
        item_id,
        status="filed",
        filed_destination=destination_id,
        filed_links_file=master,
        filed_at=_now(),
    )
    log_action(
        {
            "action": "marked_filed",
            "item_id": item_id,
            "destination": destination_id,
            "url": item.get("url"),
            "title": item.get("title"),
        }
    )
    label = dest.get("label", destination_id)
    return True, f"Marked filed → {label} (saved in queue.json)"


def apply_skip(item_id: str) -> Tuple[bool, str]:
    queue = load_queue()
    item = find_item(queue, item_id)
    if not item:
        return False, f"Item not found: {item_id}"
    update_item(queue, item_id, status="skipped")
    log_action({"action": "skipped", "item_id": item_id, "url": item.get("url")})
    return True, "Skipped (can re-queue manually later)"


def apply_stay_in_chrome(item_id: str) -> Tuple[bool, str]:
    queue = load_queue()
    item = find_item(queue, item_id)
    if not item:
        return False, f"Item not found: {item_id}"
    update_item(queue, item_id, status="stay_in_chrome")
    log_action({"action": "stay_in_chrome", "item_id": item_id, "url": item.get("url")})
    return True, "Marked stay in Chrome — bookmark unchanged"


# Backward-compatible alias used by older CLI/tests
def apply_file(item_id: str, destination_id: str, config: Dict[str, Any]) -> Tuple[bool, str]:
    return apply_mark_filed(item_id, destination_id, config)
