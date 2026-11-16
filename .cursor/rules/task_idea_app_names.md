# IDEA-APP-NAME-1 - Future idea names sound like apps

**Status:** Phases 0-4 done 2026-11-16. Owner asked to commit and push. Remote update is this phase.
**Attempt (backlog write):** 6
**Authoritative backlog:** this file only
**Main `task.md`:** not referenced (overloaded, about 2,800 lines). Do not add a pointer there. Section 19 stays the formulation parent. This file is a naming add-on for future runs.
**Delete when:** Phases 0-4 are done or waived, both prompt files carry the name rule, the prompt smoke is green, and the owner has committed that prompt change if they want the Cloud agent to see it. Then delete this satellite. Do not fold it into `task.md`.

## Owner ask (2026-11-16)

Future business-idea documents from the Cursor Cloud formulation agent must name a product the way an app is named. Desk, Pack, and the other non-app endings stay out of those future names. The old local idea files stay as they are.

The generator is two prompts, both already Active:

1. Prompt A, Discover, `prompts/agent_formulation_run.txt`, daily 07:00 Africa/Lagos. This invents the name.
2. Prompt B, Pack, `prompts/agent_formulation_pack.txt`, daily 11:00 Africa/Lagos. This packs the same file and must not put the banned endings back.

Confirmed from pull request 96 on 2026-11-16: both prompts already finished for that day (about 07:06 and about 11:02). This task does not rewrite `business_ideas_20261116.md` or any older output.

## Recommendations

R2, R3, and R5 confirmed 2026-11-16. R4 stays a later choice. It was not part of the Phase 0 yes.

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| R1 | Put the same name rule in both prompt files. | Pass 1 invents the name. Pass 2 copies it into the packed file. One file alone can still ship Desk or Pack. | 1, 2 |
| R2 | Leave every existing `business_ideas_*.md` and `.docx` as they are. | The owner asked for future documents, not a rewrite of the past. | all |
| R3 | Ban these endings on the product name: Desk, Pack, Clock, Board, Brief, Kit, Checklist, Playbook, Plot, Spot, Cohort, Sheet. | They sound like a paper, a folder, a timer, or a place. Found in the Nov and Oct 2026 idea titles. | 0, 1, 2 |
| R4 | Keep the news, the amount, the date, and slang in the description after the title. Keep Ready, Evidence, Diligence, and Prep out of the product name. | N52,500, $391m, Dec3, FakeCert, and Ping-Pong go stale or sound like a headline. | 1, 2 |
| R5 | End the name with one job word: Check, Scan, Verify, Track, Alert, Record, Register, Monitor, Guard. Use App only when none of those fit. NG and Lite may follow a real product name. | A licence check becomes TRCN Licence Check. A stuck transfer becomes a Track. Not every idea ends in App. | 1, 2 |
| R6 | Do not edit strategy scripts, Hub cards, Automation clocks, section 14 card labels, or the Automation screen. | The Cloud spine already says follow the two txt files. The clocks stay 07:00 and 11:00. | all |
| R7 | Cloud reads the committed remote copy. Phase 4 is a separate owner ask to commit and push. | A local prompt edit is invisible to tomorrow's 07:00 run until it is on the branch the automation checks out. | 4 |

## Out of scope

- Rewriting old outputs under `agent-business-idea-runs/outputs/`.
- Renaming Post-Wedding Comms Pack or any built app.
- Changing strategy folders, `run_all_strategies.py`, Hub, the tray, or the 07:00 and 11:00 clocks.
- Fusing Pass 1 and Pass 2 into one prompt.
- Opening Word, editing the Automation screen, or merging pull request 96.

## Layout

Two existing prompt files only, plus one assert in the existing prompt smoke. No new product folder.

## Phases

### Phase 0 - Confirm the word lists

- [x] **0a** Owner confirms the ban list in R3. Confirmed 2026-11-16.
- [x] **0b** Owner confirms the job words in R5. Confirmed 2026-11-16.
- [x] **0c** Owner confirms old output files stay unchanged (R2). Confirmed 2026-11-16.

Done when: the three boxes above are ticked. No prompt file changes in this phase. Met 2026-11-16. R4 was not ticked.

### Phase 1 - Discover prompt only

- [x] **1a** Add the name rule to `prompts/agent_formulation_run.txt`. New product titles use an R5 job word. R3 endings stay out of the title. Amounts, dates, and slang stay in the description. Done 2026-11-16.
- [x] **1b** Leave the rest of that file in place: strategy list, `_PENDING_PASS_2_PACK_`, no Docx convert, write under `agent-business-idea-runs/` only. Done 2026-11-16.

Done when: 1a and 1b are true, and Pass 2 has not been edited yet. Met 2026-11-16.

### Phase 2 - Pack prompt only

- [x] **2a** Add the same name rule to `prompts/agent_formulation_pack.txt`. Pack keeps a clean Pass 1 name, and it does not introduce an R3 ending while it rewrites cards. Done 2026-11-16.
- [x] **2b** Leave section 14 labels, the no-new-ideas rule, and the one-shot Docx step in place. Done 2026-11-16.

Done when: 2a and 2b are true, and no output file from an old date was rewritten. Met 2026-11-16.

### Phase 3 - Smoke, existing markers still hold

- [x] **3a** Extend `agent-business-idea-runs/tests/test_formulation_pack_prompt.py` so both prompts name the ban and the job words. Done 2026-11-16.
- [x] **3b** Run that test file. Existing markers still pass (Regulatory, Competitors / alternatives, pending marker, strategies list). Done 2026-11-16, 4 tests OK.

Done when: the test file prints OK, and no strategy script or Hub file changed. Met 2026-11-16.

### Phase 4 - Remote copy, only when the owner asks

- [x] **4a** Commit the two prompt files and the smoke, only after the owner asks. Owner asked 2026-11-16.
- [x] **4b** Push that commit, only after the owner asks, so the next 07:00 Cloud run can read it. Owner asked 2026-11-16.

Done when: the owner asked, and the remote has the prompt change. Owner asked 2026-11-16. Push is the step that follows this commit.

## Minutes (this conversation's slices)

| Slice | Minutes |
|-------|---------|
| Phase 0 | 15 |
| Phase 1 (1a 15, 1b 10) | 25 |
| Phase 2 (2a 15, 2b 5) | 20 |
| Phase 3 (3a 10, 3b 10) | 20 |
| Phase 4 | 15 |
| **All slices** | **95** |
