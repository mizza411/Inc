# Inc Launcher ΓÇö Manual test (Phase 4 + Track C + Phase 5)

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task tracker:** [.cursor/rules/task.md](../.cursor/rules/task.md) ┬º4 and ┬º5  
**Session closed:** 2026-06-29 (Inc launcher + interval nudges + Track C bookmark menu)  
**Phase 5 agent formulation front door:** 2026-06-30 (5.0ΓÇô5.4 shipped; ┬ºG manual once at v1 sign-off)

**Live on PC:** Interval nudges **[ON]**; Start at Windows login **[OFF]** (external `auto_launcher` boots tray). Commits: `4c54b9c` (Phase 4), `909c6d9` (Track C).

---

## Automated sign-off (agent runs ΓÇö no manual UI)

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests -q
python -m inc_launcher.tests.smoke_hub
python -m business_bookmark_sorter status
python -m pytest business_bookmark_sorter/tests/test_cli_status.py -q
```

| Area | Automated by |
|------|----------------|
| Interval nudges toggle / schedule / OFF | `test_phase4_signoff.py`, `test_phase4_toggle.py`, `test_nudge_scheduler.py`, `test_scheduled_nudges.py` |
| Phase 2 hub + menu build | `smoke_hub.py`, `test_config.py` |
| Track C bookmark review menu | `test_track_c_bookmark.py`, `test_config.py::test_formulated_has_bookmark_review` |
| Phase 5 agent run orchestration | `test_agent_run.py`, `test_phase5_signoff.py`, `test_config.py::test_formulated_has_agent_formulation_run` |
| ┬º14 Pass 2 Hub pack card | same + pack `prompt_path` / modal bullets asserts |
| Bookmark queue counts | `test_cli_status.py`, `python -m business_bookmark_sorter status` |

**Automated pass recorded:** 2026-06-30 (pytest 57+ green; smoke_hub passed; Phase 5 signoff).  
**Prior:** 2026-06-29 (pytest 38+ green).  
**Live nudge proof:** `inc_launcher/schedule_fired.json` ΓÇö 2026-06-29 09:00 task.md, 09:15 Hub, 10:00 Problem ID live (Monday).

Treat Phase 2 hub, Phase 4 A/B/C/E as **passed via automation** unless you opt into optional manual sections below.

---

## Manual only (optional ΓÇö your choice)

### D. External auto-launcher at reboot

**Why not automated:** `auto_launcher.py` is in **another repo**; login/reboot is environment-specific.

- [ ] Reboot or log off/on (or run external `auto_launcher.py`)
- [ ] Confirm **one** Inc tray icon
- [ ] Confirm **Interval nudges** matches `launcher_config.json` after boot
- [ ] Inc **Start at Windows login [OFF]** when external launcher starts tray

**Skip if:** Daily use already shows one tray after login.

---

### E. Schedule comfort check (product decision ΓÇö not a test pass/fail)

**Why manual:** Only you know if timed opens are too disruptive.

After living with nudges for a few days, decide:

- [ ] Keep schedule as-is (09:00 task, 09:15 Hub, M/W/F 10:00 Problem ID live, Sun YouTube)
- [ ] Tune `launcher_config.json` ΓåÆ `schedules.items` (e.g. remove/move **10:00 Problem ID** or **09:15 Hub**)
- [ ] Or tray ΓåÆ **Interval nudges [OFF]**

**Note (2026-06-29):** User linked unexpected auto-open to **10:00 Problem ID live** (browser tab, not Inc Hub). Hub auto-open is **09:15**.

---

### F. Bookmark filing workflow (operational ΓÇö when you choose to file)

**Why manual:** Tkinter review UI + Chrome delete confirm; ~1926 pending links.

- [ ] Tray ΓåÆ **Formulated ideas ΓåÆ Bookmark review**
- [ ] File one link (**File & open doc**); confirm section in opened docx
- [ ] Delete bookmark in Chrome; confirm dialog ΓåÆ next item

Not required for launcher sign-off. Track progress: `python -m business_bookmark_sorter status`.

---

### G. Agent formulation run (Phase 5 v1)

**Automated (agent runs ΓÇö no manual UI):**

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests/test_phase5_signoff.py inc_launcher/tests/test_agent_run.py -q
```

| ┬ºG step | Automated by |
|---------|----------------|
| Prompt file exists + loads | `test_phase5_signoff.py::test_prompt_file_exists_and_loads` |
| Formulated pillar: agent + CLI cards | `test_formulated_pillar_agent_and_cli_items` |
| Agent pinned; CLI demoted | `test_agent_formulation_run_is_pinned` |
| Hub header not clipped | `test_hub_header_subtitle_separate_rows` |
| Option B modal copy (title, bullets, buttons) | `test_option_b_modal_copy` |
| **Not now** skips run | `test_modal_not_now_skips_run_action` |
| **Start** invokes `agent_run` | `test_modal_start_runs_agent_action` |
| Hub card ΓåÆ modal (not direct action) | `test_hub_card_routes_to_modal_not_direct_action` |
| Tray path ΓåÆ Hub + modal | `test_tray_agent_run_opens_hub` (`test_agent_run.py`) |
| Orchestration (clipboard/cursor/paste) | `test_agent_run.py` |
| Kill old tray + restart + single instance | `test_tray_restart_single_instance` |

**Automated pass:** run pytest block above after tray restart (see `test_tray_restart_single_instance`).

**Manual only (deferred ΓÇö when you choose):**

**Why not automated:** Pressing **Enter** in Cursor chat to send the agent message needs your IDE session and is subjective (prompt landed correctly in chat).

- [ ] After **Start**, focus Cursor chat if paste missed ΓåÆ **Enter** ΓåÆ confirm agent begins formulation run

Not required for Phase 5 dev sign-off; automation above covers ┬ºG steps 1ΓÇô6, 9ΓÇô10.

---

## H ΓÇö Prospect Businesses folder (Formulated card) ΓÇö 2026-07-12

**Task:** `.cursor/rules/task.md` ┬º4 Prospect + Current Priority ┬º12  
**Policy:** automate-first ΓÇö **no required manual steps** for v1 sign-off.

### Automated (agent runs ΓÇö no manual UI)

| Check | Covered by |
|-------|------------|
| Formulated card `prospect_businesses_folder` present | `inc_launcher/tests/test_config.py::test_formulated_has_prospect_businesses_folder` |
| Path `Prospect-Businesses/` resolves | same test |
| Established / Formulated anchors unchanged | same test |
| Established All-launchers duplicate `prospect_businesses_folder_established` | `inc_launcher/tests/test_config.py::test_established_has_prospect_businesses_folder_duplicate` |
| Sorter destination `prospects` | `business_bookmark_sorter/tests/test_prospect_route.py` |

```powershell
python -m pytest inc_launcher/tests/test_config.py business_bookmark_sorter/tests/test_prospect_route.py -q
```

### Manual only (optional ΓÇö your choice)

**Why not automated:** Confirming the live tray/Hub UI after a local restart is a subjective ΓÇ£I see the cardΓÇ¥ glance (config already asserted in pytest).

- [ ] Restart Inc Launcher tray ΓåÆ Formulated ideas ΓåÆ **Prospect Businesses folder** opens `Prospect-Businesses/`
- [ ] Same restart ΓåÆ My Established business ideas ΓåÆ All launchers ΓåÆ **Prospect Businesses folder** opens the same folder (duplicate shortcut only)

Not required for Prospect v1 close.

---


### I. Formulation catch-up on tray start (section 19 Phase 7)

**Automated (required):** `test_formulation_phase78_signoff.py` plus sync/pending/opener/catchup/pr_fetch/catchup_schedule tests - multi-pack open, no re-open, toggle OFF skip, menu default ON, PR-branch pack fetch soft paths, post-B while-running schedule.

**Optional eyes-only (not a build blocker):** glance that Word actually appears once on a real tray restart. Why not automated: OS Word window focus is not asserted in CI.

- [x] Phase 7.8 behaviors covered by pytest (2026-10-10)
- [x] Real Word glance - owner saw the document open on this PC (2026-10-10)
- [x] Phase 7.9.1 PR-fetch unit tests (2026-10-11)
- [x] Phase 7.9.4 live proof (2026-10-11) - dirty tree + pack only on formulation branch → fetch → Word open, no merge (plus earlier A/B Test for cloud half)
- [x] Phase 7.11.1 schedule unit tests (2026-10-12) - once per day at/after 11:15, toggle OFF skip, missed-slot afternoon fire
- [x] Phase 7.11.2–7.11.3 late-retry unit tests (2026-10-12) - interval, cap, shown skip, max_retries=0 leaves primary alone
- [x] Phase 7.11.6 fast retry interval (2026-10-13) - default 10 min (not 45), cap still 8
- [ ] Phase 7.11.5 live proof (optional) - tray stays up across B, today’s pack opens without tray restart (primary or late retry). Why not automated: real Word + wall-clock after 11:00 WAT

### J. Ask people/owners always with Hub (NET-ASK-ALWAYS-SHOW-1)

**Automated (required):** `test_option_b_network_ask.py` + `test_net_ask_always_show.py` + `test_net_ask_always_show_signoff.py` + `smoke_hub` Ask checks - Hub `show` queues Ask, `daily_inc_hub` path, schedule Option B, restore, cadence copy still present off-day.

**Optional eyes-only (1c leftover):** Open Inc Hub from tray → Hub + Ask together. Dismiss → tray **Show Ask people / owners** or Hub **Show Ask reminder**. Why not automated: live tk z-order / grab feel.

### J2. Prospect nudge after Ask dismiss (2026-10-17)

**Automated (required):** `inc_launcher/tests/test_prospect_nudge_after_ask.py` - resolve Established Prospect card, Ask always-show passes `on_closed`, nudge selects Established, Open folder copy.

**Optional eyes-only:** Open Hub → dismiss Ask (Not now) → Prospect nudge appears → Established All launchers visible → **Open folder** or click the Prospect card. Why not automated: live modal grab / Hub glance.

- [x] Phase 0b + 1a + 1b + 1c automated sign-off (2026-10-12) - 18 related pytest + smoke_hub PASSED
- [ ] Optional live pair + restore glance (not a build blocker)


## Sign-off summary

| Check | Automated | Manual (optional) |
|-------|-----------|-------------------|
| Phase 4 nudges | Yes (2026-06-29) | Schedule tune (section E) |
| Phase 2 hub / menu | Yes | - |
| Track C menu wiring | Yes | Filing workflow (section F) |
| Phase 5 agent formulation | Yes - test_phase5_signoff / test_agent_run (2026-06-30) | Cursor Enter (section G, optional) |
| Prospect Businesses Hub card | Yes - prospect folder config test (2026-07-12) | Tray restart glance (section H) |
| Phase 7 formulation catch-up | Yes - Phase 7.8 signoff + module tests (2026-10-10) | Optional Word glance (section I) |
| External boot | - | section D if desired |

**Phase 5 v1:** Dev sign-off **passed via automation** (┬ºG). Optional: Cursor **Enter** when you run a live agent session.  
**Prospect v1:** Dev sign-off **passed via automation** (┬ºH). Optional: tray restart glance.

After any config change: stage, commit, and push (respect `.gitignore`).
