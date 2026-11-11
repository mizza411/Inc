# BB-MOVE-PR-1 follow-up — Inc cleanup after Project Reminder ship

**Status:** ⏳ Remaining only (Inc drift). PR package **shipped**.  
**Attempt:** 1  
**Authoritative backlog:** **this file** (main `task.md` overloaded — do not add a pointer there).  
**Delete when:** Phases A-C below are green and Inc no longer runs the old package as the live reviewer. **Hold (11/11/2026):** BB-KEYWORD-DOOR-1 keeps that Inc package for the business choice, so do not treat Phase B as the next step.

**Context (chat closed OK after this file exists):**  
The move/generic-keywords work lived in a satellite that was deleted after Phase 6. Project Reminder `bookmark_sorter/` is on `origin/master` (`34b5e40`). Inc later **regained** full `business_bookmark_sorter/` code (**48** `.py` files) and the tray menu again runs `python -m business_bookmark_sorter review`. Starter `inc_launcher/launch_bookmark_review.py` still exists but is unused by the menu.

---

## Goals already accomplished (do not redo)

| Goal | Done? | Where |
|------|-------|--------|
| Move reviewer to `C:\dev\project_reminder\bookmark_sorter\` | ✅ | PR package committed + pushed |
| Keep all review functions (timer, auto-open, file/docx, tray, mutex) | ✅ | Same package |
| Generic saved Chrome keywords (default `business`, Settings UI) | ✅ | `keyword_filter.py` + Settings |
| Boot via Project Reminder `launcher_config.json` | ✅ local | `inc_business_bookmark_review` → `-m bookmark_sorter review` (file is **gitignored**) |
| Leave old PR `bookmark_sorter.py` categorizer alone | ✅ | Untouched |
| One-time queue copy / no wipe on keyword narrow | ✅ | `migrate_local_state.py` + refresh presence rule |
| Satellite task file for the move | ✅ deleted after Phase 6 | Was `task_bookmark_sorter_move.md` |

---

## Remaining (Inc only)

### Phase A — Point Inc clocks at Project Reminder again (~15 min)

- [ ] **A.1** Set Formulated ideas → Bookmark review to `python inc_launcher/launch_bookmark_review.py` (`cwd` `.`). Keep weekday 11:00 target `bookmark_review`.
- [ ] **A.2** Update Inc tests that still assert `business_bookmark_sorter review` for that menu (`inc_launcher` + any Inc-side sorter tests still used).
- [ ] **A.3** Confirm mutex name unchanged; starter still launches `python -m bookmark_sorter review` with cwd `C:\dev\project_reminder`.

### Phase B — Remove restored Inc code copy (~20 min)

**Hold (11/11/2026):** BB-KEYWORD-DOOR-1 keeps the Inc reviewer, `Business Links.md`, `Business Links.docx`, the Inc queue, and the Inc destination folders when the choice is business. Do not delete that app while this lock stands. Phase A and Phase C stay listed. They are not part of BB-KEYWORD-DOOR-1.

- [ ] **B.1** Delete Inc `business_bookmark_sorter` **code** (modules, tests, config, scripts). Keep `Business Links.md`, `Business Links.docx`, `data\` backup.
- [ ] **B.2** Confirm `python -m business_bookmark_sorter` no longer provides the app; `python -m bookmark_sorter status` from Project Reminder still reports the queue.
- [ ] **B.3** Strategy-1 Docx sign-off still imports `bookmark_sorter.docx_export` with Project Reminder on `sys.path`.

### Phase C — Scoped Inc commit (~10 min) optional push

- [ ] **C.1** Stage only bookmark-wiring files (starter, launcher menu, related tests, analogy note if touched). Respect gitignore (no queue, no Business Links body if ignored).
- [ ] **C.2** Commit; push only if owner asks.

**Estimated remaining agent time:** ~**45 minutes** (A+B+C).

---

## Hard isolation

- Do not edit Project Reminder `bookmark_sorter.py` or `auto_launcher.py`.
- Do not force-add ignored queue/settings/actions or PR `launcher_config.json`.
- Do not dump unrelated Inc dirty tree into the commit.

---

## Done definition

Inc tray/11:00 open Project Reminder reviewer; Inc folder has docs+data only; optional Inc commit landed.

That end state is on hold for the business choice. BB-KEYWORD-DOOR-1 (below) is the later owner lock.

---

## BB-KEYWORD-DOOR-1 - Keyword front door, business stays on the Inc view

**Status:** ⏳ Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, Phase 5, Phase 6, Phase 7, Phase 8, Phase 10, Phase 11, Phase 12, and Phase 13 done 11/11/2026. Phase 9 and Phase 14 are not started.  
**Attempt:** 1  
**Where this lives:** this file. The main task list is overloaded, so this entry is not copied there.  
**Owner lock (menu 3, 11/11/2026):** Choosing business keeps the business list and the Inc files. Any other keyword gets its own list and does not write the Inc business files.  
**Owner lock (11:53, 11/11/2026):** Choose a keyword is the main window. Choosing business correctly opened the Bookmark Reviewer page with Keyword: business and List: Business Links. That page is the business page. From that page there is no way back to Choose a keyword. Going from Choose a keyword to a keyword page must keep that page's info.

### What the owner asked

1. Auto-launch should show the window where a keyword is chosen.
2. Choosing business keeps the business list and the Inc files behind it.
3. That list keeps its document and its filing setup in the Inc repo.
4. The keyword page needs a way back to Choose a keyword. Quit is not that way.
5. Going from Choose a keyword to a keyword page keeps that page's info (timer, current link, and counts). Each keyword keeps its own page.
6. A keyword that is not business opens that keyword's own page. It must not open the business bookmark page. (Seen 11/11/2026: a new keyword still opened the business page.)
7. A word typed on Choose a keyword can be saved from that main page, and it stays in Saved keywords.
8. When the tray icon is up, the window is Choose a keyword. The business page stays closed until Continue with business. (Seen 11/11/2026: starting the tray opened the business page.)
9. The tray menu has Restart above Quit. Restart shuts this icon down, then starts one new icon on Choose a keyword. It does not open the business page by itself. (Menu screenshot 11/11/2026.)
10. Closing the window hides it and shows the same minimize-to-tray banner the other trays use. The icon stays. Quit is the action that ends the app.
11. The small Bookmark Reviewer window is not that banner. Use the Windows toast the other trays already use. Also make that a global rule for every project. (Seen 11/11/2026: the small window appeared, and the owner rejected it.)

### Where those files are

| Piece | Place |
|-------|--------|
| Business page the owner accepted (11/11/2026) | Project Reminder Bookmark Reviewer, Keyword: business, List: Business Links |
| Document | `C:\dev\Inc\business_bookmark_sorter\Business Links.md` and `Business Links.docx` |
| Queue and routes | `C:\dev\Inc\business_bookmark_sorter\data` and `config\routes.json` |
| Destination folders | Other folders in `C:\dev\Inc` (Prospect-Businesses, Started-Businesses, and the rest named in routes) |
| Keyword picker today | `C:\dev\project_reminder\bookmark_sorter` (second program). It already points the business list at the Inc document. |

### Recommendations (do these with the phases, do not fold them into one edit)

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| R1 | One cold start shows Choose a keyword. Close opens no review. | The picker is skipped today when a reviewer is already open. | 1 |
| R2 | Choosing business shows the Bookmark Reviewer page the owner accepted (Keyword: business, List: Business Links). Do not replace that page with the older Inc window. | The owner said that page was the right one. | 2 |
| R3 | Do not move, copy, or delete Business Links, the Inc queue, or the Inc destination folders. | The document and the filing setup stay in Inc. | 2 |
| R4 | Any other keyword uses its own list and must not append to Business Links or an Inc destination folder. | A new keyword must not damage the business files. | 3 |
| R5 | Auto-launch opens the picker even if the Inc review is already open. After Continue with business, bring that Inc window forward. | That is the screenshot case. | 4 |
| R6 | Leave Formulated ideas, Bookmark review, as a direct open of the Inc view. | The current Inc habit stays. Auto-launch is the path that gains the picker. | 4 |
| R7 | Do not edit `auto_launcher.py`. Do not restart Project Manager. Prove with one app. | Other launched apps stay as they are. | 4, 5 |
| R8 | Leave the Chrome bookmarks path warning (Errno 2 on the screenshot) out of this parent. | A path fix is a different change and can break sync if mixed in. | 5 |
| R9 | Pause Phase B above. Deleting the Inc app would remove the business files this lock keeps. | The older cleanup and this lock disagree. This lock wins until the owner says otherwise. | hold |
| R10 | Put Back on the keyword page. Hover label: Return to Choose a keyword. Quit still exits the app. | The owner could not get back to the main window. | 6 |
| R11 | Back hides the keyword page. It does not destroy it, and it does not start a new session. | A new session would wipe the timer, the link, and the counts. | 6, 7 |
| R12 | Choosing the same keyword again shows that same page. Choosing another keyword shows that keyword's own page. | Each keyword keeps its own info. | 7 |
| R13 | Do not reset session time, the current link, or the counts on Back or on return. | That is the info the owner asked to keep. | 7 |
| R14 | The Chrome bookmarks path warning (Errno 2) stays out of Phase 6 and Phase 7. | A path fix is a different change. | 5 |
| R15 | Continue on a keyword other than business shows that keyword's page, with its own name and its own list. | The owner still landed on the business page. | 8 |
| R16 | Opening that page does not change the business page. Back, then business, shows the business page as it was left. | The business page stays the business page. | 8 |
| R17 | Save sits on Choose a keyword. Hover label: Save this keyword for later. Save adds the typed word to Saved keywords and does not open a page. | The main page says a typed word is for this open only. The owner wants to keep it. | 9 |
| R18 | A word under 3 letters is refused. The next open of Choose a keyword still shows the saved word. Save does not write Business Links. | Same length rule as the rest of the picker, and the Inc file stays untouched. | 9 |
| R19 | The tray icon is up while Choose a keyword is the open window. The business page stays closed until Continue. | Starting the tray had opened the business page. | 10 |
| R20 | Menu order is Open / focus window, Restart, Quit. Restart shuts this icon down first, then starts one replacement. A second normal start does not add another icon. Do not restart Project Manager. Do not edit auto_launcher.py. | The menu screenshot had no Restart. Two icons, or a restart that leaves the old one up, is the failure. | 11 |
| R21 | The replacement opens Choose a keyword. Restart does not open the business page by itself. Release the gate lock, the tray lock, and the review lock before the new process starts. | If those locks stay held, the new process thinks the old window is still open. | 11 |
| R22 | The window X and the Close button hide the window. The process and the icon stay. The banner is the same Windows toast the other trays use, from the shared helper. Title: Bookmark Reviewer. Body: Minimized to system tray. Right-click the tray icon to restore. | The other trays hide and show that toast. A separate small window is not the normal banner. | 12, 13 |
| R23 | Open / focus window brings the same window back. A hidden keyword page keeps its timer, link, and counts. Hiding does not open the business page and does not start a new session. The single-instance lock stays held while the window is hidden. | A new session would wipe the page. Dropping the lock would allow a second window. | 12 |
| R24 | Quit still ends the app and does not show the banner. Phase 9 Save, filing, and the Inc reviewer stay out of Phase 11 and Phase 12. The menu words are the label for Restart and Quit. | Quit is the only end. Mixing in Save or the Inc app would change work that is still waiting or on hold. | 12 |
| R25 | Drop the forced popup. Call the shared helper the same way the other trays do, toast first. The small window stays only that helper's own fallback when the toast fails. Do not bring the small window back to hide a quiet toast. | The owner saw the small window and rejected it. The first toast try drew nothing, and a forced window was the wrong fix. | 13 |
| R26 | Do not edit the other trays in Phase 13. They already call the shared helper. Change only Bookmark Reviewer, then prove that one app. Do not restart Project Manager. | A sweep of every tray would mix this fix with apps that already match. | 13 |
| R27 | The global rule says a tray close uses that shared toast. Do not add a separate banner window as the normal close. Re-check automatic User-rule creation first. If that fails, use the local plugin and the spare copy. Do not call a project rule global. | The owner asked for one rule for all projects. Two copies would apply it twice. | 14 |

### Phases

Each phase can land on its own. Do not start Phase 1 until it is picked.

#### Phase 0 - Lock only (~10 min) ✅ 11/11/2026

- [x] **0.1** Record the split, the owner lock, and the hold on Phase B. No product code.

Done when: this section exists and the Inc reviewer is unchanged.

#### Phase 1 - Picker on a cold start (~40 min) ✅ 11/11/2026

- [x] **1a** The launch used for this door opens Choose a keyword first. Close opens no review. (~20 min)
- [x] **1b** A second start while that picker is open does not skip straight into a review. (~20 min)

Done when: a cold start shows the picker. Starting the Inc reviewer the old way still shows Business links Bookmark Reviewer.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py bookmark_sorter/tests/test_bb_links_ux_phase3.py::test_run_review_panel_second_launch_requests_focus -q` from `C:\dev\project_reminder`. The Inc package was not edited. The Inc menu still runs `python -m business_bookmark_sorter review`.

#### Phase 2 - business keeps the accepted page and the Inc files (~50 min) ✅ 11/11/2026

Revised 11/11/2026 after the owner accepted the Bookmark Reviewer page (Keyword: business, List: Business Links). Do not open a different window in its place.

- [x] **2a** Choosing business shows that accepted page. (~25 min)
- [x] **2b** Filing still uses `Business Links.md`, `Business Links.docx`, and the Inc destination folders. No move and no second copy of the document. (~25 min)

Done when: choosing business shows that page, and a filed link still lands in Inc.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py::test_business_choice_keeps_the_inc_files -q` from `C:\dev\project_reminder`. The business page keeps the accepted title and the Business Links line. Its list path is `C:\dev\Inc\business_bookmark_sorter\Business Links.md`, and the Word file is the `.docx` beside it. Destination folders stay under `C:\dev\Inc`. No second list is created under `bookmark_sorter\data\keyword_homes\business`. The test does not write a link into the live Inc files.

#### Phase 3 - Other keywords stay off the Inc files (~40 min) ✅ 11/11/2026

- [x] **3a** A keyword other than business uses its own list. (~20 min)
- [x] **3b** A smoke shows that list is not `Business Links.md` and not an Inc destination folder. (~20 min)

Done when: a non-business keyword cannot append to the business document.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_home.py::test_phase3_other_keyword_stays_off_the_inc_files -q` from `C:\dev\project_reminder`. A health list is `bookmark_sorter\data\keyword_homes\health\Links.md`. That path is not `Business Links.md` and not under `C:\dev\Inc`. Filing a health link writes `Links.md` and `Links.docx` beside it. The Business Links text is unchanged. The test uses a temporary list, so it does not create the live health folder and does not write the live Inc files.

#### Phase 4 - Auto-launch uses the front door (~45 min) ✅ 11/11/2026

- [x] **4a** The Project Manager bookmark row opens the picker, not straight into whichever review is already up. (~25 min)
- [x] **4b** If a review is already open, a cold auto-launch still shows Choose a keyword. Continue with business then shows the accepted business page, and keeps that page's info if it was already open. (~20 min)

Done when: the case in the screenshot no longer hides the picker. Formulated ideas, Bookmark review, still opens the Inc view directly. No Project Manager restart.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py::test_phase4_autolaunch_uses_the_front_door -q` from `C:\dev\project_reminder`. The Project Manager row runs `pythonw -m bookmark_sorter review`, and that command calls the picker before any review page. If a review is already open, the launch focuses that page and does not build a second one. The Inc menu command stays `python -m business_bookmark_sorter review`, and that Inc review has no Choose a keyword. Project Manager was not restarted. `launcher_config.json` was not edited.

#### Phase 5 - Proof the rest still works (~35 min) ✅ 11/11/2026

- [x] **5a** Inc title and banner still match the current business view. (~10 min)
- [x] **5b** Existing keyword-home and export checks still pass. (~15 min)
- [x] **5c** Record that the Chrome bookmarks path warning stays out of this parent. No code for that warning here. (~10 min)

Done when: the checks pass and the Inc business files are still in place.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_home.py bookmark_sorter/tests/test_export.py bookmark_sorter/tests/test_file_workflow.py bookmark_sorter/tests/test_preserve_links.py bookmark_sorter/tests/test_bb_links_ux_phase4.py bookmark_sorter/tests/test_keyword_gate.py::test_business_choice_keeps_the_inc_files -q` from `C:\dev\project_reminder`, 29 passed. The business page still uses Bookmark Reviewer and Business Links. Keyword lists and export checks passed. `C:\dev\Inc\business_bookmark_sorter\Business Links.md` and `Business Links.docx` are still there. No link was written into them. The Chrome bookmarks path warning (Errno 2) stays out of this parent. No code was added for that warning.

#### Phase 6 - Back to Choose a keyword (~40 min) ✅ 11/11/2026

- [x] **6a** The keyword page has Back. It returns to Choose a keyword. Quit still exits the app. Hover label: Return to Choose a keyword. (~20 min)
- [x] **6b** Back does not discard the keyword page and does not start a new session. (~20 min)

Done when: from the business page, Back shows Choose a keyword, and the business page is still there to return to.

Close on Choose a keyword, when a page is already open, returns to that page. Close when no page is open still exits. Phase 12 changes that close: the window hides, the icon stays, and a banner shows. Quit still exits. Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py -q` from `C:\dev\project_reminder`. The Inc reviewer was not edited. Owner confirmed 11/11/2026: Back returned to Choose a keyword, and the same keyword page was still there.

#### Phase 7 - Keyword page info persists (~45 min) ✅ 11/11/2026

Added 11/11/2026.

- [x] **7a** Choose the same keyword again and the page still shows the same time left, the same link, and the same counts. (~25 min)
- [x] **7b** Each keyword keeps its own page. Opening one does not reset another. (~20 min)

Done when: business, then Back, then business again, shows the same page. A second keyword has its own page and does not clear business.

The owner saw a new keyword still open the business page. That screen is Phase 8. Phase 7 stays the timer, link, and counts.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py::test_phase7_keyword_page_keeps_its_info -q` from `C:\dev\project_reminder`. Back, then business again, keeps the same timer, the same link, and the same counts. Opening health uses a different timer and does not clear the business link or counts. Returning to business shows that same page. The test does not write the live Inc files.

#### Phase 8 - A new keyword gets its own page (~50 min) ✅ 11/11/2026

- [x] **8a** Continue with a keyword other than business opens that keyword's page, not the business bookmark page. The page shows that keyword and its own list. (~25 min)
- [x] **8b** The business page is unchanged. Back, then business, shows the business page as it was left. (~25 min)

Done when: health (or any new word) has its own page, and business is still the business page.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py -q` from `C:\dev\project_reminder`, 16 passed. The Inc reviewer was not edited. The health page heading is the word health and List: health. The business page heading stays Bookmark Reviewer, and its list stays Business Links. A link shows on the new page only when the word is in that link's title, address, or Chrome folder. If none match, the page says there are no pending links for that keyword.

#### Phase 9 - Save a typed keyword from the main page (~35 min)

Added 11/11/2026. Not started.

- [ ] **9a** Choose a keyword has Save. Hover label: Save this keyword for later. Save adds the typed word to Saved keywords and does not open a page. (~20 min)
- [ ] **9b** The word is still in Saved keywords the next time the main page opens. A word under 3 letters is refused. Save does not write Business Links. (~15 min)

Done when: type a word, Save, leave, and come back, and the word is in the list. Continue is still what opens the page.

#### Phase 10 - Tray icon with Choose a keyword (~25 min) ✅ 11/11/2026

Added 11/11/2026 from owner pick 5. The tray had been started on the business page.

- [x] **10a** The tray icon is up while Choose a keyword is the open window. The menu action is Open / focus window. (~15 min)
- [x] **10b** The business page stays closed until Continue. Close on the main window removes the icon and does not open the business page. (~10 min)

Phase 12 replaces the close part of 10b. The launch part stays: the icon is up with Choose a keyword, and the business page stays closed until Continue.

Done when: a launch shows Choose a keyword and the teal Bookmark Reviewer icon. The business page is not open yet.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py bookmark_sorter/tests/test_bb_links_ux_phase3.py -q -k "not test_inc_launcher"` from `C:\dev\project_reminder`, 23 passed, 1 deselected. The deselected test is the older Inc launcher check and was not changed. The Inc reviewer was not edited. Close records tray, then the chooser, then tray stop, and no review page. A second start while the chooser is open does not start another icon.

#### Phase 11 - Restart on the tray menu (~30 min) ✅ 11/11/2026

Added 11/11/2026 from the tray menu screenshot.

- [x] **11a** The menu is Open / focus window, Restart, then Quit. (~10 min)
- [x] **11b** Restart shuts this icon down first, then starts one replacement. The new window is Choose a keyword. The business page stays closed until Continue. A second normal start does not add another icon. (~20 min)

Done when: Restart is on the menu, one icon comes back, and Choose a keyword is the window.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py bookmark_sorter/tests/test_bb_links_ux_phase3.py -q -k "not test_inc_launcher"` from `C:\dev\project_reminder`, 24 passed, 1 deselected. Restart calls the shared handoff with exit before the new process starts. The replacement script is `bookmark_review_tray_launcher.py`, and that file opens Choose a keyword. No second-copy flag. The Inc reviewer was not edited. Project Manager was not restarted. Owner confirmed 11/11/2026: Restart is on the tray menu.

#### Phase 12 - Close hides to the tray (~40 min) ✅ 11/11/2026

Added 11/11/2026. Do not fold it into Phase 9 or Phase 10.

- [x] **12a** The window X and the Close button hide the window. The process and the icon stay. (~15 min)
- [x] **12b** One banner uses the shared tray close helper. Title: Bookmark Reviewer. Body: Minimized to system tray. Right-click the tray icon to restore. (~15 min)
- [x] **12c** Open / focus window brings the same window back. Quit still ends the app and does not show the banner. (~10 min)

Done when: closing the window shows the banner and the icon is still there. Quit is the only menu item that ends the app.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py bookmark_sorter/tests/test_bb_links_ux_phase3.py bookmark_sorter/tests/test_review_not_top.py -q -k "not test_inc_launcher"` from `C:\dev\project_reminder`, 30 passed, 1 deselected. Close on Choose a keyword withdraws the window and asks for the shared banner. Tray Quit destroys the window and does not ask for the banner. The keyword page hide path is separate from Quit. The Inc reviewer was not edited. Project Manager was not restarted. Owner check 11/11/2026: the icon stayed, and the toast did not appear. A later close showed the small window. The owner rejected that window. Phase 13 replaces the forced popup. The hide, the icon, and Quit stay as they are.

#### Phase 13 - Close banner matches the other trays (~20 min) ✅ 11/11/2026

Added 11/11/2026. Do not fold this into Phase 12's hide behavior.

- [x] **13a** Bookmark Reviewer calls the shared tray-close helper the same way the other trays do. Toast first. Title: Bookmark Reviewer. Body: Minimized to system tray. Right-click the tray icon to restore. (~10 min)
- [x] **13b** The small window is not forced. It remains only the helper's fallback when the toast fails. Hide, the icon, and Quit stay as they are. (~10 min)

Done when: close still hides the window, the icon stays, and the banner path is the shared toast, not the small window.

Proof: `python -m pytest bookmark_sorter/tests/test_keyword_gate.py bookmark_sorter/tests/test_bb_links_ux_phase3.py bookmark_sorter/tests/test_review_not_top.py -q -k "not test_inc_launcher"` from `C:\dev\project_reminder`, 30 passed, 1 deselected. The close call uses mode auto and the shared sentence. The small window is not forced. The other trays were not edited. Project Manager was not restarted. Owner check 11/11/2026: the icon stayed, and the balloon did not appear as a pop-up. It reached the notification panel, and other apps (Cursor, Auto Scroll) were hidden the same way. The cause was Windows Explorer, not this app. The owner restarted Windows Explorer from Task Manager and the pop-up now shows. The close uses only the shared balloon helper. The extra corner toast is removed. The small window stays off. No app change was needed for the pop-up.

#### Phase 14 - Global rule for the tray close banner (~25 min)

Added 11/11/2026. Not started. This is a rule for all projects. It is not a project rule.

- [ ] **14a** Re-check automatic User-rule creation in that turn. If it works, write the rule only there. (~10 min)
- [ ] **14b** If automatic creation does not work, write the plugin rule and the spare copy, then give the push line and wait. The rule says a tray close uses the shared toast, and a separate banner window is not the normal close. (~15 min)

Done when: the rule is in the one place that actually applies, and the owner can see it. No second copy is added beside a working automatic rule.

**This parent:** 530 minutes (Phase 0 through Phase 14, including the sub-phases above). Phase 7 is done. Phase 14 is still 25 minutes. Remaining for this parent: 60 minutes (Phases 9 and 14).

### Out of scope

- Deleting `C:\dev\Inc\business_bookmark_sorter` (Phase B hold).
- Moving the business document out of Inc.
- Putting the category dropdown back on the review. Filing as stays a label.
- Auto-removing Chrome bookmarks (section 5 Phase 3).
- Changing destination names in routes.
- Restarting Project Manager.
- Editing the old root `bookmark_sorter.py` categorizer.
