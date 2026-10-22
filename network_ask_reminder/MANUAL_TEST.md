# MANUAL_TEST — network_ask_reminder (NET-ASK-REMIND-1)

**Automate-first:** config validate, rotate, log append, pandoc, launcher JSON, Hub regression = agent smokes (Phases 2–4).  
**This file:** only **MAN-NAR-*** human steps. Run **once** at v1 sign-off (or when agent says ready).

## Prerequisites

- [ ] Phase 2–4 smokes green (agent reported)
- [ ] Phase 0 locks still match your preference (both surfaces · Mon/Wed/Fri · alternate)
- [ ] `ask_people_ask_owners_playbook.docx` exists beside the `.md`
- [ ] `project_reminder/launcher_config.json` has `ask_people_ask_owners_playbook` (`is_document: true`, `enabled: true`)

## T1 — Live nudge appeared *(MAN-NAR-07)*

**Why not automated:** real Windows tray / boot / Word handler.

### T1a — Inc Hub (Phase 3)

- [ ] Inc Launcher tray running · `schedules.enabled` true
- [ ] On Mon/Wed/Fri **09:30**: Hub opens with Option B “Ask people today?” **or** click Hub → Problem identification → **Ask people / owners (S3+S4)**
- [ ] **Start** opens playbook + copies openers; **Not now** dismisses (no send)
- [ ] Agent formulation Option B card still works unchanged

### T1b — project_reminder boot open (Phase 4)

- [ ] Sign in / run project_reminder auto-launch as usual
- [ ] Confirm `ask_people_ask_owners_playbook.docx` opens once (or appears in launch set)
- [ ] Unrelated launcher docs still open as before (oldies/agric/etc. unchanged)

**Pass / fail notes:**

|

## T2 — Real asks *(MAN-NAR-01–05)*

**Why not automated:** social judgment, consent, live conversation, no auto-send.

- [ ] Complete ≥3 cadence hits mixing S3 and S4
- [ ] You chose whom; you held the conversation; you did not auto-message strangers
- [ ] Each ask logged via Phase 2 CLI (no phones in git)

**Pass / fail notes:**

|

## T3 — Graduate or park *(MAN-NAR-03 / MAN-NAR-08)*

**Why not automated:** capital / taste / Started-Businesses rule.

- [ ] Decide for each logged problem: park · research more · explicit graduate (owner OK only)

**Pass / fail notes:**

|

## Sign-off

- [ ] Single manual pass complete · date: ________ · notes: ________
