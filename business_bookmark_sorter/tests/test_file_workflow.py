"""Tests for Phase 2b file + export workflow."""

from pathlib import Path
from unittest.mock import patch

from business_bookmark_sorter.export_markdown import export_master_document, master_links_path
from business_bookmark_sorter.file_workflow import file_item
from business_bookmark_sorter.queue_store import build_queue_item, load_queue, load_routes_config, save_queue

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_export_master_includes_all_sections(tmp_path, monkeypatch):
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

    count, path = export_master_document(config, load_queue())
    assert count == 2
    text = path.read_text(encoding="utf-8")
    assert "example.com/a" in text
    assert "youtube.com" in text
    assert path == master_links_path(config)


def test_file_item_rollback_on_export_error(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")

    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "X", "url": "https://example.com/x", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [item]})

    with patch(
        "business_bookmark_sorter.file_workflow.export_destination",
        side_effect=RuntimeError("disk full"),
    ):
        result = file_item(item["id"], "leads", config, open_docx=False)

    assert not result.ok
    assert "reverted" in result.message.lower()
    updated = load_queue()["items"][0]
    assert updated["status"] == "pending"


def test_file_item_success_without_docx(tmp_path, monkeypatch):
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

    result = file_item(item["id"], "leads", config, open_docx=False)
    assert result.ok
    assert result.md_path == master_links_path(config)
    assert result.md_path.is_file()
    text = result.md_path.read_text(encoding="utf-8")
    assert "## My leads" in text
    updated = load_queue()["items"][0]
    assert updated["status"] == "filed"
    assert updated.get("exported_at")
