"""Windows system tray icon with 4-pillar right-click menu."""

from __future__ import annotations

import logging
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

# Allow: python tray_app.py (from inc_launcher/) or python -m inc_launcher.tray_app (from Inc root)
_INC_ROOT = Path(__file__).resolve().parent.parent
if str(_INC_ROOT) not in sys.path:
    sys.path.insert(0, str(_INC_ROOT))

from inc_launcher.actions import run_action
from inc_launcher.config import (
    INC_ROOT,
    load_config,
    list_global_actions,
    list_pillars,
    is_formulation_catchup_enabled,
    is_interval_nudges_enabled,
    set_formulation_catchup_enabled,
    set_interval_nudges_enabled,
)
from inc_launcher.option_b_actions import uses_option_b_modal
from inc_launcher.formulation_catchup import start_formulation_catchup_background
from inc_launcher.formulation_catchup_schedule import (
    mark_post_b_day_fired,
    past_or_at_post_b,
    start_formulation_catchup_schedule,
    stop_formulation_catchup_schedule,
)
from inc_launcher.hub_window import show_hub
from inc_launcher.icon_loader import load_tray_icon
from inc_launcher.lifecycle_log import append_lifecycle
from inc_launcher.nudge_scheduler import start_nudge_scheduler, stop_nudge_scheduler
from inc_launcher.single_instance import (
    BYPASS_FLAG,
    acquire_for_start,
    bypass_requested,
    release_single_instance,
)
from inc_launcher.startup import is_login_startup_enabled, set_login_startup

logger = logging.getLogger(__name__)

# INC-TRAY-RESTART-1 — menu label + intended hover text.
# pystray MenuItem has no tooltip API on Windows, so the hover string is the
# documented action text (tests assert it, Phase 1b keeps the same wording).
RESTART_MENU_LABEL = "Restart"
RESTART_HOVER_LABEL = "Restart Inc Launcher tray"
HUB_OPEN_TIMES_MENU_LABEL = "Settings"
HUB_OPEN_TIMES_HOVER_LABEL = "Open the Settings window for the Daily Hub open clock"
# Phase 2 automated prove only. Never set in normal owner launches.
_RESTART_SMOKE_ENV = "INC_LAUNCHER_RESTART_SMOKE"

_hub_config: Dict[str, Any] | None = None
_config_path: Path | None = None
_tray_icon: Any = None


def _refresh_tray_menu() -> None:
    if _tray_icon is None:
        return
    _tray_icon.menu = build_menu(load_config(_config_path))


def _open_hub() -> None:
    if _hub_config is not None:
        show_hub(_hub_config)


def _open_hub_open_times() -> None:
    from inc_launcher.hub_window import show_hub_open_times

    show_hub_open_times(load_config(_config_path))


def _restore_network_ask() -> None:
    """Phase 1b: tray restore after Ask modal dismiss."""
    try:
        from inc_launcher.hub_window import restore_network_ask

        cfg = load_config(_config_path)
        if not restore_network_ask(cfg):
            logger.warning("Tray restore Ask: network_ask card missing from config")
    except Exception as exc:
        logger.exception("Tray restore Ask failed: %s", exc)


def _toggle_login_startup() -> None:
    try:
        set_login_startup(not is_login_startup_enabled())
        state = "enabled" if is_login_startup_enabled() else "disabled"
        logger.info("Login startup %s", state)
        _refresh_tray_menu()
    except Exception as exc:
        logger.exception("Failed to toggle login startup: %s", exc)


def _toggle_interval_nudges() -> None:
    try:
        set_interval_nudges_enabled(
            not is_interval_nudges_enabled(_config_path),
            _config_path,
        )
        state = "enabled" if is_interval_nudges_enabled(_config_path) else "disabled"
        logger.info("Interval nudges %s", state)
        _refresh_tray_menu()
    except Exception as exc:
        logger.exception("Failed to toggle interval nudges: %s", exc)



def _toggle_formulation_catchup() -> None:
    try:
        set_formulation_catchup_enabled(
            not is_formulation_catchup_enabled(_config_path),
            _config_path,
        )
        state = (
            "enabled" if is_formulation_catchup_enabled(_config_path) else "disabled"
        )
        logger.info("Formulation catch-up %s", state)
        _refresh_tray_menu()
    except Exception as exc:
        logger.exception("Failed to toggle formulation catch-up: %s", exc)


def _shutdown_for_restart(icon=None) -> None:
    """Tear down icon + schedulers + mutex before spawning a replacement."""
    append_lifecycle("Restart selected - shutting down")
    logger.info("Restart selected (%s) - shutting down", RESTART_HOVER_LABEL)
    global _tray_icon
    ic = icon if icon is not None else _tray_icon
    if ic is not None:
        try:
            ic.stop()
        except Exception:
            logger.exception("icon.stop failed during Restart")
    stop_formulation_catchup_schedule()
    stop_nudge_scheduler()
    release_single_instance()
    _tray_icon = None


def _on_quit_menu(icon=None, _item=None) -> None:
    append_lifecycle("Exit selected - shutting down")
    logger.info("Exit selected - shutting down")
    if icon is not None:
        icon.stop()


def _on_restart_menu(icon=None, _item=None) -> None:
    """Single-icon handoff: stop this tray, then start one replacement."""
    from inc_launcher.tray_process_restart import restart_tray_process

    def _exit_after_spawn(code: int) -> None:
        append_lifecycle("Restart handoff spawn ok - exiting for replacement")
        sys.exit(code)

    ok, msg = restart_tray_process(
        module="inc_launcher.tray_app",
        app_name="Inc Launcher",
        cwd=INC_ROOT,
        extra_args=(BYPASS_FLAG,),
        before_exit=lambda: _shutdown_for_restart(icon),
        exit_fn=_exit_after_spawn,
        exit_before_spawn=True,
    )
    if not ok:
        append_lifecycle(f"Restart handoff spawn failed: {msg}")
        logger.error("Tray Restart failed: %s", msg)


def _item_handler(item: Dict[str, Any]) -> Callable[[], None]:
    def _run() -> None:
        try:
            if uses_option_b_modal(item.get("action")):
                from inc_launcher.hub_window import open_hub_with_option_b

                open_hub_with_option_b(load_config(_config_path), item)
                return
            run_action(item, INC_ROOT)
        except Exception as exc:
            logger.exception("Action failed for %s: %s", item.get("label"), exc)

    return _run


def build_menu(config: Dict[str, Any]):
    import pystray
    from pystray import Menu, MenuItem as item

    entries: List[Any] = [
        item("Open Inc Hub", lambda icon, item: _open_hub(), default=True),
        item(
            "Show Ask people / owners",
            lambda icon, item: _restore_network_ask(),
        ),
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
            lambda icon, item: _toggle_login_startup(),
        )
    )
    nudges_on = is_interval_nudges_enabled(_config_path)
    entries.append(
        item(
            "Interval nudges [ON]" if nudges_on else "Interval nudges [OFF]",
            lambda icon, item: _toggle_interval_nudges(),
        )
    )
    entries.append(
        item(
            HUB_OPEN_TIMES_MENU_LABEL,
            lambda icon, item: _open_hub_open_times(),
        )
    )
    catchup_on = is_formulation_catchup_enabled(_config_path)
    entries.append(
        item(
            "Open formulation packs auto [ON]"
            if catchup_on
            else "Open formulation packs auto [OFF]",
            lambda icon, item: _toggle_formulation_catchup(),
        )
    )
    entries.append(Menu.SEPARATOR)
    entries.append(
        item(RESTART_MENU_LABEL, lambda icon, item: _on_restart_menu(icon, item))
    )
    entries.append(item("Quit", lambda icon, item: _on_quit_menu(icon, item)))

    return pystray.Menu(*entries)


def _run_menu_action(item: Dict[str, Any]) -> None:
    """Scheduled nudges: Option B actions open Hub + modal (not bare Start)."""
    if uses_option_b_modal(item.get("action")):
        from inc_launcher.hub_window import open_hub_with_option_b

        open_hub_with_option_b(load_config(_config_path), item)
        return
    run_action(item, INC_ROOT)


def run_tray(config_path: str | None = None) -> None:
    import pystray

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config_path_obj = None if config_path is None else Path(config_path)
    config = load_config(config_path_obj)
    global _hub_config, _config_path, _tray_icon
    _hub_config = config
    _config_path = config_path_obj
    handoff = bypass_requested()
    append_lifecycle(
        f"starting handoff={'yes' if handoff else 'no'} root={INC_ROOT}"
    )

    start_nudge_scheduler(
        config_path_obj,
        open_hub=show_hub,
        run_menu_action=_run_menu_action,
    )

    icon = pystray.Icon(
        "inc_launcher",
        load_tray_icon(config),
        config.get("app_name", "Inc Launcher"),
        build_menu(config),
    )
    _tray_icon = icon
    logger.info("Inc tray icon running (Inc root: %s)", INC_ROOT)
    catchup_enabled = is_formulation_catchup_enabled(config_path_obj)
    start_formulation_catchup_background(
        enabled=catchup_enabled,
        repo_root=INC_ROOT,
    )
    # If boot is already past post-B, start catch-up owns today — do not also
    # schedule-fire the same chain (avoids parallel git fetch on restart).
    if catchup_enabled and past_or_at_post_b(datetime.now()):
        mark_post_b_day_fired()
    # 7.11.1: while tray stays up, re-run catch-up at/after 11:15 local (post cloud B).
    start_formulation_catchup_schedule(
        config_path=config_path_obj,
        repo_root=INC_ROOT,
    )
    if os.environ.get(_RESTART_SMOKE_ENV) == "1":
        def _smoke_restart_soon() -> None:
            try:
                threading.Event().wait(1.5)
                logger.info("INC_LAUNCHER_RESTART_SMOKE: triggering Restart handoff")
                _on_restart_menu(_tray_icon, None)
            except Exception:
                logger.exception("INC_LAUNCHER_RESTART_SMOKE handoff failed")

        threading.Thread(
            target=_smoke_restart_soon,
            name="inc-tray-restart-smoke",
            daemon=True,
        ).start()
    try:
        icon.run()
    finally:
        append_lifecycle("shutting down")
        _tray_icon = None
        stop_formulation_catchup_schedule()
        stop_nudge_scheduler()


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    handoff = bypass_requested(args)
    config = load_config()
    settings = config.get("settings") or {}
    if settings.get("single_instance", True):
        if not acquire_for_start(bypass=handoff):
            sys.exit(0 if not handoff else 1)
    run_tray()


if __name__ == "__main__":
    main()
