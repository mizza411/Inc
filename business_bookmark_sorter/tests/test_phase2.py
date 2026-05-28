"""Tests for Phase 2 review actions (JSON-first)."""

from pathlib import Path

from business_bookmark_sorter.queue_store import build_queue_item, load_routes_config, save_queue
from business_bookmark_sorter.review_actions import apply_mark_filed, apply_skip, apply_stay_in_chrome

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_apply_mark_filed_and_skip(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs

    qpath = tmp_path / "queue.json"
    monkeypatch.setattr(qs, "QUEUE_PATH", qpath)

    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Lead tool", "url": "https://example.com/abuja", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [item]})

    ok, _ = apply_mark_filed(item["id"], "leads", config)
    assert ok
    updated = qs.load_queue()
    assert updated["items"][0]["status"] == "filed"
    assert updated["items"][0]["filed_destination"] == "leads"

    item2 = build_queue_item(
        {"type": "url", "title": "Skip me", "url": "https://example.com/skip", "folder_path": ""},
        config,
    )
    queue = qs.load_queue()
    queue["items"].append(item2)
    save_queue(queue)
    ok2, _ = apply_skip(item2["id"])
    assert ok2

    item3 = build_queue_item(
        {"type": "url", "title": "Chrome only", "url": "https://example.com/stay", "folder_path": ""},
        config,
    )
    queue = qs.load_queue()
    queue["items"].append(item3)
    save_queue(queue)
    ok3, _ = apply_stay_in_chrome(item3["id"])
    assert ok3
    assert qs.load_queue()["items"][-1]["status"] == "stay_in_chrome"
