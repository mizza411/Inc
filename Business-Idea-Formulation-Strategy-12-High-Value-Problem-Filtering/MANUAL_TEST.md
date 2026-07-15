# Strategy 12 — MANUAL_TEST.md

**Product:** High-Value Problem Filtering (GUEMF) — dual-mode (standalone CLI + agent Mode A/B)  
**Backlog:** `.cursor/rules/task.md` §13  
**Policy:** Automate-first (repo `deferred-manual-testing` rule).

## Remaining manual steps for dual-mode v1 (Phases 0–3)

**None.**

Everything that can be verified for CLI dual-mode scaffolding is automated:

| Check | How |
|-------|-----|
| GUEMF scoring helpers | `test_strategy12_noninteractive.py` |
| Non-interactive CLI (`--inputs` fixture) | same |
| Interactive import still loads | same |
| Agent prompt Mode A + Mode B markers | `test_strategy12_prompt_dual_mode.py` |
| Runner still registers Strategy 12 | `test_strategy12_regression.py` |
| Full bundle | `python test_strategy12_regression.py` (from this folder) or pytest below |

```powershell
cd Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering
$env:PYTHONIOENCODING='utf-8'
python test_strategy12_regression.py
# or:
python -m pytest test_strategy12_noninteractive.py test_strategy12_prompt_dual_mode.py test_strategy12_regression.py -q
```

## Why not automated (none for v1)

N/A — interactive TTY menu click-through is intentionally **not** a dual-mode v1 gate (would require human `input()`). Menu still launches `problem_filter.py` with no args (interactive default), unchanged by Phases 0–3.

## Optional later (not blocking §13 Phase 3)

| Item | Why not automated / why deferred |
|------|----------------------------------|
| Live Hub “Agent formulation run” producing S12 Mode A ideas in a dated Docx | End-to-end agent session; proof is next formulation run after Phase 2 prompt, not a MANUAL_TEST checkbox |
| Phase 4 `--with-strategy12` fetch key | **Shipped** 2026-07-15 — optional; default skipped |

## Sign-off

- [x] Automated regression green (Phase 3) — record date in `task.md` §13 when run.
- Manual UI pass: **not required** for dual-mode Phases 0–3.
