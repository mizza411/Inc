# Active Task List
*This file tracks all tasks - coding, business, research, and other activities*

## 🎯 Current Priority Projects

### 1. Problem Identification Tool (70% Complete - LIVE)
**Status:** Deployed at https://mizza411.github.io/Inc/problem_identification_tool/web/index.html (GitHub Pages); Netlify mirror optional

#### High Priority — Strategy 3 + “I'll pay to..” migration (NEW — Jul 2026)
**Scope:** Retire Google Form “I'll pay to..”; consolidate on Mizza411 tool; integrate paid social-capital distribution into Strategy 3.

**Decisions (locked):**
- Email **required** on `ill_pay_to_v1` (with privacy note)
- **Add** questionnaire `ill_pay_to_v1`; keep `general_problems_v1`
- **Minimal branching** in `questionnaire.js` (2 rules: existing-solutions follow-up; one-time vs subscription price)
- **One-time import** of ~12 Google Form responses before closing form
- Per-distributor **ref/UTM links** for paid sharers

**Layout:** `problem_identification_tool/` (survey + dashboard) + `Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification/` (outreach, distributor tracking)

- [x] **Phase A — Questionnaire** (target: Jul 2026)
  - [x] Add `ill_pay_to_v1` to `web/data/questionnaires.json` (title “I'll pay to..”, WTP + urgency questions)
  - [x] Add `email` question type + validation in `questionnaire.js`
  - [x] Implement minimal conditional branching (2 rules)
  - [x] Set `ill_pay_to_v1` as active questionnaire (or `?survey=ill_pay_to_v1` param)
- [ ] **Phase B — Strategy 3 integration** (split into sub-phases — Jul 2026)
  - [x] **B1 — Distributor links + templates** (standalone; no changes to live survey or collector)
    - [x] `distributor_links.py` — unique ref/UTM link generator + local registry
    - [x] `distributor_message_templates.txt` + `distributor_brief.md`
    - [x] `test_distributor_links.py` smoke tests
  - [x] **B2 — Collector integration** — optional `--distributor` mode in `network_problem_collector.py`
  - [x] **B3 — Sharing utilities** — wire `sharing_utilities.py` ref/UTM to Strategy 3 workflow
- [ ] **Phase C — Data migration** (split — Jul 2026)
  - [x] **C1 — Import script** — `scripts/import_google_forms_csv.py` + tests + sample CSV fixture
  - [ ] **C2 — Dashboard merge** — dashboard reads `imports/google_forms_ill_pay_to.json` + localStorage
  - [ ] **C3 — Retire Google Form** — run import on real export, verify counts, close form
- [ ] **Phase D — Deploy & retire Google Form**
  - [ ] Deploy to GitHub Pages; smoke-test live URL
  - [ ] Close/archive Google Form after import verified

#### High Priority - Next Steps (This Week)
- [x] **UX Improvements** (Phase 1 — May 2026: `web/questionnaire.css`, step label + dots, transitions, inline validation, keyboard Enter)
  - [x] Add progress indicators to questionnaire
  - [x] Implement smooth transitions between questions
  - [x] Create engaging visual design refresh
  - [x] Design intuitive navigation flow

- [ ] **Achievement System** (Gamification)
  - [ ] Design achievement badges/rewards
  - [ ] Implement achievement tracking
  - [ ] Add achievement display in dashboard

- [ ] **Admin Panel**
  - [ ] Create admin authentication system
  - [ ] Build admin dashboard for managing questionnaires
  - [ ] Add user management features

#### Medium Priority - Next 2 Weeks
- [ ] **AI-Powered Analysis Enhancement**
  - [ ] Implement natural language processing for problem extraction
  - [ ] Add sentiment analysis
  - [ ] Build pattern recognition algorithms
  - [ ] Create automated problem categorization

- [ ] **Automated Workflows**
  - [ ] Set up automated data collection schedules
  - [ ] Implement email notifications for new responses
  - [ ] Build automated backup system

- [ ] **Passive Data Collection**
  - [ ] Social media monitoring script
  - [ ] Forum/Reddit scraper
  - [ ] Review analysis tool
  - [ ] Search trend analyzer

#### Low Priority - Next Month
- [ ] **Testing Suite**
  - [ ] Unit tests for core functions
  - [ ] Integration testing
  - [ ] User acceptance testing
  - [ ] Performance testing

- [ ] **Accessibility Features**
  - [ ] Add keyboard navigation
  - [ ] Implement screen reader support
  - [ ] Ensure color contrast compliance
  - [ ] Add alternative text for images

- [ ] **Security & Privacy**
  - [ ] Implement data encryption
  - [ ] Add privacy controls
  - [ ] Create data retention policies
  - [ ] Build data deletion tools

---

### 2. Music ID Wearable Device (NEW PROJECT)
**Status:** Planning Phase - Needs roadmap and architecture

#### Immediate Tasks Needed
- [ ] **Project Setup**
  - [ ] Create project directory structure
  - [ ] Set up version control
  - [ ] Create project documentation

- [ ] **Hardware Research & Planning**
  - [ ] Research MCU options (ESP32, Raspberry Pi Pico, etc.)
  - [ ] Research microphone modules
  - [ ] Research connectivity options (WiFi, Bluetooth, cellular)
  - [ ] Create hardware component list with costs

- [ ] **Software Architecture**
  - [ ] Design audio capture system
  - [ ] Plan cloud API integration (ACRCloud/AudD)
  - [ ] Design data sync architecture
  - [ ] Plan offline buffering system

- [ ] **Mobile App Planning**
  - [ ] Create app mockup/sketch
  - [ ] Design user interface
  - [ ] Plan data storage and sync
  - [ ] Design safety-first UX

- [ ] **Legal & Ethical Research**
  - [ ] Research recording ambient audio legality
  - [ ] Create privacy policy framework
  - [ ] Research data protection requirements

- [ ] **MVP vs Full Version Planning**
  - [ ] Define MVP feature set
  - [ ] Plan full version features
  - [ ] Create development roadmap

- [ ] **Business Planning**
  - [ ] Create pitch strategy for investors
  - [ ] Identify early adopter market
  - [ ] Research competitive landscape

---

### 3. YouTube Content Automation (Phase 4 Complete)
**Status:** Phase 4 launch prep complete  
**Tracker:** `Strategy-2-Problem-Solving/Content-Automation/youtube/youtube_business_tasks.md`

#### Phase 3 (Complete)
- [x] **3.1** Add trending topic analysis (`core/topic_analyzer.py`, `main.py trends` command)
- [x] **3.2** Implement content performance tracking (`core/performance_tracker.py`, SQLite, `main.py performance`)
- [x] **3.3** Create automated scheduling system (`core/content_scheduler.py`, `main.py schedule`)
- [x] **3.4** Build analytics dashboard (`core/analytics_dashboard.py`, `main.py dashboard`)
- [x] **3.5** Implement automated research and fact-checking (`core/research_engine.py`, `main.py research`)
- [x] **3.6** Add automated subtitle generation (`core/subtitle_generator.py`, `main.py subtitles`)
- [x] **3.7** Comprehensive testing and bug fixes (`tests/`, `test_phase3_completion.py`, `main.py test`)

#### Phase 4 — Launch Prep
- [x] **4.1** Final system testing (end-to-end `create` pipeline, extend `tests/`, `test_phase4_completion.py`, `main.py test`)
- [x] **4.2** Create launch content batch — 10+ videos (`core/launch_batch.py`, `main.py launch`, `main.py batch` manifest)
- [x] **4.3** Set up monitoring and alerts (`core/pipeline_monitor.py`, `main.py monitor`)
- [x] **4.4** Prepare documentation and user guides (`README.md`, `docs/CLI_REFERENCE.md`, `docs/LAUNCH_CHECKLIST.md`)
- [x] **4.5** Launch system and monitor performance (`core/launch_controller.py`, `main.py go-live`)
- [x] **4.6** Set up YouTube monetization application process (`database/monetization_checker.py`, `main.py monetization`, `docs/MONETIZATION_APPLICATION.md`)

---

### 4. Inc Tray Icon + Super Main Launcher
**Status:** Phase 5 v1 complete (agent formulation front door) — **manual §G once** (`inc_launcher/MANUAL_TEST.md`) (2026-06-30)  
**Goal:** Windows **tray icon** (notification area, near the clock) + optional super main hub; all `C:\dev\Inc` entry points organized under **4 pillars** (extensible to 5+ later).  
**Folder:** `inc_launcher/` — run: `python -m inc_launcher.tray_app` from `C:\dev\Inc`  
**Manual tests:** `inc_launcher/MANUAL_TEST.md` (most checks automated; optional §D reboot only)

> **Terminology:** “Tray icon” = the small icon you right-click in the Windows notification area. Same as “system tray app” — one background process, one icon, menu on right-click.

#### Session handoff (Inc launcher + nudges + Track C — convo closed 2026-06-29)

| Item | Status |
|------|--------|
| Phase 4 interval nudges (4.1–4.5) | ✅ Shipped `4c54b9c`; **Interval nudges [ON]** in tray |
| Track C — Bookmark review menu | ✅ Shipped `909c6d9`; **Formulated ideas → Bookmark review** |
| Automated tests | ✅ `pytest inc_launcher/tests` (38+) + `smoke_hub`; `test_cli_status.py`, `test_track_c_bookmark.py` |
| Boot | External-repo `auto_launcher.py` starts tray; Inc **Start at Windows login [OFF]** (intentional) |
| Live nudge proof | `inc_launcher/schedule_fired.json` — fired 2026-06-29: 09:00 task.md, 09:15 Hub, 10:00 Problem ID live |

**Active dev:** **Phase 5 — Agent formulation front door** (approved 2026-06-30). Earlier phases optional follow-ups below.

#### Phase 5 — Inc Hub agent formulation front door (Track D)
**Status:** Approved — not started (2026-06-30)  
**Goal:** Inc Hub becomes the **front door** for the repeatable **Cursor agent** formulation run (strategies **5, 6, 7, 9, 11, 12, 13, 14, 15**; skip 3, 4, retired 8/10; read-only on existing strategy scripts; write `business_ideas_YYYYMMDD.md` under **`agent-business-idea-runs/outputs/`**). **Not** the `run_all_strategies.py` interactive CLI menu.

**Layout (2026-07-06, updated 2026-07-07):** `agent-business-idea-runs/` at repo root — `inputs/` (fetch JSON), `outputs/` (`.md` + `.docx`), `agent_strategy_run.py` (canonical fetch runner; Strategy 15 skipped by default). See `agent-business-idea-runs/README.md`.  
**User pain today:** Remember run → open Cursor on `C:\dev\Inc` → hunt/copy long prompt → paste in chat → send.  
**Target flow:** **Inc Launcher tray running** → open/focus Inc Hub → **Option B modal** → on Start: open Cursor → clipboard + auto-paste into chat (`cursor_copy_helper`) → user presses Enter. No detached OS toasts; all reminder UI lives on Hub.

**Reminder UI (user 2026-06-30 — Option B only):**
- **UI:** Mini Hub modal (Option B) — the only reminder surface for this workflow
- **Gate:** Inc Launcher **tray process must be running** (notification-area icon). If tray is not running → no modal, no nudge
- **Host:** Modal is a **child of Inc Hub** (Toplevel on Hub window). Never a freestanding Windows toast outside Hub
- **Triggers (v1):** Hub card click **“Agent formulation run”** → show modal. **Auto-open (optional later, Phase 5.5):** schedule fires only when tray is running → **open/focus Hub window first** → same Option B modal (not a separate lighter UI)
- **Modal copy:**
  - Title: “Ready for formulation agent run?”
  - Bullets: Opens Cursor at `C:\dev\Inc` · Pastes prompt into chat (~8s) · Skips 3, 4, 8, 10 per policy
  - Buttons: `[ Start ]` · `[ Not now ]`
- **Explicitly out:** Option A (detached bottom-right toast without Hub) — not needed; one UI pattern is enough

**Scope (v1):**
- Single source of truth: `prompts/agent_formulation_run.txt` (full agent prompt; editable without code changes)
- New launcher action (e.g. `agent_run` or `cursor_prompt`) orchestrating: load prompt → `copy_to_clipboard` → `cursor` open `C:\dev\Inc` → `paste_after_delay` (pyautogui; user focuses chat)
- Hub **Formulated ideas** pillar: **pinned** card **“Agent formulation run”** (primary); demote/rename existing **“Run all strategies”** → **“Run all strategies (CLI menu)”** so it is not confused with agent workflow
- Fix Hub content header clip: `_header` / `_subtitle` both on `row=0` in `hub_window.py` (overlap bug)
- Log last run timestamp optional: `inc_launcher/agent_run_log.json` (for “last run was …” in UI later)

**Out of scope (v1):**
- Fully unattended agent send (no Cursor API/deeplink in repo)
- Replacing agent execution with subprocess strategy runs
- Detached OS toasts (Option A) or any reminder UI when Inc Launcher tray is not running
- Scheduled formulation nudge (Phase 5.5) until user approves a slot — when built, must use Hub + Option B modal, not bypass Hub

**Phases:**
- [x] **5.0 — Hub UI fix:** Separate header (`row=0`) and subtitle (`row=1`); adjust canvas `row`; smoke/visual check
- [x] **5.1 — Prompt artifact:** Add `prompts/agent_formulation_run.txt` with canonical agent prompt (user’s current wording); `prompts/README.md` one-liner
- [x] **5.2 — Action orchestration:** `inc_launcher/actions.py` — new action; reuse `cursor_copy_helper.copy_to_clipboard` + `paste_after_delay`; thread/timer so paste runs after Cursor opens
- [x] **5.3 — Config + Hub card:** `launcher_config.json` — new pinned item under **formulated**; rename CLI item; tray submenu mirror optional
- [x] **5.4 — Reminder UI (Option B, Hub-hosted):** Mini Toplevel on Hub on card click; `[ Start ]` runs `agent_run`; `[ Not now ]` dismisses; tray-running gate enforced
- [ ] **5.5 — Schedule (optional, not v1):** Weekday slot (user approves first) → tray running → open/focus Hub → **same Option B modal**; no detached toast
- [x] **5.6 — Tests + docs:** `test_agent_run.py` (mock clipboard/cursor/paste); `inc_launcher/README.md`, `MANUAL_TEST.md` §G (focus-chat + Enter)

**v1 definition of done:** Inc Launcher tray running → click **Agent formulation run** → Hub shows **Option B modal** → **Start** → Cursor opens on repo → prompt on clipboard → auto-paste after delay if pyautogui present → user sends chat → agent run proceeds per prompt file. CLI menu card clearly labeled. Header no longer clipped. `pytest inc_launcher/tests -q` green.

**Dependencies:** `cursor_copy_helper.py` (repo root); `pyautogui` optional for auto-paste  
**Layout:** `prompts/` at repo root (new); changes in `inc_launcher/` only

#### Pending (optional — not blocking)

- [ ] **Schedule tune** — if 09:15 Hub or 10:00 Problem ID browser nudge is too noisy; edit `launcher_config.json` → `schedules.items` or tray **Interval nudges [OFF]**
- [ ] **Track B** — clearer boot vs nudge toggle labels — **skipped** (user 2026-06-29); reopen only if menu still confusing
- [ ] **Bookmark review schedule** — weekday nudge deferred; menu-only for now
- [ ] **Phase 4 v1.1** — toast + Snooze before auto-open; catch-up if tray starts after missed slot
- [ ] **MANUAL_TEST §D** — reboot + external `auto_launcher` one-tray check (skip if daily use already OK)
- [ ] **Operational** — file Chrome bookmarks via tray review (~**1926** pending per `python -m business_bookmark_sorter status`)

#### Four pillars (top-level nav — tray icon right-click + super main sidebar)

| Pillar | Purpose | Initial `Inc` mapping |
|--------|---------|------------------------|
| **My Established business ideas** | Businesses you are running or committed to | `Started-Businesses/`, Strategy 1 **gadget ops** (`Strategy-1-Business-Variation/gadget-business/…`), live ops (e.g. YouTube when active). Folder shortcut to Strategy 1 playbook OK here for ops adjacency. |
| **My leads** | Contacts, outreach, campaigns | `abuja_lead_generator/` (DB, scraper, email/WhatsApp, reports) |
| **Formulated ideas** | Idea pipeline outputs & strategy runs | **Strategy 1 formulation CLI** (`business_variation_collector.py` / Hub “Run Strategy 1”), `Business-Idea-Formulation-Strategy-*/`, `run_all_strategies.py`, `agent-business-idea-runs/`, `past_business_ideas.md`, `business_research/`; curated shortlist (when approved): **`Prospect-Businesses/`** |
| **Problem identification** | Discovering & capturing problems (inputs to formulation) | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/`, problem-collection strategies (3, 4, 5, 10, 11, 12, etc.) |

**Strategy 1 split:** Formulation (complaint→variation script + agent/runner) lives under **Formulated ideas**; gadget automation stays under **Established**. Do not treat the Hub folder card as a substitute for “Run Strategy 1”.

**Flow:** Problem identification → Formulated ideas → **Prospect businesses** (curated shortlist) → Established businesses; **My leads** supports outreach alongside that pipeline.

#### Prospect-Businesses folder
**Status:** Phase **0–2 complete** (2026-07-12) — Layout + scaffold + 3 user-named seeds; **Phase 3 optional (Hub/sorter)** awaits separate approval  
**Goal:** Dedicated home for businesses **not started** but with **strong prospects** — separate from `Started-Businesses/` (e.g. software) and from raw formulation dumps (`agent-business-idea-runs/outputs/`).

**Layout:** Folder `Prospect-Businesses/` at repo root (`C:\dev\Inc\Prospect-Businesses/`) — **created**.  
**Active prospects (3):** `examfee-planner.md`, `agentdispute-ai.md`, `scimlite-ng.md` (from `business_ideas_20260712.md`).

| Signal | Why |
|--------|-----|
| Twin of `Started-Businesses/` | Clear “not started yet” vs “running/committed” |
| Shortlist only (~5–10 active) | Not every weekly `business_ideas_*.md` row |
| One `.md` per prospect | Problem, why now, MVP cost, next validation date, link to source idea run |
| Own folder only in early phases | Avoids coupling to launcher, sorter, or strategy scripts until optional later phases |

**Graduation rule (locked if Layout approved):** Moving or copying a prospect into `Started-Businesses/` requires **explicit user approval** every time. Agents must **not** auto-graduate, auto-rename as “started,” or treat Hub/bookmark filing as graduation. User is the only approver of “this is now a started business.”

##### Non-negotiable safety (do not break anything anywhere)

- **No implementation until user approves Layout**, then the **named phase** (or says implement now / skip gate for that phase).
- **One phase at a time.** Do not create folder + wire Hub + change sorter routes + seed prospects in one unreviewed pass.
- **Additive only in Phases 1–2:** new files under `Prospect-Businesses/` only. No edits to strategy scripts, `run_all_strategies.py`, agent fetch runner behavior, or `Started-Businesses/software-development.md` content.
- **Do not move/rename/delete** existing `agent-business-idea-runs/outputs/`, `business_research/` plans, or `Started-Businesses/` files under this task.
- **Do not bulk-import** every idea from formulation runs into prospects.
- **Do not** add auto-graduation scripts, watchers, or Hub buttons that write into `Started-Businesses/` without a user confirm step (and even then only in a later phase if approved).
- Keep prospect docs **markdown-only** in v1; no new Python package required for Phases 1–2.
- Optional Hub/sorter wiring is **Phase 3+ only** and must be config-additive (append routes / launcher items) without changing existing targets’ behavior.
- Keep any future helper modules **under ~500 lines** and inside `Prospect-Businesses/` (or a thin dedicated helper later) — never fuse into `inc_launcher` core or strategy collectors.

##### Modular boundaries (what may change where)

| Area | Phase touch? | Rule |
|------|--------------|------|
| `Prospect-Businesses/` (new) | 1–2 | Own README + prospect `.md` files only |
| `Started-Businesses/` | **Never without user OK** | Read-only for agents; graduation = user-approved copy/move only |
| `agent-business-idea-runs/` | None (v1) | Leave outputs as history; prospects **link** to dated idea files |
| `business_research/` | None (v1) | Leave deep plans in place; optional pointer links from a prospect file |
| `inc_launcher/launcher_config.json` | Phase 3 optional | Additive card/path only; no pillar renumber; no change to Established targets |
| `business_bookmark_sorter/config/routes.json` | Phase 3 optional | Additive destination only; do not retarget existing routes |
| Strategy folders / `run_all_strategies.py` / agent prompt | **Out of scope** | Formulation pipeline unchanged |

##### Phases

**Phase 0 — Layout lock (this section)** ✅ (user 2026-07-12: approve + proceed)
- [x] User approves folder name `Prospect-Businesses/` at repo root
- [x] User confirms graduation rule (user-only approver)
- [x] User confirms shortlist cap (~5–10) and “no bulk import”

**Phase 1 — Folder scaffold only (safe / isolated)** ✅ (2026-07-12)
- [x] **1.1** Create `Prospect-Businesses/` + `README.md` (purpose, cap, graduation rule, link pattern to `business_ideas_YYYYMMDD.md`)
- [x] **1.2** Add `TEMPLATE.md` for one-prospect files — empty template only
- [x] **1.3** Smoke: folder exists; README readable; **zero** changes outside this folder (+ `task.md` status only)
- [x] **1.4** Do **not** seed real prospects yet (unless user names them in the same approval) — **no seeds this pass**

**Phase 2 — Curated seed (user-picked only)** ✅ (2026-07-12 — menu **1**)
- [x] **2.1** User named: ExamFee Planner, AgentDispute AI, SCIMLite NG (from `business_ideas_20260712.md`)
- [x] **2.2** Created `examfee-planner.md`, `agentdispute-ai.md`, `scimlite-ng.md` — each `status: prospect` + source-run link
- [x] **2.3** Optional research pointers — none (no matching `business_research/` moves; left blank)
- [x] **2.4** Smoke: count **3** ≤ cap; each file has graduation disclaimer; `Started-Businesses/` unchanged

**Phase 3 — Optional surfaces (additive; separate approval)**
- [ ] **3.1** Hub/tray: optional Formulated-ideas card/path open `Prospect-Businesses/` (config append only)
- [ ] **3.2** Bookmark sorter: optional route destination `Prospect-Businesses/` (append to `routes.json` only)
- [ ] **3.3** Smoke: existing Hub cards and sorter destinations still resolve; no regression on Established / Formulated cards

**Phase 4 — Graduation protocol (docs only unless user asks for tooling)**
- [x] **4.1** Documented in `Prospect-Businesses/README.md`: graduation checklist (user says “graduate X” → only then create/update under `Started-Businesses/`)
- [x] **4.2** Explicit: agents propose graduation in chat/menu; **never** execute without user number/phrase approval
- [x] **4.3** Out of Phase 4 unless separately approved: any script that copies files into `Started-Businesses/`

##### Layout checklist (maps to phases)

- [x] Phase 1: create folder + README + template
- [x] Phase 2: seed only user-named prospects (3 files)
- [ ] Phase 3: optional Hub/sorter wiring (additive)
- [x] Phase 4: graduation protocol documented; user remains sole approver

##### Out of scope (v1)

- Auto-promotion / auto-graduation scripts
- Moving all formulation history or `business_research/` into prospects
- Replacing or rewriting `Started-Businesses/software-development.md`
- Changing agent formulation prompt, strategy scripts, or `run_all_strategies.py`
- Making Prospects a 5th Hub pillar (keep under Formulated shortlist unless user later opens a pillar task)

**v1 definition of done:** `Prospect-Businesses/` exists with README + template; ≤10 user-named prospect files; graduation rule documented; no automatic writes to `Started-Businesses/`; no regressions in launcher/sorter/strategy pipelines from Phase 3 (if Phase 3 was skipped, still done after Phase 2).

**Related:** Inc Hub four pillars (this §); Business Bookmark Sorting destinations; agent formulation outputs under `agent-business-idea-runs/outputs/`.

#### Layout (proposed — approve before creating files)
**Recommendation:** New folder `inc_launcher/` at repo root (`C:\dev\Inc\inc_launcher\`).

| Signal | Why |
|--------|-----|
| Own tray icon process + config | Not part of Problem ID or YouTube |
| `launcher_config.json` for pillars/items | Add 5th pillar later without code churn |
| Windows-only tray icon (Phase 1) | Matches your daily workflow |

**Layout checklist:**
- [x] `inc_launcher/` — tray icon app, config, super main stub (Phase 2)
- [x] `inc_launcher/launcher_config.json` — 4 pillars + child launch targets
- [x] `inc_launcher/README.md` — install/run on Windows
- [x] Keep shared repo tools at root; do not move Strategy folders

#### Phases

**Phase 1 — Tray icon + config (MVP)** ✅
- [x] Windows tray icon (background process; visible near clock)
- [x] Right-click menu: 4 pillars → submenus (open folder, URL, or `python main.py …`)
- [x] `launcher_config.json` drives menu (no hardcoded paths in code)
- [x] Global actions: Open `Inc` in Explorer, Open in Cursor, Open `task.md`, Quit

**Phase 2 — Super main app** ✅
- [x] Left-click tray icon or menu item opens hub window (same 4-pillar nav)
- [x] Launcher grid per pillar (icons/labels from config)
- [x] Optional: show last-opened / pinned items

#### Manual verification (Phase 2 + 4)

Automated sign-off **2026-06-29**: `python -m pytest inc_launcher/tests -q` + `python -m inc_launcher.tests.smoke_hub` + Phase 4 sign-off tests. See `inc_launcher/MANUAL_TEST.md`.

- [x] **Start tray app** — verified via external `auto_launcher` + manual restarts in session
- [x] **Left-click tray icon** — Hub opens (`smoke_hub`)
- [x] **Pillar switch / Pinned** — `smoke_hub` + config tests
- [x] **Run a launcher** — action targets exist (`smoke_hub`)
- [x] **Recently opened** — `smoke_hub` records recent
- [x] **Right-click tray menu** — builds; **Interval nudges**, **Bookmark review** present (session 2026-06-29)
- [x] **Optional: commit Phase 2** — Pushed `c5057d3` on `main` (2026-05-24)
- [x] **Phase 4 live** — nudges ON; `schedule_fired.json` confirms fires (2026-06-29)

**Phase 3 — Scale beyond 4** ✅
- [x] Add pillars via config only — **Automation hub** pillar in `launcher_config.json` (add more without code changes)
- [x] Single-instance lock — second `tray_app.py` exits if one is already running
- [x] Start at login — tray menu **Start at Windows login [ON/OFF]** (writes `Inc Launcher.bat` to Startup folder)
- [x] Custom icon — optional `inc_launcher/assets/icon.png` or `settings.icon_path` in config

**Phase 4 — Interval nudges** ✅ **LIVE** (`schedules.enabled: true` on PC)  
**Problem:** Too many tray icons; Inc Hub is easy to forget. **Not** Windows login — tray already runs; **timer** fires existing menu actions so work surfaces without hunting the notification area.  
**Approved:** 2026-05-30 (user option **1** — starter interval list). **Shipped:** 2026-06-28/29 (`4c54b9c`).

| When | Action (existing tray target) | Config ref |
|------|------------------------------|------------|
| **Daily 09:00** | **Open task.md** | `global_actions` → `.cursor/rules/task.md` |
| **Daily 09:15** | **Open Inc Hub** | Same as left-click / menu default (hub window) |
| **Mon / Wed / Fri 10:00** | **Problem ID tool — live site** | `problem_identification` pillar → live URL |
| **Sunday 18:00** | **YouTube automation (status)** | `established` pillar → `python main.py status` (skip if YouTube ops inactive) |

**Rules (approved):**
- Max **3 nudges per weekday**, **2 on Sunday** (YouTube only that day) — no folder-spam, no **Run all strategies**, no **Open in Cursor** on timers.
- Scheduler lives **inside** `inc_launcher` tray process; reuses `run_action` / hub open — no extra tray icons.
- Optional later: toast + Snooze before opening (not in v1 scope until built).

**Phase 4 tasks:**
- [x] **4.1** Schedule config + `scheduled_nudges.py`
- [x] **4.2** Background timer in `nudge_scheduler.py` + `tray_app.py`
- [x] **4.3** Tray submenu: **Interval nudges [ON/OFF]**
- [x] **4.4** Tests: `test_phase4_signoff.py`, `test_nudge_scheduler.py`, `test_phase4_toggle.py`, `smoke_hub.py`
- [x] **4.5** `inc_launcher/MANUAL_TEST.md`

**Track C (bookmark review — same session):**
- [x] **Formulated ideas → Bookmark review** in `launcher_config.json` (`909c6d9`)
- [x] Tests: `test_track_c_bookmark.py`, `business_bookmark_sorter/tests/test_cli_status.py`

**Boot note:** External-repo `auto_launcher.py` starts tray at login; keep Inc **Start at Windows login [OFF]** to avoid duplicate starts (`single_instance` prevents double tray, but one boot path is clearer). Phase 4 timer runs inside the tray process Layer 1 already started.

**Stack (proposed):** Python + `pystray` + minimal UI (tkinter or lightweight webview for super main) — confirm at Phase 1 kickoff.

---

### 5. Business Bookmark Sorting (Chrome → Inc folders)
**Status:** Phase 0–2b implemented; Phase 3 (de-bookmark) pending — **~1926 pending** / 1942 total in queue (2026-06-29)  
**Goal:** Sort bookmarks from Chrome (`chrome://bookmarks/?q=business` and related trees) into the **correct folders/files inside `C:\dev\Inc`**, not into `business_bookmark_sorter\Business Links.md` (that path is a **temporary inbox only**). After Phase 2b, filing one bookmark should mean: **saved in queue, visible in the right markdown, docx open for eyeball check** — then user may delete from Chrome (Phase 3 still manual until built).  
**Tray entry:** Formulated ideas → **Bookmark review** (`inc_launcher/launcher_config.json` → `bookmark_review`)

#### Problem (what “sorting” means)

| Decision per item | Action |
|-------------------|--------|
| **Belongs in Inc** | Write link (or note) into the right Inc destination (see taxonomy below), then **remove from Chrome bookmarks** (manual preferred; optional automation later if volume is stressful). |
| **Does not belong in Inc** | **Leave in Chrome** (personal, other projects, out of scope). |

**Hard cases:** Some Chrome entries are **folders** (e.g. `Google Go Voice Listen - Business..`) containing more bookmarks — workflow must expand folders, not only flat URLs.

**Source of truth for import:** Chrome profile `Bookmarks` JSON (typical: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks`), not the `chrome://` UI (not automatable as a page).

#### Destination taxonomy (Inc — align with launcher pillars)

| Category | Example Inc destinations |
|----------|---------------------------|
| **Business started** | `Started-Businesses/`, live ops folders (**user-approved graduation only** from prospects) |
| **Prospect businesses** | `Prospect-Businesses/` (**proposed 2026-07-12** — curated shortlist; not started yet) |
| **Formulated ideas** | `Business-Idea-Formulation-Strategy-*/`, `business_research/`, `agent-business-idea-runs/outputs/business_ideas_*.md`, `past_business_ideas.md` |
| **Problem identification** | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/` |
| **My leads** | `abuja_lead_generator/` |
| **Automation / content** | `Strategy-2-Problem-Solving/Content-Automation/` |
| **Stay in Chrome** | No Inc write; bookmark unchanged |
| **Inbox (staging)** | `business_bookmark_sorter/Business Links.md` — import queue only, not final home |

Final link storage format (per-destination `.md` link lists vs `links.json` registry) — **decide in Phase 1**.

#### Existing tools (outside Inc — reuse assessment)

| Tool | Location | Fit |
|------|----------|-----|
| **Batch Link Reviewer** | `...\JavaScript Programming - Learning et al\` — Chrome extension + `scripts/links-cli.js` | **Strong UX** (Open Next / Reviewed / Skip / Delete / Pause banner). Built for JS learning links; needs Inc categories + Chrome business import. |
| **Saved Links Organizer** | `...\Digi\saved_links_organizer\` — `organizer/chrome_bookmarks.py`, `import_chrome` | **Strong import** of Chrome `Bookmarks` JSON; different product (Reddit queue). Borrow parser/import patterns. |

#### Layout (proposed — approve before creating files)

**Recommendation:** Use `business_bookmark_sorter/` at repo root; keep inbox at `business_bookmark_sorter/Business Links.md`.

| Signal | Why |
|--------|-----|
| Chrome import + review queue + routing rules | Own module, not `inc_launcher` |
| May reuse extension pattern from Batch Link Reviewer | Separate `chrome/` subfolder or fork |
| Staging inbox stays in sorter folder | Simpler references and one-tool ownership |

**Layout checklist:**
- [x] `business_bookmark_sorter/` — CLI, config (`routes.json`), queue (`data/queue.json`)
- [x] `business_bookmark_sorter/Business Links.md` — inbox only
- [ ] Optional: thin Chrome extension + local server (Batch Link Reviewer pattern)
- [x] Long-term store = per-destination `links.md` (Phase 2), not `Business Links.md` alone

#### Phases

**Phase 0 — Discovery** ✅
- [x] Export/count business bookmarks from Chrome `Bookmarks` JSON (`python -m business_bookmark_sorter discover`)
- [x] Route taxonomy in `business_bookmark_sorter/config/routes.json` (edit as needed)
- [x] Batch Link Reviewer path noted in `data/discover_report.json` for Phase 2 reuse

**Phase 1 — Import + queue (MVP)** ✅
- [x] Import business tree + inbox into `data/queue.json` (`python -m business_bookmark_sorter import`)
- [x] CLI: `status`, `list`, `next` (`--open` opens URL)
- [x] Suggested destination per item (`keyword_rules` in config)

**Phase 2 — Review UI (minimal manual work)** ✅
- [x] Tkinter review panel (`python -m business_bookmark_sorter review`) — Mark Filed / Skip / Stay in Chrome / Open URL
- [x] JSON-first: `queue.json` is source of truth; markdown via **Export Filed to Markdown** (`export-md`)
- [x] Mark Filed success/error toast (top-right banner)
- [x] Audit log: `data/actions.log`
- [x] Startup sync from current Chrome before first item is shown
- [x] Post-action sync after Mark Filed/Skip/Stay + `Refresh now` button
- [x] Missing pending links auto-mark `gone_from_chrome` (prevents stale first item)

**Phase 2b — One-click “File & open doc”** ✅  
*Replaces separate Mark Filed + Export flow in the UI. CLI `export-md` stays for recovery.*

**User requirement (single button):**
1. User picks destination → clicks one button (rename from **Mark Filed** → e.g. **File & open doc**).
2. On success, in order: update `queue.json` (`status: filed`, `filed_destination`, `filed_at`) → export that item’s destination to the correct `links.md` (per `config/routes.json`) → regenerate paired `.docx` from that `.md` → open the `.docx` in Word/default app.
3. Remove standalone **Export Filed to Markdown** button from review UI once 2b is stable (keep CLI / hidden recovery path).
4. User expectation: after success toast + doc open, they can **confidently delete the Chrome bookmark** (still manual until Phase 3; no auto-delete in 2b).

**Risks & mitigations (must implement, not optional):**

| Risk | Mitigation |
|------|------------|
| Export fails after mark → user deletes bookmark and loses link | **Atomic flow:** if export or docx step fails, show **red toast**, do **not** advance to next item; keep item `filed` only if export succeeded, or roll back to `pending` (pick one policy in code and document in README). |
| Force-closing Word loses unsaved edits | **Prefer:** save + polite close via COM; if file locked, **abort** with clear message — do not claim “safe to delete.” Never silent `taskkill` on `WINWORD.EXE`. |
| OneDrive/sync locks `.md` / `.docx` | Catch write errors; retry once with short delay; surface path in error toast. |
| Full rebuild of all destinations on every click (slow with ~2k filed) | **Destination-scoped export** on each action (rewrite only that destination’s `links.md` + optional summary). Full rebuild only via CLI `export-md` or Shift+recovery. |
| Wrong doc opened | Open **only** the `links_file` for the chosen destination (e.g. `abuja_lead_generator/links.docx`), not every destination. For `inbox`, use `business_bookmark_sorter/Business Links.md` (+ its docx). |
| `queue.json` vs markdown drift | Keep **`queue.json` source of truth**; set `exported_at` (and optionally `exported_path`) on item when export succeeds. |
| DOCX pipeline missing today | New module (e.g. `docx_export.py`); pick tool at kickoff: **Pandoc** (preferred if installed) or **Word COM** on Windows (close/reopen only when needed). |

**Recommendations (include in build):**
- [x] Config flag `auto_export_on_mark` / `open_docx_on_mark` in `config/routes.json` → `review`
- [x] Toast copy: destination label + md/docx names or failure reason
- [x] **Recovery:** Shift+click **File & open doc** = full re-export; CLI `export-md` retained
- [ ] Optional: append-only fast path later; **v1 = rewrite destination file** for consistency
- [ ] Manual verification: file one link → see it in opened docx → delete bookmark in Chrome → confirm removal dialog → next link
- [x] Post-file dialog: “Have you removed bookmark from Chrome?” — Yes = next; No = stay + **Bookmark removed — next** button

**Phase 2b tasks:**
- [x] **2b.1** `export_markdown.py`: `export_destination(dest_id, queue)` — single-destination rewrite; keep `export_filed_to_markdown()` for full rebuild.
- [x] **2b.2** `review_actions.py`: `revert_filed`, `mark_exported` (`exported_at` / `exported_path`).
- [x] **2b.3** `docx_export.py` + `file_workflow.py`: md → docx (Pandoc or Word COM); polite close if open; rollback pending on export fail.
- [x] **2b.4** `review_ui.py`: **File & open doc**; Export button removed; Shift+click = full re-export; no advance on failure.
- [x] **2b.5** Tests: `test_file_workflow.py`; inbox fixture in `test_import.py`.
- [x] **2b.6** README + `config/routes.json` `review` settings.

**Layout:** No new folder; modules stay under `business_bookmark_sorter/` (new `docx_export.py`, keep files under ~500 lines).

**Phase 2c — Single master doc + Other category** ✅
- [x] **One export target:** `business_bookmark_sorter/Business Links.md` (+ one `.docx` opened every time)
- [x] **Sections** inside master doc = dropdown categories (`## Leads`, `## Other`, …)
- [x] **Other** in dropdown; auto-suggest **Other** when no keyword match (not forced into a pillar)
- [x] User may deliberately pick **Other** even when a keyword match exists
- [x] Legacy `inbox` filings export under **## Other**; `inbox` hidden from dropdown (`assignable: false`)
- [x] Per-folder `links.md` files no longer written on file/export

**Phase 3 — De-bookmark (optional / on demand)**
- [ ] After Inc filing: mark for Chrome removal; **manual** checklist export first
- [ ] Optional automation: update Chrome `Bookmarks` JSON (backup first; Chrome closed) or extension delete API
- [ ] Never delete from Chrome without explicit user action or setting

**Phase 4 — Inc launcher integration (optional)**
- [x] Add **Business bookmark sorter** item under Formulated ideas in `inc_launcher/launcher_config.json` (Track C menu only — `bookmark_review` → `python -m business_bookmark_sorter review`; no schedule yet)

#### Manual verification (after build)

- [ ] Import produces expected count vs Chrome business folder
- [ ] One link filed to `Started-Businesses/` (or chosen folder) and visible in repo
- [ ] **Phase 2b:** File one item → docx opens with new line → delete Chrome bookmark → link still in docx/queue
- [ ] “Stay in Chrome” leaves bookmark untouched
- [ ] De-bookmark step (if enabled) removes only confirmed URLs; backup restores if mistake

#### Out of scope (unless added later)

- Syncing with Google account cloud bookmarks beyond local profile file
- Auto-classifying without user confirm (beyond suggestions)
- Sorting non-business Chrome collections

**Run (from `C:\dev\Inc`):** `import` → `python -m business_bookmark_sorter review` — see `business_bookmark_sorter/README.md`  
**After Phase 2b:** one button in review UI; `python -m business_bookmark_sorter export-md` only for full re-export / repair.

---

### 6. Abuja PropTech B2B — Verify-Ops (Phase 1)
**Status:** Research complete (B2B pivot) — **implementation not started**  
**Goal:** **B2B verify-ops infrastructure** for FCT intermediaries — agents, Kuje/Lugbe developers, law firms submit plots via partner portal; you orchestrate AGIS + lawyer/surveyor → **48h white-label PDF** (**₦35k–₦50k**/report wholesale). **End-buyers are their clients, not yours.**  
**Folder:** `Abuja-Real-Estate-Research/` (research); build TBD under `abuja_land_verify/` or similar when kickoff  
**Spec:** [abuja-real-estate-profitable-sub-niches.md](../Abuja-Real-Estate-Research/abuja-real-estate-profitable-sub-niches.md) §3.10 · §6  
**GTM:** `abuja_lead_generator/` → **paying B2B accounts** (agents + developers), not diaspora retail  
**Later phases (defer):** broker comps dashboard (Phase 2), white-label PM module (Phase 3), `titletrail.ng` escrow (Phase Later); NLRDTP/AGIS API as partnership narrative only — not v1 product

#### Phase 1 — B2B verify-ops portal (target: first **paying partner account** by **Day 21** from kickoff)

**Week 1 — Partners, portal & contracts**
- [ ] Sign MOU with **1 FCT property lawyer** + **1 licensed surveyor** (per-report fees or rev share)
- [ ] CAC registration — **B2B PropTech / verification ops** (not brokerage; not consumer-facing brand)
- [ ] Partner portal MVP: login, case submit (district, plot #, file #, uploads), case status
- [ ] White-label PDF report template (Proceed / Conditions / Do not proceed) + partner branding option
- [ ] B2B pricing sheet: **₦35k–₦50k**/report wholesale; 10-report pack discount
- [ ] Partner agreement: wholesale terms, white-label rights, SLA, liability disclaimer

**Week 2 — Pilot partners (not end-users)**
- [ ] Onboard **2 pilot B2B partners** (1 agent + 1 Kuje/Lugbe developer) — **free** pilot cases for testimonial
- [ ] T&Cs: not legal advice; 48h SLA; AGIS human-in-the-loop; no implied govt endorsement
- [ ] NDPA: minimal PII; delete uploads after 12 months unless partner opts in

**Week 3–4 — Paid B2B GTM**
- [ ] `abuja_lead_generator`: outreach → Abuja agents + Kuje/Lugbe developers as **subscription/wholesale customers**
- [ ] **Target:** 3 paying partner accounts + 10 wholesale reports in 30 days
- [ ] **Explicitly out:** B2C Paystack checkout, diaspora WhatsApp/Facebook campaigns, retail ₦75k pricing

**v1 corridors only:** Kuje, Lugbe, Lokogoma, outer Gwarinpa estates

#### 90-day success metrics
- [ ] ≥5 active B2B partner accounts
- [ ] ≥25 wholesale reports completed
- [ ] Avg turnaround ≤48h
- [ ] ≥2 anchor partners (agent or dev) each doing ≥3 reports/month
- [ ] Partner churn <20% in first 90 days

#### Out of scope (v1)
- B2C verify concierge / end-user sales
- AGIS API / NLRDTP product integration
- Escrow or holding funds for land purchase
- Nationwide coverage; broker comps (Phase 2); white-label PM (Phase 3)

**Budget:** ₦500k–₦1.5M (CAC, domain, portal build, ops float, subsidized pilot cases)

---

### 7. Post-Wedding Comms Pack (Wedding — B2C digital)
**Status:** P1 Paystack complete — **Phase 0b not started**; manual UI deferred to v1 sign-off  
**Goal:** WhatsApp-first **post-wedding comms** for couples — AI-drafted guest thank-yous (gift/spray-aware), vendor wrap-up, checklist — **one-time B2C fee**; no MC/planner SaaS.  
**Folder:** `Strategy-2-Problem-Solving/post-wedding-comms-pack/` — run: `python -m streamlit run app.py` from that folder  
**Spec:** [post-wedding-comms-pack.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack.md) · [README](../Strategy-2-Problem-Solving/post-wedding-comms-pack/README.md) · [LAUNCH_PLAN.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/LAUNCH_PLAN.md) · [MANUAL_TEST.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/MANUAL_TEST.md)  
**Related (defer):** [wedding-games-icebreakers-app.md](../Strategy-2-Problem-Solving/wedding-games-icebreakers-app.md) — guest link feeds comms import in Phase 3 (P2)

> **Phased plan:** Already defined in spec + folder README (P0/P1/P2). This section mirrors that in `task.md` for execution tracking — **not a duplicate doc**; tick here as you ship.

#### v1 definition of done (locked)

| Milestone | Includes | Manual UI (`MANUAL_TEST.md`) | Ship meaning |
|-----------|----------|------------------------------|--------------|
| **v0.5 — P0 code** | Phase 0 ✅ + Phase 1 (P0) ✅ + `test_p0_flow.py` green | **Do not run** | Agent-only; not user-facing launch |
| **v1.0 — soft launch** | v0.5 + **Phase 0b go** (≥2 couples WTP **₦10k flat** self-serve) | **P0 + P1 sections** | Paystack ₦10,000 unlock live |
| **v1 — launch-ready** | v1.0 + hosted deploy + manual test pass | Same | Public URL, same **₦10k flat** |
| **v1.x optional** | P1 WhatsApp Business API auto-send | Extra rows in MANUAL_TEST §P1 | Only if copy-export insufficient after v1 |

**WhatsApp API:** **Not required for v1.** v1 ships with copy-export + Paystack; API is v1.x if couples demand in-app send.

**Order of gates:** P0 code → Phase 0b (before P1 **launch**, may overlap P1 **build**) → P1 code → single `MANUAL_TEST.md` pass → stage/commit/deploy.

**Agent during build:** automated tests only (see `deferred-manual-testing.mdc`). **User once:** manual pass at **v1.0** (P0 only) or **v1** (P0+P1) — whichever milestone you declare complete.

#### Layout (locked — no new folder)
- [x] `post-wedding-comms-pack.md` — strategy one-pager
- [x] `post-wedding-comms-pack/` — MVP code (`app.py`, `README.md`, `requirements.txt`, `MANUAL_TEST.md`)
- [ ] Optional later: `post-wedding-comms-pack_tasks.md` only if P0 checklist outgrows this entry

#### Phase 0 — Strategy & repo ✅
- [x] Reposition from email thank-you generator → Post-Wedding Comms Pack (WhatsApp-first, vendor module)
- [x] Rename `automated-thank-you-note-generator` → `post-wedding-comms-pack` (md + folder + cross-links)
- [x] P0 Streamlit MVP (modular `app.py` + helpers)

#### Phase 0b — Validation (before P1 **launch**; target: **3 Wizard-of-Oz couples**)
- [x] Landing / pitch copy draft — [`PHASE_0b_PITCH.md`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/PHASE_0b_PITCH.md)
- [x] Launch playbook (marketing, timeline, credibility) — [`LAUNCH_PLAN.md`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/LAUNCH_PLAN.md)
- [ ] Publish landing (Carrd / Notion / Google Site) from pitch doc
- [ ] Wizard-of-Oz (optional): CSV → you generate → deliver; **₦15k** done-for-you OR test **₦10k** self-serve Paystack
- [ ] **Go/no-go:** ≥2 couples WTP **₦10,000 flat** self-serve; kill if “in-person only” + zero WTP
- [ ] **Do not launch P1 (Paystack)** to public until 0b passes

#### Phase 1 (P0) — Nigeria-usable MVP ✅
- [x] Replace `text-davinci-003` with Chat Completions API
- [x] CSV schema: `Name`, `Phone`, `GiftOrSpray`, `Relationship`, `Email` (optional)
- [x] Prompt templates with gift/relationship context
- [x] “Copy to WhatsApp” batch export (no API cost)
- [x] Vendor list + templates (thank-you, review request)
- [x] Checklist UI: pending / sent / skipped
- [x] Automated smoke test: `test_p0_flow.py`

#### Phase 2 (P1) — Monetization (required for **v1**, not v1.0) ✅
- [x] Paystack one-time unlock per wedding
- [x] Paystack webhook + basic auth (`webhook_server.py`)
- [ ] (Optional v1.x) WhatsApp Business API or local BSP integration

#### Phase 3 (P2) — Stack integration (post-v1)
- [ ] Import from guest engagement export (`wedding-games-icebreakers-app.md` product)
- [ ] Printable PDF export (print-shop affiliate)
- [ ] English + Yoruba/Igbo/Hausa/Pidgin template picker

#### v1 sign-off checklist (user — once)
- [ ] **v1.0:** Phase 0b go + run `MANUAL_TEST.md` §P0 → soft launch OK
- [ ] **v1:** P1 complete + run `MANUAL_TEST.md` §P0+P1 → launch-ready OK

#### Out of scope (v1)
- MC or planner subscription / white-label
- Native iOS/Android app store app
- Full wedding planning suite
- Physical print ops (affiliate export only)

**Priority note:** Ship **post-event comms (this project)** before guest engagement link code.

> **Manual UI testing:** Deferred — see [MANUAL_TEST.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/MANUAL_TEST.md) and `.cursor/rules/deferred-manual-testing.mdc`.

---

### 8. Google Drive Business Sorting (Drive → Inc folders)
**Status:** Planning — **implementation not started**  
**Goal:** Sort items from Google Drive `?q=business` (and related trees) into the **correct Inc destinations** under the **four launcher pillars**, without exposing private Drive content in chat or commits. Drive is a second inbox (like Chrome bookmarks); Inc is the filing cabinet.

#### Problem (what “sorting” means)

| Decision per item | Action |
|-------------------|--------|
| **Belongs in Inc** | File into the right folder/markdown (see taxonomy); optional local mirror under `Google Drive Business Files/` |
| **Already in Inc** | Mark **synced** — no duplicate write |
| **Does not belong in Inc** | Leave in Drive only |

**Privacy (non-negotiable):**
- No Drive API login or cloud sync from the agent unless you explicitly approve a later phase
- No Google Doc IDs, ChatGPT chat URLs, or personal network notes in repo outputs or chat pastebacks
- Work from **user-exported** mirrors (e.g. `Google Drive Business Files/`) or a file list you provide

#### Known mapping (12 local prompt cards → Inc strategies)

| Drive step (SaaS / Business) | Inc strategy / folder |
|------------------------------|------------------------|
| SaaS 1st — Network | Strategy **3** — `Business-Idea-Formulation-Strategy-3-*` |
| SaaS 2nd — Questionnaire | Strategy **4** |
| SaaS 3rd — Nigerian news | Strategy **5** |
| SaaS 4th — Startup niches (was Crunchbase; now **StartupList Africa** primary, Crunchbase optional legacy) | Strategy **6** |
| SaaS 5th — Trending adaptation (was Crunchbase Trending Profiles; now **Product Hunt / Techpoint** primary, Crunchbase screenshot optional legacy) | Strategy **7** |
| SaaS 6th — TrendHunter | Strategy **8** (retired) → use Strategy **14** |
| SaaS 7th — Nairametrics et al | Strategy **9** |
| SaaS 8th — ChatGPT Vision | Strategy **10** (retired) → use Strategies **3**, **4**, or **5** |
| SaaS 9th — Personal problems | Strategy **11** |
| Business 10th — GUEMF | Strategy **12** |
| Business 11th — Multi-pronged / SimilarWeb | Strategy **13** |
| Business 12th — OurWorldInData | Strategy **14** |
| *(not in Drive export)* | Strategy **15** — Inc-only (Nigeria open data) |

**Gaps to close:** anything in Drive `business` search **beyond** the 12 mirrored cards; macros, Forms templates, screenshots, and threads not yet exported locally.

#### Destination taxonomy (align with bookmark sorter + launcher pillars)

| Pillar | Inc destinations |
|--------|------------------|
| **Established** | `Started-Businesses/`, live ops folders (**user-approved graduation only** from prospects) |
| **Prospect businesses** | `Prospect-Businesses/` (**proposed 2026-07-12** — curated shortlist) |
| **Formulated ideas** | `Business-Idea-Formulation-Strategy-*/`, `business_research/`, `agent-business-idea-runs/outputs/business_ideas_*.md`, `past_business_ideas.md` |
| **Problem identification** | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/` |
| **My leads** | `abuja_lead_generator/` |
| **Automation / content** | `Strategy-2-Problem-Solving/Content-Automation/` |
| **Staging** | `Google Drive Business Files/` — mirror/inbox only, not final home |

#### Layout (proposed — approve before creating files)

**Recommendation:** Extend `business_bookmark_sorter/` patterns **or** new folder `google_drive_business_sorter/` at repo root if Drive-specific logic grows (inventory diff, export manifest, pillar routing). Reuse `config/routes.json` taxonomy where possible.

#### Phases

**Phase 0 — Discovery (read-only)** ✅ *partial — chat analysis 2026-06-16*
- [x] Map 12 local `Google Drive Business Files/` cards to Strategies 3–14
- [ ] User provides Drive `business` file list export (titles only — no private links in repo)
- [ ] Diff export vs local mirror vs Inc strategy folders; produce gap report

**Phase 1 — Inventory + routing rules**
- [ ] `routes` or manifest: Drive title patterns → Inc destination (reuse bookmark sorter pillars)
- [ ] CLI: `discover` / `status` / `list` for mirrored + inventoried items
- [ ] Mark items: `synced` | `inc_only` | `drive_only` | `needs_review`

**Phase 2 — Review UI (minimal manual work)**
- [ ] Tkinter or markdown checklist: confirm destination per item
- [ ] On file: write pointer line to correct `links.md` or master `Business Links.md` section (no raw Doc URLs in committed files unless you opt in)

**Phase 3 — Inc launcher integration (optional)**
- [ ] Add **Google Drive business sorter** under **Formulated ideas** in `inc_launcher/launcher_config.json`

#### Out of scope (v1)
- Automated Google Drive API sync
- Auto-delete or move files in Drive
- Committing private Doc/chat URLs

**Related:** Business Bookmark Sorting (task §5) — same pillar taxonomy, different source inbox.

---

### 9. Cybersecurity Vertical — Nigerian News (Strategies 5 + 9)
**Status:** Planning — **implementation not started**  
**Goal:** Derive **cybersecurity solution ideas** from Nigerian news and financial press using existing formulation pipelines — **not** physical security, insurgency, or generic “national security” headlines.

#### Scope (in)

| Signal type | Examples already in Inc captures |
|-------------|----------------------------------|
| Payment / fintech cyber risk | “digital payment boom faces rising cybersecurity threats” |
| Fraud / scams | EFCC cases, celebrity endorsement fraud, deepfake ad scams |
| Compliance | NDPR / NDPA friction in digital products |
| Enterprise / data | Breach-adjacent, AML/fraud tooling, trade-data cybersecurity |

#### Scope (out)

- Route-risk / Borno / Amotekun / communal violence (separate civic-security track if needed)
- New Strategy **16** unless cyber-only volume justifies its own playbook folder

#### Approach (recommended)

Treat cybersecurity as a **vertical filter** on **Strategy 5** (general Nigerian news) + **Strategy 9** (Nairametrics, Financial Nigeria, BusinessDay) — not a replacement strategy.

**Flow:** News extract (S5/S9) → keyword/sector tag → Prompt 1b tabulation → optional **Strategy 12** GUEMF score → ranked cyber backlog markdown.

**Privacy:** Same as Strategy 5 alignment — `Proposed domain (not verified)`; no mandatory source article URLs in committed idea tables.

#### Phases

**Phase 0 — Backlog from existing outputs (read-only)**
- [ ] Grep/collect cyber-adjacent rows from `business_ideas_*.md`, `news_problems_*.json`, `past_business_ideas.md`
- [ ] Single ranked list: `business_research/cybersecurity_ideas_backlog.md` (or Strategy 5 subfolder)

**Phase 1 — Filter config**
- [ ] `cyber_keywords.json` or config block in Strategy 5/9: cyber, fraud, phishing, ransomware, deepfake, NDPR, NDPA, breach, AML, identity, PSP, etc.
- [ ] Exclude patterns: physical security, Amotekun, kidnapping (unless explicitly cyber-enabled fraud angle)

**Phase 2 — CLI / script hook**
- [ ] `--sector cyber` or post-process command on latest `news_problems_*.json`
- [ ] Output: `cyber_news_problems_YYYYMMDD.json` + Prompt 1a payload scoped to cyber headlines only

**Phase 3 — Optional GUEMF pass**
- [ ] Pipe Phase 2 output through Strategy **12** for high-value problem scoring

**Phase 4 — Launcher (optional)**
- [ ] Shortcut under **Formulated ideas**: “Run cyber news slice (S5+S9)”

#### v1 definition of done

- [ ] One automated pass produces a cyber-filtered artifact from existing Strategy 5/9 machinery
- [ ] Backlog markdown with ≥10 ranked ideas traced to “With the mention of” headlines (domains TBD)
- [ ] No new privacy regressions (no forced article URLs in repo)

#### Out of scope (v1)

- Building a cyber product MVP
- Licensed threat-intel API integrations
- Scraping paywalled security vendor blogs

**Folders (when approved):** extend `Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction/` and/or `Business-Idea-Formulation-Strategy-9-*`; backlog under `business_research/`.

---

### 10. Strategy 1 — Business Variation (verbal → technical) (NEW — Jul 2026)
**Status:** Phase **6 complete** (2026-07-12) — v1 regression green; single manual pass via `MANUAL_TEST.md` when you choose  
**One-liner:** Turn `Strategy-1-Business-Variation/` playbook into a runnable formulation strategy (script + `run_all_strategies.py` + agent infra), keep gadget ops separate, additive/modular so nothing else breaks.  
**Full phased backlog:** see **§9** under Notes / formulation tasks below (`### 9. Strategy 1 — Business Variation…`).  
**Next:** Optional — run `MANUAL_TEST.md` once, then stage/commit/push.


---

## 📋 General Maintenance Tasks

- [ ] Set up Git version control for Problem Identification Tool
- [ ] Create user manual for Problem Identification Tool
- [ ] Write troubleshooting guide
- [ ] Document API integrations
- [ ] Regular code reviews and optimization

---

## 💼 Business & Entrepreneurship Tasks

### Nigeria Business Startup Research
- [x] **Research Startup Capital Requirements** ✅ *Guide created: `business_research/nigeria_startup_costs_guide.md`*
  - [x] Research minimum capital requirements for different business types in Nigeria
  - [x] Identify profitable business opportunities in Nigeria
  - [x] Calculate startup costs breakdown (registration, licensing, inventory, etc.)
  - [x] Research working capital needs for first 3-6 months
  - [x] Identify funding options (personal savings, loans, investors, grants)
  - [ ] Create business plan template
  - [x] Research market entry strategies
- [x] **Data-Driven Business Profitability Analysis** ✅ *Analysis created: `business_research/most_profitable_business_analysis.md`*
  - [x] Analyze profit margins and ROI data for top business ideas
  - [x] Rank businesses by objective metrics (profit margin, ROI, market demand)
  - [x] Provide recommendations based on available capital
  - [x] Compare risk levels and scalability factors

### Business Planning
- [ ] Create business model canvas for potential ventures
- [ ] Research competitive landscape for chosen business
- [ ] Develop marketing and customer acquisition strategies
- [ ] Plan financial projections and break-even analysis

### Power Solutions Platform (NEW)
- [x] **Power Solutions Platform Business Plan** ✅ *Plan created: `business_research/power_solutions_platform_business_plan.md`*
  - [x] Market analysis for national grid failure solutions
  - [x] Multiple business model options (marketplace, tracking, optimization, sharing)
  - [x] Financial projections and revenue models
  - [x] Technical requirements and development roadmap
  - [ ] Validate idea with potential users (20-50 interviews)
  - [ ] Create wireframes/mockups for MVP
  - [ ] Research competitors and market gaps
  - [ ] Identify key suppliers and partners
  - [ ] Secure funding (₦2M - ₦5M for MVP)

### BuyPower Alternative Platform (NEW)
- [x] **BuyPower Alternative Development Plan** ✅ *Plan created: `business_research/buypower_alternative_plan.md`*
  - [x] Research BuyPower features and services
  - [x] Create step-by-step development roadmap
  - [x] Define competitive advantages and USPs
  - [x] Outline business model and pricing strategy
  - [x] **Competitive Analysis** ✅ *Added: 8 competitors analyzed with market shares*
  - [x] **Cost Breakdown** ✅ *Added: AI-assisted vs Standard development comparison*
  - [x] **Development Approach Analysis** ✅ *Added: AI vs Standard vs Hybrid strategy*
  - [ ] **STEP 1 (Current):** Research Nigerian DISCOs and integration methods
  - [ ] Research competitor pricing and fees
  - [ ] Identify target customer segments
  - [ ] Research payment gateway options
  - [ ] Understand regulatory requirements
  - [ ] Create user personas
  - [ ] Define MVP features list
  - [ ] **DECISION NEEDED:** Choose development approach (AI-assisted, Standard, or Hybrid)

### Micro-Data & Utility Services Platform (NEW - ACTIVE)
- [x] **Phase 1 Implementation Plan** ✅ *Plan created: `business_research/micro_data_utility_platform_phase1.md`*
- [x] **Phase 1 Task File** ✅ *Tasks created: `business_research/micro_data_utility_platform_phase1_tasks.md`*
- [ ] **Phase 1.1:** Account Setup & Prerequisites (Twilio, Paystack, VTpass, MongoDB, Hosting)
- [ ] **Phase 1.2:** Project Setup (Node.js, dependencies, environment)
- [ ] **Phase 1.3:** Core Bot Structure (WhatsApp webhook, menu system)
- [ ] **Phase 1.4:** Database Setup (MongoDB schema, user/transaction models)
- [ ] **Phase 1.5:** VTU Integration (Airtime/Data APIs)
- [ ] **Phase 1.6:** Bill Payment Integration (Electricity, Cable TV)
- [ ] **Phase 1.7:** Payment Integration (Paystack)
- [ ] **Phase 1.8:** User Features (Balance, history, validation)
- [ ] **Phase 1.9:** Testing (All flows, error handling)
- [ ] **Phase 1.10:** Deployment & Launch (Production, beta testers)
- [ ] **Phase 1.11:** Marketing & Growth (Social media, referrals)

---

## 🎯 Decision Needed

**Which project should we prioritize next?**

1. **Problem Identification Tool** - Polish UX and add missing features
2. **Music ID Wearable Device** - Start new project from scratch
3. **YouTube Content Automation** - Continue Phase 3 development

---

## 📝 Notes

- Problem Identification Tool is live and collecting data - can be used while improving
- Music ID device requires hardware expertise and significant planning
- All projects should maintain modularity (files under ~500 lines)

---

### 4. Strategy 5 Prompt Label Alignment (NEW)
- [x] **Phase A:** Revert prompt/template sources to `Proposed domain (not verified)` only
  - [x] `news_problem_extractor.py`
  - [x] `chatgpt_prompt_1b.txt`
  - [x] `cursor_copy_block_config.example.json`
  - [x] `cursor_copy_helper_README.md`
  - [x] `business-idea-formulation-strategy-5-news-based-problem-extraction.md`
- [x] **Phase B:** Revert generated/archive `business_ideas_*.md` files to remove `Source article URL (optional)`
  - [x] `business_ideas_20260321.md`
  - [x] `business_ideas_20260303.md`
  - [x] `business_ideas_20260227.md`
  - [x] `business_ideas_20260224.md`
  - [x] `business_ideas_20260226.md`

---

### 5. Strategy 15: Nigeria National / Open Data (Data-First) (NEW)
**Goal:** New formulation strategy: **Nigeria-sourced or Nigeria-filtered official/open statistical data** as the **primary** input (not news headlines). Distinct from Strategy 14 (OurWorldInData global → adapt to Nigeria). Playbook: require **indicator + period + source** per derived problem/idea where possible; document PDFs, irregular releases, and gaps.

#### Phase 1 — Discovery & alignment
- [x] **Phase 1.1 — Discovery (read-only):** Review master runner + Strategy 14 + Strategy 5; record wiring and output alignment (no repo changes beyond this task file).
  - **Master runner** (`run_all_strategies.py`): Executable strategies are `STRATEGY_SCRIPTS` / `STRATEGY_META` keys **3–14** (parallel dicts). Adding **15** requires new entries in **both** dicts pointing at the new folder’s runnable `.py`. **Also** update user-facing copy that hardcodes `3–14` (module docstring, menu text, “Run ALL”, single-strategy prompt range) when wiring — otherwise the menu and “run all” range will omit Strategy 15.
  - **Strategy 14** (`Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation`): Playbook is OWID paste → Prompt 1a → Prompt 1b tabulation; markdown defines the **wide results table** column headers. `global_trend_adapter.py` is an interactive helper with timestamped JSON output, browser/file open helpers, optional `requests`/`beautifulsoup4`.
  - **Strategy 5** (`Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction`): `chatgpt_prompt_1b.txt` aligns with the same **Prompt 1b column philosophy** as Strategy 14, including **Proposed domain (not verified)**. Strategy 15 prompts/output should match that tabulation style; **add provenance** (indicator, period, source — and gap/quality notes as needed) alongside or as lead-in columns/fields per row.
  - **Differentiation:** Strategy 15 **starts from Nigeria** national/official/open statistics; Strategy 14 **starts global** (OWID) then localizes.

- [x] **Phase 1.2 — Finalize before scaffold:** Locked names and provenance layout (no new code files in this phase).
  - **Folder (repo root):** `Business-Idea-Formulation-Strategy-15-Nigeria-National-Open-Data`
  - **Playbook markdown:** `business-idea-formulation-strategy-15-nigeria-national-open-data.md`
  - **Runnable script:** `nigeria_national_open_data.py` (same folder; mirrors `global_trend_adapter.py` pattern for Strategy 14)
  - **Prompts:** `chatgpt_prompt_1a.txt`, `chatgpt_prompt_1b.txt` (same folder)
  - **Provenance vs Prompt 1b:** Use **one table** (same artifact as Strategies 5/14). **Lead columns** (before the existing wide Strategy 5/14 Prompt 1b columns, and before or after `Proposed domain (not verified)` per playbook wording): **Statistical indicator (or metric)**, **Period (as published; e.g. Q1 2024, FY 2023)**, **Source (organization + URL or file name)**. Optional fourth column: **Gaps / limitations** (missing periods, PDF-only extract, revision notes, lag). Each business-idea row must repeat or clearly key to these fields so ideas stay auditable.
  - **API docs:** Skim `API_INTEGRATION_GUIDE.md` / `API_IMPLEMENTATION_SUMMARY.md` only when implementing optional fetches in Phase 3.
  - **Runner preset (for Phase 5):** `STRATEGY_META[15]`: name `Nigeria National / Open Data`; desc `Derives opportunities from Nigeria official and open statistical inputs; each row ties to indicator, period, and source.`

#### Phase 2 — Scaffold (folder + playbook + prompts + minimal `.py`; no `run_all_strategies.py` yet)
- [x] **Phase 2.1 — Playbook only:** Create `Business-Idea-Formulation-Strategy-15-Nigeria-National-Open-Data/` and `business-idea-formulation-strategy-15-nigeria-national-open-data.md` (Nigeria data-first process, provenance lead columns, gap handling, differentiation from 5/14). **No** prompts, **no** `.py`, **no** runner wiring.
- [x] **Phase 2.2 — Prompts + stub script:** Add `chatgpt_prompt_1a.txt`, `chatgpt_prompt_1b.txt` (lead columns + Strategy 5/14 wide columns), `nigeria_national_open_data.py` (stub prints paths, exits 0), plus `README.md` and `requirements.txt` (placeholders for Phase 3+).

#### Phase 3 — Data-first logic
- [x] **Phase 3.1 — Manual input schema + validator + Prompt 1a payload generator:** Validate a local JSON file (`nigeria_inputs.json` or `--inputs <path>`), enforce required provenance fields (indicator/period/source), include gap handling fields, and generate `strategy15_prompt_1a_payload.txt`. No network calls.
- [x] **Phase 3.2 — Optional fetching/parsing (opt-in, non-breaking):** Add `--fetch` support to populate `statistical_content` from explicit `source_url` (HTML/text) and/or `source_file` (local) fields in the inputs JSON, with optional `extract_keywords` snippet extraction and audit-friendly saving (`--save-fetched`). No network calls unless `--fetch` is explicitly set.
- [x] **Phase 3.3 — Automated gap/revision policy:** Added centralized policy in `nigeria_national_open_data.py` to append standardized audit notes for missing periods, PDF/manual extraction, revised series, release lag, and missing excerpts so every row remains auditable.

#### Phase 4 — Output normalization
- [x] **Phase 4.1 — Deterministic normalized scaffold:** Added `output_normalizer.py` and wired `nigeria_national_open_data.py` to generate `strategy15_prompt_1b_normalized_table.md` from validated records. Provenance columns are pre-filled; Strategy 5/14-aligned analysis columns are included as placeholders.
- [x] **Phase 4.2 — Optional response post-processing:** Added markdown-table parser and index-based merger flow. `nigeria_national_open_data.py --prompt1b-response <path>` now ingests Prompt 1b table responses and writes `strategy15_prompt_1b_normalized_table_filled.md` while preserving provenance columns from validated inputs.

#### Phase 5 — Master runner integration
- [x] **Phase 5.1 — Core registration wiring:** Added Strategy **15** entries to `STRATEGY_SCRIPTS` and `STRATEGY_META` in `run_all_strategies.py` pointing to `Business-Idea-Formulation-Strategy-15-Nigeria-National-Open-Data/nigeria_national_open_data.py`.
- [x] **Phase 5.2 — Menu/range copy alignment:** Updated user-facing hardcoded `3–14` strings/ranges in `run_all_strategies.py` (docstring, menu labels, run-all prompt, single-strategy range prompt, example range) to include **15**.

#### Phase 6 — Regression checks
- [x] **Phase 6.1 — Non-runtime safety checks:** Completed static consistency pass (Strategy 15 folder/files present, runner registration + menu/range copy aligned to 3–15, no linter issues on edited files).
- [x] **Phase 6.2 — Local runtime smoke checks (user-run):**
  - [x] `python nigeria_national_open_data.py --help` executed successfully (exit code 0).
  - [x] `python nigeria_national_open_data.py --inputs .\nigeria_inputs.json` executed successfully (exit code 0; expected “inputs file not found” guidance shown).
  - [x] `python run_all_strategies.py` → menu option **3** → Strategy **15** ran successfully.
  - [x] Master runner **menu 2** (selected strategies) and **menu 3** (single strategy) confirmed OK by user.
- [x] **Phase 6.3 — Backward-compatibility spot-check (user-run):** User confirmed menus 2 and 3 behave acceptably; Strategy 15 appears alongside existing strategies in listings.

#### Strategy 15 — Phase A (opt-in browser links)
- [x] **Phase A.1 — Modular browser helper:** Added `Business-Idea-Formulation-Strategy-15-Nigeria-National-Open-Data/browser_links.py` (`collect_source_urls_from_raw_records`, `open_urls_in_browser`, Chrome-or-default on Windows).
- [x] **Phase A.2 — CLI wiring:** Added `--open-links` (default off) to `nigeria_national_open_data.py`; after inputs load successfully, optionally opens deduped http(s) `source_url` values via `browser_links.py`. If no URLs, prints a short message.

#### Strategy 15 — Phase B (portal picker, Strategy 5–style)
- [x] **Phase B — Interactive portal menu:** Added `portal_menu.py` with curated Nigeria official/open entry points; `nigeria_national_open_data.py --portal-menu` runs numbered multi-select + optional browser open (same UX pattern as Strategy 5 news source selection). Runs before the inputs-file check so you can browse portals without `nigeria_inputs.json`.

---

### 6. Retire TrendHunter / Strategy 8 (phased)
**Goal:** Remove TrendHunter from the active automation workflow (no licensed API; manual paste only). Use Strategy 14 (OurWorldInData) for global trend adaptation.

- [x] **Phase 1 — Master runner:** Remove Strategy 8 from `STRATEGY_SCRIPTS` / `STRATEGY_META` in `run_all_strategies.py`; add `RETIRED_STRATEGIES` with clear menu messaging; update `run_all_strategies_README.md`.
- [x] **Phase 2 — Cross-references:** Remove TrendHunter mentions from Strategy 12, API docs, and related READMEs (point to Strategy 14 where relevant).
- [x] **Phase 3 — Strategy 8 folder:** Archive legacy script to `_archive/trend_adapter_legacy.py`; stub `trend_adapter.py`; add `DEPRECATED.md`; deprecate playbook markdown.

---

### 7. Retire ChatGPT Vision / Strategy 10 (phased)
**Goal:** Remove manual ChatGPT Vision image workflow from the active automation pipeline (no in-repo Vision API; manual upload/paste only). Use Strategies 3–5 for construction/real estate problem discovery.

- [x] **Phase 1 — Master runner:** Remove Strategy 10 from `STRATEGY_SCRIPTS` / `STRATEGY_META` in `run_all_strategies.py`; add to `RETIRED_STRATEGIES` with clear menu messaging; update `run_all_strategies_README.md`.
- [x] **Phase 2 — Cross-references:** Remove Strategy 10 from API docs; update Drive mapping in this task file.
- [x] **Phase 3 — Strategy 10 folder:** Archive legacy script to `_archive/visual_content_analyzer_legacy.py`; stub `visual_content_analyzer.py`; add `DEPRECATED.md`; deprecate playbook markdown.

---

### 8. Deprecate Crunchbase as primary source — Strategies 6 & 7 (phased)
**Status:** Tier 1 **implemented** (2026-07-07); Tier 2 **implemented** (2026-07-08) — Tier 3 optional later  
**Goal:** Replace **Crunchbase** as the required data source for **Strategy 6** (niche combination) and **Strategy 7** (trending startup adaptation) with **Africa-first + automatable** alternatives — **without** retiring Strategies 6/7, breaking agent formulation runs, or changing strategy numbers/folder names.

**Context (why now):**
- Agent runs (`prompts/agent_formulation_run.txt`, `agent_strategy_run.py`) already succeed with **agent synthesis** when Crunchbase blocks (login wall; scrape fails).
- Tier 1–2 aligned scripts, agent fetch, and docs with StartupList / Product Hunt; Crunchbase optional legacy only.
- Nigeria-relevant sources: **StartupList Africa** (S6), **Product Hunt / YC / Techpoint RSS** (S7); Crunchbase optional as **manual secondary** for global investor graphs only.

**Non-negotiable safety (do not break anything):**
- **No implementation until this task is explicitly approved** for the target phase.
- **Keep Strategies 6 & 7** in agent run scope (`5, 6, 7, 9, 11–15`); do **not** add to `RETIRED_STRATEGIES`.
- **Backward compatibility:** existing `startup_niche_combiner.py` / `trending_startup_adapter.py` must remain runnable (manual Crunchbase paste path) until replacement fetch is proven; prefer **additive** changes over deletes in Phase 1.
- **Agent runs must keep producing** `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` + `.docx` with S6/S7 trace lines even if new fetch fails (fallback: agent synthesis + RSS already in `agent_strategy_inputs_*.json`).
- **Do not rename** strategy folders (`Business-Idea-Formulation-Strategy-6-*`, `-7-*`).
- **Do not modify** `inc_launcher/`, `run_all_strategies.py` behavior menus, or Strategy 15 in this workstream unless a phase explicitly says so.
- **One phase at a time**; run `pytest` / smoke import checks after each phase; no big-bang refactor.

#### Proposed source mapping (approval target)

| Strategy | Today (Crunchbase) | Proposed primary | Proposed secondary |
|----------|-------------------|------------------|-------------------|
| **6** — Niche combination | Nigeria startups hub paste/scrape | [StartupList Africa](https://www.startuplist.africa/startups) — filter Nigeria + sector | Techpoint RSS (already in `agent_strategy_run.py`) |
| **7** — Trending adaptation | Trending Profiles screenshot + Vision | Product Hunt daily / YC company list + Techpoint Digest | Manual Crunchbase screenshot (optional) |

#### Tier 1 — Must change (behavior / main agent run) — **approve before coding**

- [x] **8.T1.1 — Agent prompt:** Update `prompts/agent_formulation_run.txt` — S6/S7 name new sources; Crunchbase **not** required; agent may use `agent_strategy_inputs_*.json` + synthesis fallback.
- [x] **8.T1.2 — Agent fetch runner:** Extend `agent-business-idea-runs/agent_strategy_run.py` with **optional** fetches (StartupList public page snippet; Product Hunt RSS) — **default behavior unchanged** if fetch fails (log + continue).
- [x] **8.T1.3 — Strategy 6 script (additive):** `startup_niche_combiner.py` — add `collect_startup_directory_content()` for StartupList/manual paste; keep existing Crunchbase path as fallback; `collect_crunchbase_content()` unchanged.
- [x] **8.T1.4 — Strategy 7 script (additive):** `trending_startup_adapter.py` — add text/URL-based trend input (Product Hunt RSS / paste); keep Crunchbase screenshot path as fallback (menu choice 2).

**Tier 1 definition of done:** Agent run + optional `agent_strategy_run.py` produce S6/S7 inputs without Crunchbase; interactive S6/S7 scripts still work via old or new path; zero regressions in Strategies 5, 9, 11–15.

#### Tier 2 — Should change (orchestration & docs truth) — **approve after Tier 1 green**

- [x] **8.T2.1 — Master runner meta:** `run_all_strategies.py` — update `STRATEGY_META` descriptions for 6 & 7 (remove “Crunchbase” as primary; name new sources). *(descriptions only — no menu/script wiring changes)*
- [x] **8.T2.2 — API docs:** `API_INTEGRATION_GUIDE.md`, `API_IMPLEMENTATION_SUMMARY.md` — replace Crunchbase scrape priority with StartupList / Product Hunt / existing RSS; note Crunchbase optional/manual.
- [x] **8.T2.3 — Strategy playbooks:** S6/S7 `README.md` + `business-idea-formulation-strategy-*.md` — new Step 1 URLs and Prompt 1a wording.
- [x] **8.T2.4 — Drive mapping (this file):** Update table at §8 Google Drive — SaaS 4th/5th rows to reference new sources (mirror TrendHunter → Strategy 14 pattern).
- [x] **8.T2.5 — Ritual links:** `Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction/links.md` — note Tue/Thu Crunchbase Google Docs superseded or paired with StartupList/Product Hunt checks.

**Tier 2 definition of done:** No committed doc still claims Crunchbase is **required** for S6/S7; mapping table and API guide aligned with Tier 1 behavior.

#### Tier 3 — Optional / later (out of Tier 1–2 scope)

- [ ] Google Drive `Google Drive Business Files/` mirror renames (user-export archive only).
- [ ] Remove Crunchbase code paths entirely from S6/S7 (only after ≥2 successful agent runs on new sources).
- [ ] Paid StartupList Pro API / Crunchbase API if automation needs exceed free tiers.
- [ ] `inc_launcher` Hub card copy mentioning formulation data sources.

#### Out of scope

- Retiring Strategy **6** or **7** as strategies.
- Paid Crunchbase subscription unless user explicitly approves.
- Scraping behind login walls without user-provided credentials.
- Changes to Strategies 3, 4, 5, 8, 9, 10, 11–15 behavior.

#### v1 approval checkpoint (user)

- [x] User approves **proposed source mapping** table above.
- [x] User approves **Tier 1** scope (8.T1.1–8.T1.4).
- [x] User approves **Tier 2** scope (8.T2.1–8.T2.5) — implemented 2026-07-08.

**Related:** Task §8 Google Drive mapping (SaaS 4th/5th = Strategies 6/7); agent formulation Phase 5 (`agent-business-idea-runs/`); chat analysis 2026-07-07 (MerchantLift + StartupList alternative).

---

### 9. Strategy 1 — Business Variation (verbal → technical / runnable) (NEW — Jul 2026)
**Status:** Phase **6 complete** (2026-07-12) — `test_phase6_regression.py` PASS; v1 automated gate green  
**Goal:** Convert Strategy 1 from a **verbal markdown playbook** into a **functional technical formulation strategy**: CLI script from `strategy-1-business-variation.md` steps, wired into `run_all_strategies.py`, agent formulation infrastructure, and related repo surfaces — **without breaking** existing strategies, agent runs, launcher, or gadget ops.

**User-requested outcomes (must land across phases):**
- Script that operationalizes playbook steps: successful business → complaints → categorize/score → variation ideas → Prompt 1a/1b (optional 1c).
- Strategy 1 becomes **executable** in `run_all_strategies.py` (no longer “verbal instructions only”).
- Strategy 1 included in **agent run** infrastructure (`prompts/agent_formulation_run.txt`, `agent-business-idea-runs/`, fetch/synthesis path).
- Other relevant infra/docs updated so nothing still treats S1 as non-runnable.

**Recommendations captured (must land or be explicitly deferred in a phase):**
- Keep folder `Strategy-1-Business-Variation/` (no forced rename to `Business-Idea-Formulation-Strategy-1-*` in v1).
- **Do not** put formulation logic inside `gadget-business/gadget-business-automation/` (ops stays separate).
- Hybrid v1 intake: editable Nigeria seed businesses + paste/file complaints — **no** paid Brand24 / fragile social scrape required for v1.
- Explicit Prompt 1a differentiation vs **S6** (niche combine) and **S7** (trending adapt): S1 = *Successful Business + Recurring Complaint = Profitable Variation*.
- Non-interactive / agent-safe flags early (avoid `input()` hangs that already block S5–7 / 11–14 in agent probes).
- Dual launcher story: keep Established folder cards for ops; add Formulated “Run Strategy 1” (or rely on CLI menu) without removing existing cards.
- Automate-first smokes after each phase; leave S2 verbal unless a separate task is opened.
- Portfolio habit: later review other verbal/hybrid gaps (S2, interactive blockers) — out of this task’s code scope.

**Playbook source of truth:** `Strategy-1-Business-Variation/strategy-1-business-variation.md`  
**Layout (locked for v1):** Stay in `Strategy-1-Business-Variation/`.

#### Phase 0 locks (2026-07-11) — authoritative for Phases 1–3

| Lock | Decision |
|------|----------|
| **Folder** | `Strategy-1-Business-Variation/` (no rename in v1) |
| **Entrypoint** | `business_variation_collector.py` |
| **Prompts** | `chatgpt_prompt_1a.txt`, `chatgpt_prompt_1b.txt`; optional `chatgpt_prompt_1c.txt` in Phase 1+ |
| **Seeds file** | `seed_businesses.json` (editable; Nigeria-first defaults from playbook) |
| **README** | `README.md` in same folder (Phase 1) |
| **Optional modules** | Only if main file approaches ~500 lines: `complaint_intake.py`, `variation_prompts.py` (additive) |
| **Output pattern** | `business_variation_YYYYMMDD_HHMMSS.json` (+ optional Prompt 1a payload `.txt`) under Strategy 1 folder |
| **STRATEGY_META[1] (Phase 3 preset)** | name: `Business Variation & Complaint Fixing`; desc: `Turns successful businesses + recurring complaints into differentiated variation ideas (Prompt 1a/1b).` |
| **Run ALL policy (Phase 3)** | Once S1 is registered, **Run ALL includes Strategy 1** → active set `1, 3–7, 9, 11–15` (same as `sorted(STRATEGY_SCRIPTS.keys())`). Strategy **2** stays verbal and excluded. **Gate:** Phase 2 must ship `--non-interactive` / `--inputs` before Phase 3 so “Run ALL” cannot hang forever on S1 `input()`. |
| **Menu verbal note (Phase 3)** | Replace “Strategies 1 and 2 are verbal…” with **Strategy 2 only** verbal. |
| **Prompt 1b layout** | **One table.** **Lead columns (S1-specific, before S5-aligned wide columns):** (1) Target successful business, (2) Complaint theme / recurring complaint, (3) Complaint category (UX / performance / cost / support / other), (4) Frequency, (5) Impact, (6) Solvability. Then **Proposed domain (not verified)** + the same wide analysis columns as Strategy 5 `chatgpt_prompt_1b.txt`. |
| **Prompt 1a formula** | Must state S1 formula and **not** S6 niche-mash or S7 trending-adapt framing. |

#### Non-negotiable safety (do not break anything anywhere)

- **No implementation until the user explicitly approves the target phase** (or says implement now / skip gate for a named phase).
- **One phase at a time.** Do not big-bang-edit runner + agent prompt + launcher + script in one unreviewed commit.
- **Additive first:** New files in Strategy 1 folder before touching shared infra. Shared infra changes only in the phase that names them.
- **Do not modify** gadget-business automation behavior, supplier APIs, or pitch-deck generators under this task.
- **Do not retire or renumber** Strategies 3–7, 9, 11–15; **do not** change `RETIRED_STRATEGIES` (8, 10) semantics.
- **Do not break** agent formulation runs: until Phase 4 ships, agent prompt may still omit S1; after Phase 4, S1 must degrade gracefully (seed/paste/synthesis fallback) so `business_ideas_YYYYMMDD.md` + `.docx` still produce if S1 fetch is empty.
- **Backward compatibility:** Existing “verbal” playbook markdown remains readable; update it to say “technical + playbook” rather than deleting steps.
- **Runner menu:** When registering Strategy 1, update **all** hardcoded “3–15 / verbal 1–2” copy in `run_all_strategies.py` and `run_all_strategies_README.md` together in that phase — avoid half-wired menus.
- **Do not modify Strategy 15** behavior/scripts unless a later phase explicitly requires a shared helper extract (prefer copy pattern, not shared rewrite).
- **Tests:** After each infra phase, run automate-first checks (import/`py_compile`, registration assert, non-interactive fixture if available). No “please click through Hub” as the default gate mid-build.
- Keep new modules **under ~500 lines**; split rather than fuse into gadget CLI or `run_all_strategies.py`.

#### Differentiation (document in prompts + README)

| Strategy | Job |
|----------|-----|
| **1** — Business Variation | Proven successful business + recurring complaints → differentiated variation |
| **6** — Niche combination | Combine startup niches / directory sectors → new ideas |
| **7** — Trending adaptation | Adapt trending products for Nigeria with niche twist |

#### Phase 0 — Discovery & lock (read-only / task-file only; no product code) ✅
- [x] **0.1** Confirm entrypoint name and Prompt 1b column alignment.
  - **Locked entrypoint:** `business_variation_collector.py` (mirrors collector/adapter naming; not gadget CLI).
  - **Locked Prompt 1b:** S1 lead columns (target business, complaint theme, category, frequency, impact, solvability) + `Proposed domain (not verified)` + Strategy 5 wide columns (S14 playbook table lacks domain column — **follow S5** for domain rule).
- [x] **0.2** Inventory touchpoints to update in later phases (do **not** edit these in Phase 0):

| Touchpoint | Why later | Phase |
|------------|-----------|-------|
| `run_all_strategies.py` | `STRATEGY_SCRIPTS`/`META`, verbal notes (~L247–319), Run ALL via `sorted(STRATEGY_SCRIPTS.keys())` | 3 |
| `run_all_strategies_README.md` | Strategy table + overview still says 3–14/3–15 style | 3 |
| `prompts/agent_formulation_run.txt` | Include list is `5, 6, 7, 9, 11, 12, 13, 14, 15` — add **1** | 4 |
| `agent-business-idea-runs/agent_strategy_run.py` | `strategies_skipped` today `[3,4,8,10]`; add optional `strategy_1_*` fetch block | 4 |
| `agent-business-idea-runs/README.md` | Document S1 keys / fallback | 4 |
| `inc_launcher/launcher_config.json` | Established already has S1 folder + gadget cards; Formulated may get additive Run S1 | 5 |
| `inc_launcher/README.md` | Agent run copy lists strategies 5…15 — refresh when S1 in agent set | 4–5 |
| Pillar table in this `task.md` (§ Inc Launcher) | S1 under Established today; clarify formulation vs gadget | 5 |
| `API_INTEGRATION_GUIDE.md` / `API_IMPLEMENTATION_SUMMARY.md` | Enumerate some strategies; **no S1 today** — add only if listing completeness requires it | 5 |
| `Strategy-1-Business-Variation/strategy-1-business-variation.md` | Header note: technical strategy (keep steps) | 1 |

- [x] **0.3** Snapshot **do not touch** (unless a later phase explicitly names a minimal cross-ref):

| Do not touch | Reason |
|--------------|--------|
| `Strategy-1-Business-Variation/gadget-business/gadget-business-automation/**` | Ops product; not formulation |
| `Business-Idea-Formulation-Strategy-{3–7,9,11–15}/**` scripts/behavior | No drive-by refactors; copy patterns only |
| `RETIRED_STRATEGIES` / Strategy 8 & 10 archive paths | Keep retirement semantics |
| `agent-business-idea-runs/outputs/business_ideas_*.md` / `.docx` (historical) | Append-only new dated runs |
| `agent-business-idea-runs/inputs/agent_strategy_inputs_*.json` (historical) | Do not rewrite old fetches |
| `problem_identification_tool/**`, `inc_launcher` behavior beyond additive config in Phase 5 | Out of S1 formulation core |
| Strategy **2** folder / verbal status | Separate task if ever automated |

**Phase 0 definition of done:** ✅ Names + touchpoint list + Run ALL policy locked in this task entry; **zero** new formulation `.py` (Phase 1 still required for scaffold).

#### Phase 1 — Scaffold in Strategy 1 folder only (no runner / no agent / no launcher) ✅
- [x] **1.1 — Prompts:** Add `chatgpt_prompt_1a.txt` / `chatgpt_prompt_1b.txt` (optional `1c`) encoding complaint→variation formula; explicit “not S6/S7” guidance; **use Phase 0 Prompt 1b lock**.
- [x] **1.2 — Seeds:** Add editable Nigeria-first `seed_businesses.json` (or YAML) from playbook examples (Jumia Food, Bolt, GTBank app, etc.) — user-editable, not hardcoded forever in Python.
- [x] **1.3 — Stub script:** `business_variation_collector.py` prints paths / playbook formula / exits 0; `README.md` states technical strategy + how to run; optional empty `requirements.txt`.
- [x] **1.4 — Playbook note:** Update `strategy-1-business-variation.md` header: technical script exists (or “in progress”) without deleting human steps.

**Phase 1 definition of done:** ✅ Folder self-contained; `python business_variation_collector.py` exits 0; **no** changes to `run_all_strategies.py` or agent prompt yet.

#### Phase 2 — Core CLI logic (still Strategy 1 folder only) ✅
- [x] **2.1 — Business seed load + optional paste:** Choose from seeds and/or enter custom successful businesses.
- [x] **2.2 — Complaint intake:** Structured fields (source, text, category: UX / performance / cost / support / other); frequency, impact, solvability scores (playbook Steps 2–3).
- [x] **2.3 — Prompt generation:** Build Prompt 1a payload; optional Prompt 1b table scaffold for chosen variations; reuse `cursor_copy_helper` pattern only if additive and default-safe.
- [x] **2.4 — Persist:** Write `business_variation_YYYYMMDD_HHMMSS.json` (and optional payload `.txt`) under Strategy 1 folder.
- [x] **2.5 — Non-interactive mode:** Flags such as `--non-interactive` / `--inputs <path>` / `--seeds` so agents and smokes can run without hanging on `input()`. **Required before Phase 3** (Run ALL gate).
- [x] **2.6 — Modularize if needed:** Split intake/scoring/prompt builders into sibling modules before the main file exceeds ~500 lines.

**Phase 2 definition of done:** ✅ Interactive + non-interactive paths work locally; fixtures/smoke scriptable; still **not** registered in master runner.

#### Phase 3 — Master runner + runner docs (narrow shared-infra blast radius) ✅
- [x] **3.1** Add `STRATEGY_SCRIPTS[1]` + `STRATEGY_META[1]` pointing at `Strategy-1-Business-Variation/business_variation_collector.py` (meta per Phase 0 lock).
- [x] **3.2** Per Phase 0 **Run ALL** lock: include Strategy **1** in active ALL set; verbal note = Strategy **2** only; update docstring, menu, range/examples copy in one pass.
- [x] **3.3** Update `run_all_strategies_README.md` strategy table + notes.
- [x] **3.4** Smoke: menu list shows Strategy 1; option “run one” can launch S1; Strategies 3–15 still launch unchanged. *(Automated: `test_phase3_runner_smoke.py` + Phase 2 smoke updated for registration.)*

**Phase 3 definition of done:** ✅ S1 runnable via master runner; S2 still verbal; no regressions on existing strategy numbers.

#### Phase 4 — Agent formulation infrastructure ✅
- [x] **4.1 — Agent prompt:** Update `prompts/agent_formulation_run.txt` to **include Strategy 1** in the executable set; document skip/fallback rules; keep skips for 3, 4, 8, 10 (and 2 verbal).
- [x] **4.2 — Agent fetch (additive):** Extend `agent_strategy_run.py` with `strategy_1_seeds` (+ optional `--with-strategy1-run`) — **default continue on empty/fail**; no network scrape required for S1 seeds.
- [x] **4.3 — Agent README / inputs schema notes:** Document new JSON keys; Strategy 1 synthesis instructions; dedup paths unchanged.
- [x] **4.4 — Execution summary contract:** Agent outputs must show S1 status (ran / synthesized / skipped / blocked) without failing the whole run — encoded in `agent_formulation_run.txt`.

**Phase 4 definition of done:** ✅ Agent runs can produce S1-traced ideas; fetch failure does not abort RSS/OWID/S6/S7/S14/S15 paths.

#### Phase 5 — Launcher, pillars, cross-docs (opt-in polish; still modular) ✅
- [x] **5.1 — Inc Launcher:** Keep Established cards (Strategy 1 folder + gadget automation). Added Formulated pillar item `strategy1_run` → `python business_variation_collector.py` (cwd Strategy 1). Relabeled Established folder card for clarity. No removals.
- [x] **5.2 — Pillar wording in this `task.md`:** Clarified S1 formulation = Formulated ideas; gadget ops = Established.
- [x] **5.3 — API / integration docs:** Mentioned Strategy 1 under manual/local-seed strategies in `API_INTEGRATION_GUIDE.md` and `API_IMPLEMENTATION_SUMMARY.md`.
- [ ] **5.4 — Optional research URL helper:** Deferred (not required for v1 discoverability; can ship later as `--open-links` default off).

**Phase 5 definition of done:** ✅ Discoverability updated; launcher tests green (`pytest inc_launcher/tests`).

#### Phase 6 — Regression & v1 sign-off ✅
- [x] **6.1** Static checks: registration, prompt include list, no “verbal only” for S1 in runner.
- [x] **6.2** Automated smokes: non-interactive fixture run; `py_compile`; registration + Phase 2–4 smokes via `test_phase6_regression.py`.
- [x] **6.3** Spot-check: prior strategies still in `STRATEGY_SCRIPTS`; agent fetch still writes `agent_strategy_inputs_*.json` with S1 + prior keys; launcher `test_config` green.
- [x] **6.4** Former Hub/menu/playbook manual steps moved to **`test_signoff_automated.py`** (wired into `test_phase6_regression.py`). `MANUAL_TEST.md` now records **no remaining manual steps** for v1.

**v1 definition of done:** ✅ Strategy 1 is a technical strategy end-to-end (script + runner + agent path + docs); gadget ops untouched; automated regression PASS 2026-07-12. Manual Hub/menu pass optional via `MANUAL_TEST.md`.

#### Explicitly out of scope (v1)
- Strategy **2** verbal→technical conversion.
- Full Twitter/Reddit/App Store scrapers; paid Brand24/Mention integrations.
- Rewriting or relocating `gadget-business-automation/`.
- Renaming strategy folder to `Business-Idea-Formulation-Strategy-1-*` (defer unless approved).
- Changing retired Strategies 8/10 policy.
- Google Drive Macrodroid card renames.

#### Tier / phase approval checkpoints (user)
- [x] Approve **Phase 0** locks (names + Run ALL policy for including `1`) — done 2026-07-11 via “Implement only Phase 0”.
- [x] Approve **Phase 1** (folder scaffold) — done 2026-07-11 via menu “1 - recommend and approve”.
- [x] Approve **Phase 2** (CLI intake + non-interactive) — done 2026-07-11 via menu “1”.
- [x] Approve **Phase 3** (master runner wiring) — done 2026-07-11 via menu “1”.
- [x] Approve **Phase 4** (agent prompt + fetch) — done 2026-07-12 via menu “1”.
- [x] Approve **Phase 5** (launcher/docs) — done 2026-07-12 via menu “1”.
- [x] Approve **Phase 6** (regression & v1 sign-off) — done 2026-07-12 via menu “1 - pls do not break anything”.

**Suggested milestones:** Phase 0–6 ✅ 2026-07-11/12.

**Related:** Chat 2026-07-11 (S1 verbal→technical recommendations); Strategy 15 wiring pattern (task §5); Crunchbase/S6–S7 additive safety pattern (task §8); `prompts/agent_formulation_run.txt`; `inc_launcher` Established vs Formulated pillars.
