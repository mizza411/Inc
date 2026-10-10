"""Unit tests for section 19 Phase 7.4 formulation docx opener."""

from __future__ import annotations

from pathlib import Path

from inc_launcher.formulation_docx_opener import open_pending_packs
from inc_launcher.formulation_pending import (
    PendingPack,
    list_pending_packs,
    save_shown_keys,
)


def _touch_docx(folder: Path, date_key: str) -> Path:
    path = folder / f"business_ideas_{date_key}.docx"
    path.write_bytes(b"PK\x03\x04fake")
    return path


def test_opens_all_pending_oldest_first_and_marks_shown(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261012")
    _touch_docx(out, "20261010")
    _touch_docx(out, "20261011")
    state = tmp_path / "shown.json"
    log = tmp_path / "opener.log"
    opened: list[str] = []

    def fake_open(path: Path) -> None:
        opened.append(path.name)

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=fake_open,
        log_path=log,
    )

    assert result.opened_count == 3
    assert result.failed_count == 0
    assert opened == [
        "business_ideas_20261010.docx",
        "business_ideas_20261011.docx",
        "business_ideas_20261012.docx",
    ]
    assert list_pending_packs(outputs=out, state_path=state) == []
    assert "batch_done opened=3" in log.read_text(encoding="utf-8")


def test_skips_already_shown(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261010")
    _touch_docx(out, "20261011")
    state = tmp_path / "shown.json"
    save_shown_keys(["20261010"], state)
    opened: list[str] = []

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=lambda p: opened.append(p.name),
        log_path=tmp_path / "o.log",
    )

    assert opened == ["business_ideas_20261011.docx"]
    assert result.opened_count == 1


def test_failed_open_not_marked_shown(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    path = _touch_docx(out, "20261010")
    state = tmp_path / "shown.json"

    def boom(_path: Path) -> None:
        raise OSError("Word missing")

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=boom,
        log_path=tmp_path / "o.log",
    )

    assert result.opened_count == 0
    assert result.failed_count == 1
    assert list_pending_packs(outputs=out, state_path=state) == [
        PendingPack(date_key="20261010", path=path.resolve())
    ]


def test_no_pending_is_quiet(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    state = tmp_path / "shown.json"
    log = tmp_path / "o.log"
    opened: list[Path] = []

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=lambda p: opened.append(p),
        log_path=log,
    )

    assert result.attempts == []
    assert opened == []
    assert "no_pending" in log.read_text(encoding="utf-8")


def test_continues_after_one_failure(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261010")
    _touch_docx(out, "20261011")
    state = tmp_path / "shown.json"
    opened: list[str] = []

    def selective(path: Path) -> None:
        if "20261010" in path.name:
            raise OSError("locked")
        opened.append(path.name)

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=selective,
        log_path=tmp_path / "o.log",
    )

    assert result.opened_count == 1
    assert result.failed_count == 1
    assert opened == ["business_ideas_20261011.docx"]
    pending = list_pending_packs(outputs=out, state_path=state)
    assert [p.date_key for p in pending] == ["20261010"]
