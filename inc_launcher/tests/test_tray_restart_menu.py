"""INC-TRAY-RESTART-1 Phase 1a: Restart menu row above Quit."""

from __future__ import annotations

from inc_launcher.config import load_config
from inc_launcher.tray_app import (
    RESTART_HOVER_LABEL,
    RESTART_MENU_LABEL,
    build_menu,
)


def _menu_labels(menu) -> list[str]:
    return [getattr(entry, "text", "") or "" for entry in menu]


def test_restart_menu_label_above_quit():
    labels = _menu_labels(build_menu(load_config()))
    assert RESTART_MENU_LABEL in labels
    assert "Quit" in labels
    assert labels.index(RESTART_MENU_LABEL) < labels.index("Quit")


def test_restart_hover_label_constant():
    assert RESTART_HOVER_LABEL == "Restart Inc Launcher tray"
