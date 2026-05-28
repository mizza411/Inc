"""Tests for markdown export from queue.json."""

from pathlib import Path

from business_bookmark_sorter.export_markdown import (
    export_filed_to_markdown,
    export_master_document,
    master_links_path,
    section_id_for_export,
)
from business_bookmark_sorter.queue_store import build_queue_item, load_queue, load_routes_config, save_queue
from business_bookmark_sorter.review_actions import apply_mark_filed
from business_bookmark_sorter.suggest import suggest_destination

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_suggest_no_match_defaults_to_other():
    config = load_routes_config(CONFIG)
    entry = {"type": "url", "title": "Random", "url": "https://example.com/x", "folder_path": ""}
    dest, reason = suggest_destination(entry, config)
    assert dest == "other"
    assert "Other" in reason or "other" in reason.lower()


def test_section_id_maps_legacy_inbox_to_other():
    assert section_id_for_export("inbox") == "other"
    assert section_id_for_export("leads") == "leads"


def test_mark_filed_does_not_write_markdown(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Lead", "url": "https://example.com/abuja", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [item]})

    ok, _ = apply_mark_filed(item["id"], "leads", config)
    assert ok

    master = master_links_path(config)
    assert not master.is_file()


def test_export_master_single_file_with_sections(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    a = build_queue_item(
        {"type": "url", "title": "Lead", "url": "https://example.com/a", "folder_path": ""},
        config,
    )
    a["status"] = "filed"
    a["filed_destination"] = "leads"
    b = build_queue_item(
        {"type": "url", "title": "YT", "url": "https://youtube.com/b", "folder_path": ""},
        config,
    )
    b["status"] = "filed"
    b["filed_destination"] = "automation"
    save_queue({"version": 1, "items": [a, b]})
    queue = load_queue()

    count, path = export_master_document(config, queue)
    assert count == 2
    assert path == master_links_path(config)
    text = path.read_text(encoding="utf-8")
    assert "## My leads" in text
    assert "## Automation / content" in text
    assert "example.com/a" in text
    assert "youtube.com" in text

    count2, paths = export_filed_to_markdown(config, queue)
    assert count2 == 2
    assert len(paths) == 1


def test_inbox_filed_items_export_under_other_section(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Misc", "url": "https://example.com/misc", "folder_path": ""},
        config,
    )
    item["status"] = "filed"
    item["filed_destination"] = "inbox"
    save_queue({"version": 1, "items": [item]})

    _, path = export_master_document(config, load_queue())
    text = path.read_text(encoding="utf-8")
    assert "## Other" in text
    assert "example.com/misc" in text
