"""Queue persistence for bookmark sorting."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from business_bookmark_sorter.chrome_import import extract_business_entries, parse_inbox_markdown
from business_bookmark_sorter.paths import INBOX_MD, QUEUE_PATH, default_chrome_bookmarks_path
from business_bookmark_sorter.suggest import suggest_destination


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_queue(path: Path | None = None) -> Dict[str, Any]:
    p = path or QUEUE_PATH
    if not p.is_file():
        return {"version": 1, "updated_at": _now(), "items": []}
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def save_queue(data: Dict[str, Any], path: Path | None = None) -> None:
    p = path or QUEUE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_routes_config(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_queue_item(
    entry: Dict[str, Any],
    config: Dict[str, Any],
    source: str = "chrome",
) -> Dict[str, Any]:
    dest_id, reason = suggest_destination(entry, config)
    dest = config.get("destinations", {}).get(dest_id, {})
    return {
        "id": str(uuid.uuid4()),
        "type": entry.get("type", "url"),
        "title": entry.get("title", ""),
        "url": entry.get("url", ""),
        "folder_path": entry.get("folder_path", ""),
        "status": "pending",
        "source": source,
        "suggested_destination": dest_id,
        "suggested_reason": reason,
        "suggested_links_file": dest.get("links_file"),
        "chrome_id": entry.get("chrome_id"),
        "note": entry.get("note"),
        "imported_at": _now(),
    }


def merge_import(
    entries: List[Dict[str, Any]],
    config: Dict[str, Any],
    source: str = "chrome",
    replace: bool = False,
) -> Dict[str, Any]:
    queue = {"version": 1, "items": []} if replace else load_queue()
    existing_urls = {
        (i.get("url") or "").strip()
        for i in queue.get("items", [])
        if i.get("type") == "url" and i.get("url")
    }
    existing_folders = {
        (i.get("folder_path", ""), i.get("title", ""))
        for i in queue.get("items", [])
        if i.get("type") == "folder"
    }

    added = 0
    for entry in entries:
        if entry.get("type") == "url":
            u = (entry.get("url") or "").strip()
            if u and u in existing_urls:
                continue
            if u:
                existing_urls.add(u)
        else:
            key = (entry.get("folder_path", ""), entry.get("title", ""))
            if key in existing_folders:
                continue
            existing_folders.add(key)

        queue.setdefault("items", []).append(build_queue_item(entry, config, source=source))
        added += 1

    save_queue(queue)
    queue["_added"] = added
    return queue


def count_by_status(queue: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in queue.get("items", []):
        s = item.get("status", "pending")
        counts[s] = counts.get(s, 0) + 1
    return counts


def next_pending(queue: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for item in queue.get("items", []):
        if item.get("status") == "pending":
            return item
    return None


def _entry_key(entry: Dict[str, Any]) -> Tuple[str, str]:
    if entry.get("type") == "url":
        return ("url", (entry.get("url") or "").strip())
    folder = entry.get("folder_path", "")
    title = entry.get("title", "")
    return ("folder", f"{folder}|{title}")


def refresh_queue_from_sources(
    config: Dict[str, Any],
    bookmarks_path: Path | None = None,
    merge_inbox: bool = True,
) -> Dict[str, Any]:
    """
    Refresh queue with latest Chrome bookmarks while preserving completed statuses.

    Rules:
    - Keep non-pending statuses (filed/skipped/stay_in_chrome) for known items.
    - Mark previously pending items that disappeared from sources as gone_from_chrome.
    - Add new source items as pending with fresh suggestions.
    """
    src: List[Dict[str, Any]] = extract_business_entries(
        bookmarks_path or default_chrome_bookmarks_path(),
        config.get("chrome_filter"),
    )
    if merge_inbox:
        src.extend(parse_inbox_markdown(INBOX_MD))

    latest_by_key = {_entry_key(e): e for e in src}
    queue = load_queue()
    existing_items = queue.get("items", [])
    existing_by_key = {_entry_key(i): i for i in existing_items}
    existing_keys = set(existing_by_key.keys())

    refreshed: List[Dict[str, Any]] = []
    for key, entry in latest_by_key.items():
        old = existing_by_key.get(key)
        if old:
            item = dict(old)
            item["title"] = entry.get("title", item.get("title", ""))
            item["folder_path"] = entry.get("folder_path", item.get("folder_path", ""))
            item["chrome_id"] = entry.get("chrome_id")
            item["note"] = entry.get("note")
            if item.get("status") == "gone_from_chrome":
                item["status"] = "pending"
            refreshed.append(item)
        else:
            refreshed.append(build_queue_item(entry, config, source="chrome"))

    for old in existing_items:
        key = _entry_key(old)
        if key in latest_by_key:
            continue
        if old.get("status") == "pending":
            gone = dict(old)
            gone["status"] = "gone_from_chrome"
            gone["removed_at"] = _now()
            refreshed.append(gone)
        else:
            refreshed.append(old)

    queue["items"] = refreshed
    queue["last_sync_at"] = _now()
    save_queue(queue)
    queue["_added_on_sync"] = len(set(latest_by_key.keys()) - existing_keys)
    return queue
