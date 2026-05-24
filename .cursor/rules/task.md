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

**Stack (proposed):** Python + `pystray` + minimal UI (tkinter or lightweight webview for super main) — confirm at Phase 1 kickoff.

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
