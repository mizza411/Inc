# Technical Intuition Log

## 2026-08-20 — BB-LINKS-UX-1 Phase 4: template rename + banner

**What we did**
- Added `instance_branding.py` + `routes.json` → `product` (title, banner, tray tip, master title).
- UI/tray renamed to **Business links bookmark Reviewer**; top banner explains Health/Investment reuse.
- Documented second-category hooks in `TEMPLATE.md` (no health build).

**Why it matters**
Business filing is clearly “instance one” of a reusable shell, without forking another app folder yet.

**Intuition analogy**
Like one coffee-shop POS branded for this café, with a sticker that says the same register software can be re-skinned for a juice bar later — same buttons, different name on the screen.

---

## 2026-08-20 — BB-LINKS-UX-1 Phase 3: Reviewer tray

**What we did**
- Added `review_tray.py` (pystray Open/focus + Quit) and `review_single_instance.py` (mutex + focus flag).
- Second `review` launch focuses the existing window instead of opening a duplicate.
- Inc Formulated → Bookmark review command left unchanged (config test).

**Why it matters**
You can raise or quit the Reviewer from the tray like other Inc apps, without losing the Formulated-ideas menu entry.

**Intuition analogy**
Like a phone app that stays as one icon in the status bar: tapping it brings the same screen forward instead of launching a second copy.

---

## 2026-08-20 — BB-LINKS-UX-1 Phase 2: flat Business Links

**What we did**
- Master export is now a flat list (`export.flat_list` + `sort_by: filed_at`); no category `##` headings.
- Newest filed link is the last line; live regen: 18 links, md+docx cleaned.
- Sectioned mode kept behind `flat_list: false` for later template instances.

**Why it matters**
Filing no longer scatters links under “Problem identification” / peers — the doc reads as one chronological list with the latest file at the bottom.

**Intuition analogy**
Like a single notebook page of URLs in the order you saved them, instead of a binder with tabbed category dividers you never flip through.

---

## 2026-08-20 — BB-LINKS-UX-1 Phase 1: no Assign picker

**What we did**
- Removed **Assign to:** combobox; File/Enter uses `resolve_file_destination` (suggest → `other`).
- Added read-only **Filing as:** line; toast still shows destination label; removal dialog unchanged.
- Tests: `test_bb_links_ux_phase1.py`; updated Phase 4 / removal / sign-off fixtures.

**Why it matters**
Filing no longer needs an extra category click — suggestions drive destination while you still see where the link will go.

**Intuition analogy**
Like a checkout that auto-fills your usual shipping address and shows it as text: you confirm with one button, instead of opening a long address dropdown every time.

---

## 2026-08-20 — Word Business Links.docx lock (STA Close)

**What we did**
- Diagnosed WinError 32: Word had the doc open and paths matched, but Close returned False because it ran on a **background thread** (Word COM is STA → hang/timeout).
- Close now runs on the calling thread with `DisplayAlerts=0` and `Saved=True`; temp regenerate + replace unchanged; sibling `*.updated.docx` only if master stays locked.
- Live regen with Word open: close True, master docx rewritten (~12KB).

**Why it matters**
Filing while the last export is still open in Word works again without asking you to close the tab by hand.

**Intuition analogy**
Like asking a receptionist for a file while she’s on another desk’s phone line — she never hears you. You have to speak at her own desk (the main thread), not shout from the hallway (a worker thread).

---

## 2026-08-20 — Word same-name Business Links.docx fix

**What we did**
- Fixed regenerate path: close open `Business Links.docx` **without** saving (md is source of truth), build to a temp `.__regen__.docx`, replace, reopen.
- Clearer error if Word still holds the file; never `taskkill` WINWORD.
- Pytest mocks in `test_docx_same_name_fix.py`.

**Why it matters**
Filing again while Word still shows the last export no longer dies with “same name as an open document.”

**Intuition analogy**
Like updating a printed flyer: you take the old sheet off the desk, print a new copy, then put the new one down — you don’t try to reprint onto a page that’s still sitting under someone’s hand.

---

## 2026-08-20 — BB-TIMED-1 automate sign-off + restart

**What we did**
- Killed stale `python -m business_bookmark_sorter review` processes; restarted one clean instance.
- Added `test_bb_timed_v1_signoff.py` (13) covering former MANUAL §§I–L + M/N config; suite **72** green.
- Moved I–O to automated in `MANUAL_TEST.md`; left only live login/11:00 as deferred §P with ASCII pass/fail.

**Why it matters**
You asked not to do manual testing now — logic gates are proven in pytest; only true OS login/clock remain optional later.

**Intuition analogy**
Like a car’s factory diagnostics verifying brakes and sensors on a bench, while the “drive around the block once” step waits for a road day.

---

## 2026-08-20 — BB-TIMED-1 Phase 7 polish + sign-off gate

**What we did**
- Softened review window copy to generic “Bookmark Reviewer” + config-driven filter note.
- Marked Phases 0–7 complete; §5 + satellite point at **Ready for single manual pass** (`MANUAL_TEST` §O).
- Full sorter + schedule pytest green this turn.

**Why it matters**
Build work for timed/minimal filing is done; the remaining gate is one human pass, not more mid-build clicking.

**Intuition analogy**
Like finishing a factory acceptance test checklist and handing the owner a single walkthrough sheet instead of asking them to inspect every bolt during assembly.

---

## 2026-08-20 — BB-TIMED-1 Phase 6 PR boot (config-only)

**What we did**
- Added `applications.inc_business_bookmark_review` in project_reminder `launcher_config.json` (`pythonw -m business_bookmark_sorter review`, cwd `C:\dev\Inc`).
- No `auto_launcher.py` edit; left `scripts.bookmark_sorter` alone.
- Smoke `test_pr_boot_config.py` + MANUAL_TEST §N.

**Why it matters**
Login can open the Inc filing window without moving the product into project_reminder or merging two different bookmark tools.

**Intuition analogy**
Like a startup shortcut that opens Word on a specific document in another folder — the launcher only points; the app still lives where the files are.

---

## 2026-08-20 — BB-TIMED-1 Phase 5 Inc weekday schedule

**What we did**
- Additive `bookmark_review_weekdays` schedule: Mon–Fri **11:00** → menu id `bookmark_review`.
- Confirmed existing `resolve_schedule_target` maps the menu item; updated schedule tests + MANUAL_TEST notes.
- Cleared deferred “Bookmark review schedule” checkbox in `task.md` §4.

**Why it matters**
The filing window can appear on a clock while the Inc tray (already started by project_reminder) is running — no remembering to open the menu.

**Intuition analogy**
Like a calendar reminder that launches the same app your Start menu already lists — one shared shortcut, two ways to open it.

---

## 2026-08-20 — BB-TIMED-1 Phase 4 minimal confirm

**What we did**
- Pre-select suggested destination; **Enter** files (when focus isn’t in the dropdown).
- Replacement removal dialog with “Don’t ask again this session” (in-memory flag only).
- Tests for skip-flag + dest pre-select; existing removal flow tests updated.

**Why it matters**
A timed slot becomes glance → Enter → next, instead of hunting the dropdown and answering the same Chrome question every time.

**Intuition analogy**
Like a supermarket self-checkout that already highlights the suggested bagging option and lets you press OK, with a “don’t show this tip again” for the rest of the trip.

---

## 2026-08-20 — BB-TIMED-1 Phase 3 auto-open link

**What we did**
- Added `auto_open.py` (one URL per item id; Settings toggle; no bulk open).
- Hooked pending-item display in `review_ui`; pytest covers on/off + debounce.
- `MANUAL_TEST` §K added.

**Why it matters**
You glance the page instead of clicking Open URL every time — less friction in a timed filing slot.

**Intuition analogy**
Like a slideshow that advances the slide and already opens the referenced webpage once, not fifty tabs at once.

---

## 2026-08-20 — BB-TIMED-1 Phase 2 session timer

**What we did**
- Added `session_timer.py` (countdown, pause, extend, fake-clock tests).
- Review UI shows time left; on expiry stops loading the next link; **Extend +5 min** resumes.
- Settings Apply restarts the timer with the new length.

**Why it matters**
Filing becomes a timed slot instead of an open-ended window that you forget to close — and it stops nagging when time is up.

**Intuition analogy**
Like a kitchen timer on a study block: when it rings you stop pulling the next flashcard until you hit “+5 minutes.”

---

## 2026-08-20 — BB-TIMED-1 Phase 1.2 Settings… UI


**What we did**
- Added `session_settings_ui.py` (modal Settings dialog: minutes spinbox + auto-open checkbox + Apply).
- Thin **Settings…** button on `review_ui` (no mega-edit of the 600+ line panel).
- README + `MANUAL_TEST` §I; Phase 1 marked ✅ on satellite.

**Why it matters**
You can change session length from the review window itself — the lock “not through a JSON file” is now real for the UI path.

**Intuition analogy**
Like changing a phone’s screen timeout in Settings, not by editing a hidden preferences file with Notepad.

---

## 2026-08-20 — BB-TIMED-1 Phase 1.1 session settings store


**What we did**
- Added `business_bookmark_sorter/session_settings.py` (load/save/clamp; default 15 min; auto-open flag reserved).
- Gitignored `data/session_settings.json`; pytest `test_session_settings.py` green.
- Owner confirmed Phase 0.4; satellite `task_bookmark_timed_sessions.md` updated.

**Why it matters**
Session length can later be changed from a Settings UI without hand-editing JSON, and prefs stay out of git and away from bookmark URLs.

**Intuition analogy**
Like a microwave’s cook-time memory: the number is saved on the appliance, not something you rewrite in a config printout every meal.

---


**What we did**
- Removed `python -m business_bookmark_sorter discover` (including `--dry-run`) from the CLI.
- Docs and `task.md` §5 now point at **`review`** as the one launch command.
- Added `test_cli_no_discover.py` so the old command stays gone.

**Why it matters**
You asked for one command to open the filing window. A separate count-only command was extra noise and looked like a second “start here.”

**Intuition analogy**
Like taking the “preview playlist” button off a music app when you only ever wanted Play — the library still loads when you hit Play.

---


**What we did**
- Expanded `ask_people_ask_owners_playbook.md` with S3/S4 whom/openers/capture, after-ask CLI, ASCII flow, risks; regenerated `.docx`.
- Marked Phase 5 ✅; Phase 6 (real conversations) remains owner-only.

**Why it matters**
The nudge now points at a complete how-to, not a stub — so when the Hub or morning Word file opens, you know what to say and how to log it.

**Intuition analogy**
Like upgrading a sticky note that said “ask someone” into a short field guide that still leaves the conversation to you.

---

## 2026-08-08 — NET-ASK-REMIND-1 Phase 4 PR docx


**What we did**
- Generated `ask_people_ask_owners_playbook.docx` via pandoc; additive `project_reminder` launcher key `ask_people_ask_owners_playbook` (`is_document`).
- Skipped Task Reminder seed (AUTO-NAR-05) with an on-disk reason; validate-pr-launcher + phase4 smokes green.

**Why it matters**
Morning boot can surface the ask-people ritual beside your other guides without editing `auto_launcher.py`.

**Intuition analogy**
Like putting a laminated checklist on the kitchen counter that your morning routine already opens — not a second alarm app.

---

## 2026-08-08 — NET-ASK-REMIND-1 Phase 3 Inc Hub nudge


**What we did**
- Added `network_ask` Hub action + pinned Problem identification card; Mon/Wed/Fri 09:30 schedule opens Hub Option B modal (not a silent send).
- Start opens playbook and copies openers; formulation Option B generalized via `option_b_actions` without breaking agent_run.
- Phase 2+3 smokes + launcher regressions green (43 pytest + 16 unittest).

**Why it matters**
The ask-people habit now shows up where you already live (Inc Hub/tray), while you still choose whom to message.

**Intuition analogy**
Like a calendar popup that opens your draft notepad — it never hits “send” on your behalf.

---

## 2026-08-08 — NET-ASK-REMIND-1 Phase 2 core CLI


**What we did**
- Shipped modular CLI under `network_ask_reminder/`: config validate, S3/S4 rotate, JSONL log-add, status/streak, opener drafts, isolation-check.
- 9/9 unittest smokes green; no Inc Hub / project_reminder wiring yet (Phases 3–4).

**Why it matters**
You can already run “what should I ask today?” and log answers offline before any toast or morning docx exists.

**Intuition analogy**
Like a paper habit tracker and message drafts in a notebook — the phone alarm that pokes you is a later accessory, not the notebook itself.

---

## 2026-08-08 — NET-ASK-REMIND-1 Phase 1 scaffold


**What we did**
- Created `network_ask_reminder/` with README, playbook stub, `config.example.json`, `MANUAL_TEST.md` (MAN-NAR only), data gitignore.
- Additive one-line cross-links on Strategy 3 + 4 READMEs; no Hub/PR/CLI wiring yet.
- Marked Phase 1 ✅ in `task_net_ask_remind.md` + main pointer.

**Why it matters**
The habit tool has a home and a config shape without touching formulation runners or sending messages for you.

**Intuition analogy**
Like putting a sticky-note pad and a calendar template on your desk before you wire the alarm clock — the reminder hardware comes next; the conversations stay yours.

---

## 2026-08-08 — Agric supplier quotes without sharing phones


**What we did**
- Locked privacy: owner never pastes phone numbers to the agent (supplier or grower).
- Added number-free quote paste format; locked-supplier contact column marked owner-only; day pack/MANUAL_TEST/task updated.

**Why it matters**
You can still get help logging prices into the repo without leaking personal or vendor contact data into chat logs.

**Intuition analogy**
Like telling a bookkeeper “Vendor A sold me bags at X naira in Gudu” without handing over the vendor’s phone book.

---

## 2026-08-08 — Agric supplier visit/call day pack

**What we did**
- Added `supplier_visit_day_pack.md` (call script, on-site ticks, same-day route).
- Enriched `suppliers_targets.md` with public phones for FarmFeed (0818 992 2811) and Biocrops (0805 482 5619); call log table; did **not** mark any supplier locked/visited.

**Why it matters**
You can start dialing today without inventing a route; results still require your legs and voice.

**Intuition analogy**
Like a courier giving you a call sheet and a map pin order — they don’t knock the doors; you do, then tick the sheet.

---

## 2026-08-08 — Agric ID 2 Week 1 ops scaffold

**What we did**
- Added `sku_starter_list.md` (10 SKUs), `suppliers_targets.md` (Abuja public-directory leads + visit tracker), `whatsapp_order_kit.md` (invite/order copy + 20-grower sheet).
- Split Week 1 on the pilot one-pager: scaffold ✅ vs owner visit/WhatsApp still open; no fake “supplier locked” claims.

**Why it matters**
Field work needs a shopping list, a call sheet, and paste-ready WhatsApp text — not another strategy essay.

**Intuition analogy**
Like printing a market shopping list, a vendor map, and a pre-written group announcement before you leave the house — the bags still get bought in person.

---

## 2026-08-08 — Agric pilot ID 2 confirmed (farm-input aggregation)

**What we did**
- Owner locked pilot **ID 2**; wrote `pilot_id2_farm_input_aggregation.md` (+ docx); marked idea status `pilot`; regenerated ideas docx; left blank template for later IDs.
- Task Phase **5.1** checked; 5.2–5.3 remain owner ops (no Started-Businesses write).

**Why it matters**
The shortlist is no longer “pick someday” — there is one prepaid aggregation play with a 30–90 day checklist on disk.

**Intuition analogy**
Like circling one supplier on a wholesale shortlist and writing the first purchase order draft — the other SKUs stay on the clipboard, not in the truck.

---

## 2026-08-08 — Niche event + agric Phase 4 docx + launcher

**What we did**
- Pandoc: `oldies_abuja_playbook.docx` (~15KB) · `agric_agrictech_ideas_ng.docx` (~14KB) under Inc folders.
- Additive `launcher_config.json` keys `abuja_oldies_night_playbook` + `agric_agrictech_ideas_ng` (`is_document`, enabled); no `auto_launcher.py` edit; path smoke PASS; `MANUAL_TEST.md` T1/T2 in both folders.

**Why it matters**
Morning boot can surface the playbooks in Word without hunting folders, while unrelated launcher docs stay enabled.

**Intuition analogy**
Like adding two labeled folders to the auto-open tray on your desk — the binders already written now drop onto the desk at login, without rebuilding the tray itself.

---

## 2026-08-08 — Niche event + agric ideas Phase 2 bodies

**What we did**
- Filled `niche-event-series/oldies_abuja_playbook.md` §§1–9 (positioning, cost-kill, venue, tickets, sound, promo, run sheet, risks, ASCII).
- Scored 10 agric ideas in `agric_agrictech_ideas_ng.md`; top 3 = IDs **2, 7, 6**; recommended pilot **ID 2** (input aggregation). Still no docx/launcher.

**Why it matters**
You can run venue pitches and pick an agric pilot from disk without re-asking chat for the plan.

**Intuition analogy**
Like finishing the chapters inside those two binders — the event binder is now a night-of script; the farm binder is a scored shortlist with a circled “start here,” still not stamped into the “opened businesses” drawer.

---

## 2026-08-08 — Niche event + agric ideas Phase 1 scaffolds

**What we did**
- Created `niche-event-series/` (README, playbook outline, break-even stub, venue pitch + empty targets) and `agric-business-ideas/` (README+rubric, seed ideas table, pilot one-pager template).
- Phase 0 locks already on disk; Phase 1 marked done in `task_niche_event_agric.md`; **no** pandoc/docx/`launcher_config` yet (Phase 4).

**Why it matters**
Durable folders hold the ops playbooks so chat plans don’t evaporate, while isolation rules keep Tegrid/FIR/launcher core untouched until content is ready.

**Intuition analogy**
Like labeling two empty binders (event night vs farm ideas) and slipping in section tabs before writing the chapters — the filing cabinet stays separate from the office apps that open Word every morning.

---

## 2026-07-31 — Tegrid RE GTM Phase 4 (reply → demo → close)

**What we did**
- Added `tracker/` (hot/nurture/no + outcomes), `run_phase4.py`, `offer/DEMO_CHECKLIST.md`, `MANUAL_TEST.md`; tag `no` appends STOP list.
- Phase 4 smokes green; full Phase 1–4 suite **17/17**; live send still locked.

**Why it matters**
After mock outreach, you need a simple place to mark interest and closes without mixing FIR visits or Tegrid product code.

**Intuition analogy**
Like a sticky-note board next to a practice phone log — green = call back, yellow = later, red = never dial again — while the real phone line stays switched off.

---

## 2026-07-31 — Tegrid RE GTM Phase 3 (Lane 3 mock + Tier-1 route)


**What we did**
- Built `outreach/` mock sender, rate/STOP rules, Lane 3 runner (Tier 2/3 mock drip; Tier 1 → Maps route pack), `run_phase3.py`, Phase 3 smokes (11/11 with prior phases).
- `live_send=false` hard-refuses real send; route pack explicitly not FIR construction sheets.

**Why it matters**
You can rehearse the full Blend path (auto vs visit) and keep a campaign log without burning WhatsApp reputation.

**Intuition analogy**
Like a call center training mode that writes every “call” to a practice log and prints a door-to-door route sheet — headsets stay unplugged from the live phone lines.

---

## 2026-07-31 — Tegrid RE GTM Phase 2 (templates, no send)


**What we did**
- Added one-pager, WA/email D1+D3 templates, `offer/render.py`, `config/lane_config.json` (Lane 3 on; live_send false), lead-gen adapter stub OFF.
- Phase 2 dry-render CLI + 5 new smokes (8/8 with Phase 1 green); still no outbound messages.

**Why it matters**
Personalization is separated from sending — you can preview copy for each firm before any WhatsApp/email risk.

**Intuition analogy**
Like printing personalized invitations on a home printer and stacking them in envelopes — nothing is mailed until you decide to walk them to the post office.

---

## 2026-07-31 — Tegrid RE GTM Phase 1 (fixture lead pipeline)


**What we did**
- Built `tegrid_re_gtm/` Phase 1: separate source adapters (Infoisinfo / Finelib / Maps seed), normalize+dedupe, ICP score + Tier 1/2/3, CLI export, unittest smoke (3/3 green).
- Fixture-only ingest (no live scrape, no send); isolated from FIR, §6 Land Sales OS, and `abuja_lead_generator` core.

**Why it matters**
Lane 3 Blend needs a reviewable shortlist before any WhatsApp/email — this proves the list machine without burning contacts or touching other money tracks.

**Intuition analogy**
Like a mailroom that sorts incoming business cards into labeled trays from photocopies of directories first — you check the trays before anyone dials a number from the real phone book.

---

## 2026-07-26 — Post-Wedding landing: no phone in chat/git


**What we did**
- Switched public CTA to `CONTACT_URL` (Google Form / mailto / IG); kept WhatsApp only in gitignored `config.local.js`.
- Updated `DEPLOY.md`, landing smoke tests, and `task.md` §7 notes.

**Why it matters**
Phase 0b can still collect leads without putting a personal number in Cursor chat or GitHub history.

**Intuition analogy**
Like putting a shop’s “write to this PO box” on the public flyer, while the private mobile stays in your desk drawer — customers can reach you; the flyer never prints your personal line.

---

## 2026-07-24 — IMPORTANT: Legacy Privacy one-way (§19 gate)

**What we did**
- Saved `prompts/IMPORTANT_cursor_privacy_mode_legacy.md` (cannot return to Legacy after Switch; can still disable Automations).
- Linked from `CLOUD_FORMULATION_AUTOMATIONS.md`, `prompts/README.md`, and `task.md` §19 status (Phase 2 privacy blocker).

**Why it matters**
Owner must choose Switch vs Cancel with eyes open before Automation A can finish; “undo later” ≠ restore Legacy.

**Intuition analogy**
Like leaving a rent-controlled flat for a new lease that unlocks the building gym — you can stop using the gym anytime, but you can’t move back into the old flat once you hand in those keys.

---

## 2026-07-23 — §19 Phase 1 cloud packaging (no Automations yet)

**What we did**
- Added `prompts/CLOUD_FORMULATION_AUTOMATIONS.md` (scope, cron locks, A/B instruction spines, inventory, rollback).
- Pointed `prompts/README.md` + `agent-business-idea-runs/README.md` at it; confirmed Pass 1/2 prompts + contract + schema are on `main` (`2e964fb`).
- Re-ran static smokes: **26 passed**; Hub/launcher untouched; **no** Cursor Automation created.

**Why it matters**
Cloud agents only see committed files — packaging the run contract first avoids broken remote checkouts when Phase 2 turns on Automation A.

**Intuition analogy**
Like laminating the recipe card and checking the pantry is stocked before switching on the oven timer — instructions ready; nothing cooking yet.

---

## 2026-07-23 — §19 Phase 0 lock (daily Pass 1→2 Automations)

**What we did**
- Locked Phase 0 in `.cursor/rules/task.md` §19: Pass 1 **07:00** / Pass 2 **11:00** WAT; Automations open **PR** (owner merges); **Cursor cloud**; **Docx in-repo only**; fetch prep stays Phase 4.
- Wrote acceptance sketch for Phases 1–6; still **no** Automations or Hub/code changes.

**Why it matters**
Decisions are frozen before creating cloud agents, so Hub, tray schedules, and §14 two-job rules stay safe while daily unattended formulation gets a clear contract.

**Intuition analogy**
Like writing the bus timetable and “no boarding without a ticket” rules on the depot wall before buying the buses — the schedule exists; engines stay off until Phase 1–2.

---

## 2026-07-23 — Post-Wedding landing + deploy gate

**What we did**
- Built static Phase 0b landing under `post-wedding-comms-pack/landing/` (pitch copy, WhatsApp/`APP_URL` via `config.js`).
- Added `DEPLOY.md` (GitHub Pages + Streamlit Cloud secrets), `.streamlit/config.toml`, `.env.example`, and `test_landing_smoke.py` wired into `run_automated_tests.py` (suite green).
- Updated `task.md` §7 progress + portfolio focus note.

**Why it matters**
Marketing can start from a real bio link once you set WhatsApp + push/host — without waiting on Carrd or a custom site builder.

**Intuition analogy**
Like printing a storefront flyer and taping the WhatsApp number on it before the shop’s electric meter is connected — people can find you; checkout stays off until you’re ready.

---

## 2026-07-23 — Post-Wedding Comms Pack Phase 1b (DeepSeek default)

**What we did**
- Rewrote `generation.py` for `LLM_PROVIDER=deepseek|openai|ngpt` with DeepSeek as default (`DEEPSEEK_API_KEY` / `LLM_API_KEY`, OpenAI-compatible base URL).
- Added `.env.example`, `test_generation_providers.py`, and wired it into `run_automated_tests.py` (suite green).
- Updated README, `PHASE_0b_PITCH.md` FAQ, `MANUAL_TEST.md`, and `task.md` §7 (Phase 1b ✅).

**Why it matters**
AI drafts no longer depend on OpenAI; cheaper/default DeepSeek path unblocks the soft-launch sequence (manual §B → deploy → 0b).

**Intuition analogy**
Like swapping the kitchen’s gas cylinder for a cheaper supplier while keeping the same stove knobs — same cooking steps, different fuel behind the pipe.

---

## 2026-07-20 — Bookmark sorter convo handoff (Phases 2b–2d)


**What we did**
- Synced `.cursor/rules/task.md` §5: Phase 2d (tooltips, removal dialog, gitignore) marked done; Phase 3 deferred; pending table + key commits listed.
- Refreshed `business_bookmark_sorter/MANUAL_TEST.md` with §§D–G (file/docx/dialog, Stay, Skip vs Stay, tooltips) plus existing A–C/H.
- Confirmed no new task file — §5 remains authoritative for this product.

**Why it matters**
You can delete the long bookmark-sorter chat; “what shipped / what’s next / what you must click” live on disk.

**Intuition analogy**
Like labeling a filing cabinet drawer (task.md) and taping the checkout checklist on the drawer front (MANUAL_TEST) before shredding the meeting notes (chat).

---

## 2026-07-20 — Inc Hub Phase 5 agent front door: convo handoff

**What we did**
- Synced Phase 5 Hub status in `.cursor/rules/task.md` §4 (v1 CLOSED; 5.0–5.4/5.6 done; 5.5 optional).
- Clarified `inc_launcher/MANUAL_TEST.md` §G: automation owns sign-off; Cursor **Enter** is optional only.
- Confirmed no new task file — §4 remains authoritative for this thread.

**Why it matters**
You can delete the Phase 5 delivery chat; Hub card + Option B + agent_run behavior and “what’s left” live on disk.

**Intuition analogy**
Like finishing a checklist on a whiteboard, then wiping the sticky notes — the whiteboard (task.md + MANUAL_TEST) keeps the score; the chat was just the meeting.

---

## 2026-07-20 — Post-Wedding Comms Pack: convo handoff → task.md §7

**What we did**
- Synced progress into `.cursor/rules/task.md` §7 (pricing, automation green, LAUNCH_PLAN, pending 0b + short manual + DeepSeek Phase 1b).
- Updated `MANUAL_TEST.md` with a **Your minimum checklist** (§B/§D/§P1 only) and LLM-swap note for §B.
- Confirmed no new task file needed; disk trackers hold the handoff.

**Why it matters**
You can delete the chat without losing “what’s next” — gates and your remaining manual steps live in the repo.

**Intuition analogy**
Like writing the shopping list on the fridge before leaving the store chat — the fridge (task.md + MANUAL_TEST) is what you re-read later, not the conversation.

---

## 2026-07-20 — Secure bookmark filing (plan only, no code)

**What we did**
- Documented privacy-first bookmark workflow in `task.md` §5 (Phase 5 options A–G; short-term A+B+C).
- Added `business_bookmark_sorter/MANUAL_TEST.md`; pointed launcher MANUAL_TEST §F + Drive §8 at the same local-first rule.
- Explicit handoff: safe to delete planning chat — tracker + tests hold the decisions.

**Why it matters**
~2k pending links are a time problem; dumping Chrome into chat is a privacy problem — the plan separates them so help never requires oversharing.

**Intuition analogy**
Like sorting mail at home with a “business only” tray: the postman (Chrome) delivers mixed mail, but you never hand the whole stack to a stranger—only the letters already in the business tray get filed.

---

## 2026-07-19 — Abuja PropTech → internal org SaaS (Land Sales OS)

**What we did**
- Reframed Abuja PropTech research from B2C concierge → B2B wholesale verify-ops → **internal org SaaS**.
- Updated `abuja-real-estate-profitable-sub-niches.md` (§3.10, §6) and `.cursor/rules/task.md` Project 6 for **Land Sales OS** (CRM + diligence + deal room).
- Embedded globally validated gaps (MLS, deal room, RE CRM, PMS, title workflow) as Nigeria-absent categories orgs still run on WhatsApp/Excel.

**Why it matters**
You sell seats to developer teams, not AGIS trips or diaspora support — product scales with code, not fulfillment labor.

**Intuition analogy**
Like selling Shopify to shops instead of running their warehouse — the merchant owns the customers and the staff; you own the operating system.

---

## 2026-07-16 — Formulation Pass 2 Pack (business_ideas_20260716)


**What we did**
- Packed Pass 1 draft `business_ideas_20260716.md` to §14 subheads (Regulatory + Competitors on all 12); S1 Complaint citations made explicit.
- `idea_card_schema.py` PASS (12); one-shot `regenerate_and_open_docx` → `business_ideas_20260716.docx` (no re-rank).

**Why it matters**
Same ranked set as Discover, now Word-ready with stable card shape so Regulatory/Competitors never drop in distribution.

**Intuition analogy**
Like locking a shipping label template after the warehouse already picked the boxes—you don’t re-pick stock; you just make every box scan the same fields.

---

## 2026-07-15 — Formulation §14 Phase 5 (v1 closed)

**What we did**
- Closed §14: regression docs/MANUAL_TEST; Pass 2 packed all 12 Jul 15 idea cards to fixed subheads; `idea_card_schema` PASS; one-shot Docx.
- Marked Current Priority §14 CLOSED / v1 complete.

**Why it matters**
The split is now the default operating model: Discover invents, Pack enforces Regulators/Competition shape, Hub has both buttons.

**Intuition analogy**
Like shipping a restaurant with a written menu and a plated photo for every dish—guests finally see the same garnish on every plate.

---

## 2026-07-15 — Formulation §14 Phase 4 (Hub Pass 2 card)

**What we did**
- Added Formulated Hub card `agent_formulation_pack` pointing at `prompts/agent_formulation_pack.txt`; Discover stays pinned primary.
- Extended Option B modal with optional `modal_title` / `modal_bullets` per item; tests for pack path + modal copy.

**Why it matters**
You can start Pass 2 from the tray/Hub the same way as Discover, without swapping the default clipboard path.

**Intuition analogy**
Like a second labeled button on a label printer—one prints the picking list, the other prints the shipping label—same machine, different roll.

---

## 2026-07-15 — Formulation §14 Phase 3 (idea card schema)

**What we did**
- Added `agent-business-idea-runs/idea_card_schema.py` (read-only required-label check on Idea details).
- Fixtures good/bad + pytest CLI exit codes; documented soft “after Pass 2 before Docx”; left Hub and `agent_strategy_run.py` unwired.

**Why it matters**
You can catch missing Regulatory/Competitors before Word opens, without making fetch or Hub fail.

**Intuition analogy**
Like a barcode scanner at the dock door: the truck still leaves on schedule if you skip the scan, but scanning stops short boxes from reaching the customer.

---

## 2026-07-15 — Formulation §14 Phase 2 (Discover defers Docx)

**What we did**
- Trimmed `prompts/agent_formulation_run.txt` so Pass 1 finishes the `.md` only (`_PENDING_PASS_2_PACK_`) and points at `agent_formulation_pack.txt` for card schema + one-shot Docx.
- Kept §11/§13 markers; updated agent/prompts READMEs and pack smoke asserts for the deferral.

**Why it matters**
Discover can stay dense on strategy gates without also racing to format every Regulatory/Competitors line—Pack owns Word quality.

**Intuition analogy**
Like separating recipe development from plating: the kitchen still invents the dish; the pass window won’t ring until every plate has the same garnish set.

---

## 2026-07-15 — Formulation §14 Phase 1 (Pass 2 pack prompt)

**What we did**
- Added `prompts/agent_formulation_pack.txt` (fixed idea-card subheads + Docx once; no invent/re-rank).
- Documented Pass 1→2 order in `prompts/README.md`; pointed agent README at the pack file.
- Added `agent-business-idea-runs/tests/test_formulation_pack_prompt.py`; left Hub + discover mega-prompt unchanged.

**Why it matters**
Agents can now run a second job whose only job is uniform Regulators/Competition cards, without risking the pinned Hub discover path.

**Intuition analogy**
Like adding a dedicated packing station after assembly—assembly can stay messy; packing still enforces the shipping checklist before the lid closes.

---

## 2026-07-15 — Formulation §14 Phase 0 (Pass 1/2 contract)

**What we did**
- Added `prompts/FORMULATION_PASS_CONTRACT.md`: Pass 1 Discover vs Pass 2 Pack ownership, required idea-card subheads (Regulatory + Competitors on every card), incomplete rules, Hub/loader inventory, Phases 1–5 acceptance sketch.
- Pointed `prompts/README.md` at the contract; marked `task.md` §14 Phase 0 done without editing the mega discover prompt or Hub.

**Why it matters**
Locks the “same subheads every idea” definition before any prompt split, so later pack/discover edits and Hub changes share one checklist and do not break pinned agent-run loaders.

**Intuition analogy**
Like posting the packing list on the warehouse wall before you redesign the shipping labels—everyone agrees what goes in every box before anybody remaps the conveyor.

---

## 2026-07-12 — Strategy 1 §11 Phase D (sign-off)

**What we did**
- Added `test_phase11_signoff.py`: no live seeds, URL-cited collector output, `strategy_1_discovery` unit, Docx citation sample via `convert_md_to_docx` (no Word open).
- Wired into `test_phase6_regression.py`; updated `MANUAL_TEST.md` + API guide; marked §11 A–D **CLOSED**.

**Why it matters**
Always-online Strategy 1 is now gated by automated checks, so seed-style regressions get caught before the next agent Docx run.

**Intuition analogy**
Like a final pre-flight checklist that confirms both the map (discovery) and the stamped tickets (URLs in the printed brief) before takeoff.

---

## 2026-07-12 — Strategy 1 §11 Phase C (strategy_1_discovery fetch)


**What we did**
- Removed top-level `strategy_1_seeds` from `agent_strategy_run.py` fetch JSON.
- Added `strategy_1_discovery` (`primary=agent_native_web_research` + optional `discovery_leads` from RSS/PH/StartupList); updated prompt, README, Phase 4/6 asserts.

**Why it matters**
Agent runs no longer receive a fake “seed businesses” blob—the fetch file points at web research (with optional headline leads) so S1 stays evidence-based.

**Intuition analogy**
Like replacing a printed customer list in the courier bag with a map pin pack: pins suggest where to look, but you still have to visit and photograph the real address.

---

## 2026-07-12 — Strategy 1 §11 Phase B (retire seeds; URL intake)


**What we did**
- Archived `seed_businesses.json` to `_archive/`; collector now requires `success_url` + complaint `source_url`; `--seed-ids` rejected.
- Updated fixture, smokes, and `agent_strategy_run` (`strategy_1_seeds` status **retired**; `--with-strategy1-run` uses `--inputs`).

**Why it matters**
Regular Strategy 1 use (CLI/Hub/smokes) can no longer invent complaints from a local tip sheet—every captured complaint must carry a real URL shape, matching the agent prompt rules from Phase A.

**Intuition analogy**
Like closing the paper phone book at the front desk: staff must look up the live listing and write down the source link before filing a complaint ticket.

---

## 2026-07-12 — Strategy 1 §11 Phase A (always-online prompt)


**What we did**
- Rewrote `prompts/agent_formulation_run.txt` so S1 must web-discover businesses + complaints with citeable URLs; forbids `seed_businesses.json` / `strategy_1_seeds` / canned gaps as problem evidence.
- Updated `agent-business-idea-runs/README.md` (+ Strategy 1 README agent note); aligned Phase 4/6 prompt asserts; marked Phase A done in `task.md`.

**Why it matters**
Next agent Docx runs cannot pass off seed-file or invented complaints as Strategy 1 problems—citations are required before CLI/fetch seed retirement (Phases B/C).

**Intuition analogy**
Like telling reporters they may still have the old tip sheet in the drawer, but every published story must quote a real source with a link—not the tip sheet itself.

---

## 2026-07-12 — Agent multi-strategy formulation run (S1 + S5–7, 9, 11–15)


**What we did**
- Ran `agent-business-idea-runs/agent_strategy_run.py` for RSS/OWID/S1 seeds/S6 StartupList/S7 Product Hunt (no Strategy 15 subprocess).
- Executed Strategy 1 collector `--non-interactive` (jumia_food, bolt, whatsapp_business); synthesized other strategies after interactive script blockers.
- Wrote one output: `agent-business-idea-runs/outputs/business_ideas_20260712.md` (+ one-shot Docx convert/open); deduped vs Jul 6/10 and past lists; included GUEMF + Best ideas.

**Why it matters**
A repeatable agent path can produce a dated, scored Nigeria idea shortlist without the interactive CLI menu—and Strategy 1 now contributes complaint→variation ideas instead of only news/niche adaptations.

**Intuition analogy**
Like a newsroom that auto-pulls wire feeds into a shared inbox, then an editor writes the front page once: fetch scripts gather raw copy; the agent synthesizes the ranked package; Word export is the single “print run,” not a reprint loop.

---

## 2026-07-12 — Strategy 1 Phase 6 regression / v1 automated gate

**What we did**
- Added `test_phase6_regression.py` (static + Phase 2–4 smokes + agent fetch keys + launcher `test_config`); PASS.
- Added `MANUAL_TEST.md` for Hub/interactive-only steps; marked Phase 0–6 complete in `task.md`.

**Why it matters**
Confirms Strategy 1 stays wired end-to-end without breaking runner registration, agent fetch, or gadget ops—before any optional human Hub pass.

**Intuition analogy**
Like a restaurant opening checklist: verify the new station’s tickets, printers, and fire exits before inviting guests to walk the floor once.

---
## 2026-07-12 — Strategy 1 Phase 5 launcher + pillar split

**What we did**
- Added Formulated Hub card `strategy1_run` (runs `business_variation_collector.py`); kept Established folder + gadget cards; clarified pillar table in `task.md`.
- Noted Strategy 1 in API guide/summary as local-seed/manual; extended launcher config tests.

**Why it matters**
You can start a Strategy 1 formulation run from Formulated ideas without confusing it with gadget ops under Established.

**Intuition analogy**
Like putting “write the menu special” on the chef’s ticket rail and “run the kitchen machines” on the facilities clipboard—same restaurant, two jobs.

---
## 2026-07-12 — Strategy 1 Phase 4 agent prompt + fetch

**What we did**
- Included Strategy 1 in `prompts/agent_formulation_run.txt` with complaint→variation rules and execution-status contract.
- Extended `agent_strategy_run.py` with additive `strategy_1_seeds` (local JSON) and optional `--with-strategy1-run`; updated agent README + `test_phase4_agent_smoke.py` (PASS).

**Why it matters**
Agent formulation runs can now trace ideas to Strategy 1 without hanging on the interactive CLI or breaking RSS/OWID/S6/S7/S15 fetch paths.

**Intuition analogy**
Like giving the newsroom a pre-printed “competitor complaint” tip sheet so writers can draft that beat even when the field reporter’s phone is off.

---
## 2026-07-11 — Strategy 1 Phase 3 master runner wiring

**What we did**
- Registered Strategy 1 in `run_all_strategies.py` (`STRATEGY_SCRIPTS`/`META`, active set `1, 3–7, 9, 11–15`); verbal note is Strategy 2 only.
- Updated `run_all_strategies_README.md`; added `test_phase3_runner_smoke.py` (PASS with Phase 2 smoke).

**Why it matters**
Strategy 1 is now a first-class menu item like the other formulation scripts, without changing retired 8/10 or Strategy 2.

**Intuition analogy**
Like adding a new station to the restaurant’s ticket rail so the kitchen can take that order type from the same printer as the others.

---
## 2026-07-11 — Strategy 1 Phase 2 CLI (non-interactive gate)

**What we did**
- Built modular intake (`seeds.py`, `complaint_intake.py`, `variation_prompts.py`) and upgraded `business_variation_collector.py` with interactive + `--non-interactive` (`--inputs` / `--seed-ids`).
- Added fixture + `test_phase2_smoke.py` (PASS); confirmed Strategy 1 still absent from `run_all_strategies.py`.

**Why it matters**
Agent and “Run ALL” paths can later call Strategy 1 without hanging on `input()`—the Phase 0 safety gate before wiring the master runner.

**Intuition analogy**
Like giving the kitchen a ticket printer that accepts pre-written orders from a tablet, not only spoken requests at the counter.

---
## 2026-07-11 — Strategy 1 Phase 1 scaffold (verbal → technical)

**What we did**
- Added prompts (`chatgpt_prompt_1a/1b/1c.txt`), `seed_businesses.json`, stub `business_variation_collector.py`, and `README.md` under `Strategy-1-Business-Variation/`.
- Left playbook steps intact; header notes Phase 1 status. Confirmed `run_all_strategies.py` still has no Strategy 1 registration.

**Why it matters**
Strategy 1 can now live as a self-contained formulation folder without touching the master runner or agent prompt—safe first brick before intake logic and wiring.

**Intuition analogy**
Like laying out a new kitchen station with recipes and ingredients labeled before connecting it to the restaurant’s main ticket printer.

---
## 2026-07-11 — Multi-strategy agent formulation run

**What we did**
- Ran `agent_strategy_run.py` → `agent_strategy_inputs_20260711_154744.json` (RSS, OWID, StartupList, Product Hunt; S15 skipped).
- Synthesized 12 Nigeria-focused ideas (deduped vs Jul 6/10 + past lists); wrote `agent-business-idea-runs/outputs/business_ideas_20260711.md`.
- One-shot Docx via `regenerate_and_open_docx` → `business_ideas_20260711.docx` (opened).

**Why it matters**
Keeps the repeatable agent formulation path working when interactive strategy scripts block on `input()`—fresh headlines still become a ranked, GUEMF-scored backlog without editing strategy code.

**Intuition analogy**
Like a newsroom that still publishes when the CMS wizard hangs: pull the wire feeds, write the edition by hand, then send the PDF to print once—don’t reopen the wizard mid-draft.

---
## 2026-07-10 — Abuja area scan v3 (digital quotas)

**What we did**
- Enforced Digital/Hybrid/Physical tags + ≥40% software-solvable ideas in `abuja_area_opportunity_scan.txt`.
- Wrote `abuja_area_opportunities_20260710_v3.md` (+ docx): 6 Digital, 5 Hybrid, 1 Physical.

**Why it matters**
Area discovery now explicitly includes app/WhatsApp/SaaS wedges, not only kiosks and kitchens—without requiring you to build those products yet.

**Intuition analogy**
Like a franchise scout who notes both “open a kitchen here” and “the ordering line should be an app”—two bets, one neighbourhood walk.

---
## 2026-07-10 — Abuja area scan v2 (all-sector)

**What we did**
- Broadened `prompts/abuja_area_opportunity_scan.txt` (RE ≤25% / ≤1 in top 5).
- Re-ran scan → `abuja_area_opportunities_20260710_v2.md` (+ docx): food, education, water, energy, waste, logistics, fintech, etc.

**Why it matters**
First run accidentally became a PropTech memo; v2 matches a generalist entrepreneur hunting any local business, not only land corridors.

**Intuition analogy**
Like walking a market looking for any stall that could make money—not only interviewing the estate agents at the gate.

---
## 2026-07-10 — Agent-only Abuja area opportunity scan

**What we did**
- Added `prompts/abuja_area_opportunity_scan.txt` (agent-only; no app / no lead-generator changes).
- Ran public-source corridor scan for Kuje, Lugbe, Lokogoma, outer Gwarinpa, Wuse II, Garki.
- Wrote `agent-business-idea-runs/outputs/abuja_area_opportunities_20260710.md` (+ docx).

**Why it matters**
Proves local opportunity discovery can be a prompt-driven agent run first; software (Field Intelligence / extending `abuja_lead_generator`) stays optional until repeatability or outreach needs force it.

**Intuition analogy**
Like using Google Maps Street View before buying a delivery van for a neighborhood you have never walked—desk reconnaissance first, fleet only if the route pays.

---
## 2026-07-08 â€” Crunchbase deprecation Tier 2 (docs truth)

**What we did**
- Updated `STRATEGY_META` for S6/S7 in `run_all_strategies.py` (descriptions only).
- Rewrote API guides, S6/S7 READMEs/playbooks, Drive mapping, and `links.md` ritual so Crunchbase is optional legacy.

**Why it matters**
Docs and menus now match Tier 1 runtime (StartupList / Product Hunt); no strategy retire or folder renames.

**Intuition analogy**
Like reprinting the store directory after you moved the dairy aisleâ€”same store layout, corrected signs so shoppers stop walking to the empty shelf.

---

## 2026-07-07 â€” Crunchbase deprecation Tier 1 (S6/S7 source swap)

**What we did**
- Extended `agent_strategy_run.py` with `strategy_6_startup_directory` (StartupList) and `strategy_7_trending` (Product Hunt RSS); failures log only.
- Updated `prompts/agent_formulation_run.txt` so agent runs prefer new sources; Crunchbase optional legacy.
- Additive S6/S7 scripts: StartupList/Product Hunt primary; Crunchbase paths kept as fallback menus.

**Why it matters**
Agent formulation runs no longer depend on Crunchbase login/screenshots for Strategies 6 and 7; existing interactive flows still work if users choose legacy.

**Intuition analogy**
Like switching your recipe appâ€™s default grocery list from a paywalled store to a local market feed, while keeping the old store on the map as a backup aisle.

---

## 2026-07-04 â€” Pandoc docx table borders

**What we did**
- Added `business_bookmark_sorter/pandoc_reference.docx` (Pandoc default + Table style grid borders).
- Wired `--reference-doc` in `_convert_with_pandoc`; post-step `_inject_inline_table_borders` writes explicit `tblBorders` into `word/document.xml`.
- Regenerated `business_ideas_20260704.docx` with bordered tables.

**Why it matters**
Business-idea Word exports now show full table grids instead of header-only lines from bare Pandoc defaults.

**Intuition analogy**
Like giving Word a printed form template with boxes drawn in, not just column labels floating on the page.

---

## 2026-07-04 â€” docx_export: non-blocking Word open

**What we did**
- Hardened `business_bookmark_sorter/docx_export.py`: `GetObject` instead of `Dispatch` (skip COM when Word isnâ€™t running), 10s COM close timeout, detached `cmd /c start` for open.
- Smoke-tested convert + `regenerate_and_open_docx` on a temp copy (~0.4s end-to-end).

**Why it matters**
Agent formulation runs no longer hang on Word COM startup during docx auto-open; Pandoc convert still runs first unchanged.

**Intuition analogy**
Like knocking on a door only if the lights are on â€” donâ€™t boot the whole house just to check whether one file is already open.

---

## 2026-07-03 â€” Phase C1: Google Forms CSV import script

**What we did**
- Added `scripts/import_google_forms_csv.py` to map Google Forms CSV columns to `ill_pay_to_v1` response JSON (`source: google_forms_import`).
- Sample fixture CSV + `test_import_google_forms_csv.py`; real output gitignored at `imports/google_forms_ill_pay_to.json`.
- Dashboard untouched (C2 will merge imported + live responses).

**Why it matters**
The ~12 legacy Google Form answers can be preserved in the same schema as the live Mizza411 tool before the form is closed.

**Intuition analogy**
Like converting old paper survey cards into the same database rows the new app already uses â€” format translation first, UI hookup second.

---

## 2026-07-03 â€” Strategy 3 Phase B3: sharing_utilities ref/UTM wiring

**What we did**
- Extended `sharing_utilities.py` with `build_tracked_survey_url`, `create_distributor_url`, and `generate_strategy3_distributor_kit`.
- Added CLI flags `--distributor-ref` and `--strategy3-kit`; Strategy 3 `distributor_links.py sharing-kit` subcommand.
- `network_problem_collector.py --distributor` optionally saves a per-distributor social sharing kit.

**Why it matters**
Distributors get WhatsApp/LinkedIn-ready links from one registry; survey ref tracking stays consistent across tools.

**Intuition analogy**
Like connecting your affiliate dashboard to the same promo codes the checkout already reads â€” one attribution scheme, many share surfaces.

---

## 2026-07-03 â€” Strategy 3 Phase B2: optional distributor mode in collector

**What we did**
- Extended `network_problem_collector.py` with `--distributor` flag; classic `python network_problem_collector.py` unchanged.
- Integrated `DistributorLinkManager` for register â†’ outreach â†’ optional export sync â†’ problem capture.
- Added `count_responses_by_ref`, export loader, and `test_network_problem_collector.py` (6 tests).

**Why it matters**
One CLI entry point now covers both classic network outreach and paid survey distribution without breaking the original workflow.

**Intuition analogy**
Like adding a "promoter mode" toggle to an existing CRM â€” same tool, different pipeline, default behavior untouched.

---

## 2026-07-03 â€” Strategy 3 Phase B1: paid distributor links (no collector changes)

**What we did**
- Added `distributor_links.py` in Strategy 3 folder â€” unique `ref`/UTM URLs for `ill_pay_to_v1`, local registry, outreach message generation.
- Added `distributor_brief.md`, `distributor_message_templates.txt`, example registry, and `test_distributor_links.py`.
- Left `network_problem_collector.py`, `sharing_utilities.py`, and live survey untouched (B2/B3 deferred).

**Why it matters**
Paid distribution can start immediately with tracked links and copy-paste outreach, without risking the live survey or the existing Strategy 3 CLI flow.

**Intuition analogy**
Like giving each promoter a unique discount code before rebuilding the whole checkout â€” attribution works on day one; deeper integration comes later.

---

## 2026-07-02 â€” â€œI'll pay to..â€ survey (Phase A) in Problem Identification Tool

**What we did**
- Added `ill_pay_to_v1` questionnaire (WTP, urgency, payment model, email) to both `web/data/` and `data/questionnaires.json`.
- Extended `questionnaire.js` with `email`/`short_text` types, `show_if` branching (2 rules), `?survey=` URL override, and `ref` capture on save.
- Kept `general_problems_v1` intact; dashboard reads both survey shapes without breaking older responses.

**Why it matters**
Strategy 3 can now share one flexible hosted survey instead of Google Forms, with conditional pricing questions and per-distributor tracking hooksâ€”without forking the whole app.

**Intuition analogy**
Like swapping a paper comment card for a Typeform-style flow on your own domain: same questions as the Google Form, but you control branching, branding, and who gets credit for each reply.

---

## 2026-06-27 â€” Agent-orchestrated business idea formulation run

**What we did**
- Ran Strategies 4â€“7, 9, 11â€“15 without the interactive master runner (blocked on `input()` prompts).
- Pulled live Nairametrics/BusinessDay RSS headlines, World Bank Nigeria indicators, and OWID internet trend CSV.
- Applied each strategyâ€™s prompt logic (news problems, niche combos, trending startup adaptation, personal problems from repo docs, GUEMF filter).
- Wrote consolidated output to `business_ideas_agent_run_20260627.md`.

**Why it matters**
The strategy scripts are designed for human-in-the-loop CLI sessions; an agent can substitute for ChatGPT Vision/manual paste steps by fetching public feeds and APIs, then producing the same Prompt 1aâ†’1b idea hooksâ€”except where sites block bots (Cloudflare on full articles).

**Intuition analogy**
Like running a Bloomberg terminal scrape plus a focus group in one pass: each â€œstrategyâ€ is a different lens on the same market, and the agent is the analyst who runs all lenses before the investment committee picks three names.




