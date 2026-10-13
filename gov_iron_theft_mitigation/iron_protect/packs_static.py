"""Paths to yard engagement static packs (Council enforces)."""

from __future__ import annotations

from pathlib import Path

PACK_DIR = Path(__file__).resolve().parent.parent / "packs_static"

YARD_NOTICE = PACK_DIR / "yard_notice_template.md"
INSPECTION_CHECKLIST = PACK_DIR / "inspection_checklist.md"


def list_packs() -> list[Path]:
    return [p for p in (YARD_NOTICE, INSPECTION_CHECKLIST) if p.exists()]


def read_pack(name: str) -> str:
    mapping = {
        "yard_notice": YARD_NOTICE,
        "inspection_checklist": INSPECTION_CHECKLIST,
    }
    path = mapping.get(name)
    if path is None or not path.exists():
        raise FileNotFoundError(name)
    return path.read_text(encoding="utf-8")
