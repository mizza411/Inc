"""Apply review decisions to queue items (Phase 2)."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from business_bookmark_sorter.actions_log import log_action
from business_bookmark_sorter.file_link import append_link
from business_bookmark_sorter.queue_store import load_queue, save_queue


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


def apply_file(
    item_id: str,
    destination_id: str,
    config: Dict[str, Any],
) -> Tuple[bool, str]:
    if destination_id == "stay_in_chrome":
        return False, "Use stay-in-chrome action instead of file"

    queue = load_queue()
    item = find_item(queue, item_id)
    if not item:
        return False, f"Item not found: {item_id}"

    path = append_link(item, config, destination_id)

    update_item(
        queue,
        item_id,
        status="filed",
        filed_destination=destination_id,
        filed_links_file=str(path),
    )
    log_action(
        {
            "action": "filed",
            "item_id": item_id,
            "destination": destination_id,
            "path": str(path),
            "url": item.get("url"),
            "title": item.get("title"),
        }
    )
    return True, f"Filed to {path}"


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
