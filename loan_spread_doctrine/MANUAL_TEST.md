# MANUAL_TEST — Loan-spread doctrine (owner, once)

**When:** after agent smoke is green (v1 sign-off). **Not** during the build.  
**Why not automated:** subjective — “does this match how I think?” and whether the tone is usable. Heading presence is already checked by `tests/test_doctrine_smoke.py`.

---

## Owner read-through

Do this in **one** sitting (~15 minutes). Do not re-run it after every sentence change.

- [x] Open `README.md`. The **How to use** steps make sense; the **Seats** table matches consumer / worker+pension / operator / lender.
- [x] Open `closed_loop_doctrine.md`. Default is **pay off and keep** (closed loop), not “stay in debt forever.” **Open loop vs recycle** is clearly contrast. **Variants** and **Nigeria rate buckets** are illustrative, not your personal offer.
- [x] Open `spread_test.md`. You could run the **Spread test** table on a fake deal in 10 minutes. The **Worked fixture** (₦1,000,000 / 3 months / 24%) shows keep vs lose. **Do-not list** and **Kill conditions** would stop a bad draw.
- [x] Open `track_map.md`. Gadget = float; Abuja = do not blindly mortgage buy-to-hold; FIR/Tegrid = find **R**, not a loan button. No expectation that those apps changed.
- [x] Confirm you did **not** put BVN, passwords, or real loan offers into any tracked file. Personal ₦ only in `data/` if at all.

**Pass:** all boxes ticked; you would use the spread test before a real facility.  
**Fail:** write one sentence in the notes below (still do not paste bank secrets).

### Notes / pass-fail

- Date: 2026-08-30
- Pass / fail: **Pass** (owner chat menu **1** — sign-off + delete satellite)
- One sentence (optional): Objective checks re-read; no secrets in tracked files; smoke 4 passed.

---

## After this pass

Satellite `.cursor/rules/task_loan_spread.md` **deleted** 2026-08-30. Do **not** fold a pointer into main `task.md`. Doctrine stays in this folder.
