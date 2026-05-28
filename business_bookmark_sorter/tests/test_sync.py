"""Tests for startup/post-action sync behavior."""

from pathlib import Path

from business_bookmark_sorter.queue_store import (
    build_queue_item,
    load_routes_config,
    refresh_queue_from_sources,
    save_queue,
)

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_refresh_preserves_completed_and_marks_gone(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs

    qpath = tmp_path / "queue.json"
    monkeypatch.setattr(qs, "QUEUE_PATH", qpath)

    config = load_routes_config(CONFIG)
    keep = build_queue_item(
        {"type": "url", "title": "Keep", "url": "https://example.com/keep", "folder_path": ""},
        config,
    )
    keep["status"] = "filed"
    gone = build_queue_item(
        {"type": "url", "title": "Gone", "url": "https://example.com/gone", "folder_path": ""},
        config,
    )
    pending = build_queue_item(
        {"type": "url", "title": "Pending", "url": "https://example.com/pending", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [keep, gone, pending]}, path=qpath)

    monkeypatch.setattr(
        qs,
        "extract_business_entries",
        lambda _path, _filter: [
            {"type": "url", "title": "Keep", "url": "https://example.com/keep", "folder_path": ""},
            {"type": "url", "title": "New", "url": "https://example.com/new", "folder_path": ""},
        ],
    )
    monkeypatch.setattr(qs, "parse_inbox_markdown", lambda _path: [])
    monkeypatch.setattr(qs, "default_chrome_bookmarks_path", lambda: Path("dummy"))

    refreshed = refresh_queue_from_sources(config, merge_inbox=False)
    by_url = {item.get("url"): item for item in refreshed["items"] if item.get("type") == "url"}

    assert by_url["https://example.com/keep"]["status"] == "filed"
    assert by_url["https://example.com/new"]["status"] == "pending"
    assert by_url["https://example.com/gone"]["status"] == "gone_from_chrome"
    assert by_url["https://example.com/pending"]["status"] == "gone_from_chrome"
