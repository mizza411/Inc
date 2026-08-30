# Loan-spread operator doctrine

**Track:** LOAN-SPREAD-1  
**What this is:** a written playbook for using *other people’s money* (or *other people’s time*) so a campaign can **end** with cash in your pocket — not a 40-year job and a pension.  
**What this is not:** a lending app, a bank bot, or a reason to take a salary loan and call it “investing.”

v1 sign-off: 2026-08-30 (owner menu 1). Backlog satellite deleted. Do **not** look for this track in main `task.md`.

---

## How to use

1. Read `closed_loop_doctrine.md` once (seats, default loop, variants, rate buckets, pension).
2. Before any real deal, run `spread_test.md` (about 10 minutes). If it fails, stop.
3. If you are matching an existing Inc hunt (gadgets, Abuja, field visits), open `track_map.md` — **pointers only**; those products were not changed.
4. Put **personal** naira figures only in `data/` (gitignored). Never paste BVN, bank passwords, or live offers into git or chat.

**Default campaign:** borrow (or take supplier time) → put the money into something that returns **more than it costs** → get **cash** → **pay off** principal + interest + fees → **keep the remainder**.

---

## Seats

Which chair you sit in decides who keeps the interest.

| Seat | What you are doing | Typical outcome |
|------|--------------------|-----------------|
| **Consumer** | Borrow to consume (phone, car, lifestyle) | You **fund** the bank |
| **Worker + pension** | Sell hours for decades; wait for a delayed coupon | You **are** the coupon, later, often smaller after inflation |
| **Operator** | Rent money (or time) for a deal that pays more than the rent | You keep the **spread** (return minus cost) |
| **Lender** | You charge the interest, fee, or float | You **are** the small bank |

Same word — “loan.” Opposite businesses. This folder is written for the **operator** seat, with **pay off and keep** as the default ending.

---

## Files

| File | Role |
|------|------|
| `closed_loop_doctrine.md` | Seats, closed loop, open loop vs recycle, variants, Nigeria buckets, pension |
| `spread_test.md` | One-page R vs C gate, fixture ₦ example, do-not, kill conditions |
| `track_map.md` | Which existing Inc track fits which variant (no code edits there) |
| `MANUAL_TEST.md` | One owner read-through at sign-off |
| `tests/test_doctrine_smoke.py` | Files + required headings (agent-run) |
| `data/` | Optional personal numbers — **not** in git |

Optional later (not in v1): `spread_check.py` CLI — only if you start Phase 5.

---

## Isolation

This folder does not launch a tray, Hub card, or morning reminder. It does not edit FIR, Tegrid, gadget automation, launchers, or `.env`.
