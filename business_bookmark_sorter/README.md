# Business Bookmark Sorter

Sort Chrome **business** bookmarks into Inc project areas using **`data/queue.json` as the source of truth**.

All filed links export to **one document**: `business_bookmark_sorter/Business Links.md` (and `Business Links.docx` when you file).

**Privacy:** Import from the **local** Chrome `Bookmarks` file only — never bulk-export the full tree into chat/AI. Human checklist: [`MANUAL_TEST.md`](MANUAL_TEST.md). Task tracker: `.cursor/rules/task.md` §5.

**Main command** (opens **Business links bookmark Reviewer**):

```powershell
cd C:\dev\Inc
python -m business_bookmark_sorter review
```

Same action from the Inc tray: **Formulated ideas → Bookmark review** (launcher label unchanged).  
**Template hooks** for a future Health/Investment instance: [`TEMPLATE.md`](TEMPLATE.md).

`discover` / `discover --dry-run` is **discontinued** (2026-08-19). Do not run it.

## Phase 1 — Import + queue (only if there is no queue yet)

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
| **File & open doc** | Filed in queue → rebuild **Business Links.md** (flat list) → open **Business Links.docx** |
| **Skip** | Skip for now |
| **Stay in Chrome** | Keep bookmark; mark `stay_in_chrome` |
| **Refresh now** | Re-sync from current Chrome bookmarks |
| **Settings…** | Session length (minutes) + auto-open toggle — **change here only**, not by editing JSON |
| **Extend +5 min** | Add five minutes after the timed slot ends (or anytime) |

**Filing destination (no Assign dropdown):** uses keyword **suggestion** → else **Other**. Read-only **Filing as:** line shows the choice. Destinations in `routes.json` still drive suggestions.

**Master doc (BB-LINKS-UX-1 Phase 2):** flat chronological list by `filed_at` (newest file = last line). No category `##` headings. Set `export.flat_list: false` only if a future template instance wants sections again.

**Shift + File & open doc** — full re-export of all filed links into the master doc.

**Timed sessions (BB-TIMED-1):** **Settings…** sets session length (default 15 min) and **auto-open**. Countdown at top; at zero the UI **stops advancing**. Each new pending item can auto-open its URL once (toggle in Settings). Prefs: gitignored `data/session_settings.json`.  
**Auto-start:** project_reminder `applications.inc_business_bookmark_review` opens this UI at boot (cwd Inc). Weekdays **11:00** also via Inc tray schedule `bookmark_review_weekdays`.  
**App tray (BB-LINKS-UX-1 Phase 3):** Reviewer gets its **own** tray icon (Open / focus · Quit). Second `review` launch focuses the existing window. Does **not** replace Formulated ideas → Bookmark review.

**Workflow after success (minimal confirm):**
1. Check **Filing as:** — press **Enter** or **File & open doc**.
2. Confirm the new line is **last** in the opened doc; delete the Chrome bookmark.
3. Answer **Yes** in the dialog (optional: **Don’t ask again this session**), or use **Bookmark removed — next**.

Settings in `config/routes.json`:
- `export.master_links_file`
- `export.flat_list` / `export.sort_by` (`filed_at`)
- `export_section_order` — used only when `flat_list` is false
- `review.auto_export_on_mark`, `review.open_docx_on_mark`

**Docx:** Pandoc on PATH, or Microsoft Word + `pywin32`. If Word already has **Business Links.docx** open, File rebuilds via a temp file after politely closing that tab (**no** `taskkill` on Word).

CLI:

```powershell
python -m business_bookmark_sorter mark --dest leads
python -m business_bookmark_sorter mark --dest other
python -m business_bookmark_sorter export-md
```

Audit log: `data/actions.log` (local, gitignored).

## Phase 3 (planned)

Optional de-bookmark from Chrome after filing (backup + manual gate).
