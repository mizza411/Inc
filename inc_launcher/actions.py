"""Execute launcher actions (folder, file, URL, command, Cursor)."""

from __future__ import annotations

import logging
import os
import subprocess
import webbrowser
from pathlib import Path
from typing import Any, Dict

from inc_launcher.config import INC_ROOT, resolve_path

logger = logging.getLogger(__name__)


def run_action(item: Dict[str, Any], inc_root: Path | None = None) -> None:
    """Run a single menu item action from config."""
    action = item.get("action")
    root = inc_root or INC_ROOT

    if action == "folder":
        path = resolve_path(item["path"], root)
        _open_folder(path)
    elif action == "file":
        path = resolve_path(item["path"], root)
        _open_file(path)
    elif action == "url":
        webbrowser.open(item["url"])
    elif action == "command":
        cwd = resolve_path(item.get("cwd", "."), root)
        _run_command(item["command"], cwd)
    elif action == "cursor":
        _open_in_cursor(root)
    else:
        logger.error("Unknown action type: %s", action)


def _open_folder(path: Path) -> None:
    if not path.is_dir():
        logger.warning("Folder not found: %s", path)
    os.startfile(path)  # noqa: S606 — Windows Explorer


def _open_file(path: Path) -> None:
    if not path.is_file():
        logger.warning("File not found: %s", path)
    os.startfile(path)  # noqa: S606 — default app


def _run_command(command: str, cwd: Path) -> None:
    cwd.mkdir(parents=True, exist_ok=True)
    subprocess.Popen(  # noqa: S603
        command,
        cwd=str(cwd),
        shell=True,
    )


def _open_in_cursor(inc_root: Path) -> None:
    for cmd in (
        ["cursor", str(inc_root)],
        ["code", str(inc_root)],
    ):
        try:
            subprocess.Popen(cmd, shell=False)  # noqa: S603
            return
        except OSError:
            continue
    _open_folder(inc_root)
