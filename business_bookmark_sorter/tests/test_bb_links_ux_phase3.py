"""BB-LINKS-UX-1 Phase 3 — Reviewer tray + single-instance focus."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from business_bookmark_sorter import review_single_instance as rsi
from business_bookmark_sorter.review_tray import (
    build_menu,
    default_tray_image,
    menu_labels_for_tests,
)


def test_tray_menu_labels():
    assert menu_labels_for_tests() == ["Open / focus review", "Quit"]


def test_default_tray_image_size():
    img = default_tray_image()
    assert img.size == (64, 64)
    assert img.mode == "RGBA"


def test_build_menu_wires_open_and_quit():
    opened: list[int] = []
    quit_n: list[int] = []

    menu = build_menu(
        on_open=lambda: opened.append(1),
        on_quit=lambda: quit_n.append(1),
    )
    # pystray Menu is iterable of MenuItem
    items = list(menu)
    assert len(items) == 2
    assert items[0].text == "Open / focus review"
    assert items[1].text == "Quit"

    icon = MagicMock()
    items[0](icon)
    assert opened == [1]

    items[1](icon)
    assert quit_n == [1]
    icon.stop.assert_called_once()


def test_focus_request_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(rsi, "DATA_DIR", tmp_path)
    monkeypatch.setattr(rsi, "FOCUS_REQUEST_PATH", tmp_path / "review_focus_request.flag")
    assert rsi.consume_focus_request() is False
    path = rsi.request_focus_existing()
    assert path.is_file()
    assert rsi.consume_focus_request() is True
    assert rsi.consume_focus_request() is False


def test_run_review_panel_second_launch_requests_focus():
    from business_bookmark_sorter import review_ui as ru

    called: list[str] = []

    def fake_request():
        called.append("focus")
        return Path("x")

    with patch(
        "business_bookmark_sorter.review_single_instance.ensure_single_instance",
        return_value=False,
    ), patch(
        "business_bookmark_sorter.review_single_instance.request_focus_existing",
        side_effect=fake_request,
    ), patch(
        "business_bookmark_sorter.review_ui.ReviewPanel"
    ) as Panel:
        ru.run_review_panel()
        Panel.assert_not_called()
    assert called == ["focus"]


def test_inc_launcher_still_has_bookmark_review():
    cfg = Path(__file__).resolve().parents[2] / "inc_launcher" / "launcher_config.json"
    data = json.loads(cfg.read_text(encoding="utf-8"))
    found = False
    for pillar in data.get("pillars", []):
        for item in pillar.get("items", []):
            if item.get("id") == "bookmark_review":
                found = True
                assert "business_bookmark_sorter review" in item.get("command", "")
    assert found
