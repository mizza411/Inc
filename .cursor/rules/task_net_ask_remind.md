# NET-ASK-REMIND-1 — Ask-people / ask-owners problem collection reminder (S3 + S4)

**Status:** 🟡 **Phase 6 in progress** (2026-08-08) — automation green; owner asks + `MANUAL_TEST.md`  
**Follow-up:** Phase 7a and 7b done 2026-10-21. Phase 7c blocked 2026-10-21. Phase 4 and Not now passed. Two phase 3 checks failed for reasons outside this slice. Owner clocks were not edited.  
**Attempt (Phase 6 start / manual handoff):** 1  
**Authoritative backlog:** **this file** (main `.cursor/rules/task.md` overloaded — thin pointer only there)  
**Owner ask (2026-08-08):** Recurring reminder to ask people around you for business problems, via **Inc infrastructure** and/or **project_reminder**; connects to **Strategy 3** (network) **and** **Strategy 4** (business owners). Prove understanding first; then phased backlog; **automate-first** for all automatable parts.

**One-liner:** Nudge you on a cadence to **talk to humans** (network + owners), then dump answers into existing S3/S4 / Problem ID capture paths — without fusing those products or auto-messaging strangers.

**Related (do not merge / do not break):**

| Track | Why separate |
|-------|----------------|
| **Strategy 3** folder / `network_problem_collector.py` | Capture + distributor tooling — reminder **calls** it, does not rewrite core |
| **Strategy 4** folder / `business_owner_problem_collector.py` | Owner questionnaire collection — reminder **points** at it |
| **§1** Problem ID Tool / `ill_pay_to_v1` | Optional capture sink; do not change survey schema for this track |
| **§4** Inc Hub agent formulation Option B | Pattern precedent for Hub-hosted nudge; **separate** schedule key / modal copy |
| **§14** agent formulation / `run_all_strategies.py` | S3/S4 stay verbal/network; do **not** force into Run ALL |
| **NICHE-EVENT-1 / AGRIC-IDEAS-1** | Different ops playbooks |
| Tegrid / FIR / OTI / §6 / §5 bookmarks | Unrelated |

---

## Layout (locked 2026-08-08 — create folder only when Phase 1 starts)

**Decision:** dedicated thin folder at Inc root:

| Path | Role |
|------|------|
| `network_ask_reminder/` | Playbook, cadence config, rotate script, capture log schema, smokes, `MANUAL_TEST.md` |
| Keep S3 / S4 folders | Existing collectors + playbooks unchanged except optional **one-line** “see NET-ASK-REMIND-1” cross-link |

**Signals for dedicated folder:** own config/data/logs; dual delivery surfaces (Inc + PR); must not live inside `inc_launcher/` core or rewrite Strategy CLIs; multi-session habit tool.

**Hard isolation (modularization — avoid breaking ANYTHING ANYWHERE):**

- [x] **Never** edit Tegrid, FIR, OTI, §6, gadget ops, bookmark sorter, or Strategy 1/5/12/15 CLIs for this track
- [x] **Never** register S3/S4 into agent “Run ALL” or change `RETIRED_STRATEGIES`
- [x] **Never** scrape contacts / auto-DM / auto-WhatsApp-send strangers
- [x] **Inc surface:** additive schedule + Hub modal only (Option B pattern); **no** detached OS toasts; tray-running gate like formulation
- [x] **PR surface:** prefer additive `launcher_config.json` `is_document: true` — **no** `auto_launcher.py` edit unless proven broken; Task Reminder seed (**AUTO-NAR-05**) remains **optional** secondary
- [x] **Do not** fuse Problem ID schema, distributor registry, or Tegrid GTM
- [x] New modules **under ~500 lines**; one concern per file (config vs nudge vs log vs smoke)
- [x] Automated checks for config/schedule/isolation; `MANUAL_TEST.md` **only** for human ask + real conversation + subjective “was this ask useful”

**Phase 0 locks (2026-08-08 — owner menu 1; satellite defaults applied):**

| Lock | Locked value |
|------|----------------|
| **Primary surface** | **both** — Inc Hub/tray **and** `project_reminder` (one config SoT under `network_ask_reminder/`) |
| **Cadence** | **3×/week** — Mon / Wed / Fri |
| **Rotate mode** | **alternate** S3 ↔ S4 |
| **Folder name** | **`network_ask_reminder/`** at Inc root |
| **Capture sinks** | **local log + pointers** to S3 / S4 / Problem ID (no Problem ID schema change) |
| **PR delivery primary** | Morning **`.docx` playbook open** via additive `launcher_config` (`is_document`) — not Task Reminder-first |
| **Inc delivery** | Hub Option-B-style nudge on cadence (Phase 3) |

---

## Requirements lock (owner request + agent recommendations)

### A — Owner-requested features

1. **Habit reminder** to ask **people around you** for business problems (network / everyday contacts) → **Strategy 3**.
2. Same habit must also cover **business owners** (structured / questionnaire path) → **Strategy 4**.
3. Delivery via **Inc repo infrastructure** and/or **task reminder / project_reminder** app.
4. Must not break existing formulation, Hub, launcher, or strategy runners.

### B — Agent recommendations (in backlog)

1. One cadence config; dual copy (S3 vs S4); rotate or dual-prompt — not two unrelated apps.
2. Capture = append-only local log + links to existing tools (no new survey product in v1).
3. Hub nudge mirrors Option B (tray gate; Hub-hosted; Start / Not now).
4. PR path = morning `.docx` playbook open as **primary** (locked); Task Reminder seed optional later (**AUTO-NAR-05**).
5. Smokes for config/schedule/isolation; manual only for real conversations.
6. Portfolio habit: later review other “verbal strategy” gaps (S2) — **out of scope** unless separate task.

### C — Feature acceptance (what “done” means)

| # | Feature | Done when |
|---|---------|-----------|
| F1 | Cadence locked + stored in config | JSON/YAML loads; smoke asserts days/times |
| F2 | Reminder fires on surface(s) | Automated clock/fixture smoke + one owner live see |
| F3 | Copy names S3 and/or S4 action | Fixture asserts strings / rotate logic |
| F4 | Dismiss / snooze without killing other Hub/PR reminders | Unit/smoke; no regression on formulation Option B |
| F5 | Capture path documented + log append CLI/script | Smoke appends fixture row |
| F6 | Isolation: unrelated apps untouched | Grep/smoke allowlist of edited paths |

**Out of scope (v1):** auto-messaging people; CRM of all contacts; forcing S3/S4 into agent Run ALL; new mobile app; changing Problem ID questions.

---

## Automation vs manual (expression / operation)

### Can be automated (little/no manual intervention once wired) — **must-build** named work items

| ID | Area | What automation does |
|----|------|----------------------|
| **AUTO-NAR-01** | Cadence config | Load/validate schedule (days, time, timezone, rotate mode) from `network_ask_reminder/config.json` (name TBD) |
| **AUTO-NAR-02** | Prompt rotate | Deterministic S3 vs S4 (or both) prompt selection from date + config |
| **AUTO-NAR-03** | Inc Hub nudge | Additive schedule key → open/focus Hub → Option-B-style modal (Start / Not now); tray-running gate |
| **AUTO-NAR-04** | PR document open | Additive `launcher_config` `is_document` opens playbook `.docx` on boot (config-only) |
| **AUTO-NAR-05** | Optional PR task seed | Script to upsert a recurring Task Reminder item from template (if Task Reminder JSON API/path known; else skip) |
| **AUTO-NAR-06** | Capture log append | CLI: `ask-log add --mode s3|s4 --notes "..."` → timestamped JSONL/CSV under folder (gitignored data OK) |
| **AUTO-NAR-07** | Streak / last-asked | Derive last-ask + days-since from log; show in modal or `status` CLI |
| **AUTO-NAR-08** | Playbook → docx | Pandoc md→docx smoke beside playbook |
| **AUTO-NAR-09** | Isolation / regression smokes | Config validate; schedule key present; formulation Option B untouched; allowlisted paths |
| **AUTO-NAR-10** | Ask script drafts | Generate **copy-paste** WhatsApp/SMS openers for S3 and S4 (send stays manual) |
| **AUTO-NAR-11** | Cross-link stubs | One-line README pointers in S3/S4 folders to this track (additive only) |

### Cannot be automated (owner / manual checklist only)

| ID | Area | Why not automated |
|----|------|-------------------|
| **MAN-NAR-01** | Choosing **whom** to ask each day | Social judgment / privacy |
| **MAN-NAR-02** | Having the real conversation | Human presence / trust |
| **MAN-NAR-03** | Judging if a problem is “worth” pursuing | Taste + capital |
| **MAN-NAR-04** | Filling owner questionnaire **with** a live owner | Relationship + consent |
| **MAN-NAR-05** | Sending messages / calls | Intentional outreach; anti-spam |
| **MAN-NAR-06** | Approving Phase 0 locks (surface, cadence, folder) | Owner product decision |
| **MAN-NAR-07** | Live “did the nudge appear on my machine” once | OS tray/boot subjectivity — after smokes green |
| **MAN-NAR-08** | Graduating a captured problem into a build / Started-Businesses | Explicit user OK only |

**Automate-first rule:** every **AUTO-NAR-*** item is a **must-build** backlog item under the phase that names it. **MAN-NAR-*** items go only in `network_ask_reminder/MANUAL_TEST.md` (or Phase 0 owner checklist here) — owner runs **one** manual pass at v1 sign-off.

---

## Phases

### Phase 0 — Spec lock (backlog only; **no product files yet**)

- [x] **0.0** Satellite backlog created (`task_net_ask_remind.md`) + main `task.md` pointer — **2026-08-08**
- [x] **0.1** Owner locks **primary surface(s)** — **both** (Inc + PR) *(MAN-NAR-06)* — **2026-08-08**
- [x] **0.2** Owner locks **cadence** + **rotate mode** — **3×/week Mon/Wed/Fri** · **alternate S3↔S4** *(MAN-NAR-06)* — **2026-08-08**
- [x] **0.3** Owner approves folder **`network_ask_reminder/`** — **2026-08-08**
- [x] **0.4** Owner confirms isolation checklist above — **2026-08-08**
- [x] **0.5** Owner confirms capture sinks — **local log + pointers** (no Problem ID schema change) — **2026-08-08**

**DoD:** ✅ Phase 0 complete. **No** `network_ask_reminder/` folder until Phase 1 starts.

---

### Phase 1 — Scaffold (docs + config stub only)

- [x] **1.0** Create `network_ask_reminder/README.md` (purpose, do-not-touch list, how to run smokes) — **2026-08-08**
- [x] **1.1** Stub playbook `ask_people_ask_owners_playbook.md` (S3 + S4 daily ritual, ASCII flow) — **2026-08-08**
- [x] **1.2** Stub `config.example.json` (cadence, rotate, surfaces, quiet hours) — **AUTO-NAR-01** schema draft — **2026-08-08**
- [x] **1.3** Stub `MANUAL_TEST.md` with **MAN-NAR-*** only (no fake automated steps) — **2026-08-08**
- [x] **1.4** **AUTO-NAR-11** additive one-line cross-links in S3 + S4 READMEs — **2026-08-08**

**DoD:** ✅ Folder + stubs exist; no Hub/PR wiring yet; no strategy CLI behavior change.

---

### Phase 2 — Core automation (must-build AUTO items; no live outreach)

- [x] **2.1** **AUTO-NAR-01** — Implement config load + validate; fixture smoke — **2026-08-08**
- [x] **2.2** **AUTO-NAR-02** — Rotate / both-prompt selector; unit tests — **2026-08-08**
- [x] **2.3** **AUTO-NAR-06** — Capture log append CLI + gitignore data path; smoke — **2026-08-08**
- [x] **2.4** **AUTO-NAR-07** — `status` CLI (last asked, streak, next mode) — **2026-08-08**
- [x] **2.5** **AUTO-NAR-10** — Opener draft generator (stdout/file only; no send) — **2026-08-08**
- [x] **2.6** **AUTO-NAR-09** — Isolation smoke (path allowlist / no Hub artifacts yet) — **2026-08-08**

**DoD:** ✅ `python -m unittest network_ask_reminder.tests.test_phase2_smoke -v` green (9 tests); CLI smokes OK.

---

### Phase 3 — Inc delivery surface (only if Phase 0 includes Inc)

- [x] **3.1** **AUTO-NAR-03** — Additive Hub card `network_ask_remind` + schedule `network_ask_mwf` (Mon/Wed/Fri 09:30); logic in `hub_nudge.py`; thin `inc_launcher` hooks — **2026-08-08**
- [x] **3.2** Option-B-style modal: rotate copy; **Start** = playbook + clipboard openers; **Not now** = dismiss — **2026-08-08**
- [x] **3.3** Tray-running gate (schedule/tray → Hub modal via `open_hub_with_option_b`; no detached toasts) — **2026-08-08**
- [x] **3.4** **AUTO-NAR-09** — Regression: formulation Option B + schedule validate; phase2+3 smokes + `inc_launcher` tests green — **2026-08-08**

**DoD:** ✅ Fixture/config/schedule smokes prove nudge path; formulation Hub path unbroken (`agent_formulation_run` still pinned).

---

### Phase 4 — project_reminder delivery surface (only if Phase 0 includes PR)

- [x] **4.1** **AUTO-NAR-08** — Pandoc playbook → `.docx` (~12 KB) + `build_docx` CLI — **2026-08-08**
- [x] **4.2** **AUTO-NAR-04** — Additive `project_reminder` `launcher_config.json` key `ask_people_ask_owners_playbook` (`is_document: true`); **no** `auto_launcher.py` edit — **2026-08-08**
- [x] **4.3** **AUTO-NAR-05** — **SKIPPED** with reason in `task_reminder_seed.py` (unclear safe Task Reminder upsert; Hub + docx cover nudge) — **2026-08-08**
- [x] **4.4** Path-exists + JSON validate smoke (`test_phase4_smoke` / `validate-pr-launcher`) — **2026-08-08**
- [x] **4.5** Append boot-open steps to `MANUAL_TEST.md` T1b *(MAN-NAR-07)* — **2026-08-08**

**DoD:** ✅ Docx on disk; additive launcher key; unrelated PR apps still present in validate smoke.

---

### Phase 5 — Playbook body + dual-mode ritual (content)

- [x] **5.1** S3 section: whom to ask, 3 opener lines, what to write down — **2026-08-08**
- [x] **5.2** S4 section: owner ask + questionnaire pointer + consent note — **2026-08-08**
- [x] **5.3** After-ask: how to run log CLI + when to open Problem ID — **2026-08-08**
- [x] **5.4** ASCII “nudge → ask → log → formulate” diagram in playbook — **2026-08-08**
- [x] **5.5** Risks: spam, awkwardness, no-PII-in-git, Macrodroid legacy note — **2026-08-08**
- [x] **5.6** Regenerate `.docx` via `build-docx` after body update — **2026-08-08**

**DoD:** ✅ Playbook readable end-to-end; under ~500 lines; docx rebuilt.

---

### Phase 6 — Owner ops + v1 sign-off

**Ready for single manual pass — run `network_ask_reminder/MANUAL_TEST.md`** (2026-08-08).

**Automation already covered (agent):** Phase 2–4 smokes **20/20** · `isolation-check` · `validate-pr-launcher` · Hub card/schedule wiring · docx present · CLI `today` / `openers` / `log-add` / `status`.

**Owner still does (cannot automate):**

- [ ] **6.1** *(MAN-NAR-01–05)* Run real asks for ≥3 cadence hits (mix S3 + S4) — next cadence **Mon 2026-08-10** (today Sat is off-cadence; early asks OK)
- [ ] **6.2** Log each ask: `python -m network_ask_reminder log-add --mode s3|s4 --notes "..." --role "..."`
- [ ] **6.3** *(MAN-NAR-07)* Single live pass of `MANUAL_TEST.md` (T1a Hub and/or T1b PR boot + T2/T3)
- [ ] **6.4** *(MAN-NAR-03/08)* Decide park vs graduate per problem (explicit OK only)
- [ ] **6.5** Tell agent “Phase 6 done” (or defer in writing) → mark v1 complete here + main pointer

**DoD:** Automation green ✅; owner completed one manual pass; ≥3 logged asks **or** documented defer.

---

### Phase 7 — Start opens the Word playbook (queued 2026-10-21)

**Owner request:** Clicking **Start** in the Ask people / owners window opens `network_ask_reminder/ask_people_ask_owners_playbook.docx`. It does not open `ask_people_ask_owners_playbook.md`.

**Today:** Start opens the Word file. It does not open the markdown. Morning login already prefers that same Word file. **Not now** only closes the window.

**Out of this phase:** Phase 6 real asks, Hub open-time clocks, owner `launcher_config.json` times, funding notes, a second tray, and rebuilding the Word file on every click.

#### 7a — Open the Word file from Start

- [x] **7a.1** Point Start at the existing Word path (`PLAYBOOK_DOCX` in `build_docx.py`), not a second hardcoded path. — **2026-10-21**
- [x] **7a.2** Test with `os.startfile` mocked. Assert the opened path ends in `.docx`, and the `.md` path is not opened. Pytest must not launch Word. — **2026-10-21** (`test_start_opens_docx_not_markdown` and `test_start_writes_openers_file` passed)

**Done when:** a green test shows Start opens the Word file only. Openers are still copied. You still send them. Met 2026-10-21.

**Estimate:** 15 minutes.

#### 7b — Missing Word file does not fall back to markdown

- [x] **7b.1** If the `.docx` is missing, Start still writes and copies the openers, sets `playbook_opened` false, and does not open the `.md`. — **2026-10-21**
- [x] **7b.2** Test that case on a temp folder, or a patched missing path, so the live playbook pair is not deleted. — **2026-10-21** (`test_missing_docx_does_not_open_markdown` passed)

**Done when:** a green test shows no markdown open when the Word file is absent. Met 2026-10-21.

**Estimate:** 10 minutes.

#### 7c — Leave the other open paths alone

- [ ] **7c.1** Re-run the Ask phase 3 and phase 4 smokes. **Not now** still dismisses. Login still points at the same Word file. **Blocked 2026-10-21:** phase 4 passed, and `test_modal_not_now_skips_run_action` passed. Phase 3 `test_hub_card_and_schedule` failed because the live hour is 11 and the test still expects 9. Phase 3 `test_isolation_still_ok` failed because the cross-link line is missing in two strategy READMEs. Those README files were not edited.
- [x] **7c.2** Do not edit Hub schedule ids, `nudge_scheduler.py`, or the owner’s saved clock times. — **2026-10-21** `nudge_scheduler.py` is unchanged. `launcher_config.json` was not edited in this slice. It is still dirty from the earlier saved clocks.

**Done when:** those smokes pass, and the diff does not include `inc_launcher/launcher_config.json`. Not met. The clock file was not part of this slice, and two phase 3 checks are still red.

**Estimate:** 10 minutes.

**Phase 7 recommendations (locked for the build):**

1. One Word path, the one `build_docx.py` already uses.
2. No markdown fallback. The owner named the Word file as the only file Start opens.
3. Do not run pandoc on the click. Open the Word file that is already on disk.
4. Mock `os.startfile` in tests.
5. Do not add a manual Word-layout step. The path check is automatable.

---

## v1 definition of done

- Phases **0–5** complete on disk  
- Phase **6** owner manual checklist done once (or deferred in writing)  
- **No** breakage of Hub formulation, strategy runners, FIR/OTI/Tegrid, or PR unrelated launcher keys  

---

## Suggested milestones (from 2026-08-08)

| Milestone | Target |
|-----------|--------|
| Phase 0 locks | **2026-08-09** |
| Phase 1 scaffold | **2026-08-10** |
| Phase 2 core AUTO | **2026-08-12** |
| Phase 3 and/or 4 surfaces | **2026-08-14** |
| Phase 5 playbook | **2026-08-15** |
| Phase 6 first 3 asks + sign-off | **2026-08-22** |

---

## Chat handoff

**Safe to delete chat after Phase 6 owner pass is recorded here (or deferred).** Pending = Phase 6 checkboxes + `MANUAL_TEST.md`; not chat memory.  
Re-open with: “Phase 6 done NET-ASK-REMIND-1” or “Defer NET-ASK Phase 6”.
