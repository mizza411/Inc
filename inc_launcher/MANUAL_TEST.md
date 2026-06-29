# Inc Launcher — Manual test (Phase 4 sign-off)

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)

Most Phase 4 checks are **automated**. Run the agent/CI suite below — **you do not need to run manual steps unless noted**.

---

## Automated sign-off (run these — no manual UI)

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests -q
python -m inc_launcher.tests.smoke_hub
```

Run **both** commands. Pytest covers A/B/C/E logic; `smoke_hub` (~7s) covers Hub window + paths separately (not inside pytest — avoids tkinter subprocess hang on Windows).

| MANUAL_TEST section | Automated by | What it proves |
|---------------------|--------------|----------------|
| **A** — Interval nudges toggle | `test_phase4_signoff.py::test_manual_a_*`, `test_phase4_toggle.py` | Config ON/OFF, menu refresh hook, JSON persistence |
| **B** — Nudge fires once | `test_phase4_signoff.py::test_manual_b_*`, `test_nudge_scheduler.py` | 09:00 task, 09:15 hub, M/W/F URL, Sun YouTube; no double-fire |
| **C** — OFF stops nudges | `test_phase4_signoff.py::test_manual_c_*` | Disabled schedule fires nothing |
| **E** — Quit / relaunch scheduler | `test_phase4_signoff.py::test_manual_e_*` | Scheduler thread start/stop |
| **Phase 2 hub** | `python -m inc_launcher.tests.smoke_hub` | Hub opens/closes; config paths; menu build |
| Schedule parsing | `test_scheduled_nudges.py` | Times, days, targets, skip rules |
| Regression | Full `inc_launcher/tests` | No module regressions |
| **Track C** — Bookmark review | `test_track_c_bookmark.py`, `test_config.py::test_formulated_has_bookmark_review` | Tray menu item + `review` CLI registered |
| **Bookmark queue status** | `business_bookmark_sorter/tests/test_cli_status.py` | `status` command + pending counts |

**Bookmark backlog check (automated):**

```powershell
cd C:\dev\Inc
python -m business_bookmark_sorter status
python -m pytest business_bookmark_sorter/tests/test_cli_status.py -q
```

**Expected:** all pytest tests pass; `smoke_hub` prints `=== SMOKE TEST PASSED ===`.

---

## Manual only (cannot automate)

### D. Coexistence with external auto-launcher

**Why not automated:** External `auto_launcher.py` lives in **another repo**; Windows login/reboot flow is user-specific and outside this codebase.

- [ ] Reboot or log off/on (or run external `auto_launcher.py` if that is your boot path)
- [ ] Confirm **one** Inc tray icon appears
- [ ] Confirm **Interval nudges** state matches `launcher_config.json` after boot
- [ ] Inc **Start at Windows login [OFF]** if external launcher already starts the tray

**Expected:** Single tray; scheduler runs inside it; no duplicate icons.

**Skip if:** You already verified external launcher + single tray in daily use and do not need formal sign-off for D.

---

## Sign-off (automated path)

If pytest + smoke_hub are green, treat **A, B, C, E, Phase 2 hub** as **passed via automation**.

| Check | Automated | Manual |
|-------|-----------|--------|
| A — Toggle ON/OFF | Yes | — |
| B — Nudge fires once | Yes | — |
| C — OFF stops nudges | Yes | — |
| D — External boot OK | — | Only if you require boot verification |
| E — Quit / relaunch | Yes (scheduler lifecycle) | Live tray Quit click optional |
| Phase 2 hub | Yes | — |

Date automated pass: __________  
Optional manual D pass: __________

After sign-off: stage, commit, and push Inc launcher changes (respect `.gitignore`).
