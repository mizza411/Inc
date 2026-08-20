# Business Bookmark Sorter — Manual test

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task tracker:** [.cursor/rules/task.md](../.cursor/rules/task.md) §5 (+ launcher Operational / Track C in §4)  
**Privacy (locked 2026-07-20):** Do **not** bulk-export Chrome bookmarks into chat/AI. Sorter reads the **local** Chrome `Bookmarks` JSON on this PC only.

**When to run:** Short sessions when you choose to file — **not** mid-build for agent. One focused pass for Phase 2b/2c/2d sign-off (§§D–G); §§A–C whenever you reduce the ~2k queue.  
**BB-TIMED-1 v1 (2026-08-20):** Phases 1–7 code **shipped**. Agent automated sign-off: `pytest business_bookmark_sorter/tests/test_bb_timed_v1_signoff.py` (covers former §§I–L logic + M/N **config**). Live Windows login / tray clock feel remains manual-only below (§P) — **owner not required mid-build**.

**Sidebar chat (“Business content sorting…”):** Deleting that Cursor history is OK — **your** remaining work is §§A–F below (and Phase 3 when built). Do not rely on the old chat for what to file next. Tracker: `task.md` §5 + top **Sidebar chat batch assess** (2026-07-20) row 8.  
**Also (“Business bookmarks organizat…” — 2026-07-24):** Same §5 / §§A–F — safe to delete; see **Sidebar chat batch assess (image — 2026-07-24)** row 8.

---

## Automated first (agent runs — no browser/UI for you)

```powershell
cd C:\dev\Inc
python -m pytest business_bookmark_sorter/tests -q
python -m business_bookmark_sorter status
```

| Area | Automated by |
|------|----------------|
| Import / queue / export / file workflow | `tests/test_*.py` under this folder |
| Removal dialog Yes/No / stay-on-item | `tests/test_review_removal.py` |
| CLI status + no `discover` | `test_cli_status.py`, `test_cli_no_discover.py`, `status` command |
| Session settings store + dialog helpers | `test_session_settings.py`, `test_session_settings_ui.py` |
| Session timer (fake clock) | `test_session_timer.py` |
| Auto-open current link | `test_auto_open.py` |
| Minimal confirm / removal skip | `test_phase4_minimal_confirm.py`, `test_review_removal.py` |
| PR boot config (Inc review) | `test_pr_boot_config.py` |
| **BB-TIMED-1 v1 sign-off (I–L + M/N config)** | `test_bb_timed_v1_signoff.py` |
| Word same-name docx regenerate | `test_docx_same_name_fix.py` |
| Prospect route | `test_prospect_route.py` |
| Tray → Bookmark review menu | `inc_launcher` Track C tests (see `inc_launcher/MANUAL_TEST.md`) |

```powershell
# Kill old review windows, then agent sign-off suite:
python business_bookmark_sorter\scripts\kill_review_instances.py
python -m pytest business_bookmark_sorter/tests/test_bb_timed_v1_signoff.py business_bookmark_sorter/tests -q
```

Agent should run the above before asking you for any section below.

---

## Manual only (cannot automate safely)

### A. Chrome hygiene before large re-import

**Why not automated:** Only you know which bookmarks are personal/sensitive vs business. Wrong move would expose private URLs.

- [ ] In Chrome bookmarks, open folders whose names contain **business**
- [ ] Move **personal / finance / health / login-adjacent** links **out** of those folders (e.g. into `Personal` / non-business trees)
- [ ] Keep only business-related links under `*business*` folders
- [ ] Local only: open `python -m business_bookmark_sorter review` (or tray Bookmark review) and confirm the first pending item looks like a business link — **do not** paste titles/URLs into chat

**Pass:** Business folders no longer mix private links; the first review item looks like a business link to you.

---

### B. Keyword rules (optional, config)

**Why not automated:** Choosing which keywords match *your* queue needs your judgment. Unit tests cover `suggest.py` mechanics, not your vocabulary.

- [ ] Note a few **non-sensitive** title/URL patterns you see often (you may paste *sanitized examples only* into a future chat)
- [ ] Optionally edit `config/routes.json` → `keyword_rules` (or ask agent to edit from your sanitized list)
- [ ] Open review UI; confirm suggestions match intent more often for those patterns; no-match → **Other**

**Pass:** Obvious links suggest the right pillar more often; misses still land on **Other**.

---

### C. Batch-by-subfolder filing habit

**Why not automated:** Session strategy / which Chrome subfolder to clear is human prioritization.

- [ ] Pick **one** business subfolder for a 15–20 min session
- [ ] Tray → **Formulated ideas → Bookmark review** (or `python -m business_bookmark_sorter review`)
- [ ] File that batch mostly to **one** destination (or Stay in Chrome / Skip)
- [ ] Stop when time’s up; check `status` — pending should drop

**Pass:** You finished a batch without re-deciding pillar on every single link.

---

### D. Phase 2b/2c/2d — File & open doc + removal dialog (sign-off)

**Why not automated:** Needs live Chrome delete + Word/docx open + eyeball that the line landed in the right section + human Yes/No on the dialog.

- [ ] Start review UI with at least one **pending** item
- [ ] Pick destination (or accept **Other**) → **File & open doc**
- [ ] Confirm success toast; **same** `Business Links.docx` opens (not a different per-folder docx)
- [ ] Confirm new line under the right `##` section (e.g. My leads / Other)
- [ ] Delete that bookmark in Chrome
- [ ] Answer **Yes** in “Have you removed…?” **or** answer **No** then click **Bookmark removed — next**
- [ ] Confirm queue advanced; link still present in doc / `queue.json` as `filed`

**Pass:** One full file → eyeball → Chrome delete → next item, with no lost link.

---

### E. Stay in Chrome

**Why not automated:** Needs confirmation bookmark still exists in Chrome UI after action.

- [ ] On a pending item, choose **Stay in Chrome**
- [ ] Confirm item leaves pending / marked stay; bookmark still in Chrome unchanged
- [ ] Confirm nothing new written under that URL in master doc for this action

**Pass:** Bookmark untouched in Chrome; sorter marked stay.

---

### F. Skip vs Stay (mental check)

**Why not automated:** Subjective “decide later” vs “not for Inc” — you must feel the difference.

- [ ] Hover **Skip** and **Stay in Chrome** — tooltips match: Skip = later / may return; Stay = done here, keep in Chrome only
- [ ] Optionally Skip one item and Stay another; confirm both leave pending without writing to Business Links

**Pass:** You would not confuse Skip with Stay under time pressure.

---

### G. Tooltips (all buttons)

**Why not automated:** Subjective readability of hover copy.

- [ ] Hover: Open URL, Refresh now, File & open doc, Skip, Stay in Chrome, Quit, **Filing as** (read-only; no Assign dropdown)
- [ ] Confirm each shows a short tip (File tip mentions Shift+click re-export)

**Pass:** No blank hover; wording is clear enough without opening chat.

---

### I–O. BB-TIMED-1 timed/minimal UI — **automated** (2026-08-20)

**Moved to automation:** `tests/test_bb_timed_v1_signoff.py` (+ existing timer/settings/auto-open/removal/schedule/PR config tests).

| Former manual | Automated proof |
|---------------|-----------------|
| §I Settings persist | save/load round-trip; no URL fields in JSON |
| §J Timer stop-nagging | fake clock expiry → `_session_allows_advance` False; Extend clears flag |
| §K Auto-open | one URL per id; OFF = no open; `_display_item` calls opener |
| §L Enter + don’t-ask | Enter files when focus free; skip dialog when session flag set |
| §M 11:00 schedule | config resolves `bookmark_review`; due on weekday 11:00 |
| §N PR boot key | `applications.inc_business_bookmark_review` enabled + Inc cwd |

**Agent recorded:** 2026-08-20 — `test_bb_timed_v1_signoff.py` **13 passed**; Word same-name fix `test_docx_same_name_fix.py` **5 passed**; sorter regression green.

---

### P. Live boot / tray clock only (cannot fully automate)

**Why not automated:** Needs real Windows login + Inc tray resident + wall-clock (or owner-approved temp schedule tweak). Config shape is already pytest-covered (§M/N above).

**ASCII — what you are checking (later, when you choose):**

```
PASS — boot
  login / auto_launcher
       |
       +--(~8s)--> window title "Business links bookmark Reviewer" appears
       +---------> PR old bookmark_sorter may also open (OK — different app)
       X  FAIL if Inc review never opens and key is still enabled

PASS — weekday clock (Interval nudges ON, Inc tray running)
  Mon–Fri 11:00
       |
       +----------> Bookmark review command runs (same GUI)
       X  FAIL if 11:00 passes with nudges ON and nothing opens
           (first check: schedule_fired.json / tray still alive)

SKIP for now if you are not doing manual work this session.
```

- [ ] (Deferred) Next login: Inc Business links bookmark Reviewer opens from PR boot key
- [ ] (Deferred) Weekday 11:00 with Interval nudges ON opens review

**Pass:** Live surfaces match config tests. **Fail:** enabled config but no window after login/11:00 with tray healthy.

---

### Q. Reviewer app tray (BB-LINKS-UX-1 Phase 3) — live feel only

**Why not automated:** Needs eyes on the Windows notification area. Menu labels + single-instance focus flag are pytest-covered.

```
PASS — app tray
  review running
       |
       +--> teal tray icon near clock
       +--> right-click: Open / focus review | Quit
       +--> second `python -m business_bookmark_sorter review` focuses same window
       X  FAIL if two windows or no tray icon while review is open
```

- [ ] (Deferred) Confirm Open / focus and Quit on the Reviewer tray icon
- [ ] (Deferred) Confirm Formulated ideas → Bookmark review still opens review

---

### H. Import count sanity (after hygiene)

**Why not automated:** “Expected” count is your judgment vs Chrome folder tree.

- [ ] After §A: `python -m business_bookmark_sorter import` (local)
- [ ] `status` pending/total roughly matches business-folder reality
- [ ] Update the pending count note in `task.md` §5 if it changed a lot

**Pass:** Counts make sense; no surprise personal domains dominating the queue.

---

## Out of scope for this file

- Phase 3 auto de-bookmark (not built) — when shipped, add a section; backup/restore required
- Option D/E/F code features — add tests when approved in `task.md` §5 Phase 5
- Pasting full Chrome exports into chat — **never**

---

## Pass / fail notes

| Date | Sections run | Result | Notes |
|------|--------------|--------|-------|
| 2026-08-20 | BB-TIMED I–L + M/N config | **PASS (automated)** | `test_bb_timed_v1_signoff.py` 13/13; suite 72; review restarted pid check |
| | §P live boot/11:00 | deferred | owner not doing manual this session |

**v1 filing sign-off:** §§D–G once; §§A–C as ongoing ops until pending is manageable.  
**BB-TIMED-1 v1:** automated sign-off suite green; live §P deferred until you want it.
