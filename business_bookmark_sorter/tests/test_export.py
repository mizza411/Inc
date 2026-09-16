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


def test_export_master_flat_list_no_category_headings(tmp_path, monkeypatch):
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
    a["filed_at"] = "2026-08-20T10:00:00+00:00"
    b = build_queue_item(
        {"type": "url", "title": "YT", "url": "https://youtube.com/b", "folder_path": ""},
        config,
    )
    b["status"] = "filed"
    b["filed_destination"] = "automation"
    b["filed_at"] = "2026-08-20T11:00:00+00:00"
    save_queue({"version": 1, "items": [a, b]})
    queue = load_queue()

    count, path = export_master_document(config, queue)
    assert count == 2
    assert path == master_links_path(config)
    text = path.read_text(encoding="utf-8")
    assert "## My leads" not in text
    assert "## Automation / content" not in text
    assert "## Problem identification" not in text
    assert "example.com/a" in text
    assert "youtube.com" in text
    # last filed (b) is last link line
    link_lines = [ln for ln in text.splitlines() if ln.startswith("- ")]
    assert len(link_lines) == 2
    assert "youtube.com" in link_lines[-1]
    assert "example.com/a" in link_lines[0]

    count2, paths = export_filed_to_markdown(config, queue)
    assert count2 == 2
    assert len(paths) == 1


def test_export_sectioned_mode_when_flat_list_false(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    config = {**config, "export": {**config.get("export", {}), "flat_list": False}}
    a = build_queue_item(
        {"type": "url", "title": "Lead", "url": "https://example.com/a", "folder_path": ""},
        config,
    )
    a["status"] = "filed"
    a["filed_destination"] = "leads"
    save_queue({"version": 1, "items": [a]})
    text = export_master_document(config, load_queue())[1].read_text(encoding="utf-8")
    assert "## My leads" in text


def test_inbox_filed_items_export_in_flat_list(tmp_path, monkeypatch):
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
    item["filed_at"] = "2026-08-20T12:00:00+00:00"
    save_queue({"version": 1, "items": [item]})

    _, path = export_master_document(config, load_queue())
    text = path.read_text(encoding="utf-8")
    assert "## Other" not in text
    assert "example.com/misc" in text


def test_export_keeps_hand_typed_extra_links(tmp_path, monkeypatch):
    """Saved extra lines stay; newly filed queue links are appended."""
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    master = master_links_path(config)
    master.parent.mkdir(parents=True, exist_ok=True)
    master.write_text(
        "# Business Links\n\n"
        "- [KeepMe](https://example.com/keep)\n"
        "- [HandTypedExtra](https://example.com/extra)\n",
        encoding="utf-8",
    )
    keep = build_queue_item(
        {
            "type": "url",
            "title": "KeepMe",
            "url": "https://example.com/keep",
            "folder_path": "",
        },
        config,
    )
    keep["status"] = "filed"
    keep["filed_destination"] = "other"
    keep["filed_at"] = "2026-09-16T10:00:00+00:00"
    newbie = build_queue_item(
        {
            "type": "url",
            "title": "NewFiled",
            "url": "https://example.com/new",
            "folder_path": "",
        },
        config,
    )
    newbie["status"] = "filed"
    newbie["filed_destination"] = "other"
    newbie["filed_at"] = "2026-09-16T11:00:00+00:00"
    save_queue({"version": 1, "items": [keep, newbie]})

    count, path = export_master_document(config, load_queue())
    text = path.read_text(encoding="utf-8")
    bullets = [ln for ln in text.splitlines() if ln.startswith("- ")]
    assert count == 3
    assert bullets == [
        "- [KeepMe](https://example.com/keep)",
        "- [HandTypedExtra](https://example.com/extra)",
        "- [NewFiled](https://example.com/new)",
    ]
