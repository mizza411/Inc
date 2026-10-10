"""Unit tests for section 19 Phase 7.3 pending detector + shown ledger."""

from __future__ import annotations

from pathlib import Path

from inc_launcher.formulation_pending import (
    list_pack_docx,
    list_pending_packs,
    load_shown_keys,
    mark_shown,
    parse_date_key,
    pending_count,
    save_shown_keys,
)


def _touch_docx(folder: Path, date_key: str) -> Path:
    path = folder / f"business_ideas_{date_key}.docx"
    path.write_bytes(b"PK\x03\x04fake")
    return path


def test_parse_date_key():
    assert parse_date_key(Path("business_ideas_20261010.docx")) == "20261010"
    assert parse_date_key(Path("notes.docx")) is None
    assert parse_date_key(Path("business_ideas_20261010.md")) is None


def test_list_pack_docx_oldest_first(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261012")
    _touch_docx(out, "20261010")
    _touch_docx(out, "20261011")
    (out / "readme.txt").write_text("x", encoding="utf-8")
    (out / "business_ideas_20261010.md").write_text("md", encoding="utf-8")

    packs = list_pack_docx(out)

    assert [p.date_key for p in packs] == ["20261010", "20261011", "20261012"]


def test_pending_excludes_shown_any_count(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261008")
    _touch_docx(out, "20261009")
    _touch_docx(out, "20261010")
    state = tmp_path / "shown.json"
    save_shown_keys(["20261008"], state)

    pending = list_pending_packs(outputs=out, state_path=state)

    assert [p.date_key for p in pending] == ["20261009", "20261010"]
    assert pending_count(outputs=out, state_path=state) == 2


def test_empty_ledger_all_pending(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261001")
    _touch_docx(out, "20261005")
    state = tmp_path / "shown.json"

    pending = list_pending_packs(outputs=out, state_path=state)

    assert len(pending) == 2
    assert load_shown_keys(state) == set()


def test_mark_shown_removes_from_pending(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261010")
    state = tmp_path / "shown.json"

    assert pending_count(outputs=out, state_path=state) == 1
    mark_shown("20261010", state)
    assert pending_count(outputs=out, state_path=state) == 0
    assert "20261010" in load_shown_keys(state)


def test_missing_outputs_dir(tmp_path: Path):
    missing = tmp_path / "nope"
    state = tmp_path / "shown.json"
    assert list_pending_packs(outputs=missing, state_path=state) == []


def test_corrupt_shown_state_treated_as_empty(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261010")
    state = tmp_path / "shown.json"
    state.write_text("{not json", encoding="utf-8")

    pending = list_pending_packs(outputs=out, state_path=state)

    assert len(pending) == 1
