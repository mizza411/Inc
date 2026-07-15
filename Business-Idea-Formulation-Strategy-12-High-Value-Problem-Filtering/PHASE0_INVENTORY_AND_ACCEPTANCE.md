# Strategy 12 Phase 0 — Inventory & acceptance (2026-07-15)

Docs-only artifact for **task.md §13 Phase 0**. No runtime behavior changes.

Authoritative dual-mode **contract** lives in `README.md` → **Dual-mode contract (Mode A + Mode B)**.

---

## 0.2 — Inventory (as of 2026-07-15)

### Entrypoints

| Surface | Path / behavior | Notes |
|---------|-----------------|--------|
| CLI script | `problem_filter.py` → `HighValueProblemFilter.run()` | Interactive: `input()` for problems, Y/N scores, selection |
| `__main__` | Instantiates filter and calls `run()` | No argparse today |
| Criteria constant | `CRITERIA` in `problem_filter.py` | Growing, Urgent, Expensive to Solve, Mandatory, Frequent |
| Outputs | `high_value_problem_filtering_YYYYMMDD_HHMMSS.json`, `chatgpt_strategy12_prompts.txt` | Written under cwd (usually S12 folder when launched via runner) |
| Auto-open | `open_file_automatically` on summary JSON | Can hang CI / agent wrappers |
| Playbook md | `business-idea-formulation-strategy-12-high-value-problem-filtering.md` | Manual GUEMF + Prompt 1a/1b |
| README | This folder’s `README.md` | Historically documented `steps.py` (stale name → `problem_filter.py`) |

### Not present yet (Phases 1+)

| Item | Status |
|------|--------|
| `--non-interactive` / `--inputs` | Missing (Phase 1) |
| Pure scoring module (e.g. `guemf_scoring.py`) | Missing (Phase 1.1) |
| Fixture JSON for smokes | Missing (Phase 1.2 / 1.5) |
| Agent Mode A language in `prompts/agent_formulation_run.txt` | Missing (Phase 2) — see overlay-only phrase below |
| `strategy_12_*` in `agent_strategy_run.py` | Missing (optional Phase 4) |
| `MANUAL_TEST.md` / pytest in S12 folder | Missing (Phase 1.5 / 3) |

### Master runner registration (`run_all_strategies.py`)

Already registered (do **not** re-register in Phase 0–1):

- `STRATEGY_SCRIPTS[12]` → `.../problem_filter.py`
- `STRATEGY_META[12]` → name “High-Value Problem Filtering”, GUEMF desc
- Active range includes **11–15** (Strategy 12 included)
- Launch path: menu / Run ALL → subprocess of `problem_filter.py` in strategy cwd — still **interactive**

### Agent formulation prompt (overlay-only today)

File: `prompts/agent_formulation_run.txt`

| Signal | What it does | Gap |
|--------|----------------|-----|
| Include list has **12** | Agent is told to include Strategy 12 | Does not define Mode A discovery |
| Phrase: “GUEMF-style scoring … **where relevant**” | Encourages **Mode B overlay** on other ideas | Ambiguous — read as scoring sticker, not S12 generator |
| Strategy 1 / 6 / 7 / 15 get detailed blocks | Clear standalone behavior | **No equivalent Strategy 12 Mode A block** |
| Example non-interactive flags mention S1 + S15 only | Agents skip interactive CLIs | S12 never listed as `--non-interactive` candidate |

### Agent outputs (recent practice)

| File pattern | S12 in execution summary |
|--------------|---------------------------|
| `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` | Status **synthesized**; note “Applied in ranked table”; `problem_filter.py` not run |
| Ranked table | GUEMF (G/U/E/M/F) 1–5 + composite — **Mode B only** |
| Idea traces | Rarely `primary S12`; S12 appears as mid/late hop (`→ S12`) |

### Other consumers

| Consumer | Link |
|----------|------|
| Cyber vertical `task.md` §9 Phase 3 | Optional GUEMF pass — may use Phase 1 CLI later; **out of scope** for §13 code unless separately approved |
| Google Drive map | Business 10th → Strategy 12 |

---

## 0.3 — Acceptance sketch (Phases 1–4)

Use as the executable definition of done when coding starts. Checkboxes are **implementation** gates (not Phase 0 itself).

### Phase 1 — CLI standalone (modular)

- [x] `guemf_scoring.py` (or equivalent) exists with pure score/rank helpers; no `input()`.
- [x] Documented JSON inputs fixture under S12 folder.
- [x] `python problem_filter.py --non-interactive --inputs <fixture.json>` exits 0, writes ranked summary, **no** `input()`, **no** required GUI open (or open gated off).
- [x] Bare `python problem_filter.py` still starts interactive flow (regression).
- [x] `run_all_strategies.py` still points at same script path; menu registration unchanged.
- [x] Smoke test file green (`test_strategy12_noninteractive.py` — 7 passed 2026-07-15).

### Phase 2 — Agent prompt dual-mode

- [x] `prompts/agent_formulation_run.txt` explicitly requires **Mode A** (GUEMF Prompt-1a-style discovery → ideas with primary/trace **S12**) **and** **Mode B** (overlay scores on other strategies’ ideas).
- [x] Execution-summary guidance: S12 notes must cover **both** legs.
- [x] `agent-business-idea-runs/README.md` documents dual-mode.
- [x] Optional static smoke: prompt contains Mode A + Mode B markers (`test_strategy12_prompt_dual_mode.py`).

### Phase 3 — Docs / MANUAL / regression

- [x] S12 README script section documents interactive vs non-interactive.
- [x] `MANUAL_TEST.md`: automate-first; ideally **no** user steps for dual-mode v1.
- [x] Documented pytest/smoke command; other strategies’ `STRATEGY_SCRIPTS` keys unchanged.
- [x] Cyber §9 Phase 3 note: “can consume S12 CLI later” (doc only).

### Phase 4 — Optional soft fetch (deferrable for v1)

- [x] Soft `strategy_12_*` in fetch JSON; default skip unless `--with-strategy12`.
- [x] Failure does not abort RSS/OWID/S1/S6/S7/S14 paths.
- [x] Default fetch without flag unchanged for existing keys (`strategy_12_run` status skipped).

### Phase 0 complete when

- [x] Dual-mode contract in `README.md`
- [x] This inventory + acceptance file committed/available
- [x] `task.md` §13 Phase 0 checkboxes marked done; Phase 0 checkpoint approved (2026-07-15)
- [x] **Zero** changes to `problem_filter.py`, `run_all_strategies.py`, `agent_strategy_run.py`, or agent prompt (prompt wait = Phase 2)
