"""Networking window rows and the prospect-nudge hook. Does not start the hub."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path

from inc_launcher.config import load_config
from inc_launcher.hub_window import HubWindow
from inc_launcher.networking_rows import NO_PERSON, list_networking_rows
from inc_launcher.networking_window import (
    EMPTY,
    NetworkingWindow,
    load_networking_geometry,
    save_networking_geometry,
)


def _note(folder: Path, name: str, body: str) -> None:
    (folder / name).write_text(body, encoding="utf-8")


def test_rows_use_title_and_person_and_skip_funding(tmp_path: Path):
    _note(
        tmp_path,
        "examfee-planner.md",
        "# ExamFee Planner\n\n**Status:** prospect\n**Person:** A bursar\n",
    )
    _note(tmp_path, "examfee-planner-funding.md", "# Funding\n**Person:** Hidden\n")
    _note(tmp_path, "TEMPLATE.md", "# Template\n**Person:** Nobody\n")
    _note(tmp_path, "wedding.md", "# Wedding\n\n**Status:** prospect\n")
    _note(tmp_path, "old.md", "# Old idea\n\n**Status:** graduated\n**Person:** Gone\n")
    _note(tmp_path, "ride.md", "# Ride\n\n**Status:** prospect\n**Person:** Damz\n")

    rows = {row.business: row.person for row in list_networking_rows(tmp_path)}
    assert rows["ExamFee Planner"] == "A bursar"
    assert rows["Wedding"] == NO_PERSON
    assert rows["Ride"] == NO_PERSON
    assert "Funding" not in rows
    assert "Template" not in rows
    assert "Old idea" not in rows


def test_geometry_round_trip(tmp_path: Path):
    path = tmp_path / "launcher_config.json"
    path.write_text(json.dumps({"settings": {}}) + "\n", encoding="utf-8")
    save_networking_geometry(30, 40, 500, 360, path)
    loaded = load_networking_geometry(path)
    assert loaded == {"x": 30, "y": 40, "width": 500, "height": 360}
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert "networking_window" in raw["settings"]
    assert "password" not in path.read_text(encoding="utf-8").lower()


def _widget_is_under(widget: tk.Misc, ancestor: tk.Misc) -> bool:
    current: tk.Misc | None = widget
    while current is not None:
        if str(current) == str(ancestor):
            return True
        parent_name = current.winfo_parent()
        if not parent_name:
            return False
        current = current.nametowidget(parent_name)
    return False


def _label_texts(widget: tk.Misc) -> list[str]:
    texts: list[str] = []
    for child in widget.winfo_children():
        if isinstance(child, tk.Label):
            texts.append(str(child.cget("text")))
        texts.extend(_label_texts(child))
    return texts


def _config(tmp_path: Path) -> Path:
    path = tmp_path / "launcher_config.json"
    path.write_text(json.dumps({"settings": {}}) + "\n", encoding="utf-8")
    return path


def test_long_card_list_scrolls_and_close_stays_outside(tk_root, tmp_path: Path):
    folder = tmp_path / "prospects"
    folder.mkdir()
    for index in range(12):
        _note(
            folder,
            f"biz-{index:02d}.md",
            f"# Biz {index:02d}\n\n**Status:** prospect\n",
        )
    win = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=folder)
    try:
        tk_root.deiconify()
        win.deiconify()
        win.geometry("520x360+80+80")
        win.update_idletasks()
        win.update()
        canvas = win._card_canvas
        assert canvas is not None
        assert win._card_scrollbar is not None
        close_btn = None
        for child in _all_widgets(win):
            if isinstance(child, tk.Button) and str(child.cget("text")) == "Close":
                close_btn = child
                break
        assert close_btn is not None
        assert not _widget_is_under(close_btn, canvas)
        intro = "People to speak with about the prospective businesses just checked."
        assert intro not in _label_texts(canvas)
        bbox = canvas.bbox("all")
        assert bbox is not None
        content_height = bbox[3] - bbox[1]
        assert content_height > canvas.winfo_height()
        assert int(float(canvas.itemcget(canvas.find_all()[0], "width"))) == canvas.winfo_width()
        win.geometry("680x360")
        win.update_idletasks()
        win.update()
        assert int(float(canvas.itemcget(canvas.find_all()[0], "width"))) == canvas.winfo_width()
        canvas.yview_moveto(1.0)
        win.update_idletasks()
        top, bottom = canvas.yview()
        assert top > 0
        assert bottom == 1.0
        assert "Biz 11" in _label_texts(canvas)
        assert close_btn.winfo_ismapped()
        assert "_on_mousewheel" in win.bind("<MouseWheel>")
        assert "_on_mousewheel" not in tk_root.bind_all("<MouseWheel>")
    finally:
        win.destroy()


def test_scroll_proof_region_close_empty_and_wheel_bind(tk_root, tmp_path: Path):
    win = _open_long_list(tk_root, tmp_path)
    try:
        canvas = win._card_canvas
        assert canvas is not None
        bbox = canvas.bbox("all")
        assert bbox is not None
        assert (bbox[3] - bbox[1]) > canvas.winfo_height()
        close_btn = next(
            child
            for child in _all_widgets(win)
            if isinstance(child, tk.Button) and str(child.cget("text")) == "Close"
        )
        assert not _widget_is_under(close_btn, canvas)
        assert "_on_mousewheel" in win.bind("<MouseWheel>")
        assert "_on_mousewheel" not in tk_root.bind_all("<MouseWheel>")
    finally:
        win.destroy()

    empty = tmp_path / "empty"
    empty.mkdir()
    bare = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=empty)
    try:
        bare.update_idletasks()
        assert bare._card_canvas is None
        assert EMPTY in _label_texts(bare)
        assert not any(isinstance(widget, tk.Canvas) for widget in _all_widgets(bare))
        assert "_on_mousewheel" in bare.bind("<MouseWheel>")
        assert "_on_mousewheel" not in tk_root.bind_all("<MouseWheel>")
    finally:
        bare.destroy()


def _all_widgets(widget: tk.Misc) -> list[tk.Misc]:
    found = [widget]
    for child in widget.winfo_children():
        found.extend(_all_widgets(child))
    return found


def _open_long_list(tk_root, tmp_path: Path, count: int = 12) -> NetworkingWindow:
    folder = tmp_path / "prospects"
    folder.mkdir()
    for index in range(count):
        _note(
            folder,
            f"biz-{index:02d}.md",
            f"# Biz {index:02d}\n\n**Status:** prospect\n",
        )
    win = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=folder)
    tk_root.deiconify()
    win.deiconify()
    win.geometry("520x360+80+80")
    win.update_idletasks()
    win.update()
    return win


def test_wheel_steps_the_cards_and_leaves_header_and_close(tk_root, tmp_path: Path):
    win = _open_long_list(tk_root, tmp_path)
    try:
        canvas = win._card_canvas
        assert canvas is not None
        canvas.yview_moveto(0)
        win.update_idletasks()
        close_btn = next(
            child
            for child in _all_widgets(win)
            if isinstance(child, tk.Button) and str(child.cget("text")) == "Close"
        )
        header_y = win.winfo_rooty()
        close_y = close_btn.winfo_rooty()
        start = canvas.yview()[0]
        card_label = next(
            child
            for child in _all_widgets(canvas)
            if isinstance(child, tk.Label)
        )
        card_label.event_generate("<MouseWheel>", delta=-120)
        win.update_idletasks()
        moved_down = canvas.yview()[0]
        assert moved_down > start
        assert win.winfo_rooty() == header_y
        assert close_btn.winfo_rooty() == close_y
        close_btn.event_generate("<MouseWheel>", delta=120)
        win.update_idletasks()
        assert canvas.yview()[0] < moved_down
    finally:
        win.destroy()


def test_short_window_scrolls_and_a_tall_window_does_not(tk_root, tmp_path: Path):
    folder = tmp_path / "prospects"
    folder.mkdir()
    for index in range(2):
        _note(
            folder,
            f"biz-{index}.md",
            f"# Biz {index}\n\n**Status:** prospect\n",
        )
    win = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=folder)
    try:
        tk_root.deiconify()
        win.deiconify()
        win.geometry("520x260+40+40")
        win.update_idletasks()
        win.update()
        canvas = win._card_canvas
        bar = win._card_scrollbar
        assert canvas is not None and bar is not None
        assert win._cards_fit is False
        assert "disabled" not in bar.state()
        win.geometry("520x760+40+40")
        win.update_idletasks()
        win.update()
        assert win._cards_fit is True
        assert "disabled" in bar.state()
        parked = canvas.yview()[0]
        card_label = next(
            child
            for child in _all_widgets(canvas)
            if isinstance(child, tk.Label)
        )
        card_label.event_generate("<MouseWheel>", delta=-120)
        win.update_idletasks()
        assert canvas.yview()[0] == parked
        win.geometry("520x260+40+40")
        win.update_idletasks()
        win.update()
        assert win._cards_fit is False
        assert "disabled" not in bar.state()
        card_label.event_generate("<MouseWheel>", delta=-120)
        win.update_idletasks()
        assert canvas.yview()[0] > parked
    finally:
        win.destroy()


class _Key:
    def __init__(self, keysym: str) -> None:
        self.keysym = keysym


def test_page_keys_scroll_a_long_list_and_escape_closes(tk_root, tmp_path: Path):
    win = _open_long_list(tk_root, tmp_path)
    try:
        canvas = win._card_canvas
        assert canvas is not None
        assert "_on_page_key" in win.bind("<Next>")
        assert "_on_page_key" in win.bind("<Prior>")
        assert "lambda" in win.bind("<Escape>")
        canvas.yview_moveto(0)
        win.update_idletasks()
        close_btn = next(
            child
            for child in _all_widgets(win)
            if isinstance(child, tk.Button) and str(child.cget("text")) == "Close"
        )
        header_y = win.winfo_rooty()
        close_y = close_btn.winfo_rooty()
        win._on_page_key(_Key("Next"))
        win.update_idletasks()
        moved = canvas.yview()[0]
        assert moved > 0
        assert win.winfo_rooty() == header_y
        assert close_btn.winfo_rooty() == close_y
        win._on_page_key(_Key("Prior"))
        win.update_idletasks()
        assert canvas.yview()[0] < moved
        win.close()
        assert not win.winfo_exists()
    finally:
        if win.winfo_exists():
            win.destroy()


def test_generated_page_keys_on_a_fresh_window(tmp_path: Path):
    # This PC only delivers a generated key to the first toplevel in a process.
    folder = tmp_path / "prospects"
    folder.mkdir()
    for index in range(12):
        _note(
            folder,
            f"biz-{index:02d}.md",
            f"# Biz {index:02d}\n\n**Status:** prospect\n",
        )
    config = _config(tmp_path)
    script = tmp_path / "page_keys_once.py"
    script.write_text(
        "\n".join(
            [
                "import tkinter as tk",
                "from pathlib import Path",
                "from inc_launcher.networking_window import NetworkingWindow",
                f"folder = Path({str(folder)!r})",
                f"config = Path({str(config)!r})",
                "root = tk.Tk()",
                "root.withdraw()",
                "win = NetworkingWindow(root, config_path=config, prospects_dir=folder)",
                "root.deiconify()",
                "win.deiconify()",
                "win.geometry('520x360+40+40')",
                "win.update()",
                "canvas = win._card_canvas",
                "canvas.yview_moveto(0)",
                "win.update_idletasks()",
                "def walk(widget):",
                "    found = [widget]",
                "    for child in widget.winfo_children():",
                "        found.extend(walk(child))",
                "    return found",
                "button = next(item for item in walk(win) if isinstance(item, tk.Button))",
                "header_y = win.winfo_rooty()",
                "close_y = button.winfo_rooty()",
                "button.event_generate('<Next>')",
                "win.update_idletasks()",
                "moved = canvas.yview()[0]",
                "assert moved > 0, moved",
                "assert win.winfo_rooty() == header_y",
                "assert button.winfo_rooty() == close_y",
                "button.event_generate('<Prior>')",
                "win.update_idletasks()",
                "assert canvas.yview()[0] < moved",
                "button.event_generate('<Escape>')",
                "assert not win.winfo_exists()",
                "root.destroy()",
                "",
            ]
        ),
        encoding="utf-8",
    )
    repo = Path(__file__).resolve().parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo)
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(repo),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_page_keys_leave_a_fitted_list_still(tk_root, tmp_path: Path):
    folder = tmp_path / "prospects"
    folder.mkdir()
    _note(folder, "biz-0.md", "# Biz 0\n\n**Status:** prospect\n")
    _note(folder, "biz-1.md", "# Biz 1\n\n**Status:** prospect\n")
    win = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=folder)
    try:
        tk_root.deiconify()
        win.deiconify()
        win.geometry("520x760+40+40")
        win.update_idletasks()
        win.update()
        canvas = win._card_canvas
        assert canvas is not None
        assert win._cards_fit is True
        parked = canvas.yview()[0]
        win._on_page_key(_Key("Next"))
        win._on_page_key(_Key("Prior"))
        win.update_idletasks()
        assert canvas.yview()[0] == parked
        assert win.winfo_exists()
    finally:
        win.destroy()


def test_wheel_over_networking_does_not_replace_the_hub_wheel(tk_root, tmp_path: Path):
    hub = HubWindow(tk_root, load_config())
    win = _open_long_list(tk_root, tmp_path)
    try:
        hub_canvas = next(
            child
            for child in _all_widgets(hub)
            if isinstance(child, tk.Canvas)
        )
        net_canvas = win._card_canvas
        assert net_canvas is not None
        hub_canvas.configure(scrollregion=(0, 0, 200, 4000))
        hub_canvas.yview_moveto(0)
        net_canvas.yview_moveto(0)
        win.update_idletasks()
        hub_start = hub_canvas.yview()[0]
        net_start = net_canvas.yview()[0]
        card_label = next(
            child
            for child in _all_widgets(net_canvas)
            if isinstance(child, tk.Label)
        )
        card_label.event_generate("<MouseWheel>", delta=-120)
        win.update_idletasks()
        assert net_canvas.yview()[0] > net_start
        assert hub_canvas.yview()[0] == hub_start
        win.destroy()
        hub_canvas.event_generate("<MouseWheel>", delta=-120)
        hub.update_idletasks()
        assert hub_canvas.yview()[0] > hub_start
    finally:
        try:
            win.destroy()
        except tk.TclError:
            pass
        hub.destroy()


def test_close_button_then_hub_wheel_still_scrolls(tk_root, tmp_path: Path):
    hub = HubWindow(tk_root, load_config())
    win = _open_long_list(tk_root, tmp_path)
    try:
        hub_canvas = next(
            child
            for child in _all_widgets(hub)
            if isinstance(child, tk.Canvas)
        )
        hub_canvas.configure(scrollregion=(0, 0, 200, 4000))
        hub_canvas.yview_moveto(0)
        hub.update_idletasks()
        hub_start = hub_canvas.yview()[0]
        close_btn = next(
            child
            for child in _all_widgets(win)
            if isinstance(child, tk.Button) and str(child.cget("text")) == "Close"
        )
        close_btn.invoke()
        assert not win.winfo_exists()
        hub_canvas.event_generate("<MouseWheel>", delta=-120)
        hub.update_idletasks()
        assert hub_canvas.yview()[0] > hub_start
    finally:
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
        hub.destroy()


def test_empty_prospects_keep_the_sentence_outside_a_canvas(tk_root, tmp_path: Path):
    folder = tmp_path / "prospects"
    folder.mkdir()
    _note(folder, "examfee-planner-funding.md", "# Funding\n**Person:** Hidden\n")
    _note(folder, "old.md", "# Old idea\n\n**Status:** graduated\n**Person:** Gone\n")
    _note(folder, "TEMPLATE.md", "# Template\n**Person:** Nobody\n")
    win = NetworkingWindow(tk_root, config_path=_config(tmp_path), prospects_dir=folder)
    try:
        tk_root.deiconify()
        win.deiconify()
        win.geometry("520x420+40+40")
        win.update_idletasks()
        win.update()
        assert win._card_canvas is None
        assert win._card_scrollbar is None
        widgets = _all_widgets(win)
        assert not any(isinstance(widget, tk.Canvas) for widget in widgets)
        assert not any(widget.winfo_class() == "TScrollbar" for widget in widgets)
        texts = _label_texts(win)
        assert texts.count(EMPTY) == 1
        assert "Old idea" not in texts
        assert "Funding" not in texts
        assert "Template" not in texts
        sentence = next(
            widget
            for widget in widgets
            if isinstance(widget, tk.Label) and str(widget.cget("text")) == EMPTY
        )
        sentence.event_generate("<MouseWheel>", delta=-120)
        win._on_page_key(_Key("Next"))
        win.update_idletasks()
        assert win._card_canvas is None
        win.close()
        assert not win.winfo_exists()
    finally:
        if win.winfo_exists():
            win.destroy()


def test_prospect_nudge_opens_networking_on_close(tk_root, monkeypatch):
    calls: list[str] = []

    def _fake_show(master, item, on_started=None, on_closed=None):
        calls.append(item.get("modal_title") or "")
        assert on_closed is not None
        on_closed()

    monkeypatch.setattr("inc_launcher.hub_window.show_agent_run_modal", _fake_show)
    monkeypatch.setattr(
        "inc_launcher.hub_window.HubWindow.open_networking_window",
        lambda self: calls.append("networking"),
    )
    hub = HubWindow(tk_root, load_config())
    try:
        hub.show_prospect_folder_nudge()
        assert calls[0] == "Check your prospective businesses?"
        assert calls[1] == "networking"
    finally:
        hub.destroy()
