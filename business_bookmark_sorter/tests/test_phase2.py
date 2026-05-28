"""Tests for Phase 2 file + review actions."""

from pathlib import Path

import business_bookmark_sorter.file_link as fl
from business_bookmark_sorter.queue_store import build_queue_item, load_routes_config
from business_bookmark_sorter.review_actions import apply_file, apply_skip, apply_stay_in_chrome

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_append_link_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(fl, "INC_ROOT", tmp_path)
    config = load_routes_config(CONFIG)
    item = {
        "type": "url",
        "title": "Test Biz",
        "url": "https://example.com/biz",
        "folder_path": "bar",
    }
    path = fl.append_link(item, config, "started")
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "https://example.com/biz" in text


def test_apply_file_and_skip(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    from business_bookmark_sorter.paths import QUEUE_PATH

    qpath = tmp_path / "queue.json"
    monkeypatch.setattr(qs, "QUEUE_PATH", qpath)
    monkeypatch.setattr(fl, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Lead tool", "url": "https://example.com/abuja", "folder_path": ""},
        config,
    )
    queue = {"version": 1, "items": [item]}
    qs.save_queue(queue)

    ok, _ = apply_file(item["id"], "leads", config)
    assert ok
    updated = qs.load_queue()
    assert updated["items"][0]["status"] == "filed"

    item2 = build_queue_item(
        {"type": "url", "title": "Skip me", "url": "https://example.com/skip", "folder_path": ""},
        config,
    )
    queue["items"].append(item2)
    qs.save_queue(queue)
    ok2, _ = apply_skip(item2["id"])
    assert ok2

    item3 = build_queue_item(
        {"type": "url", "title": "Chrome only", "url": "https://example.com/stay", "folder_path": ""},
        config,
    )
    queue = qs.load_queue()
    queue["items"].append(item3)
    qs.save_queue(queue)
    ok3, _ = apply_stay_in_chrome(item3["id"])
    assert ok3
    assert qs.load_queue()["items"][-1]["status"] == "stay_in_chrome"
