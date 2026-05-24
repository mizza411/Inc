"""Tests for recent items tracking (Phase 2)."""

import json
from pathlib import Path

import inc_launcher.recent as recent_mod
from inc_launcher.config import load_config
from inc_launcher.recent import list_pinned, load_recent, record_recent, save_recent


def test_record_and_load_recent(tmp_path, monkeypatch):
    recent_file = tmp_path / "recent_items.json"
    monkeypatch.setattr(recent_mod, "RECENT_FILE", recent_file)

    item = {"label": "Test folder", "action": "folder", "path": "Started-Businesses"}
    record_recent(item, pillar_id="established")
    loaded = load_recent()

    assert len(loaded) == 1
    assert loaded[0]["label"] == "Test folder"
    assert loaded[0]["pillar_id"] == "established"


def test_recent_dedupes_and_caps(tmp_path, monkeypatch):
    recent_file = tmp_path / "recent_items.json"
    monkeypatch.setattr(recent_mod, "RECENT_FILE", recent_file)
    monkeypatch.setattr(recent_mod, "MAX_RECENT", 3)

    for i in range(5):
        record_recent({"label": f"Item {i}", "action": "folder", "path": f"p{i}"})

    assert len(load_recent()) == 3
    assert load_recent()[0]["label"] == "Item 4"

    record_recent({"label": "Item 1", "action": "folder", "path": "p1"})
    labels = [i["label"] for i in load_recent()]
    assert labels.count("Item 1") == 1
    assert labels[0] == "Item 1"


def test_list_pinned_from_config():
    config = load_config()
    pinned = list_pinned(config)
    labels = [p["label"] for p in pinned]
    assert "Run all strategies" in labels
    assert "Problem ID tool (local web)" in labels
    assert all(p.get("pillar_id") for p in pinned)


def test_save_recent_writes_json(tmp_path, monkeypatch):
    recent_file = tmp_path / "recent_items.json"
    monkeypatch.setattr(recent_mod, "RECENT_FILE", recent_file)

    save_recent([{"label": "A", "action": "file", "path": "x.md"}])
    data = json.loads(recent_file.read_text(encoding="utf-8"))
    assert data["recent"][0]["label"] == "A"
