"""BB-LINKS-UX-1 Phase 2 — flat Business Links; last filed = last line."""

from __future__ import annotations

from pathlib import Path

from business_bookmark_sorter.export_markdown import (
    export_master_document,
    use_flat_list,
)
from business_bookmark_sorter.queue_store import build_queue_item, load_routes_config, save_queue

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_routes_enable_flat_list():
    config = load_routes_config(CONFIG)
    assert use_flat_list(config) is True
    assert config.get("export", {}).get("sort_by") == "filed_at"


def test_last_filed_is_last_link_line(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    import business_bookmark_sorter.export_markdown as em

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    monkeypatch.setattr(em, "INC_ROOT", tmp_path)

    config = load_routes_config(CONFIG)
    early = build_queue_item(
        {
            "type": "url",
            "title": "Early",
            "url": "https://example.com/early",
            "folder_path": "",
        },
        config,
    )
    early.update(
        {
            "status": "filed",
            "filed_destination": "problem_identification",
            "filed_at": "2026-01-01T00:00:00+00:00",
        }
    )
    late = build_queue_item(
        {
            "type": "url",
            "title": "Late",
            "url": "https://example.com/late",
            "folder_path": "",
        },
        config,
    )
    late.update(
        {
            "status": "filed",
            "filed_destination": "started",
            "filed_at": "2026-08-20T12:00:00+00:00",
        }
    )
    # Intentionally reverse list order vs filed_at
    save_queue({"version": 1, "items": [late, early]})

    text = export_master_document(config, {"version": 1, "items": [late, early]})[1].read_text(
        encoding="utf-8"
    )
    assert "## Problem identification" not in text
    assert "## Business started" not in text
    links = [ln for ln in text.splitlines() if ln.startswith("- ")]
    assert "early" in links[0]
    assert "late" in links[-1]
