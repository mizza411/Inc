"""Load tray icon from config or built-in default (Phase 3)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from inc_launcher.config import PACKAGE_DIR, resolve_path


def load_tray_icon(config: Dict[str, Any]):
    from PIL import Image

    settings = config.get("settings") or {}
    icon_path = settings.get("icon_path")
    if icon_path:
        path = Path(icon_path)
        if not path.is_absolute():
            path = resolve_path(str(icon_path).replace("/", "\\").lstrip("\\"))
        if path.is_file():
            img = Image.open(path).convert("RGBA")
            return img.resize((64, 64), Image.Resampling.LANCZOS)

    bundled = PACKAGE_DIR / "assets" / "icon.png"
    if bundled.is_file():
        img = Image.open(bundled).convert("RGBA")
        return img.resize((64, 64), Image.Resampling.LANCZOS)

    return _default_icon()


def _default_icon():
    from PIL import Image, ImageDraw

    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, size - 4, size - 4), fill=(34, 139, 230, 255))
    draw.text((18, 20), "I", fill=(255, 255, 255, 255))
    return img
