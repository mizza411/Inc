"""Rows for the Networking window. Names come only from prospect notes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.IGNORECASE)
_PERSON_RE = re.compile(r"^\*\*(?:Person|Contact):\*\*\s*(.+)$", re.IGNORECASE)
_SKIP_NAMES = {
    "readme.md",
    "template.md",
    "manual_test.md",
    "funding_template.md",
}
_BLOCKED_PEOPLE = {"damz", "rzq"}
NO_PERSON = "No one is listed yet."


@dataclass(frozen=True)
class NetworkingRow:
    business: str
    person: str


def list_networking_rows(prospects_dir: Path) -> list[NetworkingRow]:
    """One row per active prospect note. Funding twins and templates are left out."""
    if not prospects_dir.is_dir():
        return []
    rows: list[NetworkingRow] = []
    for path in sorted(prospects_dir.glob("*.md")):
        if path.name.lower() in _SKIP_NAMES or path.name.lower().endswith("-funding.md"):
            continue
        business, person, status = _read_note(path)
        if status == "graduated":
            continue
        rows.append(NetworkingRow(business=business, person=person))
    rows.sort(key=lambda row: row.business.lower())
    return rows


def _read_note(path: Path) -> tuple[str, str, str]:
    business = path.stem.replace("-", " ")
    person = ""
    status = ""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return business, NO_PERSON, status
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and business == path.stem.replace("-", " "):
            business = stripped[2:].strip() or business
        status_match = _STATUS_RE.match(stripped)
        if status_match:
            status = status_match.group(1).strip().lower()
        person_match = _PERSON_RE.match(stripped)
        if person_match and not person:
            person = person_match.group(1).strip()
    if not person or person.casefold() in _BLOCKED_PEOPLE:
        person = NO_PERSON
    return business, person, status
