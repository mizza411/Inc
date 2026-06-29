# Inc Launcher — Manual test (Phase 4 + Track C)

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task tracker:** [.cursor/rules/task.md](../.cursor/rules/task.md) §4 and §5  
**Session closed:** 2026-06-29 (Inc launcher + interval nudges + Track C bookmark menu)

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
| Bookmark queue counts | `test_cli_status.py`, `python -m business_bookmark_sorter status` |

**Automated pass recorded:** 2026-06-29 (pytest 38+ green; smoke_hub passed).  
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

## Sign-off summary

| Check | Automated | Manual (optional) |
|-------|-----------|-------------------|
| Phase 4 nudges | Yes (2026-06-29) | Schedule tune (§E) |
| Phase 2 hub / menu | Yes | — |
| Track C menu wiring | Yes | Filing workflow (§F) |
| External boot | — | §D if desired |

**Major dev for this thread:** complete. No blocking manual steps.

After any config change: stage, commit, and push (respect `.gitignore`).
