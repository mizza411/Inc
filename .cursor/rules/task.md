# Active Task List
*This file tracks all tasks - coding, business, research, and other activities*

## Convo handoff — pending count + §7 Phase 1b + OTI Day 1 (2026-07-23)

**Safe to delete this chat?** **Yes.** Durable state is on disk below — no chat-only secrets, signup results, or decisions left only in transcript.

| Thread topic | Maps to | Progress / status | Pending (not chat-only) | Manual tests (you) |
|--------------|---------|-------------------|-------------------------|--------------------|
| Pending-task count + days-left + priority | **Portfolio time-left** (top of this file) | Recount method documented; focus order set | Refresh table after each completion | None for the count itself |
| §7 DeepSeek / wedding launch | **§7** Post-Wedding Comms Pack | Phase **1b** + **landing artifact** shipped; suite green 2026-07-23 | Publish Pages + Streamlit host (`DEPLOY.md`) → §B/§D → IG/0b | `MANUAL_TEST.md` §B/§D/§P1 once at sign-off |
| Switch to Online Tasks Income (menu **4**) | **OTI-INC-1** + tracker | Tooling complete; **core tabs opened**; all platform accounts still **No** | Day 1 signups + payment checks + CLI `update-platform` | `online_tasks_income/MANUAL_TEST.md` Day 1 |

**Recommended new task file?** **No** — keep `.cursor/rules/task.md` + existing `ONLINE_TASKS_36_DAY_INCOME_TRACKER.md` + §7. Added `online_tasks_income/MANUAL_TEST.md` only (owner signup steps; not a second backlog).

**Blocker if you delete too early?** Only if you finished a platform signup **in the browser** and never ran `update-platform` / never ticked `MANUAL_TEST.md` — then re-check accounts and record status once. Nothing unique is trapped in this chat.

---

## Portfolio time-left (update on every task completion)


**Last recount:** 2026-07-23 (updated after §19 task add — approx; refresh on next completion)  
**Method:** Unchecked `- [ ]` in this file, excluding deferred/optional/out-of-scope/parked lines; plus open checkboxes in `**/MANUAL_TEST.md` (overlap with this file is possible).

| Metric | Count | @ 1 task/day | @ 2 tasks/day |
|--------|------:|-------------:|--------------:|
| Pending checkboxes (`task.md`, excl. deferred) | **240** | ~240 days | ~120 days |
| Parent-level packages (`**…**` titles, excl. deferred) | **43** | ~43 days | ~22 days |
| Open `MANUAL_TEST.md` checkboxes (all apps) | **65** | (sign-off / human steps; not all are parallel “build” tasks) | — |
| Checked done in `task.md` | 333 | — | — |

**When a task is completed:** retick here, then refresh this table (pending counts + day columns). Do not leave stale ETAs.

**Active focus (2026-07-23):** §7 Post-Wedding — suite green; landing in repo; next = WhatsApp in `landing/config.js` → push Pages → Streamlit Cloud (`DEPLOY.md`) → short `MANUAL_TEST` §B/§D → Phase 0b DMs.

**Suggested focus order (2026-07-23):** (1) **§7 Post-Wedding** host + 0b — nearest product revenue; (2) **OTI-INC-1** Day 1 signups — cash this week if platforms ready; (3) **§5 bookmark hygiene** — stress from ~1926 Chrome queue.

---

## FIR-INC-1 — Field Intelligence Radar (copied to Inc; cutover not finished)

**Status:** 🟡 **In progress** — **Phase 0–5 ✅** (24/07/2026) · **6–8 ⏳**  
**Canonical folder:** `C:\dev\Inc\field_intelligence_radar/`  
**project_reminder:** full duplicate + stub `field_intelligence_radar/README.md` until **6a/6b**  
**Authoritative phases:** `C:\dev\project_reminder\.cursor\rules\task.md` § **FIR-INC-1**  
**Checklist:** `C:\dev\project_reminder\tests\FIR_INC_MOVE_MANUAL_TESTS.md`  
**Do not:** fuse with `abuja_lead_generator/`; delete source until owner **6a**  
**Sibling precedent:** **OTI-INC-1** below  

### Money / field tracks (prefer Inc paths)

| ID | Role | Path on Inc |
|----|------|-------------|
| **FIR-ABUJA-MON-1** | Abuja construction visit monetization (₦210k) | `field_intelligence_radar/ABUJA_DAY1_VISIT_SHEET.md` · `ABUJA_MONETIZATION_MANUAL_TESTS.md` |
| FIR product / APK | Android radar + backend | `field_intelligence_radar/` (roadmap, `build_output/`, `mobile/`, `backend/`) |
| **ABUJA-SIT-CHARGE-1** | Sit+charge venues | Pointer-only until owner saves; prefer `field_intelligence_radar/ABUJA_SIT_CHARGE_VENUES.md` here |

### Open now

```powershell
cd C:\dev\Inc\field_intelligence_radar
# Docs / scripts live here. Reinstall mobile deps only if you need to build:
# cd mobile; npm install
```

**Secrets:** `FIR_KEYS_LOCAL.txt`, `DB_PASSWORD_DO_NOT_COMMIT.txt` are local — **do not commit**.  
**Not** auto-launched / no tray / no Inc Hub card unless owner opts in (**8b**).

---

## OTI-INC-1 — Online tasks income toolkit (moved 22/07/2026)

**Status:** 🟢 **Complete (move)** · execution (platform signups) still owner-pending — **Day 1 started 2026-07-23** (tabs opened; accounts not yet recorded)  
**Folder:** `online_tasks_income/` at Inc root (`C:\dev\Inc\online_tasks_income\`)  
**Source:** moved from `project_reminder` (stub README left there)  
**Owner next:** TELUS → Clickworker → OneForma → uTest; record each with `income_cli.py update-platform`

| Item | Path / command |
|------|----------------|
| Tracker | `online_tasks_income/ONLINE_TASKS_36_DAY_INCOME_TRACKER.md` |
| CLI | `python online_tasks_income\income_cli.py status` (from Inc root) |
| Opener | `python online_tasks_income\open_platforms.py --tier core` |
| README | `online_tasks_income/README.md` |
| **Manual (you)** | `online_tasks_income/MANUAL_TEST.md` — Day 1 signups + payment checks |

**Not** auto-launched / no tray unless owner asks.

#### Session handoff (2026-07-23)
- Core opener run: TELUS, Clickworker, OneForma, uTest tabs opened.
- `status`: all core Account/Profile/Payment still **No**.
- Pending lives in tracker + `MANUAL_TEST.md` — **not** in chat.
- Original 36-day calendar (May–Jun 2026) expired without signups; treat **2026-07-23** as execution restart (cash goal unchanged; re-date daily rows as you work).

---

## Sidebar chat batch assess (image — 2026-07-20)

**Attempt:** status/handoff sync only — **no code implementation** this pass.  
**Source:** Cursor history list (9 checkmarked / completed-looking chats, titles truncated).  
**Goal:** Map each title → durable tracker + pending + manual tests + **delete yes/no**.

| # | Sidebar title (truncated) | Maps to (authoritative) | Progress / status | Pending (not chat-only) | Manual tests (you) | Safe to delete chat? |
|---|---------------------------|-------------------------|-------------------|-------------------------|--------------------|----------------------|
| 1 | Profitable sub-niches in Abuja… | **§6** Land Sales OS + `Abuja-Real-Estate-Research/abuja-real-estate-profitable-sub-niches.md` (+ docx v1/v2) | Research **done**; PropTech reframed to **internal-org SaaS**; **build not started** | Phase 1 scaffold when you kick off §6 (CAC, MVP modules, pilot orgs) | **None yet** for research. Product MANUAL_TEST only after §6 kickoff | **Yes** — research + decisions on disk |
| 2 | Run all executable business-id… | **§4** Hub + **§14** agent formulation; `run_all_strategies.py` / `agent-business-idea-runs/` (not interactive CLI as primary) | Agent front door **v1 CLOSED**; runner active set includes S1 + 3–7, 9, 11–15; **8/10 retired** | Optional live Hub two-run; schedule tune; do not confuse with CLI “Run all” | Optional: `agent-business-idea-runs/MANUAL_TEST.md` Two-run + `inc_launcher/MANUAL_TEST.md` §G/§G14 | **Yes** — tracker + tests hold it |
| 3–7 | Business idea formulation stra… (×5) | Closed strategy workstreams already handed off: **§9–§14** Current Priority + Notes **§4–§14** (S1 verbal/online, S5 labels, S12 GUEMF, Pass1/2 pack, Crunchbase S6/S7 Tier1–2, S8/S10 retire, S15, etc.) | Titles identical when truncated — treat as **completed** strategy sessions already marked **Safe to delete** in their sections | Open leftovers are **cross-cutting** (e.g. Problem ID C3, bookmark queue, §6 build, §18 WTP) — not locked inside these five chats | Per-stream: mostly **none**; S1 = closed; S12 = none; §14 = optional Hub Enter only | **Yes** *if* each was one of the closed streams above. **Blocker only if** a fifth chat held unique unlogged decisions (unlikely with checkmarks + existing handoffs) |
| 8 | Business content sorting and c… | **§5** Business Bookmark Sorting (`business_bookmark_sorter/`) | Import/review/file+docx **shipped**; secure workflow **planned**; ~**1926** pending (re-check `status`) | Hygiene → batch file; Phase 3 auto de-bookmark **not built**; Phase 5 options D–G code **not approved** | **Yes — you:** `business_bookmark_sorter/MANUAL_TEST.md` §§A–F (Chrome hygiene, batch file, Phase 2b sign-off) | **Yes** for planning/delivery chats — **pending work lives in §5 + MANUAL_TEST**, not chat memory |
| 9 | Strategy 10 overview | Notes **§7** Retire ChatGPT Vision / Strategy 10 | Phases 1–3 **all [x]** — removed from runner, archived, `DEPRECATED.md` | None for retirement; use S3–5 for RE/construction discovery | **None** | **Yes** |

### Batch delete verdict

| Verdict | Detail |
|---------|--------|
| **Can you delete all 9 chats in the image?** | **Yes — no chat-memory blockers** for this batch as mapped above. Durable state is in this file + folders/tests cited. |
| **Not blockers (still open work, but not “keep chat”)** | §6 Land Sales OS build; §5 bookmark filing (~2k queue + MANUAL_TEST A–F); §1 Problem ID **C3** Google Form retire; §18 WTP interviews; optional Hub Enter |
| **Would become a blocker** | Finding a chat whose *only* copy of a decision/secret/file path is the transcript and is **not** reflected in `task.md` / repo — none identified for these nine titles |

**Recommended new task file?** **No** — keep `.cursor/rules/task.md` authoritative. Optional later: only if §6 build grows past ~2 screens → then `abuja_land_sales_os/task.md` at kickoff (not now).

---

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

- [x] **Phase A — Questionnaire** (done Jul 2026 — commit `e43091f`)
  - [x] Add `ill_pay_to_v1` to `web/data/questionnaires.json` (title “I'll pay to..”, WTP + urgency questions)
  - [x] Add `email` question type + validation in `questionnaire.js`
  - [x] Implement minimal conditional branching (2 rules)
  - [x] Set `ill_pay_to_v1` as active questionnaire (or `?survey=ill_pay_to_v1` param)
- [x] **Phase B — Strategy 3 integration** (done Jul 2026)
  - [x] **B1 — Distributor links + templates** (`534a3ba`)
    - [x] `distributor_links.py` — unique ref/UTM link generator + local registry
    - [x] `distributor_message_templates.txt` + `distributor_brief.md`
    - [x] `test_distributor_links.py` smoke tests
  - [x] **B2 — Collector integration** — optional `--distributor` mode (`6e8c8cd`)
  - [x] **B3 — Sharing utilities** — wire `sharing_utilities.py` ref/UTM (`1011558`)
- [ ] **Phase C — Data migration** (in progress — Jul 2026)
  - [x] **C1 — Import script** — `scripts/import_google_forms_csv.py` + tests + sample CSV fixture (`cfbef67`)
  - [x] **C2 — Dashboard merge** — merges localStorage + `web/data/imports/google_forms_ill_pay_to.json`; `--sync-dashboard` flag; tests (`4c631ce`, pushed to `origin/main`)
  - [ ] **C3 — Retire Google Form** — **USER ACTION** (see `problem_identification_tool/MANUAL_TEST.md`)
    - [ ] Export real Google Form CSV (~12 responses)
    - [ ] Run: `python scripts/import_google_forms_csv.py --input <csv> --sync-dashboard`
    - [ ] Commit/push updated import JSON; verify dashboard count matches
    - [ ] Close/archive Google Form
- [ ] **Phase D — Deploy & smoke**
  - [x] Survey live on GitHub Pages (A–C2 code pushed)
  - [ ] Smoke-test live dashboard merge after C3 real-import push
  - [ ] Optional: register first paid distributor + generate tracked link (`network_problem_collector.py --distributor`)

**Manual tests for this work:** `problem_identification_tool/MANUAL_TEST.md` (C3 + live dashboard sign-off only; automate-first otherwise).

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
**Status:** Phase 5 **v1 CLOSED** (agent formulation front door) — **2026-07-20 handoff**  
**Goal:** Windows **tray icon** (notification area, near the clock) + optional super main hub; all `C:\dev\Inc` entry points organized under **4 pillars** (extensible to 5+ later).  
**Folder:** `inc_launcher/` — run: `python -m inc_launcher.tray_app` from `C:\dev\Inc`  
**Manual tests:** `inc_launcher/MANUAL_TEST.md` (Phase 5 §G mostly automated; optional Cursor **Enter** + §D reboot)

> **Terminology:** “Tray icon” = the small icon you right-click in the Windows notification area. Same as “system tray app” — one background process, one icon, menu on right-click.

#### Session handoff — Phase 5 Hub agent front door (convo close 2026-07-20)

| Item | Status |
|------|--------|
| **5.0–5.4, 5.6** | ✅ Shipped — Hub header fix; `prompts/agent_formulation_run.txt`; `agent_run` action; pinned Hub card; Option B modal; docs |
| **Option B only** | ✅ Documented — Hub-hosted modal; no detached Option A toast; tray must be running |
| **CLI card demoted** | ✅ **Run all strategies (CLI menu)** — not confused with agent card |
| **Automated sign-off** | ✅ `pytest inc_launcher/tests` (57+) + `smoke_hub` + `test_phase5_signoff.py` (incl. tray kill/`pythonw` restart + single-instance) |
| **Manual remaining** | Optional only — `MANUAL_TEST.md` §G: Cursor chat **Enter** after Start (cannot automate reliably) |
| **5.5 Schedule** | ⬜ Optional / not requested for v1 — weekday Hub+Option B modal only if you approve a slot later |
| **Safe to delete this chat?** | **Yes** — tracker = this §4; tests = `inc_launcher/MANUAL_TEST.md` §G; no unique decisions left only in chat |

**Earlier handoff (nudges + Track C — 2026-06-29):** Phase 4 nudges `4c54b9c`; Track C `909c6d9`; boot via external `auto_launcher`; Inc login startup OFF.

#### Session handoff — Problem ID live URL auto-launch (Q&A 2026-07-20)

| Item | Status |
|------|--------|
| **Q:** Does Inc Hub (or anything else) auto-open `https://mizza411.github.io/Inc/problem_identification_tool/web/index.html`? | **Answered** |
| **Source of auto-open** | **Inc Launcher interval nudges only** — schedule `problem_id_live_mwf` → target `problem_id_live` (`action: url`) |
| **When** | **Mon / Wed / Fri 10:00** (while tray running + `schedules.enabled: true`) |
| **Not** | Inc Hub open/startup; Windows login; 09:15 Hub nudge; local pinned HTML file |
| **Live proof** | `inc_launcher/schedule_fired.json` includes `problem_id_live_mwf:2026-06-29 10:00` |
| **Elsewhere in repo** | Docs / QR / social copy only — **no other auto-launch** |
| **Pending (optional)** | **Schedule tune** — keep / move / remove 10:00 Problem ID, or tray **Interval nudges [OFF]** — see `MANUAL_TEST.md` §E |
| **Safe to delete this chat?** | **Yes** — durable answer = this block + Phase 4 schedule table + `MANUAL_TEST.md` §E; no code change this session |

**Active Phase 5 Hub work:** none (v1 closed). Optional follow-ups: **5.5** schedule, §G Cursor Enter, older pending list below.

#### Phase 5 — Inc Hub agent formulation front door (Track D)
**Status:** **v1 CLOSED** (2026-06-30 ship; 2026-07-20 handoff synced) — automation signed off; Cursor Enter optional  
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
- [x] **5.6 — Tests + docs:** `test_agent_run.py`, `test_phase5_signoff.py`; `inc_launcher/README.md`; `MANUAL_TEST.md` §G (automation + deferred Enter)

**v1 definition of done:** ✅ Met via automation (header, config, modal, orchestration, tray single-instance). Live Cursor **Enter** remains optional ops check in `MANUAL_TEST.md` §G — not a blocker to close Phase 5 Hub v1 or to delete the delivery chat.

**Key files:** `inc_launcher/agent_run.py`, `agent_run_modal.py`, `hub_window.py`, `actions.py`, `tray_app.py`, `launcher_config.json`; `prompts/agent_formulation_run.txt`; tests `test_agent_run.py`, `test_phase5_signoff.py`.

**Dependencies:** `cursor_copy_helper.py` (repo root); `pyautogui` optional for auto-paste  
**Layout:** `prompts/` at repo root; orchestration in `inc_launcher/` (later Pass 1/2 / `agent-business-idea-runs/` tracked under §14 — do not reopen Phase 5 Hub for that)

#### Pending (optional — not blocking)

- [ ] **Phase 5.5** — scheduled Hub + Option B modal (only after you pick weekday/time) — **local tray nudge path**; do **not** conflate with **§19** cloud Automations
- [ ] **MANUAL_TEST §G** — Cursor **Enter** once on a live agent session (when you choose)

- [ ] **Schedule tune** — if 09:15 Hub or **10:00 Problem ID live** browser nudge is too noisy; edit `launcher_config.json` → `schedules.items` (id `problem_id_live_mwf`) or tray **Interval nudges [OFF]**. Confirmed 2026-07-20: that URL is **not** opened by Hub itself — only by this nudge (see handoff above + `MANUAL_TEST.md` §E).
- [ ] **Track B** — clearer boot vs nudge toggle labels — **skipped** (user 2026-06-29); reopen only if menu still confusing
- [ ] **Bookmark review schedule** — weekday nudge deferred; menu-only for now
- [ ] **Phase 4 v1.1** — toast + Snooze before auto-open; catch-up if tray starts after missed slot
- [ ] **MANUAL_TEST §D** — reboot + external `auto_launcher` one-tray check (skip if daily use already OK)
- [ ] **Operational** — file Chrome bookmarks via tray review (~**1926** pending as of 2026-06-29; re-check with `python -m business_bookmark_sorter status`). **Do not** bulk-export Chrome into chat. Secure workflow + pending options: **§5** + `business_bookmark_sorter/MANUAL_TEST.md`

#### Four pillars (top-level nav — tray icon right-click + super main sidebar)

| Pillar | Purpose | Initial `Inc` mapping |
|--------|---------|------------------------|
| **My Established business ideas** | Businesses you are running or committed to | `Started-Businesses/`, Strategy 1 **gadget ops** (`Strategy-1-Business-Variation/gadget-business/…`), live ops (e.g. YouTube when active). Folder shortcut to Strategy 1 playbook OK here for ops adjacency. |
| **My leads** | Contacts, outreach, campaigns | `abuja_lead_generator/` (DB, scraper, email/WhatsApp, reports) |
| **Formulated ideas** | Idea pipeline outputs & strategy runs | **Strategy 1 formulation CLI** (`business_variation_collector.py` / Hub “Run Strategy 1”), `Business-Idea-Formulation-Strategy-*/`, `run_all_strategies.py`, `agent-business-idea-runs/`, `past_business_ideas.md`, `business_research/`; curated shortlist: **`Prospect-Businesses/`** (Hub card + sorter route shipped) |
| **Problem identification** | Discovering & capturing problems (inputs to formulation) | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/`, problem-collection strategies (3, 4, 5, 10, 11, 12, etc.) |

**Strategy 1 split:** Formulation (complaint→variation script + agent/runner) lives under **Formulated ideas**; gadget automation stays under **Established**. Do not treat the Hub folder card as a substitute for “Run Strategy 1”.

**Flow:** Problem identification → Formulated ideas → **Prospect businesses** (curated shortlist) → Established businesses; **My leads** supports outreach alongside that pipeline.

#### Prospect-Businesses folder
**Status:** **CLOSED / v1 complete** (2026-07-12) — Phases **0–4** done (incl. Hub **3.1** + sorter **3.2**)  
**Goal:** Dedicated home for businesses **not started** but with **strong prospects** — separate from `Started-Businesses/` (e.g. software) and from raw formulation dumps (`agent-business-idea-runs/outputs/`).

**Layout:** Folder `Prospect-Businesses/` at repo root (`C:\dev\Inc\Prospect-Businesses/`) — **created**.  
**Active prospects (3):** `examfee-planner.md`, `agentdispute-ai.md`, `scimlite-ng.md` (from `business_ideas_20260712.md`).  
**Hub:** Formulated ideas → **Prospect Businesses folder** (`id: prospect_businesses_folder` in `inc_launcher/launcher_config.json`).  
**Bookmark sorter:** destination id `prospects` → `Prospect-Businesses/` (`business_bookmark_sorter/config/routes.json`).

**Shipped on remote (`origin/main`):**
| Commit | What |
|--------|------|
| `d0f6e10` | `Prospect-Businesses/` folder + README/TEMPLATE + 3 seeded prospects |
| `4a95968` | Hub Formulated card + `test_formulated_has_prospect_businesses_folder` |
| `d3db322` | Sorter `prospects` route + `test_prospect_route.py` |

**Manual tests (you):** **None required** for feature sign-off — see `inc_launcher/MANUAL_TEST.md` §H (automated; optional Hub glance only). Sorter covered by `business_bookmark_sorter/tests/test_prospect_route.py`.

**Pending (optional — not blocking close; not chat-only memory):**
- [ ] Business validation: discovery calls for **ExamFee Planner** + **AgentDispute AI** (dates in each prospect `.md`) — product research, not a code gate
- [ ] Optional: re-run agent formulation so next `business_ideas_YYYYMMDD` includes post-§11 live-cited Strategy 1 rows (separate from Prospect close)
- [ ] Graduation of any prospect → `Started-Businesses/` **only when you explicitly approve** (rule locked)

**Same-day related artifact (formulation run, not Prospect phases):** `agent-business-idea-runs/outputs/business_ideas_20260712.md` (+ `.docx`) — may still be untracked locally; commit separately if you want it on remote.

**Conversation handoff:** **Safe to delete this chat.** Tracker = this section + Current Priority **§12**; code/docs = `Prospect-Businesses/`, Hub config, sorter routes; git = commits above. Nothing unique remains only in conversation memory.
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

**Phase 3 — Optional surfaces (additive; separate approval)** — *split: Hub vs sorter (different modules)* ✅
- [x] **3.1** Hub/tray: Formulated-ideas card open `Prospect-Businesses/` (config append only) — done 2026-07-12; `test_formulated_has_prospect_businesses_folder`
- [x] **3.2** Bookmark sorter: route destination `prospects` → `Prospect-Businesses/` (append to `routes.json` only) — done 2026-07-12; `test_prospect_route.py`
- [x] **3.3a** Smoke (Hub side of 3.1): existing Formulated/Established anchors still resolve via pytest — done with 3.1
- [x] **3.3b** Smoke (sorter side): prior destinations + started suggest still resolve — done with 3.2

**Phase 4 — Graduation protocol (docs only unless user asks for tooling)**
- [x] **4.1** Documented in `Prospect-Businesses/README.md`: graduation checklist (user says “graduate X” → only then create/update under `Started-Businesses/`)
- [x] **4.2** Explicit: agents propose graduation in chat/menu; **never** execute without user number/phrase approval
- [x] **4.3** Out of Phase 4 unless separately approved: any script that copies files into `Started-Businesses/`

##### Layout checklist (maps to phases)

- [x] Phase 1: create folder + README + template
- [x] Phase 2: seed only user-named prospects (3 files)
- [x] Phase 3.1: Hub/tray Formulated card (additive)
- [x] Phase 3.2: bookmark sorter `prospects` route (additive)
- [x] Phase 4: graduation protocol documented; user remains sole approver

##### Out of scope (v1)

- Auto-promotion / auto-graduation scripts
- Moving all formulation history or `business_research/` into prospects
- Replacing or rewriting `Started-Businesses/software-development.md`
- Changing agent formulation prompt, strategy scripts, or `run_all_strategies.py`
- Making Prospects a 5th Hub pillar (keep under Formulated shortlist unless user later opens a pillar task)

**v1 definition of done:** `Prospect-Businesses/` exists with README + template; ≤10 user-named prospect files; graduation rule documented; no automatic writes to `Started-Businesses/`; Hub + sorter wired additively; pytest green for 3.1/3.2. **Met 2026-07-12.**

**Related:** Inc Hub four pillars (this §); Business Bookmark Sorting destinations; agent formulation outputs under `agent-business-idea-runs/outputs/`; Current Priority **§12**.

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
**Status:** Phase **0–2c + Track C + removal dialog + tooltips + gitignore** shipped on `origin/main`; Phase **3** (auto de-bookmark) **not started** — user returning later. Queue ~**1926 pending** (re-check: `python -m business_bookmark_sorter status`). Secure filing plan (A–G) locked 2026-07-20.  
**Goal:** Sort bookmarks from Chrome (`chrome://bookmarks/?q=business` and related trees) into the **correct folders/files inside `C:\dev\Inc`**, not into `business_bookmark_sorter\Business Links.md` (that path is a **temporary inbox only**). After Phase 2b/2c, filing means: **saved in `queue.json`**, visible under a **section** in one master **Business Links.md/.docx**, toast + **“Have you removed bookmark?”** gate, then user deletes in Chrome (Phase 3 still optional automation).  
**Tray entry:** Formulated ideas → **Bookmark review** (`inc_launcher/launcher_config.json` → `bookmark_review`)  
**Manual tests:** [`business_bookmark_sorter/MANUAL_TEST.md`](../business_bookmark_sorter/MANUAL_TEST.md) (human-only; agent runs pytest/status first)  
**Task file note:** Keep tracking here in **§5** — no separate backlog file needed (same product as existing sorter).

#### Problem (what “sorting” means)

| Decision per item | Action |
|-------------------|--------|
| **Belongs in Inc** | Write link (or note) into the right Inc destination (see taxonomy below), then **remove from Chrome bookmarks** (manual preferred; optional automation later if volume is stressful). |
| **Does not belong in Inc** | **Leave in Chrome** (personal, other projects, out of scope). |

**Hard cases:** Some Chrome entries are **folders** (e.g. `Google Go Voice Listen - Business..`) containing more bookmarks — workflow must expand folders, not only flat URLs.

**Source of truth for import:** Chrome profile `Bookmarks` JSON (typical: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks`), not the `chrome://` UI (not automatable as a page).

#### Privacy (non-negotiable) — locked 2026-07-20

| Do | Don’t |
|----|--------|
| Read Chrome **local** `Bookmarks` JSON on this PC via sorter CLI/UI | Bulk-export / zip / paste full Chrome bookmark trees into chat or cloud AI |
| Rely on `chrome_filter` (folder name contains `business`) + queue on disk | Assume agent should “see everything” to help sort |
| Keep `data/queue.json` / `actions.log` local (gitignored) | Commit or paste sensitive URLs into repo/chat |
| Same model as Drive §8: Inc is filing cabinet; Chrome is inbox | Auto-delete Chrome before export succeeds |

**Bottleneck understood:** Sorting ~2k items is slow; the **blocker to “just dump everything for AI help” is privacy** (mixed personal + business bookmarks), not tooling absence.

#### Secure workflow planning (2026-07-09 convo → documented 2026-07-20)

**Progress this session (docs only — no implementation):**
- [x] User concern understood: time cost of filing vs risk of sharing sensitive Chrome data
- [x] Secure options outlined (A–G); user confirmed understanding
- [x] Short-term combo recommended: **A + B + C** (no new code)
- [x] Medium/long options recorded for later approval (D, E, F); Drive parallel = G / §8

| Option | Name | Code? | Status |
|--------|------|-------|--------|
| **A** | Chrome hygiene — move personal/sensitive out of `*business*` folders before import | No | **Pending user** — see MANUAL_TEST §A |
| **B** | Tune local `keyword_rules` in `routes.json` (already used by `suggest.py`) | Config only | **Pending user** — paste example titles/URLs *you choose*, never full dump |
| **C** | Batch by Chrome subfolder (one destination per session) | No | **Pending user** — MANUAL_TEST §C |
| **D** | Two-speed queue + local domain blocklist (fast confirm vs slow open) | Yes — needs task approval | **Pending approval** — not started |
| **E** | Separate Chrome profile for business only | Ops / habit | **Deferred** — long-term |
| **F** | Local-only model suggest (e.g. Ollama on title/URL/path) | Yes — needs approval | **Deferred** — not started |
| **G** | Drive sorting — same privacy; local mirrors only | See §8 | **Planning** — §8 |

**Recommended next (when user has time):** run MANUAL_TEST **§A → §B → §C** in short sessions; **do not** request Option D/E/F code until user picks a combo and approves implementation.

#### Destination taxonomy (Inc — align with launcher pillars)

| Category | Example Inc destinations |
|----------|---------------------------|
| **Business started** | `Started-Businesses/`, live ops folders (**user-approved graduation only** from prospects) |
| **Prospect businesses** | `Prospect-Businesses/` (**shipped 2026-07-12** — curated shortlist; Hub + sorter) |
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
- [ ] Manual verification: file one link → see it in opened docx → delete bookmark in Chrome → confirm removal dialog → next link — **see** `business_bookmark_sorter/MANUAL_TEST.md` §D
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

**Phase 2d — UX polish (this convo arc)** ✅ (pushed)
- [x] Hover tooltips on all review controls (`ui_tooltips.py`) — Skip vs Stay explained in tip text
- [x] Post-file dialog: “Have you removed this bookmark from Chrome?” — **Yes** = sync + next; **No** = stay + **Bookmark removed — next** (`4387b96`)
- [x] Unit tests: `tests/test_review_removal.py` (agent-automated)
- [x] Gitignore local data: `data/**` (keep README), `Business Links.md/.docx`, Word `~$*` — `queue.json` **never** was on remote (`bcc4866`)

**Phase 3 — De-bookmark (optional / on demand)** — **deferred (user returning)**
- [ ] After Inc filing: mark for Chrome removal; **manual** checklist export first
- [ ] Optional automation: update Chrome `Bookmarks` JSON (backup first; Chrome closed) or extension delete API
- [ ] Never delete from Chrome without explicit user action or setting
- **Note:** Until Phase 3 ships, Chrome delete stays **manual**; dialog (2d) is the gate before next link.

**Phase 4 — Inc launcher integration** ✅ (Track C)
- [x] Add **Business bookmark sorter** item under Formulated ideas in `inc_launcher/launcher_config.json` (Track C menu only — `bookmark_review` → `python -m business_bookmark_sorter review`; no schedule yet)

**Phase 5 — Secure / faster filing (planning → implement only after approval)**
- [x] **5.0** Privacy + options documented (this § + MANUAL_TEST)
- [ ] **5.A** User: Chrome hygiene (personal out of business folders) — MANUAL_TEST §A
- [ ] **5.B** User/agent (config): expand `keyword_rules` from *user-selected* samples — MANUAL_TEST §B
- [ ] **5.C** User: batch-by-subfolder filing habit — MANUAL_TEST §C
- [ ] **5.D** (optional code) Two-speed queue + domain blocklist — **await user choice**
- [ ] **5.E/F** (optional) Business Chrome profile / local LLM suggest — deferred
- [ ] Re-run `python -m business_bookmark_sorter status` after hygiene/import; update pending count here

#### Manual verification (after build)

**Authoritative checklist:** [`business_bookmark_sorter/MANUAL_TEST.md`](../business_bookmark_sorter/MANUAL_TEST.md) (automate-first; user runs once at sign-off / when filing).

- [ ] Import produces expected count vs Chrome business folder
- [ ] One link filed to `Started-Businesses/` (or chosen folder) and visible in repo
- [ ] **Phase 2b:** File one item → docx opens with new line → delete Chrome bookmark → link still in docx/queue
- [ ] “Stay in Chrome” leaves bookmark untouched
- [ ] De-bookmark step (if enabled) removes only confirmed URLs; backup restores if mistake
- [ ] **Secure path:** no full Chrome dump shared; hygiene (§A) before large re-import

#### Out of scope (unless added later)

- Syncing with Google account cloud bookmarks beyond local profile file
- Auto-classifying **without** user confirm (beyond local suggestions); cloud AI on full bookmark export
- Sorting non-business Chrome collections
- Agent reading / pasting user’s full Chrome profile into chat

**Run (from `C:\dev\Inc`):** `import` → `python -m business_bookmark_sorter review` — see `business_bookmark_sorter/README.md`  
**After Phase 2b/2c:** one button **File & open doc**; always opens master `Business Links.docx`; `export-md` / Shift+click = full re-export.

**Pending after this convo (code vs you):**

| Item | Owner | Where |
|------|--------|--------|
| Phase 3 de-bookmark | Agent (when you ask) | this § Phase 3 |
| MANUAL_TEST §§D–E (file → delete → dialog; Stay in Chrome) | **You** — sign-off | `MANUAL_TEST.md` |
| MANUAL_TEST §§A–C (hygiene, keywords, batch habit) | **You** — ops | `MANUAL_TEST.md` |
| Phase 5.D/E/F optional faster filing | Agent after approval | this § Phase 5 |
| Append-only export / “don’t ask again” dialog | Optional later | not started |
| Strategy 4 (Business Owner Problem Collection) | Q&A only this convo — scaffold exists; **no real collection run documented** | folder + `run_all_strategies.py` → **4**; not a §5 blocker |

**Key commits (bookmark sorter):** `1904e54` (master doc + tooltips), `bcc4866` (gitignore), `4387b96` (removal dialog), `909c6d9` (tray Track C), `d3db322` (prospects route).

**Conversation handoff (2026-07-20):** **Safe to delete this chat.** Tracker = this **§5**; tests = `business_bookmark_sorter/MANUAL_TEST.md`; code on `origin/main` as commits above. Nothing unique remains only in conversation memory. Re-open with: “Continue Business Bookmark Sorting Phase 3” or “Run MANUAL_TEST §D”.

**Sidebar alias (2026-07-20):** “Business content sorting and c…” → this §5. **Safe to delete** that history item — pending filing is §§A–F in `MANUAL_TEST.md` + Phase 3/5 checkboxes here, not chat memory. See top **Sidebar chat batch assess** row 8.

---

### 6. Abuja PropTech B2B — Land Sales OS (internal org SaaS)
**Status:** Research updated for **internal-org SaaS** — **implementation not started**  
**Goal:** Sell a **digital application for real estate organizations’ internal use** — **Land Sales OS** (CRM + diligence checklist + deal room + doc vault + buyer-pack PDF). Customers = **Kuje/Lugbe developers** first, then agencies. **Their staff** run workflows; you do **not** fulfill AGIS trips or sell to end-buyers.  
**Folder:** `Abuja-Real-Estate-Research/` (research); build TBD under `abuja_land_sales_os/` or similar when kickoff  
**Spec:** [abuja-real-estate-profitable-sub-niches.md](../Abuja-Real-Estate-Research/abuja-real-estate-profitable-sub-niches.md) §3.10 · §6  
**GTM:** `abuja_lead_generator/` → **paying developer orgs** (teams with many plots/month), not diaspora retail, not AGIS fulfillment  
**Later phases (defer):** comps/pricing module (Phase 2), PM workspace module (Phase 3), `titletrail.ng` escrow (Phase Later); national MLS / NLRDTP API — not v1

**Conversation handoff (sidebar “Profitable sub-niches in Abuja…” — 2026-07-20):** Research + niche ranking + B2B SaaS reframes are on disk (`abuja-real-estate-profitable-sub-niches.md` / `.docx`). **Safe to delete that chat.** Pending = Phase 1 kickoff below (not chat-only). **Manual tests:** none until product scaffold exists — then create `abuja_land_sales_os/MANUAL_TEST.md` (or app-folder equivalent). See also top **Sidebar chat batch assess**.

#### Phase 1 — Land Sales OS MVP (target: first **paying org subscription** by **Day 30** from kickoff)

**Week 1 — Product scaffold & packaging**
- [ ] CAC registration — **B2B PropTech / software** (not brokerage; not consumer-facing brand)
- [ ] MVP modules: plot inventory, lead/CRM pipeline stages, diligence checklist (AGIS step as human task), per-plot doc vault, buyer-pack PDF export
- [ ] Org seats: admin + sales-user roles; team dashboard for sales manager
- [ ] Pricing sheet: **₦15k–₦30k/mo** starter (2–3 seats); **₦50k–₦120k/mo** growth (5–10 seats)
- [ ] T&Cs: software does not replace legal advice; no implied AGIS/government clearance

**Week 2 — Pilot org (not end-users)**
- [ ] Onboard **1–2 pilot developers** (Kuje/Lugbe) — free or discounted seats for feedback + testimonial
- [ ] Seed 5–10 real plots into pipeline; confirm sales team can complete checklist without WhatsApp-only workflow
- [ ] NDPA: minimal PII; retention policy for uploaded docs

**Week 3–4 — Paid B2B GTM**
- [ ] `abuja_lead_generator`: outreach → **Abuja estate developers** (primary) + land-focused agencies (secondary)
- [ ] **Target:** 2 paying org subscriptions in 30 days
- [ ] **Explicitly out:** B2C Paystack to end-buyers; wholesale “we run AGIS for you” as core product; diaspora WhatsApp campaigns

**v1 corridors focus:** Kuje, Lugbe, Lokogoma, outer Gwarinpa (developer inventory)

#### 90-day success metrics
- [ ] ≥4 active paying org accounts
- [ ] ≥2 orgs with ≥3 seats each (team use, not single login)
- [ ] Weekly active use (≥3 login days/week) for ≥50% of paying seats
- [ ] Org churn <25% in first 90 days
- [ ] At least 1 org producing buyer-pack PDFs from the app (not WhatsApp only)

#### Out of scope (v1)
- B2C verify concierge / end-user sales
- AGIS fulfillment / white-label report service as core revenue
- AGIS API / NLRDTP product integration
- Escrow or holding funds for land purchase
- National MLS; mortgage origination; nationwide expansion

**Budget:** ₦500k–₦1.5M (CAC, domain, MVP build, ops float, pilot discounts)

---

### 7. Post-Wedding Comms Pack (Wedding — B2C digital)
**Status (2026-07-23):** P0+P1 **code done**; Phase 1b DeepSeek shipped; **landing page in repo** (`landing/` + `DEPLOY.md`); automated suite **re-pass green** (incl. landing smoke); **Streamlit host + Phase 0b outreach still pending**; short manual **§B/§D/§P1** pending (you, once after host).  
**Goal:** WhatsApp-first **post-wedding comms** for couples — AI-drafted guest thank-yous (gift/spray-aware), vendor wrap-up, checklist — **one-time B2C fee**; no MC/planner SaaS.  
**Folder:** `Strategy-2-Problem-Solving/post-wedding-comms-pack/` — run: `python -m streamlit run app.py` from that folder  
**Spec:** [post-wedding-comms-pack.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack.md) · [README](../Strategy-2-Problem-Solving/post-wedding-comms-pack/README.md) · [LAUNCH_PLAN.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/LAUNCH_PLAN.md) · [DEPLOY.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/DEPLOY.md) · [MANUAL_TEST.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/MANUAL_TEST.md)  
**Related (defer):** [wedding-games-icebreakers-app.md](../Strategy-2-Problem-Solving/wedding-games-icebreakers-app.md) — guest link feeds comms import in Phase 3 (P2)

> **Phased plan:** Spec + folder README (P0/P1/P2) + `LAUNCH_PLAN.md`. Track ticks here — **no separate `post-wedding-comms-pack_tasks.md` needed** unless this section exceeds ~2 screens.

#### Progress snapshot (updated 2026-07-23 convo → disk)

| Area | State |
|------|--------|
| P0 MVP + `test_p0_flow.py` | ✅ |
| P1 Paystack + `test_paystack.py` | ✅ |
| Streamlit UI smoke `test_streamlit_p0.py` + `run_automated_tests.py` | ✅ Pass 2026-06-30; **re-pass agent 2026-07-23** (providers + landing) |
| Pricing ₦10k flat (`PAYSTACK_AMOUNT_KOBO=1000000`) | ✅ Committed (`2e05157`) |
| `LAUNCH_PLAN.md` / `DEPLOY.md` | ✅ Written |
| Phase 1b DeepSeek / multi-provider | ✅ Shipped |
| Landing HTML (`landing/` + smoke) | ✅ **In repo** — set `config.js` WhatsApp; Pages URL after push |
| Phase 0b couple outreach | ⬜ Pending (after live landing / app URL) |
| Hosted Streamlit app | ⬜ Pending — see `DEPLOY.md` §B |
| Short manual: §B AI, §D phone, §P1 live Paystack | ⬜ Pending — see `MANUAL_TEST.md` (DeepSeek for §B) |

#### v1 definition of done (locked)

| Milestone | Includes | Manual UI (`MANUAL_TEST.md`) | Ship meaning |
|-----------|----------|------------------------------|--------------|
| **v0.5 — P0 code** | Phase 0 ✅ + Phase 1 (P0) ✅ + automated suite green | **Do not run** | Agent-only; not user-facing launch |
| **v1.0 — soft launch** | v0.5 + **Phase 0b go** (≥2 couples WTP **₦10k flat** self-serve) | Short pass §B/§D + §P1 | Paystack ₦10,000 unlock live |
| **v1 — launch-ready** | v1.0 + hosted deploy + manual test pass | Same | Public URL, same **₦10k flat** |
| **v1.x optional** | WhatsApp Business API auto-send | Extra rows in MANUAL_TEST §P1 | Only if copy-export insufficient after v1 |

**WhatsApp API:** **Not required for v1.**  
**Native mobile app:** **Not required for v1** — mobile web / WhatsApp send is enough (see `LAUNCH_PLAN.md`).

**Order of gates (your flow):** Dev complete (`run_automated_tests.py` + short `MANUAL_TEST.md`) → hosted URL → **then** IG + Phase 0b DMs → 0b go → `PAYMENTS_DISABLED=0` public.

**Agent during build:** automated tests only (see `deferred-manual-testing.mdc`).

#### Layout (locked — no new folder)
- [x] `post-wedding-comms-pack.md` — strategy one-pager
- [x] `post-wedding-comms-pack/` — MVP code + `MANUAL_TEST.md` + `LAUNCH_PLAN.md` + `PHASE_0b_PITCH.md`
- [x] Keep tracking in this §7 — do **not** split to a new task file unless checklist grows again

#### Phase 0 — Strategy & repo ✅
- [x] Reposition → Post-Wedding Comms Pack (WhatsApp-first, vendor module)
- [x] Rename `automated-thank-you-note-generator` → `post-wedding-comms-pack`
- [x] P0 Streamlit MVP (modular)

#### Phase 0b — Validation (before public Paystack; target: **3 couples**)
- [x] Pitch copy — [`PHASE_0b_PITCH.md`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/PHASE_0b_PITCH.md)
- [x] Launch playbook — [`LAUNCH_PLAN.md`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/LAUNCH_PLAN.md) (dev first → IG; IG-first variant documented)
- [x] Landing artifact — [`landing/`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/landing/) + [`DEPLOY.md`](../Strategy-2-Problem-Solving/post-wedding-comms-pack/DEPLOY.md) + `test_landing_smoke.py` (2026-07-23)
- [ ] Publish landing live (GitHub Pages URL + `WHATSAPP_E164` in `landing/config.js`)
- [ ] Host Streamlit Cloud app (`DEPLOY.md` §B); set `APP_URL` in `landing/config.js`
- [ ] Create IG + 3 posts (**after** hosted URL / manual short pass)
- [ ] DM 3 couples (Version A — ₦10k WTP); optional ₦15k done-for-you
- [ ] **Go/no-go:** ≥2 couples WTP **₦10,000 flat** self-serve
- [ ] **Do not** flip public Paystack until 0b passes

#### Phase 1 (P0) — Nigeria-usable MVP ✅
- [x] Chat Completions API (`generation.py` — DeepSeek default; OpenAI / NGPT via `LLM_PROVIDER`)
- [x] CSV schema + prompts + WhatsApp export + vendors + checklist
- [x] `test_p0_flow.py` + `test_streamlit_p0.py` + `run_automated_tests.py`

#### Phase 1b — LLM provider swap ✅ (2026-07-23)
- [x] **Preferred:** DeepSeek via OpenAI-compatible client (`LLM_PROVIDER=deepseek`, `DEEPSEEK_API_KEY`, `base_url=https://api.deepseek.com`)
- [x] Optional multi-provider: `deepseek` \| `openai` \| `ngpt` (NGPT for Pidgin/Yoruba/Igbo later — set `LLM_BASE_URL` if endpoint differs)
- [x] Update `generation.py`, `.env.example`, README, pitch FAQ (“not ChatGPT — workflow”)
- [ ] Re-run `run_automated_tests.py` on your machine after pull; then **MANUAL_TEST §B** with DeepSeek key
- [x] African alternatives noted: NGPT (text via `ngpt`), OkeyMeta / Orinode documented as non-default (speech-only Orinode skipped for drafts)

#### Phase 2 (P1) — Monetization ✅ (code)
- [x] Paystack one-time unlock + webhook
- [ ] Public live keys + `PAYMENTS_DISABLED=0` (after 0b go)
- [ ] (Optional v1.x) WhatsApp Business API

#### Phase 3 (P2) — Stack integration (post-v1)
- [ ] Guest-engagement import · PDF export · local-language templates (NGPT fit)

#### v1 sign-off checklist (user — once)
- [x] Automated: `python run_automated_tests.py` — **Pass 2026-06-30**; **re-pass 2026-07-23** (providers + landing smoke)
- [ ] Short manual: `MANUAL_TEST.md` §B (AI tone) · §D (phone WhatsApp) · §P1 (live Paystack)
- [ ] Hosted deploy + bio/landing URL (`DEPLOY.md` — Pages + Streamlit)
- [ ] Phase 0b go → soft launch
- [ ] Optional: Stage/commit/push landing + deploy docs when you choose

#### Out of scope (v1)
- MC/planner SaaS · native App Store app · full wedding suite · print ops · WhatsApp API required

**Priority:** Set WhatsApp in `landing/config.js` → push → Streamlit Cloud → short manual §B/§D → IG/0b.

> **Manual UI:** Only remaining human steps live in [MANUAL_TEST.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/MANUAL_TEST.md) (“Your minimum checklist”). Policy: `.cursor/rules/deferred-manual-testing.mdc`.

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
- **Aligned with Bookmark §5 (2026-07-20):** same rule — local-first inbox; never bulk-share private trees into chat for “help sorting”

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
| **Prospect businesses** | `Prospect-Businesses/` (**shipped 2026-07-12** — curated shortlist) |
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
- [ ] Pipe Phase 2 output through Strategy **12** for high-value problem scoring — prefer CLI  
  `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/problem_filter.py --non-interactive --inputs <cyber_problems.json>`  
  once Phase 2 cyber JSON exists (**§13 Phase 1** shipped that path; do not invent a second GUEMF tool).

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
**Status:** **CLOSED / v1 complete** (2026-07-12) — Phases 0–6 done; commits `b95aa77` + `fe3780a` on `origin/main`  
**One-liner:** Turn `Strategy-1-Business-Variation/` playbook into a runnable formulation strategy (script + `run_all_strategies.py` + agent infra), keep gadget ops separate, additive/modular so nothing else breaks.  
**Full phased backlog:** see **§9** under Notes / formulation tasks below (`### 9. Strategy 1 — Business Variation…`).  
**Manual tests (you):** **None** — see `Strategy-1-Business-Variation/MANUAL_TEST.md`.  
**Follow-on:** **§11 CLOSED** (2026-07-12) — always-online S1; commit/push `e383983` on `origin/main`.  
**Also optional (not blocking):** Phase 5.4 research URL helper (`--open-links`); Strategy 2 verbal→technical (separate task only if requested); re-run agent formulation so next Docx uses live-cited S1 (not a manual-test gate).  
**Conversation handoff:** **Safe to delete this chat.** Progress lives in `task.md` §9/§10/§11 + Strategy 1 folder + git (`e383983`).

### 11. Strategy 1 — Always-online discovery; retire `seed_businesses.json` (NEW — Jul 2026)
**Status:** **CLOSED / complete** (2026-07-12) — Phases **A–D** shipped; on `origin/main` as **`e383983`**  
**One-liner:** Strategy 1 must **always discover successful businesses/startups online** and **always discover gaps/complaints online** (with citeable sources in outputs) — for **both** agent formulation runs and normal CLI/Hub Strategy 1 use. **Do not** use `seed_businesses.json` as the source of businesses or complaints.  
**Full phased backlog:** see **§11** under Notes / formulation tasks below.  
**User intent (locked):** Seed file is unnecessary; offline canned `example_complaints` must not appear as problem statements in Docx/md or CLI results.  
**Sign-off:** `test_phase11_signoff.py` + `test_phase6_regression.py` (automated; **no manual Hub/browser pass**).  
**Manual tests (you):** **None** — see `Strategy-1-Business-Variation/MANUAL_TEST.md`.  
**Pending (optional, not blocking close):** Next agent formulation run so `business_ideas_YYYYMMDD` S1 rows cite live URLs (earlier same-day run predated §11).  
**Conversation handoff:** **Safe to delete this chat** — nothing unique remains only in conversation memory.

### 12. Prospect-Businesses shortlist (NEW — Jul 2026)
**Status:** **CLOSED / v1 complete** (2026-07-12) — Phases **0–4** shipped on `origin/main`  
**One-liner:** Curated folder for strong **not-started** prospects (twin of `Started-Businesses/`), with Hub Formulated card + bookmark-sorter destination; **you** alone approve any graduation to Started.  
**Full phased backlog:** nested under **§4 Inc Tray** → **Prospect-Businesses folder** (same file).  
**Manual tests (you):** **None required** — `inc_launcher/MANUAL_TEST.md` §H (automated); sorter `test_prospect_route.py`.  
**Shipped:** `d0f6e10` (folder + seeds) · `4a95968` (Hub 3.1) · `d3db322` (sorter 3.2).  
**Pending (optional, not blocking):** discovery calls on ExamFee / AgentDispute (in prospect `.md` files); graduate only on your explicit OK.  
**Conversation handoff:** **Safe to delete this chat.** Progress lives in `task.md` §4 Prospect section + this §12 + git — nothing unique remains only in conversation memory.

### 13. Strategy 12 — GUEMF dual-mode (standalone + overlay) (NEW — Jul 2026)
**Status:** **CLOSED / v1 complete** (2026-07-15) — Phases **0–4** shipped  
**One-liner:** Make Strategy 12 a real **standalone** GUEMF pipeline (CLI + `run_all_strategies.py`) **and** require multi-strategy agent runs to do **both** (A) S12-origin GUEMF discovery ideas **and** (B) GUEMF overlay scores on other strategies’ ideas.  
**Full phased backlog:** see **§13** under Notes / formulation tasks below.  
**User locks (2026-07-15):** Mode A ideas in same ranked table with primary trace `S12`; agent overlay scale **1–5**; cyber §9 Phase 3 may reuse CLI.  
**Shipped:** contract + `guemf_scoring.py` + `--non-interactive` + prompt Mode A/B + MANUAL_TEST (no user steps) + regression + optional `--with-strategy12` / `strategy_12_run`.  
**Manual tests (you):** **None** — `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/MANUAL_TEST.md`.  
**Pending (optional, not blocking):** next agent formulation run so dated Docx shows S12 Mode A rows + dual-leg execution summary.  
**Conversation handoff:** **Safe to delete this chat** for §13 delivery — tracker + tests + git hold the work.

### 14. Agent formulation — Pass 1 Discover / Pass 2 Pack (prompt split) (NEW — Jul 2026)
**Status:** **CLOSED / v1 complete** (2026-07-15) — Phases **0–5** shipped; operating model locked same day  
**One-liner:** Split the mega agent formulation prompt into **Pass 1 (Discover & rank)** + **Pass 2 (Normalize/pack → Docx)** so every idea card keeps the same subheads (esp. **Regulatory**, **Competitors / alternatives**), without breaking Hub, strategy CLIs, §11/§13 gates, or existing one-file paste workflows.  
**Full phased backlog:** see **§14** under Notes / formulation tasks below.  
**Shipped:** contract; pack prompt; Discover defers Docx; `idea_card_schema.py`; Hub Pass 2 card; Phase 5 proof pack; git **`2e964fb`** on `origin/main`.  
**Operating model (locked 2026-07-15):** Prefer **two agent runs** (two Hub Starts), **not** one mega-prompt and **not** one chat that silently does both. Inc Hub **left as-is** — no meta-prompt card; card 1 = Run 1, card 2 = Run 2.  
**Manual tests (you):** Optional once — Hub two-run flow in `agent-business-idea-runs/MANUAL_TEST.md` §Two-run + `inc_launcher/MANUAL_TEST.md` §G14. Not a build blocker.  
**Optional pending (not blocking close / not started):** (A) Hub modal copy “Run 1 of 2 / Run 2 of 2” — still optional Hub polish. **(B) superseded** → build tracked as **§19** (Cursor Automations daily Pass 1→2; not tray paste+Enter).  
**Conversation handoff:** **Safe to delete this chat** — see Notes §14 close-out (meta paste drafts + Hub leave-as-is locked there).

### 15. Evergreen / always-in-demand formulation (NEW — Jul 2026)
**Status:** Planning — **implementation not started**  
**One-liner:** Generate business ideas from **things that stay in demand** (staples / evergreen consumer demand), via scrape or free API — **not** the same as trending (S7), OWID (S14), SimilarWeb peaks (S13), or GUEMF filtering (S12).  
**Decision (open):** Strategy **16** dedicated folder vs Mode under `business_research/` + Prompt 1a/1b only. Prefer dedicated strategy if volume/reuse matches S5/S14; else Mode first.  
**Not covered by:** S7 (hot now), S14 (macro data), S13 (traffic/seasonal demand), S12 (scores existing problems), S5/S9 (news), `problem_finder` Trends (rising searches), gadget `demand_analyzer` (ops tool).  
**Do not fold into:** §9 cyber vertical.

#### Phases
**Phase 0 — Scope lock (read-only)**
- [ ] Confirm sources in scope (e.g. category bestsellers, stable search, staple consumption) vs out (one-off trends, paywalled scrapes without approval)
- [ ] Lock Strategy **16** vs `business_research/` Mode
- [ ] Sketch Prompt 1a/1b contract (align with other formulation strategies)

**Phase 1 — Scaffold (only after Phase 0 approve)**
- [ ] Folder or Mode layout note in this section; wait for layout approval before many files
- [ ] CLI stub + fixture smoke; wire to `run_all_strategies.py` only if Strategy 16 chosen

**Phase 2 — Fetch + formulate**
- [ ] Scrape and/or API intake → demand list artifact
- [ ] Prompt 1a/1b path → dated `business_ideas_*.md` (privacy: proposed domain TBD)

#### Out of scope (v1)
- Paid marketplace APIs without explicit approval
- Live login scrapers for Amazon/Jumia seller portals

**Related:** §8 (if playbook Doc maps here); §16 Doc automation; agent formulation Pass 1/2 (§14).

---

### 16. Google Doc playbook automation (NEW — Jul 2026)
**Status:** Planning — **implementation not started**  
**One-liner:** After **local export** of one Google Doc playbook, automate it in Inc — either as a formulation strategy script (if it’s a new method) or as filing into pillars (if it’s unsorted notes).  
**Privacy (non-negotiable):** No Drive API login unless you approve later; **no Doc IDs/URLs in committed outputs**; work from user-exported `.md`/`.txt` under `Google Drive Business Files/` or a paste you provide.

#### Hypotheses (confirm one before build)
| ID | Meaning | Then automate as |
|----|---------|------------------|
| **A** | Doc = always-in-demand playbook | Hook to §15 (Strategy 16 / Mode) |
| **B** | Doc = unsorted business notes/ideas | Hook to §8 Drive sorter routing |
| **C** | Doc = already mirrored Macrodroid step (S3–S14) | Dedupe only — do not rebuild |

#### Phases
**Phase 0 — Export + classify**
- [ ] User exports Doc → local mirror (titles/body; no need to commit private links)
- [ ] Agent classifies A / B / C against 12 Drive cards + Strategies 3–15
- [ ] Write classification into this section; choose build path

**Phase 1 — Automate chosen path**
- [ ] If A → implement under §15
- [ ] If B → inventory + route rules under §8
- [ ] If C → mark synced; close this task

#### Out of scope (v1)
- Editing the live Google Doc in place
- Committing private Doc URLs

**Related:** §8 Google Drive Business Sorting; §15 evergreen demand; §17 ChatGPT sorter (same privacy/export model).

---

### 17. ChatGPT conversation sorter (NEW — Jul 2026)
**Status:** Planning — **implementation not started**  
**One-liner:** Treat a ChatGPT thread as a third **inbox** (after Chrome bookmarks §5 and Drive §8): user **exports** the chat → route items into Inc pillar destinations — no live chatgpt.com login from the agent.  
**Privacy (non-negotiable):** No ChatGPT URLs in committed outputs or chat pastebacks to repo; work from local export only.

#### Destination taxonomy (reuse §5 / §8)
| Pillar | Inc destinations |
|--------|------------------|
| **Established** | `Started-Businesses/` (graduation only with your OK) |
| **Prospect businesses** | `Prospect-Businesses/` |
| **Formulated ideas** | `Business-Idea-Formulation-Strategy-*/`, `business_research/`, `agent-business-idea-runs/`, `past_business_ideas.md` |
| **Problem identification** | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/` |
| **My leads** | `abuja_lead_generator/` |
| **Automation / content** | `Strategy-2-Problem-Solving/Content-Automation/` |
| **Skip** | Leave in ChatGPT only / no Inc write |

#### Layout (proposed — approve before creating files)
**Recommendation:** Extend `business_bookmark_sorter/` with an `import-chatgpt-export` path **or** thin `chatgpt_conversation_sorter/` that reuses `config/routes.json` pillars.

#### Phases
**Phase 0 — Export + read-only map**
- [ ] User provides local export (markdown/text; bullets/titles)
- [ ] Diff/map each item → proposed destination; gap report only

**Phase 1 — Inventory + routing**
- [ ] Manifest: item id → destination + status (`needs_review` / `filed` / `skip`)
- [ ] CLI: `discover` / `status` / `list` on export file

**Phase 2 — Review + file**
- [ ] Minimal review UI or markdown checklist (same pattern as bookmark sorter)
- [ ] On file: append pointer lines to correct Inc markdown (no raw chat URLs unless you opt in)

**Phase 3 — Launcher (optional)**
- [ ] Hub card under Formulated ideas

#### Out of scope (v1)
- Scraping chatgpt.com while logged in
- Auto-deleting ChatGPT messages
- Committing private chat URLs

**Related:** §5 Business Bookmark Sorting; §8 Drive sorter; same pillar model.

---

### 18. Abuja area opportunity scan + SME Compliance Lite (NEW — Jul 2026)
**Status:** Discovery in progress — **no product code**; agent-only scan + MVP brief  
**One-liner:** Ethically discover Abuja corridor business opportunities via Cursor agent (not Field Intelligence Android, not extending `abuja_lead_generator/` yet); advance **SME Compliance Lite** as reminders + checklists (**no CAC/FIRS document custody**).  
**Conversation handoff (2026-07-20):** **Safe to delete** the discovery chat — progress lives here + files below.

#### Decisions locked
| Decision | Choice |
|----------|--------|
| Primary discovery mode | **Agent-only** (`prompts/abuja_area_opportunity_scan.txt`) — not drive-around Android as default |
| `abuja_lead_generator/` extension | **Deferred** until agent-only proves need for DB/outreach factory |
| Field Intelligence Android migrate | **Deferred** (optional capture-only later; not the engine) |
| Agent formulation run (S5–15) | **Separate** — area scan may feed it later; not a new Strategy 16 yet |
| Opportunity lens | **All-sector** (not real-estate-only); **Digital/Hybrid/Physical** quotas in prompt |
| SME Compliance Lite custody | **No see/store** of CAC/FIRS docs — checklists + due dates + WhatsApp reminders only |
| Problem provenance | Stonehill: https://stonehillresearch.com/the-hidden-cost-of-compliance-in-nigerias-msme-sector/ |

#### Artifacts (repo)
| Artifact | Path |
|----------|------|
| Area-scan prompt | `prompts/abuja_area_opportunity_scan.txt` |
| Scan outputs | `agent-business-idea-runs/outputs/abuja_area_opportunities_20260710.md` (v1 RE-heavy), `_v2.md` (all-sector), `_v3.md` + `.docx` (**use v3**) |
| Compliance Lite brief | `agent-business-idea-runs/outputs/sme_compliance_lite_mvp_brief_20260710.md` + `_r4.docx` (**use r4**) |
| Manual / WTP steps | `agent-business-idea-runs/MANUAL_TEST.md` § Area scan / Compliance Lite |

#### Done
- [x] Rethink Field Intelligence vs agent vs leads (ethos: desk discovery first)
- [x] Canonical area-scan prompt (all-sector + digital modality quotas + RE caps)
- [x] Agent runs: v1 → v2 → **v3** dated outputs
- [x] User interest: v3 #2 SME Compliance Lite → pivot off vault
- [x] MVP brief (no custody) + Stonehill problem source + Word `r4`

#### Pending
- [ ] **WTP:** 5 Wuse II / Garki owner interviews per brief §8 (go/no-go) — see `MANUAL_TEST.md`
- [ ] If go → Phase 0 product task (disclaimer copy + checklist/reminder MVP; **no vault**; layout folder TBD)
- [ ] If no-go → revisit v3 Digital #5 (merchant ledger) or #3 (tutor match)
- [ ] Optional: Hub card to paste area-scan prompt (like formulation run) — only after WTP path chosen
- [ ] Optional: feed top Digital rows into a future agent formulation Pass 1
- [ ] Do **not** build Field Intelligence port or lead-generator area scanner unless explicitly reopened

#### Out of scope (until approved)
- Implementing Compliance Lite app/code
- Extending `abuja_lead_generator/` for geo opportunity scoring
- Migrating Field Intelligence Android into Inc
- New Strategy 16 solely for area scanning

**Layout note:** Stay under `agent-business-idea-runs/outputs/` + `prompts/` for discovery; new product folder only after WTP go + task Phase 0 approve.  
**Related:** §6 PropTech (verify-ops parked from area v1 — separate GTM); `abuja_lead_generator/` (My leads pillar).

---


### 19. Daily unattended formulation Pass 1→2 (Cursor Automations) (NEW — 2026-07-23)
**Status:** Phase **0–1 done** (2026-07-23, on `origin` `c0a51d2`/`c9e1961`) — **Phase 2 blocked** pending owner Privacy decision: Cursor requires leaving **Privacy Mode (Legacy)** (one-way; see `prompts/IMPORTANT_cursor_privacy_mode_legacy.md`). Automation A draft was approved in Agents Window; editor blocked until privacy switch or Cancel → park cloud path.
**One-liner:** Replace manual Hub two-run (clipboard paste + Enter) with **daily Cursor Automations** that run **Pass 1 Discover** then **Pass 2 Pack** so `business_ideas_YYYYMMDD.md` + matching `.docx` land in-repo without babysitting — **without breaking** Hub, tray schedules, strategy CLIs, §11/§13 gates, or the §14 contract.
**Full phased backlog:** see **§19** under Notes / formulation tasks below.
**Locks (2026-07-23):** Cadence = **daily**; Autonomy = **B** (cloud Automations); Scope = Inc **A** now + **B** later opt-in; **C** = reminder only; **Phase 0 table** in Notes §19 (07:00 / 11:00 WAT; PR not direct main; cloud; Docx in-repo only; fetch separate).
**Phase 1 shipped:** `prompts/CLOUD_FORMULATION_AUTOMATIONS.md` + README pointers; prompt inventory on `origin` (`2e964fb`); static smokes **26 passed** (2026-07-23).
**Depends on:** §14 v1 CLOSED (prompts, `FORMULATION_PASS_CONTRACT.md`, `idea_card_schema.py`, Hub Pass 1/2 cards remain source of truth).
**Layout:** Prefer **Cursor Automations** (dashboard / Agents Window) + existing `prompts/` + `agent-business-idea-runs/outputs/`. Do **not** create a third formulation product folder. Hub cards stay as **manual override**.
**Manual tests (you):** None until Phase 2+ exists — then one live cloud-run sign-off section in `agent-business-idea-runs/MANUAL_TEST.md` (Automate-first otherwise).
**Related:** §14; §4 Phase 5.5 (tray Hub nudge — separate path); reminder to integrate pattern **C** in other repos later (not here).

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

### Software Development — Client follow-up playbook (NEW — Jul 2026)
**One-liner:** Ethical post-delivery client contact playbook for hard-to-reach software clients (Started business ops doc — not a product build).

**Canonical doc:** [`Started-Businesses/software-development.md`](../../Started-Businesses/software-development.md) — sections *Client follow-up playbook* + *Ethical hacks*.

**No new task file needed** — stay on `.cursor/rules/task.md` (this section).  
**No MANUAL_TEST.md** — ops/process documentation only; no app UI or automate-first product tests.

#### Progress (2026-07-20)
- [x] Ethical contact principles (do/don’t) documented
- [x] Pre-delivery contract hooks + post-delivery touchpoint schedule
- [x] Message templates (check-in, light ping, day-to-day contact, end-of-support, testimonial)
- [x] Silence protocol + per-client internal checklist
- [x] Ethical hacks table (15 tactics + red lines) + highest-ROI combo

#### Pending (optional — approve before agent work)
- [ ] Customize highest-ROI combo + message for one named hard-to-reach client
- [ ] Draft standard post-delivery contract clause (acceptance + support window + check-ins)
- [ ] Nigeria-specific channel notes (WhatsApp norms) in playbook
- [ ] One-page printable client handover checklist
- [ ] Stage / commit / push `Started-Businesses/software-development.md` + this task entry (user decides)

#### Conversation close-out (2026-07-20)
- **Safe to delete this chat.** Durable content is in `Started-Businesses/software-development.md` + this task section. No open agent work, no secrets-only-in-chat, no MANUAL_TEST blocker.

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
**Status:** **CLOSED** (all phases done)  
**Goal:** Remove manual ChatGPT Vision image workflow from the active automation pipeline (no in-repo Vision API; manual upload/paste only). Use Strategies 3–5 for construction/real estate problem discovery.

- [x] **Phase 1 — Master runner:** Remove Strategy 10 from `STRATEGY_SCRIPTS` / `STRATEGY_META` in `run_all_strategies.py`; add to `RETIRED_STRATEGIES` with clear menu messaging; update `run_all_strategies_README.md`.
- [x] **Phase 2 — Cross-references:** Remove Strategy 10 from API docs; update Drive mapping in this task file.
- [x] **Phase 3 — Strategy 10 folder:** Archive legacy script to `_archive/visual_content_analyzer_legacy.py`; stub `visual_content_analyzer.py`; add `DEPRECATED.md`; deprecate playbook markdown.

**Conversation handoff (sidebar “Strategy 10 overview” — 2026-07-20):** **Safe to delete that chat.** Retirement is complete in runner + folder archive. **Manual tests:** none. Cross-ref: top **Sidebar chat batch assess** row 9.

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
**Status:** **CLOSED / v1 complete** (2026-07-12) — Phases **0–6** shipped; automated sign-off green; **no user manual tests pending**  
**Shipped on `main`:** `b95aa77` (runnable S1 end-to-end), `fe3780a` (automate Hub/menu/playbook sign-off)  
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

**v1 definition of done:** ✅ Strategy 1 is a technical strategy end-to-end (script + runner + agent path + docs); gadget ops untouched; automated regression + sign-off PASS 2026-07-12 (`test_phase6_regression.py`, `test_signoff_automated.py`). **No human MANUAL_TEST steps for v1.**

#### Pending after v1 (optional — new work needs approval; not blockers)

| Item | Status | Notes |
|------|--------|-------|
| **§11** Always-online S1 / retire seeds | **CLOSED** | Phases A–D 2026-07-12 |
| **5.4** research URL helper (`--open-links`) | Deferred | Opt-in only; may merge later if needed |
| Strategy **2** verbal → technical | Out of scope | Open a **new** task entry if/when requested |
| Gadget-business automation improvements | Separate | Do not fold into S1 formulation task |

#### Conversation close-out (2026-07-12) — v1 + §11

- Authoritative tracker: **this file** (`.cursor/rules/task.md` §9 + Current Priority §10/§11) — **no separate task file needed**.
- Product docs/tests: `Strategy-1-Business-Variation/` (`README.md`, `MANUAL_TEST.md`, smokes including `test_phase11_signoff.py`).
- **§11 shipped on `origin/main`:** `e383983` (retire seeds; URL-cited intake; `strategy_1_discovery`).
- **You may delete chats** that delivered Strategy 1 v1 and §11 always-online work: nothing pending that only exists in conversation memory. Optional next formulation run is not a delete-blocker.

#### Explicitly out of scope (v1)
- Strategy **2** verbal→technical conversion.
- Full Twitter/Reddit/App Store scrapers; paid Brand24/Mention integrations.
- Rewriting or relocating `gadget-business-automation/`.
- Renaming strategy folder to `Business-Idea-Formulation-Strategy-1-*` (defer unless approved).
- Changing retired Strategies 8/10 policy.
- Google Drive Macrodroid card renames.

#### Tier / phase approval checkpoints (user) — v1
- [x] Approve **Phase 0** locks (names + Run ALL policy for including `1`) — done 2026-07-11 via “Implement only Phase 0”.
- [x] Approve **Phase 1** (folder scaffold) — done 2026-07-11 via menu “1 - recommend and approve”.
- [x] Approve **Phase 2** (CLI intake + non-interactive) — done 2026-07-11 via menu “1”.
- [x] Approve **Phase 3** (master runner wiring) — done 2026-07-11 via menu “1”.
- [x] Approve **Phase 4** (agent prompt + fetch) — done 2026-07-12 via menu “1”.
- [x] Approve **Phase 5** (launcher/docs) — done 2026-07-12 via menu “1”.
- [x] Approve **Phase 6** (regression & v1 sign-off) — done 2026-07-12 via menu “1 - pls do not break anything”.
- [x] Automate former MANUAL A–D — done 2026-07-12 (`fe3780a`); `MANUAL_TEST.md` = no user steps.

**Suggested milestones:** Phase 0–6 ✅ 2026-07-11/12 — **v1 closed.** §11 A–D ✅ 2026-07-12 — **always-online closed** (`e383983`).

**Related:** Chat 2026-07-11 (S1 verbal→technical recommendations); Strategy 15 wiring pattern (task §5); Crunchbase/S6–S7 additive safety pattern (task §8); `prompts/agent_formulation_run.txt`; `inc_launcher` Established vs Formulated pillars.

---

### 11. Strategy 1 — Always-online discovery; retire `seed_businesses.json` (NEW — Jul 2026)
**Status:** **CLOSED / complete** (2026-07-12) — Phases **A–D** shipped  
**Parent:** §9/§10 Strategy 1 v1 (closed). This task **changed** the v1 seed-first intake model.

**Goal:** For Strategy 1, **always go online** to find (a) successful businesses/startups and (b) recurring gaps/complaints with **real citeable sources** in outputs — for **agent formulation runs** and **regular CLI/Hub Strategy 1 use**. Retire `seed_businesses.json` as a live input (no canned `example_complaints` as problem statements).

**User locks (2026-07-12):**
- Do **not** prefer / require `seed_businesses.json` for agent or CLI formulation.
- S1 formula unchanged: *Successful Business + Recurring Complaint = Profitable Variation* (still **not** S6 niche-combo or S7 trending-adapt alone).
- Every S1-traced idea in `business_ideas_YYYYMMDD.md` / `.docx` must show **online source(s)** for the complaint (and preferably for why the business is “successful”).
- Same online standard for normal Strategy 1 collector runs — not agent-only.

**Layout:** Stay in `Strategy-1-Business-Variation/` + `prompts/agent_formulation_run.txt` + `agent-business-idea-runs/` as needed. No gadget-ops changes.

#### Proposed phases (approve before coding)

| Phase | Scope | Done when |
|-------|--------|-----------|
| **A — Spec & prompt** | Update `prompts/agent_formulation_run.txt`: S1 must web-discover businesses + gaps; cite URL/title/date/quote; **forbid** seed-file complaints as sole problem evidence; update agent README S1 section | Prompt + docs match user locks; still no collector rewrite required if deferred to B |
| **B — Collector / CLI** | Replace seed-driven intake in `business_variation_collector.py` / `seeds.py` / `complaint_intake.py` with online discovery path (or explicit paste-of-URLs); retire or archive `seed_businesses.json`; Hub/Run ALL must not depend on seeds | CLI + non-interactive path works without seeds; Run ALL does not hang |
| **C — Agent fetch** | Change `agent_strategy_run.py`: stop shipping `strategy_1_seeds` from local JSON as primary; optional live fetch keys (or document agent-native web research); soft-fail must not abort whole agent run | Fetch JSON + execution summary reflect online/cited S1 |
| **D — Tests & sign-off** | Update Phase 4/6 smokes that assert `strategy_1_seeds` / seed `example_complaints`; automate-first; `MANUAL_TEST.md` only if truly non-automatable | Regression green; Docx sample shows cited complaints |

#### Safety
- One phase at a time; no big-bang unless user says so.
- Do not break other strategies, agent RSS/OWID/S6/S7/S14/S15 paths, or gadget automation.
- Non-interactive/CI: use **fixture URLs / recorded HTML** if live web is flaky — **not** a return of canned business+complaint seed lists as the product path.
- Paid scrapers (Brand24 etc.) still optional / out of scope unless later approved.

#### Checkpoints (user)
- [x] **Approve task entry** — 2026-07-12 (menu “1”).
- [x] Approve **Phase A** (prompt/docs only) — done 2026-07-12 via “1 - recommend and proceed”.
- [x] Approve **Phase B** (CLI/collector retire seeds) — done 2026-07-12 via “1 - recommend and proceed”.
- [x] Approve **Phase C** (agent fetch) — done 2026-07-12 via “1 - recommend and proceed”.
- [x] Approve **Phase D** (tests/sign-off) — done 2026-07-12 via “1 - recommend and proceed”.

**Phase A shipped (2026-07-12):** Prompt + agent README require always-online S1 + citeable URLs.

**Phase B shipped (2026-07-12):** Seeds archived; CLI URL-cited intake; `--seed-ids` rejected.

**Phase C shipped (2026-07-12):** Removed top-level `strategy_1_seeds`. Added `strategy_1_discovery`.

**Phase D shipped (2026-07-12):** `test_phase11_signoff.py` (no live seeds; URL-cited collector; discovery unit; Docx citation sample via `convert_md_to_docx` without opening Word); wired into `test_phase6_regression.py`; `MANUAL_TEST.md` + API guide updated. **§11 closed.**

**Shipped on remote:** `e383983` on `origin/main` (2026-07-12).

#### Conversation close-out (2026-07-12) — §11
- **Safe to delete this chat.** Tracker = this file §11 + Current Priority §11; tests = `Strategy-1-Business-Variation/MANUAL_TEST.md` (no user steps).
- **Pending (optional only):** Re-run Hub/agent formulation so the next `business_ideas_YYYYMMDD.md/.docx` S1 ideas cite live URLs (same-day earlier run used pre-§11 seeds). Not required to close §11; not a MANUAL_TEST item.

**Related:** Chat 2026-07-12 (S1 Docx showed seed/AI gaps → always-online); §9 Phase 1.2 seeds (superseded); `prompts/agent_formulation_run.txt`; `agent-business-idea-runs/`.

---

### 12. Prospect-Businesses shortlist — conversation close-out (2026-07-12)

- **CLOSED / v1 complete** — Phases 0–4 (Hub 3.1 + sorter 3.2).
- **Authoritative tracker:** Current Priority **§12** + §4 nested **Prospect-Businesses folder**.
- **Git:** `d0f6e10`, `4a95968`, `d3db322` on `origin/main`.
- **Manual tests (you):** **None required** (`inc_launcher/MANUAL_TEST.md` §H).
- **Safe to delete the chat that delivered Prospect-Businesses + this formulation run handoff.** Optional pending items (discovery calls; commit `business_ideas_20260712.*` if desired; S1 live-cite re-run) are written in §12 / prospect `.md` files — not chat-only.

---

### 13. Strategy 12 — GUEMF dual-mode (standalone + overlay) (NEW — Jul 2026)
**Status:** **CLOSED / v1 complete** (2026-07-15) — Phases **0–4** shipped  
**Parent / Current Priority:** §13  
**Related:** Google Drive “Business 10th — GUEMF” → Strategy **12**; cyber vertical §9 Phase 3 (optional GUEMF pipe — consumer of this work later).

**Goal:** Strategy 12 must work as:

| Mode | Description | Today |
|------|-------------|--------|
| **Standalone** | Discover/filter high-value problems via Growing / Urgent / Expensive / Mandatory / Frequent; produce S12 outputs; runnable alone + via `run_all_strategies.py` | `problem_filter.py` exists but **interactive-only** (`input()`); agent does not treat S12 as a generator |
| **Overlay (B)** | Score ideas from other strategies with GUEMF in agent ranked tables | **Already works** — keep explicit |
| **Agent dual** | Multi-strategy agent run must do **Mode A** (S12-origin / Prompt-1a-style GUEMF discovery → S12-traced ideas) **and** **Mode B** (overlay) | Prompt lists `12` + “GUEMF-style scoring where relevant” → agents only do **B** |

**User locks (2026-07-15):**
- Mode A ideas → **same** ranked table; primary strategy trace includes **S12**.
- Agent GUEMF scale remains **1–5** per criterion (composite sum max 25) to match recent `business_ideas_YYYYMMDD.md`.
- CLI can keep historic **0–1 / total 0–5** scoring for interactive parity; document mapping to agent 1–5 when synthesizing (do not silently break interactive Y/N UX).
- Additive modularization — **do not break anything anywhere** (see Safety).

**Layout (locked unless later approved):**
- Stay in `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/`
- Prefer **new small modules** over a monolithic rewrite of `problem_filter.py` (e.g. scoring helpers, JSON I/O, argparse entry)
- Touch also (later phases): `prompts/agent_formulation_run.txt`, `agent-business-idea-runs/README.md`, optional soft key in `agent_strategy_run.py`
- **Do not** create a second GUEMF product outside Strategy 12

#### Modularization / anti-break rules (apply every phase)

1. **Interactive default preserved** — bare `python problem_filter.py` (and menu launch) still runs today’s `input()` flow until deliberately replaced behind flags.
2. **New behavior behind flags** — `--non-interactive`, `--inputs`, optional `--output`; never change Run ALL menu contract without a sub-phase.
3. **One surface per sub-phase** — e.g. scoring helper ≠ prompt text ≠ agent fetch key in the same PR-sized change unless user okays a bundled ship.
4. **Soft-fail on agent path** — empty S12 Mode A must not abort RSS/OWID/S1/S6/S7/S14/S15; status `synthesized` / `blocked` / `ran` with notes.
5. **No drive-by refactors** of Strategies 1, 5–7, 9, 11, 13–15, Hub launcher, or gadget ops.
6. **Automate-first verification** — pytest/smoke in S12 folder; update `MANUAL_TEST.md` only for leftover non-automatable steps.

#### Phase 0 — Spec lock & inventory (docs only; zero runtime risk) ✅

**Why first:** Freeze dual-mode contract before touching CLI so agent prompt and tests share one vocabulary.

- [x] **0.1 — Contract note in S12 README:** Mode A vs Mode B; CLI 0–1 vs agent 1–5 mapping; Mode A ideas in same ranked table with S12 trace (`README.md` — Dual-mode contract).
- [x] **0.2 — Inventory:** Entrypoints, runner registration, overlay-only prompt phrases — `PHASE0_INVENTORY_AND_ACCEPTANCE.md`.
- [x] **0.3 — Acceptance sketch:** Executable checklist for Phases 1–4 — same file §0.3.

**Phase 0 definition of done:** ✅ README/contract + inventory/acceptance docs; **no** behavior change to `problem_filter.py`, `run_all_strategies.py`, `agent_strategy_run.py`, or `prompts/agent_formulation_run.txt` (prompt = Phase 2).

**Phase 0 shipped (2026-07-15):** Dual-mode contract + Phase 0 inventory/acceptance; stale README `steps.py` name corrected to `problem_filter.py`.

#### Phase 1 — CLI standalone (non-interactive; modular) ✅

**Goal:** Strategy 12 can score/rank without `input()` so standalone + menu-launched scripts can complete in CI/agent wrappers.

- [x] **1.1 — Extract scoring module** `guemf_scoring.py`: pure normalize/rank/require-complete; CLI↔agent band helpers; no argparse/file side effects.
- [x] **1.2 — JSON inputs schema** `fixtures/INPUTS_SCHEMA.md` + `fixtures/sample_inputs.json` (complete `criteria_scores` required — no invented Y/N).
- [x] **1.3 — Wire `--non-interactive --inputs`** on `problem_filter.py`; optional `--output`, `--select-min-score`, `--open`; non-interactive skips auto-open by default.
- [x] **1.4 — Keep interactive `run()` path** for bare script / `run_all_strategies.py` menu (shared scoring helpers only).
- [x] **1.5 — Smoke:** `test_strategy12_noninteractive.py` — **7 passed** (2026-07-15).

**Phase 1 definition of done:** ✅ Non-interactive standalone run green; interactive path preserved; menu still points at same script.

**Phase 1 shipped (2026-07-15):** Modular scoring + NI CLI + fixture + smokes. **Does not** change agent Mode A (Phase 2).

#### Phase 2 — Agent prompt dual-mode (Mode A + Mode B) ✅

**Goal:** Multi-strategy agent runs must produce S12-traced ideas **and** keep overlay scoring.

- [x] **2.1 — Update `prompts/agent_formulation_run.txt`:** Explicit Mode A (Prompt 1a-style → S12-traced ideas) **and** Mode B (GUEMF 1–5 overlay); execution summary must note **both** legs; removed overlay-only “where relevant” as sole GUEMF instruction.
- [x] **2.2 — Update `agent-business-idea-runs/README.md`:** Strategy 12 dual-mode section; optional NI CLI as aid.
- [x] **2.3 — Static assert:** `test_strategy12_prompt_dual_mode.py` — markers present; old overlay-only phrase absent (**8** S12-related pytest cases incl. Phase 1 when run together, 2026-07-15).

**Phase 2 definition of done:** ✅ Prompt + agent README require dual-mode; next agent formulation run can satisfy Mode A without fetch-runner edits.

**Phase 2 shipped (2026-07-15):** Prompt dual-mode + README + static smoke. Fetch `strategy_12_*` still optional (Phase 4).

#### Phase 3 — Docs, MANUAL_TEST, regression gate ✅

- [x] **3.1 — S12 README script section:** Interactive vs `--non-interactive --inputs` + fixture (shipped Phase 1; still current).
- [x] **3.2 — `MANUAL_TEST.md`:** Automate-first — **no remaining manual steps** for dual-mode Phases 0–3.
- [x] **3.3 — Regression bundle:** `test_strategy12_regression.py` (+ NI + prompt smokes) — **10 passed** 2026-07-15; confirms `STRATEGY_SCRIPTS[12]` + neighbors 1,5–7,9,11,13–15; 8/10 retired.
- [x] **3.4 — Cross-ref:** Cyber §9 Phase 3 note points at S12 NI CLI (consumer later; no cyber code this task).

**Phase 3 definition of done:** ✅ Automated green; docs match; cyber optional consumer noted.

**Phase 3 shipped (2026-07-15):** MANUAL_TEST (no user steps) + regression bundle + cyber one-liner.

#### Phase 4 — Optional soft agent fetch integration ✅

**Goal:** Optional `strategy_12_*` in `agent_strategy_run.py` without aborting the fetch.

- [x] **4.1 — Soft block:** `strategy_12_run` skipped by default; `--with-strategy12` runs non-interactive against fixture / `--strategy12-inputs`; failures → status in JSON only.
- [x] **4.2 — Mode A remains agent-native** — fetch note states Mode B aid only; does not replace Mode A synthesis.
- [x] **4.3 — Smoke:** `test_strategy12_fetch_soft.py` (default skip flag; fixture run ok; missing inputs soft status).

**Phase 4 definition of done:** ✅ Optional soft fetch shipped; default agent fetch path unchanged for other keys.

**Phase 4 shipped (2026-07-15):** `--with-strategy12` + `strategy_12_run` in fetch JSON.

#### Explicitly out of scope (this task)

- Replacing or retiring Mode B overlay.
- Changing strategy numbers/folders; building a separate “GUEMF app.”
- Rewriting Strategies 1, 5–7, 9, 11, 13–15; Hub Inc formulation front door Phase 5.
- Cybernews vertical full Phase 3 implementation (may call S12 later).
- Forcing paid news APIs for Mode A.

#### Checkpoints (user)

- [x] **Approve task entry** — 2026-07-15 (menu “1”).
- [x] Approve **Phase 0** (docs/contract only) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 1** (CLI modular non-interactive) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 2** (agent prompt dual-mode) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 3** (docs/tests/sign-off) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 4** (optional fetch) — done 2026-07-15 via menu “1”.

**Suggested milestones:** Phase 0–4 ✅ **2026-07-15** — **dual-mode v1 closed.**

**v1 definition of done:** ✅ Standalone NI CLI + interactive preserved; agent prompt requires Mode A+B; soft `strategy_12_run`; automated suite green (`pytest Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering -q` — **13 passed** 2026-07-15). **No human MANUAL_TEST steps.**

#### Conversation close-out (2026-07-15) — §13
- **Safe to delete this chat.** Tracker = Current Priority §13 + Notes §13; tests = S12 folder `MANUAL_TEST.md` + pytest suite.
- **Pending (optional only):** Re-run Hub/agent formulation so next `business_ideas_YYYYMMDD` includes S12 Mode A–traced ideas + dual-leg execution summary.

**Related:** Chat 2026-07-15 (GUEMF overlay-only diagnosis + ASCII); `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/`; `prompts/agent_formulation_run.txt`; `run_all_strategies.py` already registers S12; Strategy 1 non-interactive / agent soft-fail patterns (§9 / §11).

---

### 14. Agent formulation — Pass 1 Discover / Pass 2 Pack (prompt split) (NEW — Jul 2026)
**Status:** **CLOSED / v1 complete** (2026-07-15) — Phases **0–5** ✅  
**Parent / Current Priority:** §14  
**Related:** Inc Hub Phase 5; §11 S1; §13 S12; `agent-business-idea-runs/`; Docx via `business_bookmark_sorter/docx_export.py`.  
**Artifacts:** `prompts/FORMULATION_PASS_CONTRACT.md`; `prompts/agent_formulation_pack.txt`; Discover defer Docx; `idea_card_schema.py`; Hub `agent_formulation_pack`; proof `business_ideas_20260715.md` packed.

**Goal:** Restore **consistent idea-card distribution** in `business_ideas_YYYYMMDD.md` / `.docx` by splitting agent work into two jobs:

| Pass | Job | Output duty |
|------|-----|-------------|
| **1 — Discover** | Strategies, evidence, invent, score, dedup, rank, Best ideas, execution summary | Content-complete draft `.md` (uneven cards OK) |
| **2 — Pack** | Rewrite **every** ranked idea to a **fixed subhead checklist**; then Docx **once** | Packed `.md` + paired `.docx` |

**Diagnosis locked (2026-07-15):** Jul 15 run was §13-gate-complete but idea details dropped per-card **Regulatory**, uneven **Competitors** shape vs Jul 13 — one mega-prompt over-optimized for gates over schema.

**User locks (2026-07-15):**
- Prefer **two different jobs**, not two copies of the same mega-prompt.
- Required card labels (exact / near-exact): Problem (or S1 Formula+citations), Solution, Target, MVP cost, **Regulatory**, **Competitors / alternatives** (2–4 + per-item why-Nigeria-buyer line), GUEMF (Mode A or B), Commercial viability, Dedup, Founder fit.
- S1 / S12 Mode A extras are **add-ons**, never replacements for the shared list.
- Incomplete Pass 2 = any ranked idea missing Regulatory, Competitors block, Solution, Target, or MVP cost.
- Docx convert/open stays **Pass 2 only**, one-shot (existing rule).

**Layout (locked unless later approved):**
- Keep prompts under repo-root `prompts/`
- **Add** `prompts/agent_formulation_pack.txt` (Pass 2) — do **not** delete `agent_formulation_run.txt` in early phases
- Pass 1 stays the discover file (`agent_formulation_run.txt` after Phase 2 trim, or alias kept for Hub default)
- Optional validator module under `agent-business-idea-runs/` only (new small file) — **not** inside strategy folders
- Docs: `prompts/README.md`, `agent-business-idea-runs/README.md`
- **Do not** create a third formulation product or a second outputs folder

#### Modularization / anti-break rules (apply every phase)

1. **Hub default preserved until Phase 4** — `inc_launcher` `DEFAULT_PROMPT_PATH` / card `agent_formulation_run` continues to load `prompts/agent_formulation_run.txt` until an explicit additive Hub sub-phase ships.
2. **Additive files first** — new pack prompt + docs before rewriting discover prompt; never “swap path + rewrite” in one hop.
3. **No strategy-script edits** — do not touch `Business-Idea-Formulation-Strategy-*/`, `run_all_strategies.py`, or gadget ops for this task.
4. **Preserve §11 / §13 gates** — Pass 1 keeps S1 online cites + S12 Mode A (≥2 primary S12) + Mode B overlay; moving text between files must not drop gates.
5. **One surface per sub-phase** — pack prompt ≠ discover trim ≠ schema validator ≠ Hub second card, unless user okays a bundled ship.
6. **Soft-fail / non-abort** — Pass 2 must not invent fake competitors or silently change ranks; soft-fail missing fields = mark incomplete and fill from Pass 1 evidence, or note gap.
7. **Automate-first** — static asserts on prompt files + optional markdown schema smoke; `MANUAL_TEST.md` only for leftover non-automatable Hub UX.
8. **No drive-by** Hub Phase 5 rewrite, Prospect folder changes, or Docx exporter refactors beyond calling existing `regenerate_and_open_docx`.

#### Phase 0 — Spec lock & inventory (docs only; zero runtime risk) ✅

**Why first:** Freeze idea-card contract + Pass duties before editing either prompt so Hub and smokes share one vocabulary.

- [x] **0.1 — Idea-card contract** in `prompts/FORMULATION_PASS_CONTRACT.md` (§0.1): required subheads; S1/S12 add-ons; incomplete definition; Pass 1 vs Pass 2 ownership table.
- [x] **0.2 — Inventory:** Who loads `agent_formulation_run.txt` today — Hub `agent_run.py` / `actions.py` / pinned card, README pointers, §11/§13 prompt smokes (`FORMULATION_PASS_CONTRACT.md` §0.2).
- [x] **0.3 — Acceptance sketch:** Executable checklist for Phases 1–5 — same file §0.3.
- [x] **0.4 — README pointer:** `prompts/README.md` lists contract + notes Pass 2 file not created yet.

**Phase 0 definition of done:** ✅ Contract + inventory + acceptance docs; **no** edits to Hub config, `agent_formulation_run.txt` body, strategy scripts, or `agent_strategy_run.py`.

**Phase 0 shipped (2026-07-15):** `prompts/FORMULATION_PASS_CONTRACT.md` + README pointer.

#### Phase 1 — Add Pass 2 pack prompt (additive; discover unchanged) ✅

**Goal:** Ship a standalone pack prompt agents can paste second, without changing Pass 1 or Hub.

- [x] **1.1 — Create** `prompts/agent_formulation_pack.txt`: fixed card checklist; Best ideas must reference packed details; Docx one-shot only after all cards pass; no new invent/re-rank by default.
- [x] **1.2 — README one-liners:** `prompts/README.md` documents Pass 1 file vs Pass 2 file and run order; agent README points at pack file.
- [x] **1.3 — Static smoke:** `agent-business-idea-runs/tests/test_formulation_pack_prompt.py` — pack markers + discover still present; §13 dual-mode prompt smoke still green.

**Phase 1 definition of done:** ✅ Pack file exists + documented + static assert green; Hub still single-prompt; discover mega-prompt **unchanged**.

**Phase 1 shipped (2026-07-15):** Pack prompt + README + smoke (3 passed with S12 dual-mode smoke).

#### Phase 2 — Slim Pass 1 discover prompt (content only; Docx deferred) ✅

**Goal:** Move schema-lock + Docx ownership out of Pass 1 so discover stops competing with formatting.

- [x] **2.1 — Trim** `agent_formulation_run.txt`: keep strategies, S1, S12 dual-mode, dedup, Best ideas, ranked table, viability, execution summary; ends with Pass 2 pack required + `agent_formulation_pack.txt`; Docx status `_PENDING_PASS_2_PACK_`; no Pass 1 convert/open.
- [x] **2.2 — §11/§13 preserved** — dual-mode + S1 markers still present (`test_strategy12_prompt_dual_mode.py` + pack discover asserts green).
- [x] **2.3 — Agent README:** Two-pass workflow documented; same outputs path.

**Phase 2 definition of done:** ✅ Discover is content/gate-focused; pack owns card uniformity + Docx; §13 prompt tests still pass.

**Phase 2 shipped (2026-07-15):** Discover deferral + README + smoke updates.

#### Phase 3 — Optional schema validator (modular aid; non-blocking) ✅

**Goal:** Automate “does this `.md` have Regulatory + Competitors on every idea?” so Pass 2 gaps are detectable without human reading.

- [x] **3.1 — New module** `agent-business-idea-runs/idea_card_schema.py`: parse Idea details cards; require Solution/Target/MVP cost/Regulatory/Competitors (+ Problem spine); exit non-zero on miss — **read-only**.
- [x] **3.2 — Fixture smoke:** `fixtures/idea_cards_good.md` + `idea_cards_bad.md`; `tests/test_idea_card_schema.py` (4 passed).
- [x] **3.3 — Soft integration:** README + pack prompt “run after Pass 2 before Docx”; **not** in Hub Start; **not** in `agent_strategy_run.py` (asserted in smoke).

**Phase 3 definition of done:** ✅ Validator exists + tested; Hub/fetch paths unchanged.

**Phase 3 shipped (2026-07-15):** Schema CLI + fixtures + MANUAL_TEST (no user steps).

#### Phase 4 — Hub / clipboard (additive; optional second card) ✅

**Goal:** Make two-pass usable from Inc Hub **without** breaking the existing Agent formulation run.

- [x] **4.1 — Keep** primary card `agent_formulation_run` → Pass 1 discover path (same id / action / pinned).
- [x] **4.2 — Add** `agent_formulation_pack` → `prompt_path` `agent_formulation_pack.txt`; custom `modal_title` / `modal_bullets`; **not** pinned.
- [x] **4.3 — Tests:** config + `test_agent_run` pack path + phase5 pack modal/load asserts; Discover pin preserved.
- [x] **4.4 — Fallback:** paste-two-files still valid via `prompts/`.

**Phase 4 definition of done:** ✅ Hub supports both prompts additively; Discover stays primary pin.

**Phase 4 shipped (2026-07-15):** Formulated Pass 2 card + modal item overrides.

#### Phase 5 — Docs, MANUAL_TEST, regression, sign-off ✅

- [x] **5.1 — Cross-READMEs** aligned (`prompts/`, `agent-business-idea-runs/`, Hub README).
- [x] **5.2 — `MANUAL_TEST.md`:** Automate-first; leftover = Cursor Enter send only.
- [x] **5.3 — Regression bundle:** pack asserts + §13 dual-mode + schema + Hub config/agent_run (2026-07-15). Tk modal tests may need a healthy local Tk install.
- [x] **5.4 — Proof run:** Pass 2 packed `business_ideas_20260715.md` → `idea_card_schema` **PASS (12)** → Docx one-shot OK.

**Phase 5 definition of done:** ✅ Automated green for formulation surfaces; proof shows uniform cards; §14 v1 closed.

**Phase 5 shipped (2026-07-15):** Sign-off + Jul 15 packed Docx proof.

#### Checkpoints (user)

- [x] **Approve task entry** — 2026-07-15 (menu “2”).
- [x] Approve **Phase 0** (docs/contract only) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 1** (add pack prompt; discover unchanged) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 2** (slim discover; Docx→Pass 2) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 3** (optional schema validator) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 4** (Hub second card) — done 2026-07-15 via menu “1”.
- [x] Approve **Phase 5** (docs/tests/sign-off + optional proof run) — done 2026-07-15 via menu “1”.

**Suggested milestones (from 2026-07-15):**
- Phase 0–5: ✅ **2026-07-15** — **§14 packaging v1 closed.**

**v1 definition of done:** ✅ Pass 2 pack file; Pass 1 discover defers Docx; schema validator; Hub Pass 2 card; static/Hub smokes; proof packed Docx. §11/§13 markers preserved.

#### Explicitly out of scope (this task)

- Rewriting strategy CLIs or `run_all_strategies.py`.
- Changing S12 Mode A/B semantics (§13) or S1 online-discovery rules (§11).
- Replacing Docx library / multi-convert loops.
- Auto-committing formulation outputs.
- Forcing Pass 2 to invent new ideas or re-rank.
- Hub auto-chaining Pass 1→2 without user Start (nice-to-have later).

#### Conversation close-out (2026-07-15) — §14
- **Safe to delete this chat.** Tracker = Current Priority §14 + Notes §14; tests = `agent-business-idea-runs/MANUAL_TEST.md` + `inc_launcher/MANUAL_TEST.md` §G/§G14; code/prompts on `origin/main` as **`2e964fb`**.
- **No new task file needed** — stay on `.cursor/rules/task.md` §14.
- **Hub:** leave as shipped (two cards). Hub does **not** paste a meta-prompt; two Starts = two agent runs.
- **Meta paste drafts** (manual Cursor only; optional — Hub cards preferred):

**RUN 1 of 2 (or Hub “Agent formulation run”):**
```
Inc formulation — AGENT RUN 1 of 2 (Pass 1 Discover only) at C:\dev\Inc.
Follow prompts/agent_formulation_run.txt.
Write agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md.
Do NOT pack cards. Do NOT convert/open Docx. Leave _PENDING_PASS_2_PACK_.
Stop when the draft .md is complete. Do not start Pass 2 in this response.
Read-only on strategy scripts; write under agent-business-idea-runs/ only.
Today’s local date in filenames; PYTHONIOENCODING=utf-8 on Windows.
```

**RUN 2 of 2 (or Hub “Agent formulation pack (Pass 2)”):**
```
Inc formulation — AGENT RUN 2 of 2 (Pass 2 Pack) at C:\dev\Inc.
Follow prompts/agent_formulation_pack.txt on today’s agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md (same file from Run 1).
Normalize every idea to §14 subheads (Regulatory + Competitors / alternatives on every idea).
Optional: python agent-business-idea-runs/idea_card_schema.py <that .md> — fix gaps before Word.
Then one-shot Docx convert/open. Do not invent a new ranked set.
Contract: prompts/FORMULATION_PASS_CONTRACT.md.
```

- **Ongoing use:** Hub card 1 → finish chat → later Hub card 2; optional schema before Docx.
- **Optional later:** modal “Run N of 2” wording (Hub polish). Tray intervals for card 1→2 superseded by **§19** (Cursor Automations).

**Related:** Chat 2026-07-15 (Docx quality → prompt split → two-agent-run meta); `prompts/agent_formulation_run.txt` + `agent_formulation_pack.txt`; Jul 13 vs Jul 15 idea-detail shape.

### 19. Daily unattended formulation Pass 1→2 (Cursor Automations) (NEW — 2026-07-23)
**Status:** Phase **0–1 done** (2026-07-23) — **no Automations created yet**; next = Phase 2 (Automation A only) after approve
**Parent / Current Priority:** §19
**Related:** §14 (Pass 1/2 contract — CLOSED v1); §4 Phase 5.5 (tray Hub modal schedule — **do not merge** into this task); `prompts/agent_formulation_run.txt`; `prompts/agent_formulation_pack.txt`; `prompts/FORMULATION_PASS_CONTRACT.md`; `prompts/CLOUD_FORMULATION_AUTOMATIONS.md`; `agent-business-idea-runs/`; Hub `agent_formulation_run` / `agent_formulation_pack`.

**Goal:** Daily **unattended** cloud agent runs that produce today’s packed idea pack (`.md` + `.docx`) using the **same two-job model** as §14 — Discover then Pack — without requiring Inc Hub Start or Cursor Enter.

**User locks (2026-07-23):**
- Cadence: **daily** — see **Phase 0 decision table** below.
- Autonomy: **Cursor Automations / cloud agents** (not Hub clipboard + paste + Enter).
- Scope for this task: Inc **A** (formulation Pass 1→2 + closely related high-fit) and Inc **B** (medium-fit) only as **later opt-in phases**.
- **C (other repos):** remind only — `project_reminder`, `anki_automation`, BrowserUse/Screenshot, `reelops`, Tegrid/Digi/Cooking Robot, gated trading checks, learning digests — **do not implement under §19**.
- PC power: **cloud = PC may be off**; My Machines / open Word on desktop = **not** default (Phase 0.3–0.4).
- Hub two-card manual path remains valid **override**; do not delete or fuse Hub cards.

**Layout (locked unless Phase 0 changes it):**
- Orchestration = **Cursor Automations** (scheduled / event triggers), not a new Python product.
- Prompts stay under repo-root `prompts/`; outputs under `agent-business-idea-runs/outputs/`.
- Optional small **docs-only** aids under `agent-business-idea-runs/` or `prompts/` (cloud run notes) — no strategy-folder edits.
- Do **not** reopen §14 Phases 0–5 as a rewrite; additive follow-on only.

#### Modularization / anti-break rules (apply every phase)

1. **One surface per sub-phase** — Automation A (Pass 1) ≠ Automation B (Pass 2) ≠ fetch prep ≠ Hub tray schedule ≠ medium-fit B items. Ship one at a time unless user okays a bundle.
2. **Hub left additive** — keep `agent_formulation_run` + `agent_formulation_pack` as manual override; do not remove, rename destructively, or replace with a mega-prompt card.
3. **Do not fuse Pass 1 + Pass 2** into one mega-prompt or one chat that silently does both (§14 operating model stays locked).
4. **No strategy-script edits** — do not touch `Business-Idea-Formulation-Strategy-*/`, `Strategy-1-Business-Variation/` formulation CLIs, or `run_all_strategies.py` for §19.
5. **Preserve §11 / §13 gates** — Pass 1 Automations instructions must keep S1 online cites + S12 Mode A (≥2 primary) + Mode B overlay; soft-fail aids must not abort the run.
6. **Preserve §14 card contract** — Pass 2 must normalize Regulatory + Competitors / alternatives on every idea; no invent/re-rank; Docx **one-shot** after cards pass; optional `idea_card_schema.py` before Word.
7. **Do not break existing tray schedules** — `daily_task_md`, `daily_inc_hub`, `problem_id_live_mwf` stay unless a dedicated schedule-tune task says otherwise. §19 must not hijack Phase 4 nudge IDs for cloud work.
8. **§4 Phase 5.5 stays separate** — tray “open Hub + Option B modal” is a **local nudge**; §19 is **cloud unattended**. Cross-link only; never implement 5.5 inside a §19 phase without explicit approve.
9. **Git / cloud readiness** — cloud agents see **committed remote** state. Phase 0 must lock commit/PR policy for outputs before enabling auto-write. Do not assume unpushed local files exist in the sandbox.
10. **Write scope** — Automations write under `agent-business-idea-runs/` (and agreed commit/PR); read-only on strategy scripts; `PYTHONIOENCODING=utf-8` guidance retained for any Windows-local helpers.
11. **Automate-first verification** — prefer static prompt asserts + schema CLI + existing Hub/config pytest; `MANUAL_TEST.md` only for live cloud-run residual (cannot fully fake Cursor Automations billing/runtime locally).
12. **No drive-by** Hub Phase 5 rewrite, Prospect folder changes, Docx exporter refactors, or other-repo C work in this task.
13. **Rollback-friendly** — prefer disable/pause Automation over deleting Hub or prompt files if a run misbehaves.

#### Phase 0 — Spec lock (docs / decisions only; zero runtime risk) ✅

**Why first:** Lock times, git policy, and cloud vs local side effects before creating any Automation (avoids breaking Hub or polluting outputs).

**Phase 0 decision table (locked 2026-07-23 — menu “1”; change only via explicit re-open):**

| ID | Decision | Lock |
|----|----------|------|
| **0.1** | Clocks | **Pass 1 Discover:** daily **07:00** Africa/Lagos (WAT). **Pass 2 Pack:** daily **11:00** Africa/Lagos (WAT). Soft gate: if today’s draft `.md` missing or not `_PENDING_PASS_2_PACK_`, Pass 2 **no-ops** (no invent). Not “blind sleep after paste.” |
| **0.2** | Git | Automations **open a PR** (branch e.g. `formulation/auto-YYYYMMDD`) against default branch; **you merge**. No direct push to `main`/`master`. (§14 “no auto-commit” superseded **only** for this PR path.) |
| **0.3** | Runtime | **Cursor cloud** (PC may be off). My Machines = later opt-in only. |
| **0.4** | Docx | **Create `.docx` in repo only** — do **not** auto-open Word on desktop. |
| **0.5** | Fetch prep | **Separate** (Phase 4) — not bundled into Automation A v1. |

- [x] **0.1 — Clock times** — 07:00 / 11:00 WAT + Pass 2 soft no-op gate (above).
- [x] **0.2 — Git policy** — PR to default branch; owner merges (above).
- [x] **0.3 — Runtime** — Cursor cloud (above).
- [x] **0.4 — Docx open** — in-repo only (above).
- [x] **0.5 — Fetch prep** — separate Phase 4 (above).
- [x] **0.6 — Acceptance sketch** — see **Acceptance sketch (Phases 1–6)** below.
- [x] **0.7 — Checkpoint** — user menu **1** (2026-07-23) approved this Phase 0 package.

**Acceptance sketch (Phases 1–6) — docs-only:**

| Phase | Done looks like |
|-------|-----------------|
| **1** | Cloud-run note + prompt inventory on Automation branch; existing pack/discover/schema/Hub pytest green; Hub untouched |
| **2** | Automation A only; one PR with pending `business_ideas_YYYYMMDD.md`; Hub Start still works |
| **3** | Automation B at 11:00; soft gate; packed `.md` + `.docx` on PR; schema preferred; Hub Pass 2 override intact |
| **4** | Optional fetch prep isolated; disable-able without breaking A/B |
| **5** | Only user-approved medium-fit items; each solo; no C repos |
| **6** | READMEs + MANUAL_TEST Automations section; regression green; pause/disable documented |

**Phase 0 definition of done:** ✅ Decisions 0.1–0.5 locked in this file; acceptance sketch written; **no** Automations created; **no** `launcher_config.json` / prompt body changes required.

#### Phase 1 — Cloud-ready packaging (additive docs; discover/pack prompts unchanged unless gap found) ✅

**Goal:** Make Pass 1/2 instructions safe to paste into Automations without rewriting Hub or strategy code.

- [x] **1.1 — Cloud run note (docs):** `prompts/CLOUD_FORMULATION_AUTOMATIONS.md` + pointers in `prompts/README.md` and `agent-business-idea-runs/README.md` (2026-07-23).
- [x] **1.2 — Prompt inventory:** `agent_formulation_run.txt` / `agent_formulation_pack.txt` / `FORMULATION_PASS_CONTRACT.md` / `idea_card_schema.py` are **git-tracked** on `main` (last formulation ship `2e964fb`). Cloud note + Phase 0–1 tracker **pushed** as `c0a51d2` (2026-07-23) so Automations can see them on remote.
- [x] **1.3 — Static smokes still green:** pack + schema + §13 dual-mode + Hub config/agent_run — **26 passed** (2026-07-23). Hub untouched.
- [x] **1.4 — Checkpoint:** Phase 1 complete via menu **1** (2026-07-23). **Do not** create Automation A until user approves Phase 2.

**Phase 1 definition of done:** ✅ Docs/inventory ready; prompts/contract unchanged in spirit; tests green; Hub untouched; **no** Automations created.

#### Phase 2 — Automation A only (Pass 1 Discover) — modular ship

**Goal:** First unattended daily Discover run. **Stop after draft `.md`.** Do not pack; do not Docx.

- [ ] **2.1 — Create Automation A** (Cursor Automations): daily cron; repo = Inc; instructions = Pass 1 Discover contract (same intent as Hub Run 1 meta / `agent_formulation_run.txt`).
- [ ] **2.2 — Outputs:** Writes `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` with `_PENDING_PASS_2_PACK_`; no Pass 2 work in the same run.
- [ ] **2.3 — Persist per Phase 0 git policy** (commit/PR/artifacts-only).
- [ ] **2.4 — Prove once:** One successful cloud Pass 1 artifact reviewed; Hub manual path still works (smoke or short MANUAL note).
- [ ] **2.5 — Checkpoint:** Pause here unless user approves Phase 3 (do **not** auto-build Pass 2 in the same hop).

**Phase 2 definition of done:** Daily Pass 1 Automation exists and has produced at least one valid pending draft; Pass 2 Automation **not** required yet; Hub unbroken.

#### Phase 3 — Completion gate + Automation B (Pass 2 Pack) — modular ship

**Goal:** Second job only after Pass 1 ready — pack cards + one-shot Docx; no new ranked set.

- [ ] **3.1 — Gate:** Pass 2 starts only when today’s draft exists and still pending (marker / path / commit event) — **not** a blind short sleep after Pass 1 paste.
- [ ] **3.2 — Create Automation B:** instructions = Pass 2 Pack (`agent_formulation_pack.txt` + §14 contract); same dated `.md`.
- [ ] **3.3 — Schema:** Prefer `idea_card_schema.py` before Docx; fix gaps from Pass 1 evidence; soft-fail incomplete cards without inventing competitors.
- [ ] **3.4 — Docx:** One-shot convert per contract; open-on-desktop only if Phase 0.4 allowed it.
- [ ] **3.5 — Prove once:** Same-day `.md` + `.docx` pair; Hub Pass 2 card still works as override.
- [ ] **3.6 — Checkpoint:** User sign-off on A→B chain before Phase 4 medium-fit work.

**Phase 3 definition of done:** Daily chain yields packed `.md` + `.docx`; two Automations (or cron+event) remain separable; §14 gates intact; Hub override intact.

#### Phase 4 — Optional fetch prep (A+) — still modular

- [ ] **4.1 — Optional Automation or pre-step:** `agent_strategy_run.py` fetch → `inputs/*.json` before Pass 1 (soft-fail; never abort Discover).
- [ ] **4.2 — Tests/docs** for fetch-prep path only; do not fold fetch failures into Hub `agent_run` clipboard behavior.
- [ ] **4.3 — Checkpoint** before any Phase 5 medium-fit items.

**Phase 4 definition of done:** Fetch prep optional and isolated; Pass 1/2 Automations still independently disable-able.

#### Phase 5 — Inc medium-fit (bucket B) — opt-in only; one item per sub-phase

**Do not start until Phases 2–3 signed off.** Each sub-phase is independently approvable:

- [ ] **5.1 — PR hygiene on Inc** (PR opened/pushed → comment-only review) — optional.
- [ ] **5.2 — Daily digest** (summarize new `outputs/` + `task.md` focus) — optional.
- [ ] **5.3 — CI fail triage** (on checks failed → propose fix) — optional; only if CI exists and user wants it.
- [ ] **5.4 — §5 bookmark classify-from-export** (cloud classify dump → proposed routes; **no** live Chrome delete) — optional.
- [ ] **5.5 — §7 Post-Wedding** (`run_automated_tests.py` on PR/push comment if red) — optional.
- [ ] **5.6 — §3 YouTube status digest** from exports JSON — optional.
- [ ] **5.7 — Checkpoint** after each enabled item; never batch-break Hub or formulation Automations.

**Phase 5 definition of done:** Only approved medium-fit Automations exist; formulation A/B still green; no other-repo C work.

#### Phase 6 — Docs, MANUAL_TEST, regression, sign-off

- [ ] **6.1 — READMEs:** Point at Automations as preferred daily path; Hub = manual override (`agent-business-idea-runs/README.md`, `prompts/README.md`, Hub README one-liners).
- [ ] **6.2 — `MANUAL_TEST.md`:** Add Automations live sign-off section; keep Hub Two-run as optional override; Automate-first for everything else.
- [ ] **6.3 — Regression bundle:** Existing pack/discover/schema/Hub pytest still green after any incidental doc/config touch.
- [ ] **6.4 — Operating model lock:** Document disable/pause steps if a bad run occurs (rollback without deleting prompts).
- [ ] **6.5 — User checkpoint:** §19 v1 complete (A+B daily chain) vs keep iterating Phase 5 items.

**Phase 6 definition of done:** Docs + one live proof of daily `.md`+`.docx`; Hub override documented; automated tests green.

#### Explicitly out of scope (this task)

- Implementing **C** Automations in other repos (reminder only — integrate later outside §19).
- Fusing Pass 1+2 into one mega-prompt / one Automation that invents a new ranked set on Pack.
- Replacing or deleting Hub Pass 1/2 cards.
- Editing strategy CLIs / `run_all_strategies.py` / gadget ops for this task.
- Hijacking or rewriting existing tray schedules (`problem_id_live_mwf`, etc.) as the formulation engine.
- Building §4 Phase 5.5 tray Hub modal schedule **inside** §19 (track under §4 if still desired).
- Forcing My Machines / local Word-open as default.
- Auto-trading, live payment, or credentialed browser signup Automations.
- Chrome live de-bookmark without a separate approved local/browser design (§5 Phase 3 remains its own track).

#### Reminder — C (other repos; not §19 work)

When Inc A/B is stable, **separately** consider Automations for: `project_reminder`, `anki_automation`, BrowserUse/Screenshot_script, `reelops`, Tegrid IMS / Digi / Cooking Robot, gated Algorithmic trading health checks, learning-folder digests. Create **per-repo task entries** then — do not expand §19.

#### Checkpoints (user)

- [x] **Approve task entry** — 2026-07-23 (user asked to add phased §19; **implementation still not started**).
- [x] Approve **Phase 0** (spec lock) — 2026-07-23 menu **1** (07:00/11:00 WAT; PR; cloud; Docx in-repo; fetch separate).
- [x] Approve **Phase 1** (docs/inventory) — 2026-07-23 menu **1** (cloud note + inventory + 26 smokes; **no** Automation yet).
- [ ] Approve **Phase 2** (Automation A only).
- [ ] Approve **Phase 3** (gate + Automation B).
- [ ] Approve **Phase 4** (optional fetch prep) if desired.
- [ ] Approve each **Phase 5** medium-fit item individually.
- [ ] Approve **Phase 6** sign-off.

**Suggested milestones (from 2026-07-23):**
- Phase 0: ✅ **2026-07-23** (spec lock)
- Phase 1: ✅ **2026-07-23** (cloud note + inventory + smokes)
- Phase 2: next after approve (Automation A only)
- Phase 3: next day after first good Pass 1 cloud proof
- Phase 4–5: only after A→B stable
- Phase 6: when daily `.md`+`.docx` proven

**v1 definition of done (formulation chain):** Daily Automation A + gated Automation B produce same-day packed `.md` + `.docx` under `agent-business-idea-runs/outputs/`; §14 contract held; Hub manual override intact; existing pytest green; **C not required**.

