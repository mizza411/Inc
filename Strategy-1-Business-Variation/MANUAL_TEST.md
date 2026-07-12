# Strategy 1 — Manual test (v1 sign-off only)

**When to run:** Once at v1 complete, after `python test_phase6_regression.py` is green.  
**Do not** use as mid-build click-through.

## Already covered by automation (do not re-test manually)

- Non-interactive collector (`--inputs` / `--seed-ids`)
- Master runner registration of Strategy 1; Strategy 2 verbal; 8/10 retired
- Agent fetch JSON includes `strategy_1_seeds` + prior S5–S7/S14/S15 keys
- Launcher config: Formulated `strategy1_run` + Established folder/gadget cards
- `py_compile` on Strategy 1 formulation modules

**Why the items below are not automated:** Hub tray UI, interactive CLI prompts, and subjective playbook readability cannot be asserted headlessly without flaky GUI automation.

---

## Prerequisites

1. Repo at `C:\dev\Inc` (or your Inc root)
2. Phase 6 smoke green:

```powershell
cd Strategy-1-Business-Variation
python test_phase6_regression.py
```

---

## Manual steps (single pass)

### A. Inc Hub — Formulated card

1. Start Inc Launcher tray if not running.
2. Open Inc Hub → **Formulated ideas**.
3. Confirm **Run Strategy 1 — Business Variation** is listed.
4. Click it → interactive Strategy 1 CLI should open (pick a seed, add/accept complaints, confirm JSON + Prompt 1a files written under `Strategy-1-Business-Variation/`).

**Why not automated:** Hub tray / Tk launch + interactive `input()`.

### B. Inc Hub — Established cards still present

1. Hub → **My Established business ideas**.
2. Confirm **Strategy 1 folder (playbook + gadget ops)** and **Gadget business automation** still open their folders.

**Why not automated:** Subjective Hub navigation; config presence already tested in pytest.

### C. Master runner — single strategy

1. From repo root: `python run_all_strategies.py`
2. Menu **3** → Strategy **1** → confirm it launches (you may Ctrl+C after intro if not completing a full interactive run).
3. Menu **3** → Strategy **2** → should say verbal only.
4. Menu **3** → Strategy **5** (or another active number) → still listed/launchable (cancel after start if desired).

**Why not automated:** Interactive menu `input()` loop.

### D. Playbook readability

1. Open `strategy-1-business-variation.md` — human steps still present under the technical status banner.

**Why not automated:** Subjective doc check.

---

## Pass / fail notes

| Step | Pass? | Notes |
|------|-------|-------|
| A Hub Run Strategy 1 | | |
| B Established cards | | |
| C Runner menu 1 / 2 / other | | |
| D Playbook intact | | |

**Sign-off:** ☐ Ready for staging/commit after manual pass
