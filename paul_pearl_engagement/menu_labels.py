"""Tray menu captions + intended hover/action text.

Owner-facing product title (one tray): Paul Pearl/Upstream Drive.
pystray MenuItem has no tooltip API on Windows, so the hover string is the
documented action text (smoke asserts it). Visible menu uses short captions.
"""

from __future__ import annotations

# Locked PAUL-PEARL-TRAY-INC-1 Phase 1b-fix
APP_TITLE = "Paul Pearl/Upstream Drive"

OPEN_OFFER_MENU = "Open offer lines"
OPEN_OFFER_HOVER = "Open the offer lines Word document"

# PAUL-PEARL-UPSTREAM-1 Phase 0 / 1b — extra menu, does not replace offer_lines
OPEN_NOTE_MENU = "Open Paul Pearl note"
OPEN_NOTE_HOVER = "Open the Paul Pearl market / Air-gap note"

SETTINGS_MENU = "Settings…"
SETTINGS_HOVER = "Open Paul Pearl/Upstream Drive Settings"

RESTART_MENU = "Restart"
RESTART_HOVER = "Restart Paul Pearl/Upstream Drive tray"

EXIT_MENU = "Exit"
EXIT_HOVER = "Exit Paul Pearl/Upstream Drive tray"
