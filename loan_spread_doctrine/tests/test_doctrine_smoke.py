"""Smoke: required doctrine files and headings exist (no live rates, no personal ₦)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "closed_loop_doctrine.md",
    "spread_test.md",
    "track_map.md",
    "MANUAL_TEST.md",
)

REQUIRED_HEADINGS: dict[str, tuple[str, ...]] = {
    "README.md": (
        "## How to use",
        "## Seats",
    ),
    "closed_loop_doctrine.md": (
        "## Seats",
        "## Closed loop",
        "## Open loop vs recycle",
        "## Variants",
        "## Nigeria rate buckets",
        "## Pension vs spread",
    ),
    "spread_test.md": (
        "## Spread test",
        "## Worked fixture",
        "## Do-not list",
        "## Kill conditions",
    ),
    "track_map.md": (
        "## Gadget / supplier float",
        "## Abuja leveraged buy-to-hold",
        "## Finding R > C vs FIR and Tegrid",
        "## Which variant fits which track",
    ),
    "MANUAL_TEST.md": (
        "## Owner read-through",
        "Why not automated",
    ),
}

# Fixture teaching numbers must remain in the spread test (not live quotes).
FIXTURE_MARKERS = (
    "₦1,000,000",
    "24%",
    "₦60,000",
)


def test_required_files_exist() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    assert not missing, f"missing files: {missing}"


def test_required_headings() -> None:
    failures: list[str] = []
    for name, headings in REQUIRED_HEADINGS.items():
        text = (ROOT / name).read_text(encoding="utf-8")
        for heading in headings:
            if heading not in text:
                failures.append(f"{name}: missing {heading!r}")
    assert not failures, "\n".join(failures)


def test_fixture_numbers_in_spread_test() -> None:
    text = (ROOT / "spread_test.md").read_text(encoding="utf-8")
    missing = [m for m in FIXTURE_MARKERS if m not in text]
    assert not missing, f"spread_test.md missing fixture markers: {missing}"


def test_gitignore_covers_personal_data() -> None:
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/" in gi or "data/**" in gi
    assert (ROOT / "data" / "README.md").is_file()
