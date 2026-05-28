"""Import business-related entries from Chrome Bookmarks JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

def _matches_business(name: str, filter_cfg: Dict[str, Any]) -> bool:
    tokens = [t.lower() for t in filter_cfg.get("folder_name_contains", ["business"])]
    text = name.lower()
    return any(tok in text for tok in tokens)


def _walk_tree(
    node: Dict[str, Any],
    folder_path: List[str],
    filter_cfg: Dict[str, Any],
    in_business_subtree: bool,
    out: List[Dict[str, Any]],
) -> None:
    if not isinstance(node, dict):
        return

    name = (node.get("name") or "").strip()
    path_parts = folder_path + ([name] if name else [])
    path_str = " / ".join(path_parts) if path_parts else "(root)"

    node_is_business = _matches_business(name, filter_cfg) if name else False
    active = in_business_subtree or node_is_business

    ntype = node.get("type")
    if ntype == "url" and active:
        url = (node.get("url") or "").strip()
        if url and not url.startswith("chrome://"):
            out.append(
                {
                    "type": "url",
                    "title": name,
                    "url": url,
                    "folder_path": " / ".join(folder_path) if folder_path else "(root)",
                    "chrome_id": node.get("id"),
                }
            )
        return

    if ntype == "folder":
        if node_is_business and not in_business_subtree:
            # Folder entry user may need to drill into in Chrome
            out.append(
                {
                    "type": "folder",
                    "title": name,
                    "url": "",
                    "folder_path": path_str,
                    "chrome_id": node.get("id"),
                    "note": "Open this folder in Chrome to review nested bookmarks",
                }
            )
        for child in node.get("children") or []:
            if isinstance(child, dict):
                _walk_tree(child, path_parts, filter_cfg, active, out)
        return

    if ntype == "url" and filter_cfg.get("match_url_or_title"):
        url = (node.get("url") or "").strip()
        title = name.lower()
        url_l = url.lower()
        if url and any(
            tok in title or tok in url_l
            for tok in filter_cfg.get("folder_name_contains", ["business"])
        ):
            out.append(
                {
                    "type": "url",
                    "title": name,
                    "url": url,
                    "folder_path": " / ".join(folder_path) if folder_path else "(root)",
                    "chrome_id": node.get("id"),
                }
            )


def load_chrome_bookmarks(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def extract_business_entries(
    bookmarks_path: Path,
    filter_cfg: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    filter_cfg = filter_cfg or {"folder_name_contains": ["business"], "match_url_or_title": True}
    data = load_chrome_bookmarks(bookmarks_path)
    out: List[Dict[str, Any]] = []
    roots = data.get("roots") if isinstance(data, dict) else None
    if not isinstance(roots, dict):
        return out
    for key in ("bookmark_bar", "other", "synced"):
        root = roots.get(key)
        if isinstance(root, dict):
            _walk_tree(root, [key], filter_cfg, False, out)
    return dedupe_entries(out)


def dedupe_entries(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_urls: set[str] = set()
    seen_folders: set[str] = set()
    unique: List[Dict[str, Any]] = []
    for row in rows:
        if row.get("type") == "url":
            u = row.get("url") or ""
            if u in seen_urls:
                continue
            seen_urls.add(u)
        else:
            key = row.get("folder_path", "") + "|" + row.get("title", "")
            if key in seen_folders:
                continue
            seen_folders.add(key)
        unique.append(row)
    return unique


def parse_inbox_markdown(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if re.match(r"^https?://", text, re.I):
            rows.append(
                {
                    "type": "url",
                    "title": text[:80],
                    "url": text,
                    "folder_path": "business_bookmark_sorter / Business Links.md",
                    "source_hint": "inbox",
                }
            )
        else:
            rows.append(
                {
                    "type": "folder",
                    "title": text,
                    "url": "",
                    "folder_path": "business_bookmark_sorter / Business Links.md",
                    "note": "Folder label from inbox — locate in Chrome",
                    "source_hint": "inbox",
                }
            )
    return rows
