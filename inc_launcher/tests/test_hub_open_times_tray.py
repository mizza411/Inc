"""HUB-OPEN-TIMES-1 Phase 3: tray row opens the form on the Hub thread."""

from __future__ import annotations

import queue
from pathlib import Path

import tkinter as tk

from inc_launcher.config import DEFAULT_CONFIG, load_config
from inc_launcher.hub_open_times_window import HubOpenTimesWindow
from inc_launcher.hub_window import HubController
from inc_launcher.tray_app import (
    HUB_OPEN_TIMES_HOVER_LABEL,
    HUB_OPEN_TIMES_MENU_LABEL,
    build_menu,
)


def _menu_labels(menu) -> list[str]:
    return [getattr(entry, "text", "") or "" for entry in menu]


def test_tray_menu_label_and_hover_constant():
    labels = _menu_labels(build_menu(load_config()))
    assert HUB_OPEN_TIMES_MENU_LABEL in labels
    assert HUB_OPEN_TIMES_MENU_LABEL == "Settings"
    assert HUB_OPEN_TIMES_HOVER_LABEL == (
        "Open the Settings window for the Daily Hub open clock"
    )


def test_queue_uses_existing_hub_thread_and_does_not_create_tk(monkeypatch):
    created: list[str] = []

    def _forbid_tk():
        created.append("tk")
        raise AssertionError("A second Tk root was created")

    monkeypatch.setattr(tk, "Tk", _forbid_tk)
    controller = HubController()
    controller._queue = queue.Queue()
    controller._thread = type("Alive", (), {"is_alive": lambda self: True})()
    controller.show_hub_open_times({"_config_path": str(DEFAULT_CONFIG)})
    assert controller._queue.get_nowait() == "show_hub_open_times"
    assert created == []


def test_form_opens_on_the_given_root(tk_root, tmp_path: Path):
    dest = tmp_path / "launcher_config.json"
    dest.write_text(DEFAULT_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    controller = HubController()
    controller._root = tk_root
    controller._config = {"_config_path": str(dest)}
    controller._open_hub_open_times()
    children = [child for child in tk_root.winfo_children() if isinstance(child, HubOpenTimesWindow)]
    assert len(children) == 1
    children[0].withdraw()
    controller._open_hub_open_times()
    again = [child for child in tk_root.winfo_children() if isinstance(child, HubOpenTimesWindow)]
    assert again == children
    children[0].destroy()
