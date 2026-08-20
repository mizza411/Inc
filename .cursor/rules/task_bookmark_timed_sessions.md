# BB-TIMED-1 — Timed / minimal-UI bookmark review sessions (§5 add-on)

**Status:** 🟢 **Phases 0–7 ✅** + automated sign-off ✅ + **Word same-name / lock fix ✅** (2026-08-20)  
**Attempt (Word same-name / lock fix):** 3 (passed)  
**Authoritative backlog:** **this file** (main `.cursor/rules/task.md` §5 is overloaded — thin pointer only there)  
**Delete when:** owner optional §P done (or explicitly skips) — then fold notes into §5 and **delete this satellite**.

**Bugfix (2026-08-20):** Word COM “same name as an open document” / WinError 32 on File — root cause was Close on a **worker thread** (Word STA hang). Fix: Close on calling thread + `DisplayAlerts=0` + `Saved=True` + temp regenerate; sibling `*.updated.docx` only if master stays locked. Tests: `test_docx_same_name_fix.py`.

**Owner ask (2026-08-20):** Complete Chrome→Inc filing **ASAP** via **timed actions / timed windows**; keep product **generic**; **auto-launch** from `project_reminder` (`launcher_config.json` preferred; `auto_launcher.py` only if config cannot launch); **Settings UI** for session length (not hand-edit JSON); **auto-open** the current bookmark link; **minimal UI** interaction while still filing correctly. Prove understanding first — phases below. **Do not move** the sorter into `project_reminder`.

**One-liner:** Clock/boot opens Inc `review`; a timed slot + auto-open + one-confirm filing burns down the pending queue with almost no clicks; duration lives in a **Settings control** on the GUI.

**Parent track:** `.cursor/rules/task.md` **§5** Business Bookmark Sorting (`business_bookmark_sorter/`).

**Related (do not merge / do not break):**

| Track | Why separate |
|-------|----------------|
| **§5** Phase 0–2d shipped sorter | Extend; do not rewrite core file/export/queue |
| **§5** Phase 3 auto de-bookmark | Optional later; not required for timed sessions v1 |
| **§5** Phase 5 A–C hygiene | Owner ops; still valid; not blocked by this satellite |
| **§8** Drive sorter / ChatGPT inbox | Sibling inboxes; reuse patterns later — not v1 |
| **Inc** `inc_launcher` schedules / Track C `bookmark_review` | Additive schedule target; keep tray menu |
| **PR** `bookmark_sorter.py` | **Different** product (Strategy/Marketing categories) — **never fuse or replace** |
| **PR** `inc_launcher_tray` | Already boots Inc tray; daytime clocks stay in Inc |
| Tegrid / FIR / OTI / NET-ASK | Unrelated |

---

## Layout (locked 2026-08-20)

**Decision:** **Stay in Inc** — keep `business_bookmark_sorter/` at Inc root. **Do not** move to `project_reminder`.

| Path | Role |
|------|------|
| `business_bookmark_sorter/` | Review UI, queue, export, **new** session Settings + timer + auto-open modules |
| `inc_launcher/launcher_config.json` | Additive schedule item → `bookmark_review` (daytime timed open) |
| `project_reminder/launcher_config.json` | Additive boot entry pointing at Inc `review` (**prefer config-only**) |
| `project_reminder/auto_launcher.py` | Touch **only** if config-only launch proven broken |

**Signals to stay in Inc:** filing cabinet = Inc destinations; queue + Business Links already here; PR already starts Inc tray.

**Hard isolation (modularization — avoid breaking ANYTHING ANYWHERE):**

- [x] **Never** move/delete `business_bookmark_sorter/` into PR
- [x] **Never** edit or replace PR `bookmark_sorter.py` for this track
- [x] **Never** bulk-export Chrome trees into chat/AI; local Bookmarks JSON only
- [x] **Never** auto-file with **zero** user confirm in v1 (judgment stays human)
- [x] **Never** open all ~2k URLs at once — **one URL per current item** only
- [x] Prefer **new modules** under ~500 lines (`session_settings.py`, `session_timer.py`, `auto_open.py`); thin hooks in `review_ui.py` only
- [x] Inc schedule: **additive** `schedules.items` entry; do not break Hub / Problem ID / network_ask nudges
- [x] PR: **additive** `launcher_config` key; **no** `auto_launcher.py` unless proven necessary
- [x] Automated pytest for timer/settings/auto-open/isolation; owner `MANUAL_TEST.md` only for live Chrome + timed feel + boot once

---

## Requirements lock (owner + agent)

### A — Owner-requested features

1. **Timed windows / timed actions** so filing happens ASAP without relying on memory.
2. **Generic** sorter (business = today’s config; engine reusable for other trees later).
3. **Auto-launch** via project_reminder (`launcher_config.json` preferred).
4. **Session length configurable in UI**, not by hand-editing JSON.
5. **Auto-open** the current bookmark link (so Open URL is not a manual click).
6. **Minimal UI** interaction while still achieving correct Inc filing.
7. Stay on this importance track until queue burnout is realistic.

### B — Agent recommendations (in backlog)

1. **Stay in Inc**; PR only boots/schedules the Inc GUI.
2. **Daytime clock** via existing Inc tray `schedules` (PR already starts that tray).
3. **Boot open** via additive PR `launcher_config` entry → `python -m business_bookmark_sorter review` (cwd Inc).
4. Settings UI persists duration (and toggles) to a **local gitignored** settings file — user never edits it.
5. Default session **15 minutes**; Settings control changes it.
6. **Auto-open on/off** toggle in same Settings (default **on**).
7. Pre-select suggested category; **one confirm** = File & open doc.
8. Optional **“Don’t ask again this session”** on Chrome-removal dialog (less nag; still your delete until Phase 3).
9. When timer ends: **stop nagging** (close or idle banner); do not force more items.
10. Smokes with fake queue + no live Chrome/Word in CI; owner one manual pass at end.
11. Leave PR `bookmark_sorter.py` alone (enabled or owner-disables separately — out of scope unless asked).
12. Phase 3 Chrome auto-delete remains **optional** after timed v1 ships.

### C — Feature acceptance

| # | Feature | Done when |
|---|---------|-----------|
| 1 | Session Settings UI | User sets minutes in GUI; survives restart; no JSON hand-edit required |
| 2 | Timed slot | Review runs for configured minutes then stops nagging |
| 3 | Auto-open | Showing item N opens URL N once (toggleable) |
| 4 | Minimal confirm | Suggested dest pre-selected; one primary action files |
| 5 | Inc clock | Schedule fires `bookmark_review` on chosen weekdays/time |
| 6 | PR boot | Login/boot opens Inc review (or documented config-only path) |
| 7 | Isolation | PR other sorter untouched; Hub/other schedules green; sorter pytest green |
| 8 | Generic | Duration/auto-open/session behavior not hard-coded only for “business” strings in UI code |

---

## Phases / sub-phases

### Phase 0 — Locks + isolation notes ✅ (docs)

- [x] **0.1** Owner intent understood (timed + generic + PR auto-launch + Settings UI + auto-open + stay in Inc)
- [x] **0.2** Satellite backlog created (this file); §5 pointer in main `task.md`
- [x] **0.3** Isolation rules written (no move, no fuse PR sorter, one-URL open, no zero-confirm file)
- [x] **0.4** Owner confirms Phase 0 locks (or edits) before Phase 1 code — **confirmed 2026-08-20** (menu **1**)

**Agent ETA:** ~10 min (docs only; this convo)

---

### Phase 1 — Session Settings UI (duration) — modular

**Goal:** Duration control on review GUI; persist locally; default 15.

- [x] **1.1** New `session_settings.py` — load/save gitignored settings (`data/session_settings.json`); defaults; no Chrome URLs in file — **2026-08-20**; tests `test_session_settings.py`
- [x] **1.2** Settings panel/controls on `review_ui` via `session_settings_ui.py` (**Settings…** button) — **2026-08-20**
- [x] **1.3** Unit tests: default, save/load round-trip, invalid clamp — done with **1.1** (+ `test_session_settings_ui.py`)
- [x] **1.4** README + `MANUAL_TEST` §I: change duration in UI only — **2026-08-20**

**Agent ETA:** ~50 min  
**Risk:** keep `review_ui.py` thin — extract panel if file approaches 500 lines

---

### Phase 2 — Session timer (timed window / stop nagging)

**Goal:** Active slot countdown; end → stop prompting next items / soft-close.

- [x] **2.1** New `session_timer.py` — start/pause/remaining; uses Settings duration — **2026-08-20**
- [x] **2.2** Wire into review: show remaining time; on expiry stop advance / show “session ended” — **2026-08-20**
- [x] **2.3** Tests: timer expiry with fake clock — `test_session_timer.py`
- [x] **2.4** “Extend +5 min” button — shipped with Phase 2

**Agent ETA:** ~45 min

---

### Phase 3 — Auto-open current link

**Goal:** When current pending item is shown, open its URL once; Settings toggle.

- [x] **3.1** New `auto_open.py` — open URL; debounce same id; respect toggle — **2026-08-20**
- [x] **3.2** Hook on item display / next-item; **never** bulk-open queue — **2026-08-20**
- [x] **3.3** Settings: Auto-open [ON/OFF] (default ON) — already in Settings UI; wired to opener
- [x] **3.4** Tests: toggle off = no open; same item not re-opened spam — `test_auto_open.py`

**Agent ETA:** ~40 min

---

### Phase 4 — Minimal confirm path (UI friction cut)

**Goal:** One primary action when suggestion is right.

- [x] **4.1** Ensure suggested destination pre-selected on show item — **2026-08-20**
- [x] **4.2** Keyboard/primary path: **Enter** = File & open doc — **2026-08-20**
- [x] **4.3** “Don’t ask again this session” on removal dialog — session flag only — **2026-08-20**
- [x] **4.4** Tests: removal dialog skip-when-flag; suggest still applied — `test_phase4_minimal_confirm.py`

**Agent ETA:** ~45 min

---

### Phase 5 — Inc daytime schedule (timed open)

**Goal:** Clock opens Bookmark review via existing Inc nudge scheduler.

- [x] **5.1** Additive `schedules.items` entry targeting `bookmark_review` — weekdays **11:00** (`bookmark_review_weekdays`) — **2026-08-20**
- [x] **5.2** `resolve_schedule_target` already maps menu id `bookmark_review` — confirmed; no code change
- [x] **5.3** Unittest: schedule parses + resolves; other schedule ids unchanged — `test_scheduled_nudges.py`
- [x] **5.4** Update `inc_launcher/MANUAL_TEST.md` + sorter `MANUAL_TEST` — **2026-08-20**

**Agent ETA:** ~40 min  
**Note:** Clears deferred “Bookmark review schedule” checkbox in §4/§5 once shipped

---

### Phase 6 — project_reminder boot auto-launch

**Goal:** PC start opens Inc review with minimal PR surface change.

- [x] **6.1** Inventory: `applications` supports `path` + `arguments` + `working_dir` (same as launching an exe) — **config-only OK**; scripts need hardcoded `__init__` keys so avoided
- [x] **6.2** Additive `applications.inc_business_bookmark_review` → `pythonw -m business_bookmark_sorter review` cwd Inc — **2026-08-20**; **no** `auto_launcher.py` edit
- [x] **6.3** N/A — config-only path worked
- [x] **6.4** Isolation smoke: PR `scripts.bookmark_sorter` untouched; Inc path only — `test_pr_boot_config.py`
- [x] **6.5** Owner `MANUAL_TEST` §N one boot check documented

**Agent ETA:** ~45 min (config-only) / ~70 min if `auto_launcher.py` needed

---

### Phase 7 — Generic polish + docs + smokes

**Goal:** Session behavior not glued to business-only UI strings; backlog hygiene.

- [x] **7.1** Settings labels/generic session copy; chrome filter stays in `routes.json` — window title **Bookmark Reviewer** + config note — **2026-08-20**
- [x] **7.2** Full `pytest business_bookmark_sorter` + Inc schedule tests green — recorded with Phase 7
- [x] **7.3** Update §5 status blurb + this satellite checkboxes; analogy log entry — **2026-08-20**
- [x] **7.4** `MANUAL_TEST.md` §§I–N + consolidated §O sign-off — **2026-08-20**

**Agent ETA:** ~35 min

---

### Phase 8 — Optional (not in v1 total unless you ask)

- [ ] **8.1** §5 Phase 3 Chrome auto de-bookmark (backup + gate)
- [ ] **8.2** Zero-confirm auto-file for high-confidence keyword matches (privacy/risk — needs explicit OK)
- [ ] **8.3** Clock time / weekdays also in Settings UI (today: schedule JSON via agent or tray config; duration stays UI)

**Agent ETA if all optional:** ~120+ min — **excluded** from v1 total below

---

## Agent time estimate (this convo — build phases only)

| Phase | Minutes (agent) |
|-------|----------------:|
| 0 (done docs) | 10 |
| 1 Settings UI | 50 |
| 2 Timer | 45 |
| 3 Auto-open | 40 |
| 4 Minimal confirm | 45 |
| 5 Inc schedule | 40 |
| 6 PR boot | 45 |
| 7 Polish + smokes | 35 |
| **Total v1 (Phases 0–7)** | **~310 min (~5.2 h)** |

Update if Phase 6 needs `auto_launcher.py`: **~335 min**.  
Optional Phase 8: **+120+ min** — not counted unless approved.

**Sub-phase count (owner pacing):** **~24** unchecked build boxes in Phases 1–7 (excl. 0.4 confirm).  
At **1 sub-phase/day** ≈ **24 days**. At **2/day** ≈ **12 days**.  
If pacing by **phase** (1–7): **7 days** @1/day or **~4 days** @2/day.

Owner filing of ~1926 bookmarks is **separate** (human judgment time); this estimate is **agent build** only.

---

## How to automate to cut phase time

1. **Pytest-first every sub-phase** — fake clock, fake webbrowser.open, temp settings file; no mid-build “open GUI and click.”
2. **One module per concern** — less debug churn; keep `review_ui` hooks tiny.
3. **Config-only PR wire** — avoid `auto_launcher.py` edit unless smoke proves need (saves ~25 min + regression risk).
4. **Reuse Inc schedule plumbing** — additive JSON + existing `NudgeScheduler`; do not build a second timer service for daytime open.
5. **No live Word/Chrome in agent tests** — mock export path where Phase 4 touches file workflow; keep Phase 2b file_workflow tests as regression only.
6. **Single MANUAL_TEST pass** at v1 end (Settings + one timed slot + one auto-open + one boot) — not after each sub-phase.
7. **Owner Phase 0.4 confirm in chat** before coding — prevents rework.

---

## Out of scope (v1)

- Moving folder to `project_reminder`
- Fusing/replacing PR `bookmark_sorter.py`
- Cloud AI classify / full Chrome dump to chat
- Zero-confirm auto-file (unless Phase 8.2 approved)
- Drive / ChatGPT inbox sorting
- Changing Inc Hub pillars or Tegrid/FIR/OTI

---

## Kickoff command (when owner picks a phase)

From Inc: implement **only** the picked sub-phase ID (e.g. “BB-TIMED-1 Phase 1.1”). Main launch remains:

```powershell
python -m business_bookmark_sorter review
```
