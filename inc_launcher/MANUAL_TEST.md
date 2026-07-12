# Inc Launcher — Manual test (Phase 4 + Track C + Phase 5)

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task tracker:** [.cursor/rules/task.md](../.cursor/rules/task.md) §4 and §5  
**Session closed:** 2026-06-29 (Inc launcher + interval nudges + Track C bookmark menu)  
**Phase 5 agent formulation front door:** 2026-06-30 (5.0–5.4 shipped; §G manual once at v1 sign-off)

**Live on PC:** Interval nudges **[ON]**; Start at Windows login **[OFF]** (external `auto_launcher` boots tray). Commits: `4c54b9c` (Phase 4), `909c6d9` (Track C).

---

## Automated sign-off (agent runs — no manual UI)

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
| Bookmark queue counts | `test_cli_status.py`, `python -m business_bookmark_sorter status` |

**Automated pass recorded:** 2026-06-30 (pytest 57+ green; smoke_hub passed; Phase 5 signoff).  
**Prior:** 2026-06-29 (pytest 38+ green).  
**Live nudge proof:** `inc_launcher/schedule_fired.json` — 2026-06-29 09:00 task.md, 09:15 Hub, 10:00 Problem ID live (Monday).

Treat Phase 2 hub, Phase 4 A/B/C/E as **passed via automation** unless you opt into optional manual sections below.

---

## Manual only (optional — your choice)

### D. External auto-launcher at reboot

**Why not automated:** `auto_launcher.py` is in **another repo**; login/reboot is environment-specific.

- [ ] Reboot or log off/on (or run external `auto_launcher.py`)
- [ ] Confirm **one** Inc tray icon
- [ ] Confirm **Interval nudges** matches `launcher_config.json` after boot
- [ ] Inc **Start at Windows login [OFF]** when external launcher starts tray

**Skip if:** Daily use already shows one tray after login.

---

### E. Schedule comfort check (product decision — not a test pass/fail)

**Why manual:** Only you know if timed opens are too disruptive.

After living with nudges for a few days, decide:

- [ ] Keep schedule as-is (09:00 task, 09:15 Hub, M/W/F 10:00 Problem ID live, Sun YouTube)
- [ ] Tune `launcher_config.json` → `schedules.items` (e.g. remove/move **10:00 Problem ID** or **09:15 Hub**)
- [ ] Or tray → **Interval nudges [OFF]**

**Note (2026-06-29):** User linked unexpected auto-open to **10:00 Problem ID live** (browser tab, not Inc Hub). Hub auto-open is **09:15**.

---

### F. Bookmark filing workflow (operational — when you choose to file)

**Why manual:** Tkinter review UI + Chrome delete confirm; ~1926 pending links.

- [ ] Tray → **Formulated ideas → Bookmark review**
- [ ] File one link (**File & open doc**); confirm section in opened docx
- [ ] Delete bookmark in Chrome; confirm dialog → next item

Not required for launcher sign-off. Track progress: `python -m business_bookmark_sorter status`.

---

### G. Agent formulation run (Phase 5 v1)

**Automated (agent runs — no manual UI):**

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests/test_phase5_signoff.py inc_launcher/tests/test_agent_run.py -q
```

| §G step | Automated by |
|---------|----------------|
| Prompt file exists + loads | `test_phase5_signoff.py::test_prompt_file_exists_and_loads` |
| Formulated pillar: agent + CLI cards | `test_formulated_pillar_agent_and_cli_items` |
| Agent pinned; CLI demoted | `test_agent_formulation_run_is_pinned` |
| Hub header not clipped | `test_hub_header_subtitle_separate_rows` |
| Option B modal copy (title, bullets, buttons) | `test_option_b_modal_copy` |
| **Not now** skips run | `test_modal_not_now_skips_run_action` |
| **Start** invokes `agent_run` | `test_modal_start_runs_agent_action` |
| Hub card → modal (not direct action) | `test_hub_card_routes_to_modal_not_direct_action` |
| Tray path → Hub + modal | `test_tray_agent_run_opens_hub` (`test_agent_run.py`) |
| Orchestration (clipboard/cursor/paste) | `test_agent_run.py` |
| Kill old tray + restart + single instance | `test_tray_restart_single_instance` |

**Automated pass:** run pytest block above after tray restart (see `test_tray_restart_single_instance`).

**Manual only (deferred — when you choose):**

**Why not automated:** Pressing **Enter** in Cursor chat to send the agent message needs your IDE session and is subjective (prompt landed correctly in chat).

- [ ] After **Start**, focus Cursor chat if paste missed → **Enter** → confirm agent begins formulation run

Not required for Phase 5 dev sign-off; automation above covers §G steps 1–6, 9–10.

---

## H — Prospect Businesses folder (Formulated card) — 2026-07-12

**Task:** `.cursor/rules/task.md` §4 Prospect + Current Priority §12  
**Policy:** automate-first — **no required manual steps** for v1 sign-off.

### Automated (agent runs — no manual UI)

| Check | Covered by |
|-------|------------|
| Formulated card `prospect_businesses_folder` present | `inc_launcher/tests/test_config.py::test_formulated_has_prospect_businesses_folder` |
| Path `Prospect-Businesses/` resolves | same test |
| Established / Formulated anchors unchanged | same test |
| Sorter destination `prospects` | `business_bookmark_sorter/tests/test_prospect_route.py` |

```powershell
python -m pytest inc_launcher/tests/test_config.py business_bookmark_sorter/tests/test_prospect_route.py -q
```

### Manual only (optional — your choice)

**Why not automated:** Confirming the live tray/Hub UI after a local restart is a subjective “I see the card” glance (config already asserted in pytest).

- [ ] Restart Inc Launcher tray → Formulated ideas → **Prospect Businesses folder** opens `Prospect-Businesses/`

Not required for Prospect v1 close.

---

## Sign-off summary

| Check | Automated | Manual (optional) |
|-------|-----------|-------------------|
| Phase 4 nudges | Yes (2026-06-29) | Schedule tune (§E) |
| Phase 2 hub / menu | Yes | — |
| Track C menu wiring | Yes | Filing workflow (§F) |
| Phase 5 agent formulation | Yes — `test_phase5_signoff.py`, `test_agent_run.py` (2026-06-30) | Cursor **Enter** send (deferred §G) |
| Prospect Businesses Hub card | Yes — `test_formulated_has_prospect_businesses_folder` (2026-07-12) | Tray restart glance (§H) |
| External boot | — | §D if desired |

**Phase 5 v1:** Dev sign-off **passed via automation** (§G). Optional: Cursor **Enter** when you run a live agent session.  
**Prospect v1:** Dev sign-off **passed via automation** (§H). Optional: tray restart glance.

After any config change: stage, commit, and push (respect `.gitignore`).
