# Business Bookmark Sorter

Sort Chrome **business** bookmarks into the right **Inc** folders (not into `Business Links Sort/Business Links.md` as the final home — that file is staging only).

## Phase 0 — Discover

```powershell
cd C:\dev\Inc
python -m business_bookmark_sorter discover --dry-run
```

Reads Chrome `Bookmarks` JSON (close Chrome first if the file is locked).  
Report: `business_bookmark_sorter/data/discover_report.json`

## Phase 1 — Import + queue

```powershell
python -m business_bookmark_sorter import --merge-inbox
python -m business_bookmark_sorter status
python -m business_bookmark_sorter list
python -m business_bookmark_sorter next
python -m business_bookmark_sorter next --open
```

- **import** — Chrome business tree + lines from `Business Links Sort/Business Links.md`
- **next** — next pending item with **suggested** Inc destination (`config/routes.json`)
- Filed links (Phase 2) will append to per-destination `links.md` files

## Customize routing

Edit `config/routes.json` — destinations and `keyword_rules`.

## Phase 2 — Review panel

```powershell
python -m business_bookmark_sorter review
```

Floating panel (like Batch Link Reviewer):

| Button | Action |
|--------|--------|
| **Open URL** | Opens link in browser |
| **File here** | Appends to destination `links.md`, marks **filed** |
| **Skip** | Skip for now |
| **Stay in Chrome** | Keep bookmark; mark **stay_in_chrome** |
| **Refresh now** | Re-sync from current Chrome bookmarks |

Sync behavior:
- On startup, `review` performs a Chrome sync before showing first item.
- After `File here`, `Skip`, or `Stay in Chrome`, it re-syncs automatically.
- Missing pending items become `gone_from_chrome` so stale links stop blocking the top.

CLI (no UI):

```powershell
python -m business_bookmark_sorter file --dest started
python -m business_bookmark_sorter skip
python -m business_bookmark_sorter stay
```

Audit log: `data/actions.log` (local, gitignored).

## Phase 3 (planned)

Optional de-bookmark from Chrome after filing (backup + manual gate).
