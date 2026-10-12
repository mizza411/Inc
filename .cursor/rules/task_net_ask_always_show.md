# NET-ASK-ALWAYS-SHOW-1 — Ask people / owners small window always with Inc launcher

**Status:** 🟢 **COMPLETE** (2026-10-12) — Phases **0 · 0b · 1a · 1b · 1c** done. Optional live glance only in `inc_launcher/MANUAL_TEST.md` section J.  
**Attempt (intake):** 2 (re-confirmed 2026-10-12 with Inc Launcher screenshot + live diagnose)  
**Authoritative backlog:** **this file** (thin pointer in Inc `.cursor/rules/task.md`).  
**Raised from:** project_reminder OWNER BATCH 01/09 evening (groups 1–3 moved off that repo). Reconfirmed with owner **2026-10-12**.

**One-liner:** Every time **Inc launcher** (Hub) is up, the Ask people / owners **small window** (Hub Option-B `network_ask` modal) is **on screen with it** — not sometimes missing.

**Parent:** **NET-ASK-REMIND-1** (`task_net_ask_remind.md`, `network_ask_reminder/`, `inc_launcher` Option B). This track is **pairing reliability**, not a new ask product.

**Related (do not merge / do not break):** NET-ASK-REMIND-1 Phase 6 manual asks · formulation Option B · **BB-TIMED** / **BB-IDLE-AUTO** · Tegrid / FIR / OTI · project_reminder playbook `.docx` boot key (`ask_people_ask_owners_playbook`) — that Word open is **not** a substitute for this small window · §19 formulation Word catch-up (**7.11**) is a different window.

---

## Prove-understanding lock (owner)

- Pain: window **sometimes** appears with Inc launcher, **sometimes not**. Want **always**.
- Surface: the **small** Ask people / owners modal (`show_agent_run_modal` / Option-B path for `network_ask`), same session and screen as Inc launcher (screenshot: Inc Launcher on My Established business ideas).
- Dismiss is allowed. **Restore** from tray/hub must exist. **Next Inc start** still shows the pair.
- Cadence (Mon/Wed/Fri copy rotate) may still change **text**. It must **not** be why the window is absent when the launcher is up. **Lock:** launcher up → window visible (off-cadence = preview copy is OK).
- Never auto-message anyone.

---

## Diagnose lock (2026-10-12 — Phase 0 done, no code)

| Finding | Evidence |
|---------|----------|
| Hub alone ≠ Ask modal | `daily_inc_hub` fired **2026-10-12 09:15** (big window only) |
| Ask schedule “fires” but does nothing useful | `network_ask_mwf` fired **2026-10-12 09:30**, then `run_action` logs **`Unknown action type: network_ask`** (no raise, still marked fired) |
| Dispatch broken | `inc_launcher/actions.py` has no `network_ask` branch. Phase 3 test `test_run_action_dispatches_network_ask` **FAILED** on this PC |
| Modal wiring incomplete | `uses_option_b_modal("network_ask")` is True, but Hub/tray only open the Option B modal for `agent_run` |
| Always-show missing | No path shows the Ask modal on every launcher/Hub open or tray start |

```
09:15  Hub opens           -->  big window only
09:30  network_ask "fires" -->  unknown action --> no small window
tray / Hub start           -->  no always-show pair yet
click Ask card             -->  same broken run_action
```

---

## Layout

Stay in Inc: `inc_launcher/` + `network_ask_reminder/hub_nudge.py`. Do **not** move code to project_reminder. PR may keep booting the tray (`inc_launcher_tray`) and the playbook doc — do not treat the doc as the small window.

---

## Detailed ASCII

```
  Project Manager / boot / login
           |
           spawn Inc launcher tray  (pythonw -m inc_launcher.tray_app)
           |
           Inc launcher (Hub) is up
           |
           MUST ALSO (same session, same screen):
           Ask people / owners SMALL WINDOW
           (Hub Option-B modal · action=network_ask)
           |
           diagnose (2026-10-12): unknown action + Hub-only
           schedule + cadence-only path + no always-show
           |
           fix: Hub/launcher up  ==>  small window visible
           |
           owner dismisses --> restore from tray / hub
           next Inc start --> pair again (always-show rule unchanged)
```

---

## Phases (do not start code until picked)

| Phase | Scope | Est. min | Status |
|-------|--------|----------|--------|
| **0** | Diagnose miss (startup, cadence, Hub vs modal, dispatch) | 20 | ✅ **2026-10-12** |
| **0b** | Fix `network_ask` dispatch + Hub/tray Option B modal path. `actions.py` → `run_network_ask_start`. Hub card + tray + schedule open modal via `open_hub_with_option_b` + `prepare_option_b_item`. Phase 3 dispatch test green. Formulation Option B unchanged. | 35 | ✅ **2026-10-12** |
| **1a** | Always show Ask modal whenever Inc launcher (Hub) opens (tray Open Hub, `daily_inc_hub`, and always-show rule). Cadence may change copy only. | 40 | ✅ **2026-10-12** |
| **1b** | Restore after dismiss (tray/hub menu) | 15 | ✅ **2026-10-12** |
| **1c** | Smoke/manual: launcher up ⇒ window every time. Automate what can be mocked. | 15 | ✅ **2026-10-12** |

**0b shipped (2026-10-12):** `inc_launcher/actions.py` · `option_b_actions.prepare_option_b_item` · Hub/tray/schedule Option B path · tests `test_option_b_network_ask.py` + Phase 3 dispatch.

**1a shipped (2026-10-12):** `HubController.show` queues `always_show_network_ask` after `show`. Covers tray Open Hub + `daily_inc_hub`. `prompt_agent_run` for `agent_run` does **not** stack a second Ask grab. Tests: `test_net_ask_always_show.py`.

**1b shipped (2026-10-12):** Tray **Show Ask people / owners** + Hub sidebar **Show Ask reminder** (hover label) + `restore_network_ask()`. Hub Ask card still works. Dismiss then restore without waiting for next boot.

**1c shipped (2026-10-12):** Automated sign-off `test_net_ask_always_show_signoff.py` + existing 0b/1a/1b tests (**18** related passed) + `smoke_hub` checks Ask card, tray restore label, Hub open (pairs Ask). Live tk z-order glance remains optional in MANUAL_TEST section J (Why not automated: OS window grab feel).

**Hard isolation:** additive. Do not break formulation Option B, bookmark review schedule, or NET-ASK capture CLIs. No auto-DM. Do not treat playbook Word as the small window.

**Effort remaining:** **0** (parent complete). Satellite may be deleted after you stage/commit; pointer in `task.md` can stay as done one-liner.
