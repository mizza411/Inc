# Business Bookmark Sorter

Sort Chrome **business** bookmarks into Inc project areas using **`data/queue.json` as the source of truth**.

All filed links export to **one document**: `business_bookmark_sorter/Business Links.md` (and `Business Links.docx` when you file).

## Phase 0 — Discover

```powershell
cd C:\dev\Inc
python -m business_bookmark_sorter discover --dry-run
```

## Phase 1 — Import + queue

```powershell
python -m business_bookmark_sorter import
python -m business_bookmark_sorter status
python -m business_bookmark_sorter next
```

- **import** — loads Chrome business bookmarks into `data/queue.json`
- Optional legacy inbox merge: plain URLs/lines in `Business Links.md` (import only)

## Phase 2 — Review panel

```powershell
python -m business_bookmark_sorter review
```

| Button | Action |
|--------|--------|
| **Open URL** | Opens link in browser |
| **File & open doc** | Filed in queue → rebuild **Business Links.md** (all sections) → open **Business Links.docx** |
| **Skip** | Skip for now |
| **Stay in Chrome** | Keep bookmark; mark `stay_in_chrome` |
| **Refresh now** | Re-sync from current Chrome bookmarks |

**Categories (dropdown):** Business started, Formulated ideas, Idea formulation, Problem identification, My leads, Automation / content, **Other**, Stay in Chrome (separate).

**Other means:**
- System could not match keywords → suggested **Other** (not forced into a pillar)
- You chose **Other** on purpose

**Shift + File & open doc** — full re-export of all filed links into the master doc.

Workflow after success:
1. Scroll to the **section** you picked (e.g. `## My leads` or `## Other`) in the opened doc.
2. Confirm the link is there.
3. Delete the Chrome bookmark manually.

Settings in `config/routes.json`:
- `export.master_links_file`
- `export_section_order` — section order in the doc
- `review.auto_export_on_mark`, `review.open_docx_on_mark`

**Docx:** Pandoc on PATH, or Microsoft Word + `pywin32`.

CLI:

```powershell
python -m business_bookmark_sorter mark --dest leads
python -m business_bookmark_sorter mark --dest other
python -m business_bookmark_sorter export-md
```

Audit log: `data/actions.log` (local, gitignored).

## Phase 3 (planned)

Optional de-bookmark from Chrome after filing (backup + manual gate).
