"""Mark filed + append the new link (do not rebuild the Word document)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from business_bookmark_sorter.actions_log import log_action
from business_bookmark_sorter.docx_export import convert_md_to_docx, docx_path_for_md
from business_bookmark_sorter.export_markdown import master_links_path
from business_bookmark_sorter.file_link import append_to_master_md
from business_bookmark_sorter.instance_branding import master_title
from business_bookmark_sorter.queue_store import load_queue
from business_bookmark_sorter.review_actions import (
    apply_mark_filed,
    find_item,
    mark_exported,
    revert_filed,
)
from business_bookmark_sorter.word_open import append_filed_link_in_word, open_docx_for_owner


@dataclass
class FileResult:
    ok: bool
    message: str
    md_path: Optional[Path] = None
    docx_path: Optional[Path] = None
    destination_id: str = ""
    destination_label: str = ""


def review_settings(config: Dict[str, Any]) -> Dict[str, Any]:
    return config.get("review", {})


def file_item(
    item_id: str,
    destination_id: str,
    config: Dict[str, Any],
    *,
    open_docx: bool | None = None,
) -> FileResult:
    """Mark filed, append one line to the master md and to Word. Never rebuilds Word."""
    settings = review_settings(config)
    if not settings.get("auto_export_on_mark", True):
        ok, msg = apply_mark_filed(item_id, destination_id, config)
        return FileResult(ok, msg, destination_id=destination_id)

    dest = config.get("destinations", {}).get(destination_id, {})
    label = dest.get("label", destination_id)

    ok, msg = apply_mark_filed(item_id, destination_id, config)
    if not ok:
        return FileResult(False, msg, destination_id=destination_id, destination_label=label)

    queue = load_queue()
    item = find_item(queue, item_id) or {}
    md_path = master_links_path(config)
    try:
        count = append_to_master_md(
            md_path,
            item,
            heading=master_title(config),
        )
    except Exception as exc:
        revert_filed(item_id)
        log_action(
            {
                "action": "file_rollback",
                "item_id": item_id,
                "destination": destination_id,
                "reason": str(exc),
            }
        )
        return FileResult(
            False,
            f"Export failed — reverted to pending: {exc}",
            destination_id=destination_id,
            destination_label=label,
        )

    mark_exported(item_id, md_path)

    should_open = (
        open_docx
        if open_docx is not None
        else settings.get("open_docx_on_mark", True)
    )
    docx_path: Optional[Path] = None
    if should_open:
        docx_path = docx_path_for_md(md_path)
        title = str(item.get("title") or "Untitled")
        url = str(item.get("url") or "").strip()
        try:
            if not docx_path.is_file():
                convert_md_to_docx(md_path, docx_path)
                open_docx_for_owner(docx_path)
            else:
                added = append_filed_link_in_word(docx_path, title, url)
                if not added:
                    open_docx_for_owner(docx_path)
        except Exception as exc:
            log_action(
                {
                    "action": "docx_open_failed",
                    "item_id": item_id,
                    "md_path": str(md_path),
                    "error": str(exc),
                }
            )
            return FileResult(
                False,
                f"Saved to {md_path.name} ({count} links) but could not open docx: {exc}",
                md_path=md_path,
                destination_id=destination_id,
                destination_label=label,
            )

    log_action(
        {
            "action": "filed_and_exported",
            "item_id": item_id,
            "destination": destination_id,
            "md_path": str(md_path),
            "docx_path": str(docx_path) if docx_path else None,
            "link_count": count,
        }
    )
    docx_name = docx_path.name if docx_path else ""
    return FileResult(
        True,
        f"Filed → {label} — added to {md_path.name} ({count} total links)"
        + (f" — opened {docx_name}" if docx_name else ""),
        md_path=md_path,
        docx_path=docx_path,
        destination_id=destination_id,
        destination_label=label,
    )
