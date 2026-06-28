# Active Task List
*This file tracks all tasks - coding, business, research, and other activities*

## 🎯 Current Priority Projects

### 1. Problem Identification Tool (70% Complete - LIVE)
**Status:** Deployed and operational at https://vermillion-figolla-b9efb8.netlify.app/

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
**Status:** Phase 3 complete; manual Phase 2 UI checks still pending  
**Goal:** Windows **tray icon** (notification area, near the clock) + optional super main hub; all `C:\dev\Inc` entry points organized under **4 pillars** (extensible to 5+ later).  
**Folder:** `inc_launcher/` — run: `python -m inc_launcher.tray_app` from `C:\dev\Inc`

> **Terminology:** “Tray icon” = the small icon you right-click in the Windows notification area. Same as “system tray app” — one background process, one icon, menu on right-click.

#### Four pillars (top-level nav — tray icon right-click + super main sidebar)

| Pillar | Purpose | Initial `Inc` mapping |
|--------|---------|------------------------|
| **My Established business ideas** | Businesses you are running or committed to | `Started-Businesses/`, `Strategy-1-Business-Variation/`, live ops (e.g. YouTube publish workflow when channel is active) |
| **My leads** | Contacts, outreach, campaigns | `abuja_lead_generator/` (DB, scraper, email/WhatsApp, reports) |
| **Formulated ideas** | Idea pipeline outputs & strategy runs | `Business-Idea-Formulation-Strategy-*/`, `run_all_strategies.py`, `business_ideas_*.md`, `past_business_ideas.md`, `business_research/` |
| **Problem identification** | Discovering & capturing problems (inputs to formulation) | `problem_identification_tool/`, `Strategy-2-Problem-Solving/problem_finder/`, problem-collection strategies (3, 4, 5, 10, 11, 12, etc.) |

**Flow:** Problem identification → Formulated ideas → Established businesses; **My leads** supports outreach alongside that pipeline.

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

#### Manual verification (you — do later on your PC)

Automated checks already pass (`python -m pytest inc_launcher/tests -q` and `python -m inc_launcher.tests.smoke_hub` from `C:\dev\Inc`). Complete these **on your machine** before treating Phase 2 as fully signed off:

- [ ] **Start tray app** — `cd C:\dev\Inc\inc_launcher` then `python tray_app.py`; icon appears near the clock
- [ ] **Left-click tray icon** — Inc Hub window opens (sidebar + launcher cards; no error dialog)
- [ ] **Pillar switch** — Click **Formulated ideas** in sidebar; **Run all strategies** shows under **Pinned**
- [ ] **Run a launcher** — Click a card (e.g. opens `task.md` or a folder); target opens in Explorer/default app
- [ ] **Recently opened** — Re-open Inc Hub; same pillar shows the item under **Recently opened**
- [ ] **Right-click tray menu** — Menu shows **Open Inc Hub**, four pillar submenus, global actions, **Quit** (no crash)
- [x] **Optional: commit Phase 2** — Pushed `c5057d3` on `main` (2026-05-24); tick UI items below when you finish hands-on checks

**Phase 3 — Scale beyond 4** ✅
- [x] Add pillars via config only — **Automation hub** pillar in `launcher_config.json` (add more without code changes)
- [x] Single-instance lock — second `tray_app.py` exits if one is already running
- [x] Start at login — tray menu **Start at Windows login [ON/OFF]** (writes `Inc Launcher.bat` to Startup folder)
- [x] Custom icon — optional `inc_launcher/assets/icon.png` or `settings.icon_path` in config

**Phase 4 — Interval nudges (approved schedule — not implemented)**  
**Problem:** Too many tray icons; Inc Hub is easy to forget. **Not** Windows login — tray already runs; **timer** fires existing menu actions so work surfaces without hunting the notification area.  
**Approved:** 2026-05-30 (user option **1** — starter interval list).

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

**Phase 4 tasks (build when user picks implement):**
- [x] **4.1** Schedule config + `scheduled_nudges.py` (parse, resolve targets, due logic) — **`enabled: false`**; no tray/timer wiring yet (zero runtime change)
- [x] **4.2** Background timer in `nudge_scheduler.py` + `tray_app.py`; calls `run_action` / `show_hub`; persists fired keys in `schedule_fired.json` (gitignored). **Still idle while `schedules.enabled` is false.**
- [x] **4.3** Tray submenu: **Interval nudges [ON/OFF]** — persists `schedules.enabled` in `launcher_config.json`; menu label refreshes after toggle
- [x] **4.4** Tests: scheduler + sign-off automation in `test_phase4_signoff.py`, `test_nudge_scheduler.py`, `test_phase4_toggle.py`, `smoke_hub.py`
- [x] **4.5** `inc_launcher/MANUAL_TEST.md` — one manual pass at Phase 4 sign-off (deferred per `deferred-manual-testing.mdc`)

**Boot note:** External-repo `auto_launcher.py` starts tray at login; keep Inc **Start at Windows login [OFF]** to avoid duplicate starts (`single_instance` prevents double tray, but one boot path is clearer). Phase 4 timer runs inside the tray process Layer 1 already started.

**Stack (proposed):** Python + `pystray` + minimal UI (tkinter or lightweight webview for super main) — confirm at Phase 1 kickoff.

---

### 5. Business Bookmark Sorting (Chrome → Inc folders)
**Status:** Phase 0–2b implemented; Phase 3 (de-bookmark) pending — **~1937** items in queue  
**Goal:** Sort bookmarks from Chrome (`chrome://bookmarks/?q=business` and related trees) into the **correct folders/files inside `C:\dev\Inc`**, not into `business_bookmark_sorter\Business Links.md` (that path is a **temporary inbox only**). After Phase 2b, filing one bookmark should mean: **saved in queue, visible in the right markdown, docx open for eyeball check** — then user may delete from Chrome (Phase 3 still manual until built).

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
| **Business started** | `Started-Businesses/`, live ops folders |
| **Formulated ideas** | `Business-Idea-Formulation-Strategy-*/`, `business_research/`, `business_ideas_*.md`, `past_business_ideas.md` |
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
- [ ] Add **Business bookmark sorter** item under Formulated ideas or new pillar in `inc_launcher/launcher_config.json`

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
**Spec:** [post-wedding-comms-pack.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack.md) · [README](../Strategy-2-Problem-Solving/post-wedding-comms-pack/README.md) · [MANUAL_TEST.md](../Strategy-2-Problem-Solving/post-wedding-comms-pack/MANUAL_TEST.md)  
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
| SaaS 4th — Crunchbase niche | Strategy **6** |
| SaaS 5th — Crunchbase trending | Strategy **7** |
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
| **Established** | `Started-Businesses/`, live ops folders |
| **Formulated ideas** | `Business-Idea-Formulation-Strategy-*/`, `business_research/`, `business_ideas_*.md`, `past_business_ideas.md` |
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
