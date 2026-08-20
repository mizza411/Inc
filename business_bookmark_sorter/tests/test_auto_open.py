"""BB-TIMED-1 Phase 3 — auto-open debounce + toggle."""

from __future__ import annotations

from business_bookmark_sorter.auto_open import LinkAutoOpener


def test_opens_once_when_enabled():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert opener.maybe_open(item_id="a1", url="https://example.com/a", enabled=True)
    assert opened == ["https://example.com/a"]
    assert not opener.maybe_open(item_id="a1", url="https://example.com/a", enabled=True)
    assert opened == ["https://example.com/a"]


def test_toggle_off_never_opens():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert not opener.maybe_open(item_id="b1", url="https://example.com/b", enabled=False)
    assert opened == []


def test_different_ids_open_separately():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert opener.maybe_open(item_id="1", url="https://a.test", enabled=True)
    assert opener.maybe_open(item_id="2", url="https://b.test", enabled=True)
    assert opened == ["https://a.test", "https://b.test"]


def test_blank_url_or_id_skipped():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert not opener.maybe_open(item_id="", url="https://x", enabled=True)
    assert not opener.maybe_open(item_id="x", url="", enabled=True)
    assert opened == []


def test_reset_allows_reopen():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    opener.maybe_open(item_id="z", url="https://z.test", enabled=True)
    opener.reset()
    assert opener.maybe_open(item_id="z", url="https://z.test", enabled=True)
    assert opened == ["https://z.test", "https://z.test"]
