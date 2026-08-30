# Spread test

Run this **before** you take a facility or stretch supplier terms. About **10 minutes**. Fixture numbers below are **teaching only** — not a live quote and not your bank offer.

---

## Spread test

Fill in order. If any line is “no” or blank, **stop**.

| # | Check | Your note (personal ₦ → `data/` only, not git) |
|---|--------|--------------------------------------------------|
| 1 | **C** — cost of money for *this* hold: interest + fees + penalties if late. Annual rate × days/365 (or the lender’s formula). | |
| 2 | **R** — cash you will actually hold at exit (sale, collection, markup), after tax if you know it. Not a listing price. Not “it might go up.” | |
| 3 | **Start date** — when the clock on **C** starts. | |
| 4 | **Repay / pay-supplier date** — calendar day you must settle. | |
| 5 | **Cash on repay day?** — Yes only if the money is in hand *or* in a signed collection you can force that day. Paper profit = **no**. | |
| 6 | **Fees** — facility fee, transfer, FX spread, agent, legal, logistics. Add into **C**. | |
| 7 | **Tax** — if the remainder is taxable, shrink **R** or the keep. If unknown, treat keep as smaller. | |
| 8 | **Idle time** — days money sits doing nothing still accrue **C**. | |
| 9 | **Keep or lose** — Keep only if **R > C** *and* line 5 is yes. | |

**Spread** here means: what the money **earns in cash** minus what the money **costs**. If you cannot write **C** and **R** in naira, you do not have a test.

---

## Worked fixture

**Do not** treat this as advice to borrow ₦1,000,000. It only shows the *shape*.

Assumptions (simple interest, no extra fees):

- Principal: **₦1,000,000**
- Hold: **3 months** (¼ year)
- Stated rate: **24% a year**
- Interest **C** ≈ ₦1,000,000 × 0.24 × (3/12) = **₦60,000**
- Amount due at month 3 ≈ **₦1,060,000** (before fees)

| Exit cash **R** | vs ₦1,060,000 due | Keep or lose |
|-----------------|-------------------|--------------|
| ₦1,250,000 | Remainder ₦190,000 | **Keep** (in this toy) |
| ₦1,060,000 | Remainder ₦0 | Flat — you worked for the bank |
| ₦1,040,000 | Short ₦20,000 | **Lose** |

If fees are ₦15,000, **C** becomes ₦75,000 and due is ₦1,075,000. The “keep” column shrinks. That is why the checklist adds fees **before** you celebrate **R**.

Same fixture, **wrong** use: borrow ₦1,000,000 at 24% to “invest” in something that cannot be cash in 3 months. Calendar mismatch — see kill conditions.

---

## Do-not list

Do **not** call these the closed loop:

- **Consumption / salary / card loans** labeled as invest (phone, car, lifestyle). That is the consumer seat.
- **Abuja buy-to-hold with a commercial mortgage** when typical commercial rates (**15–25%**) sit **above** typical gross rental yields (**about 10–15%** in the existing Inc research). Cash buyers and true concessional buckets are a different story — cite only, do not rewrite that file: `Abuja-Real-Estate-Research/abuja-real-estate-profitable-sub-niches.md` (financing section: cash-rich and rental models vs leveraged buy-to-hold unless NHF/FMBN-eligible).
- **Paper profit** — the asset “went up” but you cannot sell or collect on the due date.
- **Calendar mismatch** — loan due on a Tuesday; cash maybe next quarter.
- **FX mismatch** — naira debt vs a dollar hope, or the reverse, with no real hedge.
- **Bad title / fraud asset** — especially FCT land: you cannot repay from something that was never yours.
- **Grey ROI apps / guaranteed monthly %** with no real **R**.

---

## Kill conditions

Stop the campaign (do not draw, or unwind if you already did) when:

1. **Dates** — you cannot name a repay day, or **R** is not cash that day.
2. **Paper profit** — line 5 of the spread test is no.
3. **Consumption labeled as invest** — the facility would have been taken even with no deal.
4. **R not clearly above C** after fees, tax, and idle time.
5. **You would need a miracle** (new buyer, new rate, new title) for the numbers to work.

Personal naira, offers, and BVN never go in this file. If you must compute a real deal, use gitignored `data/` and do not commit it.
