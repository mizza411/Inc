# BB-BRAND-1 — Title casing + template-as-guide wording (BB-LINKS-UX polish)

**Status:** 🟢 **Phase 1 ✅** (2026-08-20) — delete after owner title/banner glance  
**Attempt (Phase 1):** 1 (passed)
**Authoritative backlog:** **this file** (main `task.md` §5 / BB-LINKS-UX-1 = thin pointers)  
**Delete when:** Phase **1** (required) complete + tests green + owner quick title/banner glance — then fold 3–5 lines into §5 / BB-LINKS-UX-1 and **delete this satellite**.  
**Parent:** §5 · `business_bookmark_sorter/` · follows **BB-LINKS-UX-1** Phases 0–4 ✅  

**Owner ask (2026-08-20):**
1. Change **“Business links bookmark Reviewer”** → **“Business links Bookmark Reviewer”** (and other references).
2. Banner / TEMPLATE should read as a **guide for building other apps** (Health, Investment, etc.) — **not** “not a second app / via config only” framing.

**One-liner:** Fix title casing + rewrite template copy so Health/Investment are clearly **future apps you can build from this pattern**, without shipping those apps now.

---

## A — Owner-requested (must)

| # | Ask |
|---|-----|
| **A1** | Rename product strings to **Business links Bookmark Reviewer** (window, header, tray tip, defaults, docs/tests that assert the old casing). |
| **A2** | Leave Inc menu **Formulated ideas → Bookmark review** unchanged unless a later task asks. |
| **A3** | Rewrite top banner + `TEMPLATE.md` (+ README lines that match) as a **guide to building other apps** (e.g. Health / Investment Bookmark Reviewers). |
| **A4** | Do **not** implement Health/Investment apps in this track — guidance only. |

---

## B — Agent recommendations (in backlog)

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| **R1** | Drive title/banner only via `instance_branding.py` + `routes.json` → `product.*` (no scattered hard-codes) | One place to edit; already modular | **1.1** |
| **R2** | Grep whole sorter + satellites for old casing / “not a second app” / “via config, not a second app” | Catch tray logger, MANUAL_TEST, tests | **1.2** / **1.4** |
| **R3** | Suggested banner tone: “Use this Business links app as the pattern/guide when you build Health or Investment Bookmark Reviewer apps later.” | Matches owner intent | **1.3** |
| **R4** | Suggested TEMPLATE tone: checklist to **scaffold another app** (folder/config/tray/launcher) from this shell — allow either same-package instance **or** sibling app folder later | Guide ≠ forbid second app | **1.3** |
| **R5** | Keep Python package `business_bookmark_sorter` name; no big rename | Avoid breaking imports / Inc / PR boot | hard lock |
| **R6** | Pytest string asserts for new title + banner keywords (`Health`, `guide`/`pattern`/`build`); fail if old anti-fork phrase remains | Automate-first | **1.4** |
| **R7** | Agent kill/restart `review` after ship so tray/title refresh | No mid-build owner click-through | **1.5** |
| **R8** | *(Optional)* Align BB-LINKS-UX-1 / §5 pointer titles to new casing when folding | Tracker hygiene | after delete |
| **R9** | *(Optional / separate)* Phase 5 Settings dest override remains optional on BB-LINKS-UX-1 — not this satellite | Don’t mix scopes | out |

---

## Layout + modularization (don’t break ANYTHING ANYWHERE)

| Path | Touch | Don’t |
|------|--------|--------|
| `instance_branding.py` | Defaults for title + banner | — |
| `config/routes.json` → `product` | `app_title`, `tray_tooltip`, `template_banner` | Destinations / chrome_filter |
| `review_ui.py` / `review_tray.py` | Only if still hard-coded | Tray Open/Quit behavior |
| `TEMPLATE.md` / `README.md` / `MANUAL_TEST.md` | Wording | Live queue / Word files |
| `tests/test_bb_links_ux_phase4.py` (+ small polish test) | Assert new strings | Broad unrelated suite rewrites |
| `inc_launcher/launcher_config.json` | **No** (keep “Bookmark review” menu) | — |
| PR `bookmark_sorter.py` | **Never** | — |

**Hard locks:** stay in Inc sorter · no PR fuse · no Health/Investment product build · no package folder rename · no Assign picker return.

---

## ETA (agent — this track only)

**Total (Phase 1 required):** **~35 minutes**  
**With optional R8 tracker fold only:** still ~35–40 min (docs).

| Phase | Focus | Est. (min) |
|-------|--------|------------|
| **0** | Lock wording intent (guide for other apps) | 5 |
| **1** | Title casing + banner/TEMPLATE rewrite + tests + restart | 30 |
| | **Sum** | **35** |

**Calendar @ 1–2 phases/day:** **1 day** (both phases same day is fine; or 1–2 days if split).  
**Leaf items (~8) @ 1–2/day:** **4–8 days** — prefer **phase** cadence (**1 day**).

---

## Phase 0 — Confirm copy intent

- [x] **0.1** Lock: title = **Business links Bookmark Reviewer** (capital **B**ookmark).
- [x] **0.2** Lock: template copy = **guide for building other apps** (Health / Investment), not “forbidden second app”.
- [x] **0.3** Owner pick: implement **Phase 1** *(2026-08-20)*.

**Done when:** Owner says implement / **1**. → **Phase 1 started/done.**

---

## Phase 1 — Title + guide wording *(Owner A1–A4 + R1–R7)*

- [x] **1.1** Update `product.app_title` / `tray_tooltip` / branding defaults → **Business links Bookmark Reviewer**.
- [x] **1.2** Grep-fix references (UI, tray, MANUAL_TEST window title, README, tests, logger).
- [x] **1.3** Rewrite `template_banner` + `TEMPLATE.md` (+ README) as build-other-apps **guide** (R3–R4); remove “not a second app” framing.
- [x] **1.4** Tests: new title; banner/TEMPLATE mention Health + guide/build; no old anti-fork phrase.
- [x] **1.5** Kill/restart `review`; agent verify title via config load.
- [ ] **1.6** Owner title/banner glance → then **delete this satellite** (fold 3–5 lines into §5 / BB-LINKS-UX-1).

**Done when:** New casing live; guide wording live; pytest green. → **✅ code 2026-08-20** (1.6 = owner glance).

---

## Automation (reduce wall-clock)

| What | How |
|------|-----|
| Title casing | `load_routes_config` + `app_title()` assert; source grep test |
| Banner/TEMPLATE | Assert Health + guide/pattern/build; assert absence of “not a second app” |
| Tray tip | `tray_tooltip(config)` assert |
| Regression | Full `business_bookmark_sorter/tests` once |
| Live | Agent restart review only; owner optional 10s glance |

---

## Out of scope

- Building Health / Investment apps now  
- Renaming Inc menu “Bookmark review”  
- Package rename `business_bookmark_sorter`  
- Optional BB-LINKS Phase 5 Settings override (separate)  
- Re-opening Assign dropdown  

---

## Owner pick (next)

Reply **1** (or **0→1**) to implement Phase 1 now.
