# BB-LINKS-UX-1 — Reviewer UX: no Assign picker, flat master doc, app tray, template rename

**Status:** 🟢 **Phases 0–4 ✅** (2026-08-20) · optional Phase 5 open · **delete this satellite after owner MANUAL (§Q + one File→last line) + fold into §5**  
**Attempt (Phase 4):** 1 (passed)
  
**Authoritative backlog:** **this file** (main `.cursor/rules/task.md` §5 = thin pointer only)  
**Delete when:** Phases **0–4** (and optional **5** if chosen) **complete + automated tests green + owner one MANUAL pass** — then fold 5–10 lines into §5 and **delete this satellite**.  
**Parent:** §5 Business Bookmark Sorting · `business_bookmark_sorter/`  
**Related shipped:** BB-TIMED-1 Phases 0–7 ✅ · Word STA close fix ✅  

---

## A — Owner-requested features (must ship)

1. Remove **Assign to:** dropdown + label from Reviewer; File still works with a default destination; Enter / File / remove-bookmark flow intact.
2. Stop writing / showing category subsection headings in Business Links (e.g. “Problem identification”); identify from live md/docx + exporter; regen cleans noise; **last filed link = last entry**.
3. Dedicated **tray icon** for this app (peer behavior to today’s trays): open/focus + quit; do **not** break Formulated ideas → Bookmark review.
4. Treat business flow as **template instance #1**; UI name **Business links Bookmark Reviewer** (casing polish = **BB-BRAND-1**); top banner + `TEMPLATE.md` = **guide for building other apps** (Health / Investment) — see [task_bb_links_branding_polish.md](task_bb_links_branding_polish.md).

---

## B — Agent recommendations (in backlog; implement with phases unless marked optional)

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| **R1** | Default dest = `suggested_destination` → else `other` (not hard-force `started`) | Matches keyword engine; Skip/Stay still available | **0.1** lock → **1.2** |
| **R2** | Keep a **read-only** “Filing as: {label}” line (not a dropdown) | Trust without re-adding Assign clicks | **1.5** |
| **R3** | Toast after File still shows destination label | Confirm where it went | **1.3** |
| **R4** | Config flags `export.flat_list` + `export.sort_by: filed_at` (default on for business instance) | Template-ready; no hard-code only in Python | **2.0** / **4.1** |
| **R5** | New modules only: `review_tray.py`, thin `instance_branding.py` (title/banner/tray tip from config); **thin hooks** in `review_ui.py` / `__main__` | Avoid mega-file + breaking Inc tray | **3** / **4** |
| **R6** | Single-instance guard for Reviewer+tray (second launch = focus) | Prevent duplicate windows/tray icons | **3.3** |
| **R7** | After flat-export change: agent runs one full `export-md` + docx regen (automated) | Clean existing subsection noise without owner Word clicks | **2.3** |
| **R8** | Automate-first tests + append MANUAL_TEST only for live tray/feel | Deferred-manual rule | **0.2** / each phase |
| **R9** | *(Optional)* Settings: “Default destination override” if suggestion often wrong | Escape hatch without Assign dropdown | **5** optional |
| **R10** | *(Optional)* Keep `filed_destination` in queue for future filters/stats; never drop field | Analytics / later re-section tools | **2** (already assumed) |
| **R11** | Do **not** edit Inc `tray_app.py` menu structure beyond label string if needed; sorter owns its icon | Isolation | **3** |
| **R12** | Portfolio hygiene later: review other apps’ tray/UX — not a blocker for this track | Cross-project standing note | out of critical path |

---

## One-liner

Faster filing (no Assign) + flat chronological Business Links + own tray + template branding — **modular** add-ons inside Inc sorter; Inc Formulated menu and PR boot stay.

---

## Layout + modularization (avoid breaking ANYTHING ANYWHERE)

**Decision:** Stay in **`business_bookmark_sorter/`**. No move to `project_reminder`. No new top-level product folder.

| Path | Role | Touch rules |
|------|------|-------------|
| `review_ui.py` | Thin UI hooks only | Remove Assign row; add banner/read-only filing line; start tray |
| `export_markdown.py` | Flat list + `filed_at` order | Do not change queue schema except use existing fields |
| `docx_export.py` | Regen only | Keep STA-safe close; no behavior change beyond input md |
| **NEW** `review_tray.py` | pystray Open/Quit | Do not merge into `inc_launcher/tray_app.py` |
| **NEW** `instance_branding.py` (or keys in `routes.json` → `product`) | Title, banner, tray tip | Config-driven for template |
| `config/routes.json` | destinations + export flags + product strings | Additive keys; don’t remove destinations (still used by suggest) |
| `inc_launcher/launcher_config.json` | `bookmark_review` menu/schedule | Label tweak OK; **do not** remove target / schedule |
| `project_reminder/launcher_config.json` | boot key | Leave alone unless path/title string only |
| PR `bookmark_sorter.py` | **Never touch** | Different product |

**Hard isolation checklist:**

- [ ] Never move/delete sorter into PR
- [ ] Never fuse/replace PR `bookmark_sorter.py`
- [ ] Never kill WINWORD via taskkill
- [ ] Never zero-confirm auto-file
- [ ] Never open all pending URLs at once
- [ ] Never break `bookmark_review` / `bookmark_review_weekdays` / PR boot key
- [ ] Prefer new modules &lt; ~500 lines; no god-file growth in `review_ui.py`
- [ ] Package folder name `business_bookmark_sorter` stays (rename = separate owner task)

---

## ETA (agent — this track only)

**Updated total (Phases 0–4 required):** **~250 minutes** (~4.2 h)  
**With optional Phase 5:** **~290 minutes** (~4.8 h)

| Phase | Focus | Source | Est. (min) |
|-------|--------|--------|------------|
| **0** | Locks, layout, MANUAL_TEST stubs, confirm R1 | Owner + agent | 15 |
| **1** | No Assign + default dest + read-only “Filing as” (R2) | Owner A1 + R1–R3 | 45 |
| **2** | Flat master + last-filed-last + regen (R4, R7, R10) | Owner A2 | 60 |
| **3** | App tray + single-instance (R5, R6, R11) | Owner A3 | 80 |
| **4** | Rename + banner + hooks doc + branding module (R5, R8) | Owner A4 | 50 |
| **5** | *(Optional)* Settings default-dest override (R9) | Agent rec | 40 |
| | **Required sum (0–4)** | | **250** |
| | **+ optional 5** | | **290** |

**Calendar (owner pace):**

| Cadence | Required (0–4 = **5** phase units) | + optional 5 |
|---------|-------------------------------------|--------------|
| **1–2 phases/day** | **3–5 days** | **3–6 days** |
| Leaf items (~20) @ 1–2/day | **10–20 days** (don’t use this; prefer phase cadence) | — |

---

## Detailed ASCII (architecture)

```
OWNER / INC TRAY (unchanged)
  Formulated ideas → Bookmark review ──► python -m business_bookmark_sorter review
  weekday 11:00 schedule ──────────────► same target
  PR boot key ─────────────────────────► same cwd/command

SORTER PROCESS (this app)
  ┌─ review_tray.py (NEW) ─────────────────┐
  │  [icon] Open/Focus │ Quit              │
  └──────────┬─────────────────────────────┘
             │ focus / quit
  ┌──────────▼─────────────────────────────┐
  │ Business links Bookmark Reviewer       │
  │ banner: shell also for Health / …      │
  │ timer | Settings…                      │
  │ current item                           │
  │ Filing as: {suggest}   ← read-only R2  │
  │ (NO Assign dropdown)                   │
  │ [File] [Skip] [Stay] [Quit]            │
  └──────────┬─────────────────────────────┘
             │ Enter / File
             ▼
        queue.json  (filed_destination kept)
             │
             ▼
   export_markdown.py  (flat, filed_at ASC)
             │
             ▼
   Business Links.md → docx_export.py → .docx
   # title + meta
   - oldest …
   - … newest LAST
```

---

## Phase 0 — Confirm locks (docs / gates)

**Goal:** No code until R1 default dest + modularization accepted (or overridden in chat).

- [x] **0.1** Lock **R1:** default = suggest → `other` (not always `started`). *(owner: “1 - recommend and proceed”, 2026-08-20)*
- [ ] **0.2** Append MANUAL_TEST stubs for track-end only (tray feel, flat last-line in Word); automate-first note.
- [x] **0.3** Mark layout/isolation checklist acknowledged in this file.
- [x] **0.4** Owner phase pick: **Phase 1** first *(2026-08-20)*.

**Done when:** Owner replies with pick (or “implement 1→4”). → **Phase 1 started.**

---

## Phase 1 — Review UI: remove destination picker *(Owner A1 + R1–R3)*

**Goal:** No Assign control; File/Enter uses default dest; read-only filing line.

- [x] **1.1** Remove **Assign to:** label + combobox from `review_ui.py`.
- [x] **1.2** File path: `suggested_destination` → else `other`; still set `filed_destination` on queue.
- [x] **1.3** Enter / File / removal dialog / next advance unchanged; toast shows dest label (**R3**).
- [x] **1.4** Tests + MANUAL_TEST hover list (drop Assign tip).
- [x] **1.5** (**R2**) Read-only “Filing as: {label}” (or equivalent) — not a picker.

**Done when:** No Assign row; pytest/CLI File works; Enter still files. → **✅ 2026-08-20** (`test_bb_links_ux_phase1.py` + related).

---

## Phase 2 — Master document: flat list *(Owner A2 + R4, R7, R10)*

**Goal:** No category `##` subsections; last filed = last line; regen cleans live noise.

- [x] **2.0** (**R4**) Additive config: `export.flat_list: true`, `export.sort_by: filed_at`.
- [x] **2.1** Stop emitting `## {label}` in `export_markdown.py` (when flat).
- [x] **2.2** Confirm from live md/docx + exporter: noise was destination `##` labels — gone after regen.
- [x] **2.3** (**R7**) Full rebuild queue → md → docx (agent-automated); 18 filed URLs preserved.
- [x] **2.4** Order by `filed_at` ascending; stable id tie-break → **last filed = last line**.
- [x] **2.5** Tests: `test_bb_links_ux_phase2.py` + updated `test_export.py` / `test_file_workflow.py`.

**Done when:** Regenerated master is flat; newest File at bottom. → **✅ 2026-08-20** (live regen: 18 links, no `##` category headings).

---

## Phase 3 — Tray icon for this Reviewer *(Owner A3 + R5, R6, R11)*

**Goal:** Dedicated tray; Inc menu unbroken.

- [x] **3.1** **NEW** `review_tray.py` (pystray peer pattern; not inside Inc tray).
- [x] **3.2** Actions: **Open / focus**, **Quit** (minimal set).
- [x] **3.3** (**R6**) Single-instance: second `review` focuses existing; no duplicate tray (`review_single_instance.py`).
- [x] **3.4** Regression: Inc `bookmark_review` command unchanged (pytest asserts config).
- [x] **3.5** Tests: `test_bb_links_ux_phase3.py`.

**Done when:** Tray Open/Quit works; Formulated→Bookmark review still starts app. → **✅ 2026-08-20**

---

## Phase 4 — Template shell + rename *(Owner A4 + R5, R8)*

**Goal:** Business = instance #1 of reusable shell; visible rename + banner + hooks doc.

- [x] **4.1** Config-driven product title / banner (`instance_branding.py` + `routes.json` → `product`).
- [x] **4.2** Rename UI → **Business links Bookmark Reviewer** (casing polish completed in **BB-BRAND-1**); top template banner (Health / Investment as guide for other apps).
- [x] **4.3** Document second-category hooks — `business_bookmark_sorter/TEMPLATE.md`.
- [x] **4.4** Grep user-facing “Bookmark Reviewer” in UI/tray; package path unchanged.
- [x] **4.5** Automated suite green; owner one MANUAL pass still required before **deleting this satellite**.

**Done when:** New name + banner live; hooks documented; tests green. → **✅ 2026-08-20** (delete satellite after MANUAL).

---

## Phase 5 — Optional escape hatch *(Agent R9 only)*

- [ ] **5.1** Settings UI: optional default-destination override (still no Assign dropdown on main panel).
- [ ] **5.2** Persist in gitignored session settings; tests for load/save.
- [ ] **5.3** Skip entirely if owner declines.

---

## Automation (reduce wall-clock)

| What | Automate how |
|------|----------------|
| No Assign | Mock-root UI test: widget/text absent |
| Default dest | `mark` / file_workflow pytest |
| Read-only Filing as | Assert label text from suggest |
| Flat export + last@bottom | Fixture queue → md asserts |
| Docx clean | Agent `export-md` + regenerate after Phase 2 |
| Tray | Mock pystray; menu item names |
| Single-instance | Second-launch focus unit test (mock) |
| Rename/banner | String asserts on construct |
| Inc unbroken | Existing `inc_launcher` config tests |
| Live only once | MANUAL: tray feel + one File → last Word line |

**Do not** ask owner to click through mid-build; agent kill/restart `review` after phases.

---

## Out of scope

- Full Health / Investment instance  
- Renaming package folder `business_bookmark_sorter/`  
- §5 Phase 3 Chrome auto-delete  
- Fusing PR `bookmark_sorter.py`  
- Editing Inc tray pillars beyond optional label string  
- Re-adding Assign dropdown without a new task  

---

## Owner pick (next)

- BB-LINKS-UX optional **5** (Settings dest override) — reply on that track if wanted.  
- **Branding polish** → [task_bb_links_branding_polish.md](task_bb_links_branding_polish.md) — reply **1** / **0→1** there.  
- Delete **this** satellite after MANUAL §Q (+ BB-BRAND-1 done if still open).
