#!/usr/bin/env python3
"""One-app smoke: Paul Pearl Inc tray wiring + offer_lines.docx resolve (no PM)."""

from __future__ import annotations

import sys
from pathlib import Path

INC_ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
sys.path.insert(0, str(INC_ROOT))
sys.path.insert(0, str(PKG))


def main() -> int:
    launcher = INC_ROOT / "paul_pearl_engagement_tray_launcher.py"
    if not launcher.is_file():
        print(f"FAIL: missing {launcher}")
        return 1
    print("  OK  tray launcher stub")

    from lifecycle_log import lifecycle_log_path
    from paths import PACKAGE_DIR, resolve_offer_lines_docx, resolve_paul_pearl_note

    if PACKAGE_DIR.resolve() != PKG.resolve():
        print(f"FAIL: PACKAGE_DIR {PACKAGE_DIR} != {PKG}")
        return 1
    print("  OK  PACKAGE_DIR under Inc")

    log_path = lifecycle_log_path()
    if log_path.parent.resolve() != PKG.resolve():
        print(f"FAIL: log not under package: {log_path}")
        return 1
    if not log_path.is_absolute():
        print(f"FAIL: log path must be absolute: {log_path}")
        return 1
    print(f"  OK  lifecycle log -> {log_path}")

    docx = resolve_offer_lines_docx()
    if docx is None or not docx.is_file():
        print("FAIL: offer_lines.docx not found")
        return 1
    print(f"  OK  docx -> {docx}")

    note = resolve_paul_pearl_note()
    if note is None or not note.is_file():
        print("FAIL: Paul Pearl note not found")
        return 1
    print(f"  OK  note -> {note}")

    # Import tray modules without starting pystray mainloop
    import open_offer_lines  # noqa: F401
    import open_paul_pearl_note  # noqa: F401
    import schedule  # noqa: F401
    import schedule_poll  # noqa: F401
    import single_instance  # noqa: F401
    import settings_ui  # noqa: F401
    import ui_geometry  # noqa: F401
    from menu_labels import (
        APP_TITLE,
        EXIT_HOVER,
        OPEN_NOTE_HOVER,
        OPEN_NOTE_MENU,
        OPEN_OFFER_HOVER,
        RESTART_HOVER,
        SETTINGS_HOVER,
        SETTINGS_MENU,
    )

    print("  OK  package imports")

    if APP_TITLE != "Paul Pearl/Upstream Drive":
        print(f"FAIL: APP_TITLE must be Paul Pearl/Upstream Drive, got {APP_TITLE!r}")
        return 1
    print(f"  OK  APP_TITLE -> {APP_TITLE}")

    if OPEN_NOTE_MENU != "Open Paul Pearl note":
        print(f"FAIL: note menu caption unexpected: {OPEN_NOTE_MENU!r}")
        return 1
    if OPEN_NOTE_HOVER != "Open the Paul Pearl market / Air-gap note":
        print(f"FAIL: note hover unexpected: {OPEN_NOTE_HOVER!r}")
        return 1

    for label in (OPEN_OFFER_HOVER, SETTINGS_HOVER, RESTART_HOVER, EXIT_HOVER):
        if not label or len(label) < 8:
            print(f"FAIL: hover/action text too short: {label!r}")
            return 1
        if "Paul Pearl/Upstream Drive" not in label and label != OPEN_OFFER_HOVER:
            print(f"FAIL: hover should name product: {label!r}")
            return 1
    if SETTINGS_MENU != "Settings…":
        print(f"FAIL: Settings menu caption unexpected: {SETTINGS_MENU!r}")
        return 1
    tray_src = (PKG / "tray_host.py").read_text(encoding="utf-8")
    if "SETTINGS_MENU" not in tray_src or "open_settings" not in tray_src:
        print("FAIL: Settings not wired in tray_host")
        return 1
    if "OPEN_NOTE_MENU" not in tray_src or "open_paul_pearl_note" not in tray_src:
        print("FAIL: Paul Pearl note menu not wired in tray_host")
        return 1
    if "OPEN_OFFER_HOVER" not in tray_src:
        print("FAIL: hover constants not referenced in tray_host")
        return 1
    if 'APP_TITLE = "Paul Pearl"' in tray_src:
        print("FAIL: tray_host still hardcodes old Paul Pearl-only title")
        return 1
    print("  OK  Settings stub + note menu + hover action strings")

    pkg_src = "\n".join(
        p.read_text(encoding="utf-8")
        for p in PKG.glob("*.py")
        if p.name != "test_paul_pearl_engagement_smoke.py"
    )
    for banned in (
        "lean_roles.docx",
        "company_requirements.docx",
        "risk_management_requirements.docx",
        "README.docx",
    ):
        if banned in pkg_src:
            print(f"FAIL: package must not open {banned}")
            return 1
    # Startup/schedule must stay offer_lines; note is menu-only
    poll_src = (PKG / "schedule_poll.py").read_text(encoding="utf-8")
    if "paul_pearl_market_airgap" in poll_src or "open_paul_pearl_note" in poll_src:
        print("FAIL: schedule poll must not open the Paul Pearl note")
        return 1
    print("  OK  schedule stays on offer_lines; note is extra menu only")

    if "project_reminder" in str(PACKAGE_DIR).replace("\\", "/").lower():
        print("FAIL: package must live under Inc, not project_reminder")
        return 1
    print("  OK  Inc home (not project_reminder)")

    print("PASS paul_pearl_engagement Phase UPSTREAM-1 1b smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
