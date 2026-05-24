"""Documentation presence tests (Phase 4.4)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DOCS = [
    ROOT / "README.md",
    ROOT / "docs" / "CLI_REFERENCE.md",
    ROOT / "docs" / "LAUNCH_CHECKLIST.md",
]


def test_user_guides_exist():
    missing = [p for p in REQUIRED_DOCS if not p.is_file()]
    assert not missing, f"Missing docs: {missing}"


def test_cli_reference_lists_main_commands():
    text = (ROOT / "docs" / "CLI_REFERENCE.md").read_text(encoding="utf-8")
    for cmd in ("create", "launch", "monitor", "go-live", "test", "dashboard", "schedule"):
        assert cmd in text
