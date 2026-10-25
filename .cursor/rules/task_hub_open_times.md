# HUB-OPEN-TIMES-1 - Settings control for Inc Hub open times

**Status:** Phases 1-6 done (Phase 6 on 2026-10-25). Phases 1-5 had 39 tests on 2026-10-21. Phase 6 checks passed, with one Tcl file-lock error on a crowded run that passed when that single check was run again. Manual layout line waived. A tray already running keeps the old menu until that tray is restarted.
**Attempt (backlog write):** 1. Follow-up write: 1 (2026-10-25).
**Authoritative backlog:** this file only
**Main `task.md`:** not referenced (overloaded, about 2,700 lines). Do not add a pointer there.
**Delete when:** Phases 1-5 and Phase 6 are done or waived, the temp-config tests are green, and the one manual layout look is done or waived. Then delete this satellite. Do not fold it into `task.md`. Do not delete this file while Phase 6 is open.

## Owner ask (2026-10-21)

A Settings control for the times that auto-open Inc Hub. Confirmed in chat: hold the build until this note exists, then still do not build until a later pick.

The two clocks in scope:

| Id | What it does today | Time now | Days now |
|----|--------------------|----------|----------|
| `daily_inc_hub` | Opens Inc Hub, and the Ask window with it | 09:15 | every day |
| `network_ask_mwf` | Opens Inc Hub again for Ask | 09:30 | mon, wed, fri |

## Recommendations (locked with the phases)

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| R1 | Only those two rows. Leave 09:00 `task.md`, 10:00 Problem ID, 11:00 bookmark review, and Sunday 18:00 YouTube on their current clocks. | The ask was Hub open times. | 1 |
| R2 | New modules. Do not grow `hub_window.py` (already long) or fold the form into `tray_app.py`. | A small tray edit cannot take down the Hub. | 2, 3 |
| R3 | One patch writer. Load the config, change time and days on those two ids only, write the file back. Leave `schedules.enabled`, other items, pillars, and paths alone. | The on/off toggle already rewrites this file. A wide write would clobber it. | 1 |
| R4 | Settings is a Toplevel on the existing Hub window, queued onto the Hub UI thread. Do not create a second Tk root from the tray callback. | A second root is a known way for the tray icon to vanish. | 2, 3 |
| R5 | Save stores the clocks. Cancel closes without writing. Save stays disabled when a row has no day ticked, or the time is not a real hour and minute. | Empty days would silently stop that open. The tray on/off switch remains the master switch. | 2 |
| R6 | Tray label is the action text, because this tray has no Windows hover API. Buttons inside the window get real hover labels. | Same pattern as Restart. | 2, 3 |
| R7 | Remember the Settings window position and size on the same config write, after a short delay. If the saved spot is off the screen, place it back on the visible screen. First open uses a normal default size. | New window rule. The owner does not set this by hand. | 4 |
| R8 | Tests use a temp copy of the config. Do not write the live `launcher_config.json` from tests. Do not restart Project Manager. | Proves isolation. | 1, 5 |
| R9 | After Save, the running scheduler picks up the new clock on its next poll. No tray restart is required for the time change. | `tick` already reloads the config. | 5 |

## Out of scope

- Turning Interval nudges on or off (that tray row already exists).
- Changing any schedule id other than the two above.
- A per-row off switch. Clearing every day is refused, not stored.
- Funding notes, prospect files, and `task_prospect_funding_equity.md`.
- A second tray, a login change, or a Project Manager restart.

## Layout

| Path | Role | Touch |
|------|------|-------|
| **NEW** `inc_launcher/hub_open_times.py` | Load, validate, and patch-save the two rows | New in Phase 1 |
| **NEW** `inc_launcher/hub_open_times_window.py` | Settings form, hover labels, Cancel, geometry | New in Phase 2 and 4 |
| **NEW** `inc_launcher/tests/test_hub_open_times.py` | Temp-file round trip and reject rules | New in Phase 1 |
| `inc_launcher/hub_window.py` | One queued hook that opens the Toplevel | A few lines in Phase 3 |
| `inc_launcher/tray_app.py` | One menu row, plus a hover-text constant | A few lines in Phase 3 |
| `inc_launcher/config.py` | Leave the existing on/off writers as they are | Do not edit |
| `inc_launcher/nudge_scheduler.py` | Already reloads config each poll | Do not edit |
| `inc_launcher/launcher_config.json` | Live clocks change only when the owner presses Save later | Do not edit in the build phases except through that Save |
| `inc_launcher/MANUAL_TEST.md` | One layout line only if the smoke cannot judge readability | Phase 5, only if needed |
| `.cursor/rules/task.md` | Overloaded | Do not add a pointer |

## Phases

### Phase 0 - Scope lock

- [x] **0.1** Owner confirmed (2026-10-21): Settings for the two Hub-opening clocks only, Save and Cancel, other clocks untouched, do not build in that same turn.
- **Done when:** this file is the backlog and no product code has been added for it.
- **Minutes:** 0 (already locked)

### Phase 1 - Patch writer, no window

- [x] **1.1** Read `scheduled_nudges.py` and the two ids. Do not add a third id. (10 min)
- [x] **1.2** Add `hub_open_times.py`: read the two rows, validate hour 0-23, minute 0-59, and at least one real day, patch-save time and days only. (25 min, saved 2026-10-21)
- [x] **1.3** Tests on a temp config: change one row, prove the other row and `schedules.enabled` and a non-hub item stay byte-for-purpose the same, prove hour 24 and zero days are refused and the file is not written. (20 min, 5 passed 2026-10-21)
- **Done when:** tests pass and the live `launcher_config.json` is unchanged.
- **Minutes:** 55

### Phase 2 - Settings form, not on the tray yet

- [x] **2.1** Add `hub_open_times_window.py`. Two rows, plain names, hour, minute, and day ticks. Default size on first show. (30 min, saved 2026-10-21)
- [x] **2.2** Save and Cancel. Save calls the Phase 1 writer only. Cancel does not. Save disabled when a row is invalid, with a hover label that says why. Every button gets a hover label. (15 min, tests passed 2026-10-21)
- **Done when:** a test or a direct call can show the form on a Tk root without a menu row, and Cancel does not call save.
- **Minutes:** 45

### Phase 3 - Open it from the tray, on the Hub thread

- [x] **3.1** One queue message in `hub_window.py` that opens the form as a Toplevel on the Hub root. If the Hub thread is down, start that same Hub thread first. No second `Tk()`. (15 min, saved 2026-10-21)
- [x] **3.2** Tray row whose label is the action, constant beside it for the hover text tests assert. Wire it to that queue message only. (10 min, tests passed 2026-10-21)
- **Done when:** the menu text is "Settings", the constant says it opens the Settings window for those two clocks, and no new Tk root is created. Menu label changed from "Hub open times" on 2026-10-21 after the owner could not find a Settings row.
- **Minutes:** 25

### Phase 4 - Remember where the window was

- [x] **4.1** On move or resize, after a short delay, patch-save x, y, width, and height under a settings key used only by this window. Restore on the next open. If that spot is off-screen, put the window on the visible screen. (20 min, tests passed 2026-10-21)
- **Done when:** a temp-config test saves a position and restores it, and an off-screen sample is moved back.
- **Minutes:** 20

### Phase 5 - Prove nothing else broke

- [x] **5.1** Run the existing nudge schedule tests plus `test_hub_open_times.py`. Diff check: product edits are the two new modules, the two small hooks, and tests. No edit to `config.py`, the scheduler, funding notes, or live config from the test run. (15 min, 39 passed 2026-10-21, live config hash unchanged)
- [x] **5.2** Manual layout line waived. Tests lock the row titles, Save, Cancel, and the disabled-save hover sentence. No line was added to `inc_launcher/MANUAL_TEST.md`. (10 min waived)
- **Done when:** 5.1 passes, and 5.2 is done or waived.
- **Minutes:** 25

## Follow-up Phase 6 - Remove the Ask alarm row (2026-10-25)

**Do not code until a later pick.** This section is the backlog only.

### Owner ask

Remove only the Settings row "Ask window, which also opens Hub" (`network_ask_mwf`, 11:30, Mon Tue Wed Fri Sat Sun). That row is the extra Ask window.

Keep Daily Hub open. The Hub still opens one Ask window. Start on that window stays. Not now on that window still opens the prospect window. No other Settings row is removed.

### Recommendations

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| R10 | Take the row off the form and stop `network_ask_mwf` from firing. Unticking every day is not the removal. Save already refuses a row with no day ticked. | The owner asked to remove the alarm, and the form will not store an empty day list. | 6.1, 6.2 |
| R11 | Keep Show Ask reminder, the tray Show Ask people / owners item, and the Ask card. | Those open one Ask window on purpose. They are not the 11:30 duplicate. | 6.3 |
| R12 | Keep always-show on Hub open, and keep Not now on that window opening the prospect window. | Daily Hub open is the one Ask window that stays. | 6.3, 6.4 |
| R13 | Patch-remove only the `network_ask_mwf` schedule entry. Leave the saved Daily Hub open time and days as they are. Leave every other schedule id alone. | One writer, same isolation as R3. | 6.1 |
| R14 | Tests use a temp config. Do not write the live `launcher_config.json` from tests. Do not restart Project Manager. | Same proof rule as R8. | 6.4, 6.5 |
| R15 | With one row left, Save stays refused when Daily Hub open has no day ticked. | R5 still holds for the row that remains. | 6.2 |

### Out of scope for Phase 6

- Changing the time or days the owner saved on Daily Hub open.
- Removing the Ask window that opens with the Hub.
- Changing Start, the playbook, or the copied openers.
- A second Hub program, a tray restart, or a Project Manager restart.

### Phase 6 - Remove the Ask alarm row

- [x] **6.1** Narrow the patch writer to `daily_inc_hub` only. On save, remove the `network_ask_mwf` schedule entry and no other entry. Leave `daily_inc_hub` time and days unchanged. (20 min, 2026-10-25)
- [x] **6.2** Settings form shows one row, Daily Hub open. The Ask alarm title, hour, minute, and day ticks are gone. Save, Cancel, hover labels, and the zero-day refusal stay. (20 min, 2026-10-25)
- [x] **6.3** The scheduler does not fire `network_ask_mwf`, even if an old copy of that entry is still in a file. A click on the Ask card, Show Ask reminder, or the tray Show Ask item still opens one Ask window. (15 min, 2026-10-25)
- [x] **6.4** Temp-config tests: Sunday 11:30 fires `daily_inc_hub` only. Hub open still queues one Ask window, and that window's Not now still schedules the prospect step. Other schedule ids stay. The test run does not write the live config. (25 min, 2026-10-25)
- [x] **6.5** Update the Hub-open-times tests that still expect two rows, then run those tests plus the nudge schedule tests. Done when they pass and no product file outside this row's writer, form, scheduler skip, and tests was edited. (15 min, 2026-10-25. Also updated the tray hover sentence and the isolation check that required the old alarm id.)
- **Done when:** the Settings window has Daily Hub open only, 11:30 no longer adds a second Ask window, and the one Hub Ask window still reaches the prospect window on Not now.
- **Minutes:** 95

## Minutes (this plan)

| Phase | Minutes |
|-------|--------:|
| 0 | 0 (done) |
| 1 | 55 (done) |
| 2 | 45 (done) |
| 3 | 25 (done) |
| 4 | 20 (done) |
| 5 | 25 (done) |
| 6 | 95 (done 2026-10-25) |
| **Remaining** | **0** |

## Cloud

Phases 1, 2, and 5 are tracked code and temp-file tests. They are cloud-safe. Phase 3 and a live tray glance are this PC only, because the icon and the Hub thread are on this machine. No secrets.
