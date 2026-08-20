"""Export filed queue items to the single master Business Links document."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from business_bookmark_sorter.file_link import format_link_line
from business_bookmark_sorter.instance_branding import master_title
from business_bookmark_sorter.paths import INC_ROOT


def master_links_path(config: Dict[str, Any]) -> Path:
    rel = config.get("export", {}).get(
        "master_links_file",
        "business_bookmark_sorter/Business Links.md",
    )
    return (INC_ROOT / rel).resolve()


def section_id_for_export(destination_id: str | None) -> str:
    """Map legacy inbox filings into the Other section (sectioned export mode)."""
    if not destination_id or destination_id in ("inbox", "other"):
        return "other"
    return destination_id


def _export_opts(config: Dict[str, Any]) -> Dict[str, Any]:
    return config.get("export", {}) or {}


def use_flat_list(config: Dict[str, Any]) -> bool:
    """BB-LINKS-UX-1: default flat when unset (business instance)."""
    opts = _export_opts(config)
    if "flat_list" not in opts:
        return True
    return bool(opts.get("flat_list"))


def _filed_items(queue: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for item in queue.get("items", []):
        if item.get("status") != "filed":
            continue
        dest = item.get("filed_destination")
        if not dest or dest == "stay_in_chrome":
            continue
        items.append(item)
    return items


def _sort_key_filed_at(item: Dict[str, Any]) -> Tuple[str, str]:
    """Oldest first → last filed is last line. Missing filed_at sorts first."""
    return (str(item.get("filed_at") or ""), str(item.get("id") or ""))


def _filed_by_section(queue: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    by_section: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in _filed_items(queue):
        by_section[section_id_for_export(item.get("filed_destination"))].append(item)
    return by_section


def _section_order(config: Dict[str, Any], by_section: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    destinations = config.get("destinations", {})
    ordered: List[str] = []
    for dest_id in config.get("export_section_order", []):
        if dest_id in destinations or dest_id == "other":
            if dest_id not in ordered:
                ordered.append(dest_id)
    for dest_id in sorted(by_section.keys()):
        if dest_id not in ordered:
            ordered.append(dest_id)
    return ordered


def _header_lines(config: Dict[str, Any], stamp: str) -> List[str]:
    title = master_title(config)
    if use_flat_list(config):
        blurb = (
            "_One flat list (oldest → newest by filed time). "
            "Source of truth: queue.json._"
        )
    else:
        blurb = (
            "_One document — sections match review categories. "
            "Source of truth: queue.json._"
        )
    return [
        f"# {title}",
        "",
        f"_Exported from `business_bookmark_sorter/data/queue.json` on {stamp}._",
        blurb,
        "",
    ]


def _export_flat(config: Dict[str, Any], queue: Dict[str, Any], path: Path) -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    items = sorted(_filed_items(queue), key=_sort_key_filed_at)
    lines = _header_lines(config, stamp)
    for item in items:
        lines.append(format_link_line(item))
    if items:
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return len(items)


def _export_sectioned(config: Dict[str, Any], queue: Dict[str, Any], path: Path) -> int:
    by_section = _filed_by_section(queue)
    destinations = config.get("destinations", {})
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = _header_lines(config, stamp)
    total = 0
    for section_id in _section_order(config, by_section):
        items = by_section.get(section_id, [])
        if not items:
            continue
        items = sorted(items, key=_sort_key_filed_at)
        label = destinations.get(section_id, {}).get("label", section_id)
        if section_id == "other":
            label = destinations.get("other", {}).get("label", "Other")
        lines.append(f"## {label}")
        lines.append("")
        for item in items:
            lines.append(format_link_line(item))
            total += 1
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return total


def export_master_document(
    config: Dict[str, Any],
    queue: Dict[str, Any],
) -> Tuple[int, Path]:
    """
    Rebuild the single master markdown file.

    Default (``export.flat_list`` true): no category ``##`` headings; links ordered
    by ``filed_at`` ascending so the newest file is the last line.
    """
    path = master_links_path(config)
    if use_flat_list(config):
        total = _export_flat(config, queue, path)
    else:
        total = _export_sectioned(config, queue, path)
    return total, path


def export_destination(
    config: Dict[str, Any],
    queue: Dict[str, Any],
    destination_id: str,
) -> Tuple[int, Path]:
    """Rebuild master document (always one file; destination_id is for API compatibility)."""
    _ = destination_id
    return export_master_document(config, queue)


def export_filed_to_markdown(
    config: Dict[str, Any],
    queue: Dict[str, Any],
) -> Tuple[int, List[Path]]:
    """Rebuild master Business Links markdown from all filed items."""
    count, path = export_master_document(config, queue)
    return count, [path]


def export_summary_markdown(
    config: Dict[str, Any],
    queue: Dict[str, Any],
    output_path: Path | None = None,
) -> Path:
    """Legacy alias — master document is the only export."""
    _ = output_path
    _, path = export_master_document(config, queue)
    return path
