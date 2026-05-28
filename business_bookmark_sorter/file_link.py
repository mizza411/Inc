"""Append filed links to destination markdown files."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from business_bookmark_sorter.paths import INC_ROOT


def links_file_path(config: Dict[str, Any], destination_id: str) -> Path | None:
    dest = config.get("destinations", {}).get(destination_id, {})
    rel = dest.get("links_file")
    if not rel:
        return None
    return (INC_ROOT / rel).resolve()


def format_link_line(item: Dict[str, Any]) -> str:
    title = (item.get("title") or "Untitled").replace("\n", " ").strip()
    if item.get("type") == "folder" or not item.get("url"):
        return f"- **{title}** _(folder — {item.get('folder_path', '')})_"
    url = item.get("url", "").strip()
    return f"- [{title}]({url})"


def append_link(
    item: Dict[str, Any],
    config: Dict[str, Any],
    destination_id: str,
) -> Path:
    path = links_file_path(config, destination_id)
    if path is None:
        raise ValueError(f"Destination '{destination_id}' has no links_file")

    path.parent.mkdir(parents=True, exist_ok=True)
    line = format_link_line(item)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if path.is_file():
        content = path.read_text(encoding="utf-8", errors="replace")
        if url := (item.get("url") or "").strip():
            if url in content:
                return path
    else:
        content = f"# Links — {destination_id}\n\n_Auto-filed from business bookmark sorter._\n\n"

    block = f"\n## Filed {stamp}\n{line}\n"
    path.write_text(content.rstrip() + block, encoding="utf-8")
    return path
