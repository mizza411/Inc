"""Mark filed + export markdown + open docx (Phase 2b)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from business_bookmark_sorter.actions_log import log_action
from business_bookmark_sorter.docx_export import regenerate_and_open_docx
from business_bookmark_sorter.export_markdown import export_destination
from business_bookmark_sorter.queue_store import load_queue
from business_bookmark_sorter.review_actions import (
    apply_mark_filed,
    mark_exported,
    revert_filed,
)


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
    """
    Mark item filed, export its destination markdown, optionally open docx.
    Rolls back to pending if markdown export fails.
    """
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
    try:
        count, md_path = export_destination(config, queue, destination_id)
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
        try:
            docx_path = regenerate_and_open_docx(md_path)
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
        f"Filed → {label} — section in {md_path.name} ({count} total links)"
        + (f" — opened {docx_name}" if docx_name else ""),
        md_path=md_path,
        docx_path=docx_path,
        destination_id=destination_id,
        destination_label=label,
    )
