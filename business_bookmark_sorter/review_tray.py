"""Dedicated system-tray icon for the Reviewer (BB-LINKS-UX-1 Phase 3).

Peer pattern to ``inc_launcher.tray_app`` — does **not** merge into the Inc tray.
Formulated ideas → Bookmark review still launches ``python -m … review``.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Callable

logger = logging.getLogger(__name__)

_tray_icon: Any = None
_tray_thread: threading.Thread | None = None


def default_tray_image():
    """Simple bookmark-colored icon (no asset file required)."""
    from PIL import Image, ImageDraw

    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Teal mark — distinct from Inc blue "I"
    draw.rounded_rectangle((10, 8, 54, 56), radius=6, fill=(16, 120, 120, 255))
    draw.rectangle((18, 16, 46, 22), fill=(240, 248, 248, 255))
    draw.rectangle((18, 28, 46, 34), fill=(240, 248, 248, 255))
    draw.rectangle((18, 40, 38, 46), fill=(240, 248, 248, 255))
    return img


def build_menu(
    *,
    on_open: Callable[[], None],
    on_quit: Callable[[], None],
):
    import pystray
    from pystray import MenuItem as item

    def _open(icon, _item) -> None:  # noqa: ARG001
        on_open()

    def _quit(icon, _item) -> None:  # noqa: ARG001
        on_quit()
        try:
            icon.stop()
        except Exception:
            pass

    return pystray.Menu(
        item("Open / focus review", _open, default=True),
        item("Quit", _quit),
    )


def start_review_tray(
    *,
    on_open: Callable[[], None],
    on_quit: Callable[[], None],
    title: str | None = None,
    image=None,
    config: dict | None = None,
) -> Any:
    """Start pystray in a daemon thread. Returns the Icon (or None if unavailable)."""
    global _tray_icon, _tray_thread

    if _tray_icon is not None:
        return _tray_icon

    try:
        import pystray
    except ImportError:
        logger.warning("pystray not installed — Reviewer tray skipped.")
        return None

    from business_bookmark_sorter.instance_branding import tray_tooltip

    tip = title if title is not None else tray_tooltip(config)

    icon = pystray.Icon(
        "inc_business_bookmark_reviewer",
        image if image is not None else default_tray_image(),
        tip,
        build_menu(on_open=on_open, on_quit=on_quit),
    )
    _tray_icon = icon

    def _run() -> None:
        try:
            icon.run()
        except Exception:
            logger.exception("Reviewer tray stopped with error")
        finally:
            global _tray_icon
            if _tray_icon is icon:
                _tray_icon = None

    _tray_thread = threading.Thread(target=_run, name="review-tray", daemon=True)
    _tray_thread.start()
    logger.info("Reviewer tray icon started (%s)", tip)
    return icon


def stop_review_tray() -> None:
    """Stop the tray icon if running."""
    global _tray_icon, _tray_thread
    icon = _tray_icon
    _tray_icon = None
    if icon is None:
        return
    try:
        icon.stop()
    except Exception:
        logger.exception("Failed to stop Reviewer tray")
    _tray_thread = None


def menu_labels_for_tests() -> list[str]:
    """Stable labels for pytest (no live tray)."""
    return ["Open / focus review", "Quit"]
