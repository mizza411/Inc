"""Windows system tray icon with 4-pillar right-click menu."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

# Allow: python tray_app.py (from inc_launcher/) or python -m inc_launcher.tray_app (from Inc root)
_INC_ROOT = Path(__file__).resolve().parent.parent
if str(_INC_ROOT) not in sys.path:
    sys.path.insert(0, str(_INC_ROOT))

from inc_launcher.actions import run_action
from inc_launcher.config import INC_ROOT, load_config, list_global_actions, list_pillars
from inc_launcher.hub_window import show_hub
from inc_launcher.icon_loader import load_tray_icon
from inc_launcher.single_instance import ensure_single_instance
from inc_launcher.startup import is_login_startup_enabled, set_login_startup

logger = logging.getLogger(__name__)

_hub_config: Dict[str, Any] | None = None


def _open_hub() -> None:
    if _hub_config is not None:
        show_hub(_hub_config)


def _toggle_login_startup() -> None:
    try:
        set_login_startup(not is_login_startup_enabled())
        state = "enabled" if is_login_startup_enabled() else "disabled"
        logger.info("Login startup %s", state)
    except Exception as exc:
        logger.exception("Failed to toggle login startup: %s", exc)


def _item_handler(item: Dict[str, Any]) -> Callable[[], None]:
    def _run() -> None:
        try:
            run_action(item, INC_ROOT)
        except Exception as exc:
            logger.exception("Action failed for %s: %s", item.get("label"), exc)

    return _run


def build_menu(config: Dict[str, Any]):
    import pystray
    from pystray import Menu, MenuItem as item

    entries: List[Any] = [
        item("Open Inc Hub", lambda icon, item: _open_hub(), default=True),
        Menu.SEPARATOR,
    ]

    for pillar in list_pillars(config):
        sub_items = [
            item(sub["label"], _item_handler(sub))
            for sub in pillar.get("items", [])
        ]
        entries.append(item(pillar["label"], pystray.Menu(*sub_items)))

    entries.append(Menu.SEPARATOR)

    for global_item in list_global_actions(config):
        entries.append(item(global_item["label"], _item_handler(global_item)))

    entries.append(Menu.SEPARATOR)
    login_on = is_login_startup_enabled()
    entries.append(
        item(
            "Start at Windows login [ON]" if login_on else "Start at Windows login [OFF]",
            _toggle_login_startup,
        )
    )
    entries.append(Menu.SEPARATOR)
    entries.append(item("Quit", lambda icon, item: icon.stop()))

    return pystray.Menu(*entries)


def run_tray(config_path: str | None = None) -> None:
    import pystray

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config = load_config(None if config_path is None else __import__("pathlib").Path(config_path))
    global _hub_config
    _hub_config = config

    icon = pystray.Icon(
        "inc_launcher",
        load_tray_icon(config),
        config.get("app_name", "Inc Launcher"),
        build_menu(config),
    )
    logger.info("Inc tray icon running (Inc root: %s)", INC_ROOT)
    icon.run()


def main() -> None:
    config = load_config()
    settings = config.get("settings") or {}
    if settings.get("single_instance", True) and not ensure_single_instance():
        sys.exit(0)
    run_tray()


if __name__ == "__main__":
    main()
