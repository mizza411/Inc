"""Tests for business bookmark sorter."""

from pathlib import Path

from business_bookmark_sorter.chrome_import import dedupe_entries, parse_inbox_markdown
from business_bookmark_sorter.queue_store import build_queue_item, load_routes_config
from business_bookmark_sorter.suggest import suggest_destination

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_suggest_leads_keyword():
    config = load_routes_config(CONFIG)
    entry = {"type": "url", "title": "Abuja outreach", "url": "https://example.com", "folder_path": ""}
    dest, reason = suggest_destination(entry, config)
    assert dest == "leads"
    assert "abuja" in reason.lower() or "lead" in reason.lower()


def test_parse_inbox_urls_and_folder(tmp_path):
    inbox = tmp_path / "Business Links.md"
    inbox.write_text(
        "https://example.com/inbox\n"
        "My Business folder label\n",
        encoding="utf-8",
    )
    rows = parse_inbox_markdown(inbox)
    assert any(r["type"] == "url" for r in rows)
    assert any(r["type"] == "folder" for r in rows)


def test_dedupe_urls():
    rows = dedupe_entries(
        [
            {"type": "url", "title": "a", "url": "https://x.com"},
            {"type": "url", "title": "b", "url": "https://x.com"},
        ]
    )
    assert len(rows) == 1


def test_build_queue_item():
    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "YouTube", "url": "https://youtube.com", "folder_path": ""},
        config,
    )
    assert item["status"] == "pending"
    assert item["suggested_destination"] in config["destinations"]
