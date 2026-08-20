"""CLI for business bookmark sorting — import/queue plus review UI."""

from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from business_bookmark_sorter.chrome_import import (
    extract_business_entries,
    parse_inbox_markdown,
)
from business_bookmark_sorter.paths import (
    CONFIG_PATH,
    INBOX_MD,
    QUEUE_PATH,
    default_chrome_bookmarks_path,
)
from business_bookmark_sorter.queue_store import (
    count_by_status,
    load_queue,
    load_routes_config,
    merge_import,
    next_pending,
)
from business_bookmark_sorter.export_markdown import export_filed_to_markdown
from business_bookmark_sorter.file_workflow import file_item
from business_bookmark_sorter.review_actions import apply_mark_filed, apply_skip, apply_stay_in_chrome
from business_bookmark_sorter.review_ui import run_review_panel


def cmd_import(args: argparse.Namespace) -> int:
    bookmarks = Path(args.bookmarks)
    config = load_routes_config(CONFIG_PATH)
    entries: list = []

    if not args.inbox_only:
        if not bookmarks.is_file():
            print(f"Bookmarks file not found: {bookmarks}")
            return 1
        entries.extend(extract_business_entries(bookmarks, config.get("chrome_filter")))

    if args.inbox_only or not args.no_merge_inbox:
        entries.extend(parse_inbox_markdown(INBOX_MD))

    if not entries:
        print("Nothing to import.")
        return 1

    queue = merge_import(entries, config, source="chrome", replace=args.replace)
    print(f"Imported {queue.get('_added', 0)} new item(s). Queue: {QUEUE_PATH}")
    print(f"Status: {count_by_status(queue)}")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    if not QUEUE_PATH.is_file():
        print("No queue yet. Run: python -m business_bookmark_sorter.cli import")
        return 1
    queue = load_queue()
    counts = count_by_status(queue)
    print(f"Queue: {QUEUE_PATH}")
    print(f"Total: {len(queue.get('items', []))}")
    print(f"By status: {counts}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    queue = load_queue()
    items = queue.get("items", [])
    if args.status:
        items = [i for i in items if i.get("status") == args.status]
    for i in items[: args.limit]:
        print(
            f"{i.get('id', '')[:8]}  [{i.get('status')}]  "
            f"{i.get('suggested_destination')}: {i.get('title', '')[:50]}"
        )
        if i.get("url"):
            print(f"         {i.get('url')[:70]}")
    if len(items) > args.limit:
        print(f"... {len(items) - args.limit} more (use --limit)")
    return 0


def cmd_review(_args: argparse.Namespace) -> int:
    if not QUEUE_PATH.is_file():
        print("No queue. Run: python -m business_bookmark_sorter import")
        return 1
    run_review_panel()
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    config = load_routes_config(CONFIG_PATH)
    queue = load_queue()
    item = next_pending(queue) if not args.id else None
    if args.id:
        from business_bookmark_sorter.review_actions import find_item

        item = find_item(queue, args.id)
    if not item:
        print("No matching item.")
        return 1
    dest = args.dest or item.get("suggested_destination")
    if args.queue_only:
        ok, msg = apply_mark_filed(item["id"], dest, config)
        print(msg)
        return 0 if ok else 1
    result = file_item(item["id"], dest, config, open_docx=not args.no_docx)
    print(result.message)
    if result.md_path:
        print(f"  Markdown: {result.md_path}")
    if result.docx_path:
        print(f"  Docx: {result.docx_path}")
    return 0 if result.ok else 1


def cmd_file(args: argparse.Namespace) -> int:
    return cmd_mark(args)


def cmd_export_md(_args: argparse.Namespace) -> int:
    config = load_routes_config(CONFIG_PATH)
    queue = load_queue()
    count, paths = export_filed_to_markdown(config, queue)
    print(f"Exported {count} filed link(s) to master document:")
    for p in paths:
        print(f"  - {p}")
    return 0


def cmd_skip(args: argparse.Namespace) -> int:
    queue = load_queue()
    item = next_pending(queue) if not args.id else None
    if args.id:
        from business_bookmark_sorter.review_actions import find_item

        item = find_item(queue, args.id)
    if not item:
        print("No matching item.")
        return 1
    ok, msg = apply_skip(item["id"])
    print(msg)
    return 0 if ok else 1


def cmd_stay(args: argparse.Namespace) -> int:
    queue = load_queue()
    item = next_pending(queue) if not args.id else None
    if args.id:
        from business_bookmark_sorter.review_actions import find_item

        item = find_item(queue, args.id)
    if not item:
        print("No matching item.")
        return 1
    ok, msg = apply_stay_in_chrome(item["id"])
    print(msg)
    return 0 if ok else 1


def cmd_next(args: argparse.Namespace) -> int:
    queue = load_queue()
    item = next_pending(queue)
    if not item:
        print("No pending items.")
        return 0
    config = load_routes_config(CONFIG_PATH)
    dest = config.get("destinations", {}).get(item.get("suggested_destination"), {})
    print(f"ID:       {item.get('id')}")
    print(f"Type:     {item.get('type')}")
    print(f"Title:    {item.get('title')}")
    if item.get("url"):
        print(f"URL:      {item.get('url')}")
    print(f"Folder:   {item.get('folder_path')}")
    print(f"Suggest:  {item.get('suggested_destination')} — {item.get('suggested_reason')}")
    master = config.get("export", {}).get("master_links_file", "business_bookmark_sorter/Business Links.md")
    print(f"Section:  {dest.get('label')} → {master}")
    if item.get("note"):
        print(f"Note:     {item.get('note')}")
    if args.open and item.get("url"):
        webbrowser.open(item["url"])
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Business bookmark sorter (Inc)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_imp = sub.add_parser("import", help="Phase 1: build queue.json")
    p_imp.add_argument("--bookmarks", default=str(default_chrome_bookmarks_path()))
    p_imp.add_argument("--no-merge-inbox", action="store_true", help="Skip Business Links.md inbox")
    p_imp.add_argument("--inbox-only", action="store_true")
    p_imp.add_argument("--replace", action="store_true", help="Replace queue instead of merge")
    p_imp.set_defaults(func=cmd_import)

    p_st = sub.add_parser("status", help="Queue counts")
    p_st.set_defaults(func=cmd_status)

    p_li = sub.add_parser("list", help="List queue items")
    p_li.add_argument("--status", default="")
    p_li.add_argument("--limit", type=int, default=30)
    p_li.set_defaults(func=cmd_list)

    p_nx = sub.add_parser("next", help="Show next pending item")
    p_nx.add_argument("--open", action="store_true", help="Open URL in browser")
    p_nx.set_defaults(func=cmd_next)

    p_rev = sub.add_parser("review", help="Phase 2: floating review panel")
    p_rev.set_defaults(func=cmd_review)

    p_mark = sub.add_parser("mark", help="File item: queue + export md + open docx (default)")
    p_mark.add_argument("--dest", required=True, help="Destination id from routes.json")
    p_mark.add_argument("--id", default="", help="Queue item UUID (default: next pending)")
    p_mark.add_argument("--queue-only", action="store_true", help="Update queue.json only (no export)")
    p_mark.add_argument("--no-docx", action="store_true", help="Export markdown but do not open docx")
    p_mark.set_defaults(func=cmd_mark)

    p_file = sub.add_parser("file", help="Alias for mark")
    p_file.add_argument("--dest", required=True, help="Destination id from routes.json")
    p_file.add_argument("--id", default="", help="Queue item UUID (default: next pending)")
    p_file.add_argument("--queue-only", action="store_true", help="Update queue.json only (no export)")
    p_file.add_argument("--no-docx", action="store_true", help="Export markdown but do not open docx")
    p_file.set_defaults(func=cmd_file)

    p_exp = sub.add_parser("export-md", help="Export filed queue items to markdown files")
    p_exp.set_defaults(func=cmd_export_md)

    p_skip = sub.add_parser("skip", help="Skip current/next item")
    p_skip.add_argument("--id", default="")
    p_skip.set_defaults(func=cmd_skip)

    p_stay = sub.add_parser("stay", help="Mark stay in Chrome")
    p_stay.add_argument("--id", default="")
    p_stay.set_defaults(func=cmd_stay)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
