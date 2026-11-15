# Post-Wedding Comms Pack — Launch plan

**Created:** 2026-06-14  
**Product:** WhatsApp-first post-wedding thank-yous + vendor wrap-up  
**Pricing (v1):** ₦10,000 flat self-serve · optional ₦15,000 done-for-you pilot  
**Related:** [PHASE_0b_PITCH.md](./PHASE_0b_PITCH.md) · [MANUAL_TEST.md](./MANUAL_TEST.md) · [task.md](../../.cursor/rules/task.md) §7

---

## Order of operations (your flow)

**Yes — finish development first, then create the IG page and start posting.** That is the correct sequence for this project.

```
1. Development complete     →  2. Instagram + marketing (Phase 0b)
   (build + test + deploy)       (IG, landing, DMs, posts)
```

Do **not** create the public IG page or post about the product until **development is complete**. You need a working product (and ideally a link for bio) before you promise ₦10k to strangers.

### Development complete — checklist (do this before IG)

| Step | Status | Notes |
|------|--------|--------|
| P0 MVP (upload, generate, export, checklist) | ✅ Code done | `test_p0_flow.py` green |
| P1 Paystack unlock + webhook | ✅ Code done | `test_paystack.py` green |
| **Manual UI pass** | ⬜ You, once | [`MANUAL_TEST.md`](./MANUAL_TEST.md) §B + §D (+ §P1 at soft launch) |
| **Landing page** | ✅ In repo | [`landing/`](./landing/) — set `config.js` WhatsApp + push for Pages URL (see [`DEPLOY.md`](./DEPLOY.md)) |
| **Hosted app URL** | ⬜ Deploy | Streamlit Cloud — steps in [`DEPLOY.md`](./DEPLOY.md) |
| Paystack live keys in `.env` | ⬜ When ready | Keep `PAYMENTS_DISABLED=1` until Phase 0b go if you want validation before public checkout |

**Development = complete** when you can run the full couple journey yourself (upload CSV → pay/unlock → generate → export) without surprises — and you have a URL to put in IG bio (hosted app or landing that points to app).

### After development — then marketing

| Step | When |
|------|------|
| Create IG account + bio | After dev checklist above |
| Publish landing (Carrd / Notion) | Same week as IG (or use hosted app URL in bio) |
| Post #1–#3 | After IG account exists |
| Phase 0b: DM 3 couples | Same week as first posts (parallel) |
| Flip `PAYMENTS_DISABLED=0` | After ≥2 couples say yes to ₦10k (Phase 0b go) |

> **Optional shortcut (not your default flow):** Some founders DM 3 friends for WTP *during* late dev, before IG. Your chosen flow is stricter: **dev done → IG**. Stick to that if it keeps you from marketing a half-finished product.

---

## Should you launch today?

**Finish development first.** Do not create the IG page or post publicly until the [development checklist](#development-complete--checklist-do-this-before-ig) is done.

After dev is complete: start marketing (IG + landing + Phase 0b DMs). Do not turn on **public Paystack checkout** until Phase 0b passes (≥2 couples say yes to ₦10k).

| Action | When? | Why |
|--------|--------|-----|
| P0/P1 code + automated tests | **Now (mostly done)** | Agent runs these during build |
| `MANUAL_TEST.md` §P0+P1 | **Before IG** | One UI pass — you confirm it works |
| Host app (public URL) | **Before IG** | Link-in-bio needs a real destination |
| Create Instagram + 3 posts | **After dev complete** | See [Instagram-first launch](#instagram-first-launch-after-development) |
| DM 3 couples (WhatsApp Version A) | **After dev complete** (same week as IG) | Phase 0b WTP validation |
| Public Paystack (`PAYMENTS_DISABLED=0`) | **After Phase 0b go** | Don’t charge strangers until WTP confirmed |

**Your launch** = development sign-off → IG + outreach → 0b go → flip Paystack live.

---

## What you actually need (minimum vs full)

### Phase 0b — this week (credibility-light, speed-heavy)

1. **One landing page** — paste from `PHASE_0b_PITCH.md` into Carrd (free) or Notion public page  
   - Hero + how it works + FAQ + CTA: “DM me on WhatsApp” or a Google Form for early access  
   - **No custom website needed** — a single scrollable page is enough  
2. **WhatsApp** — personal number or dedicated business line  
3. **Payment for pilots** — bank transfer or Paystack payment link is fine for 0b  
4. **The app running locally** — you generate for done-for-you (₦15k) or walk them through self-serve  

**Not needed for 0b:** logo, LLC, ads budget, 20 posts, or a “real company” feel.

### v1 public launch — after 0b go (1–2 weeks out if 0b moves fast)

1. Hosted app (Streamlit Cloud / Railway / similar)  
2. Paystack live keys, `PAYMENTS_DISABLED=0`, `PAYSTACK_AMOUNT_KOBO=1000000`  
3. One `MANUAL_TEST.md` pass (you, once)  
4. Landing CTA → live Paystack checkout  
5. **1–2 real testimonials** from 0b couples (even paraphrased with permission)

---

## Website — yes, but tiny

**Yes, you need *a* web presence — not a full website.**

Typical Nigerian couple flow: **Instagram post or WhatsApp forward → landing page → Paystack or DM you**.

A Carrd page with:

- Headline: *“Post-wedding thank-yous in one afternoon”*
- ₦10,000 flat
- 3 problem bullets
- How it works (4 steps)
- WhatsApp button

**1–2 hours** using copy in `PHASE_0b_PITCH.md`. Skip WordPress and hiring a dev for v1.

---

## Social media — how many posts?

**Start with 3 posts, not 30.** Post one every 2–3 days.

| # | Type | Purpose |
|---|------|---------|
| 1 | Problem hook | “Still owe thank-yous 6 weeks later?” + landing link |
| 2 | How it works | Guest list → drafts → WhatsApp → checklist (screenshot or mock) |
| 3 | Price + CTA | “₦10,000 flat. No tiers.” + DM “ACCESS” |

### Platform priority (Nigeria weddings)

1. **WhatsApp** (direct + church/asoebi groups with admin permission) — highest ROI  
2. **Instagram** — `#AbujaWedding` `#LagosWedding` `#NigerianWedding`  
3. **Twitter/X or TikTok** — optional; one repost of post 1 is enough  

You don’t need daily content. This product sells on **timing and guilt**, not influencer volume. Couples search for this 2–8 weeks *after* the wedding — pinned posts still work.

**Bio:** one line + link to landing + “DM for early access.”

---

## Instagram-first launch (after development)

**IG is your primary marketing channel — but only after development is complete** (see [Order of operations](#order-of-operations-your-flow)).

Once the dev checklist is done:

- **Don’t rely on IG alone** for Phase 0b (pair with 2–3 warm DMs the same week).
- **Don’t turn on public Paystack** until Phase 0b passes (≥2 couples say yes to ₦10k).

### What “development complete” unlocks

| Ready after dev | Still for Phase 0b / post-0b |
|-----------------|----------------------------|
| Real app screenshots for posts | 3 couple conversations |
| Hosted URL in bio | ≥2 yes to ₦10k |
| Paystack wired (can stay disabled) | Flip `PAYMENTS_DISABLED=0` after go |
| Confidence the product won’t embarrass you on DM | Testimonials from early users |

### Minimum before first IG post

**Prerequisite:** [Development complete checklist](#development-complete--checklist-do-this-before-ig) ✅

Then:

1. **IG account** — name + bio + one line (*“Post-wedding thank-yous · ₦10k flat · link below”*)
2. **One link** — hosted app URL **or** Carrd/Notion landing → app
3. **Way to respond** — WhatsApp or IG DMs

**Posting:** **3 posts** (problem → how it works → price/CTA), spaced 2–3 days apart.

### Why warm DMs still matter (even if IG-first)

| Channel | Best for |
|---------|----------|
| **Instagram** | Strangers, hashtags, “I exist” |
| **WhatsApp to people you know** | “Would you pay ₦10k?” — often answers in 48 hours |

Phase 0b needs **≥2 couples to say yes to ₦10k**. That usually comes from **3 DMs to recently married friends**, not from week one of IG alone.

| Approach | Typical result |
|----------|----------------|
| **IG only, no DMs** | Slow validation; likes, few sales |
| **IG + 3 warm DMs** | Good balance (recommended) |
| **IG only, no landing, no reply plan** | Visibility without conversions |

### Practical path (dev first → then IG)

```
Phase A — Development (before any IG page)
  → test_p0_flow.py + test_paystack.py green
  → MANUAL_TEST.md §P0+P1 once
  → Deploy hosted app URL
  → Paystack keys in .env (PAYMENTS_DISABLED=1 OK for now)

Phase B — Marketing (after Phase A)
  → Create IG + bio + link to hosted app / landing
  → Post #1 (problem hook) — use real screenshots
  → DM 2–3 couples (Version A; Phase 0b)
  → Posts #2 and #3 over the next week
  → Reply every DM within hours

Phase C — After Phase 0b go (≥2 yes to ₦10k)
  → PAYMENTS_DISABLED=0
  → Update bio CTA to live checkout
  → Optional: ₦15k done-for-you for one couple = first testimonial
```

### Credibility on IG when you’re new

Early posts can say:

- *“Built for Nigerian newlyweds stuck on thank-yous”*
- *“Early access — Abuja/Lagos first”*
- *“₦10,000 flat · you send from your WhatsApp”*

No fake social proof. **Honest early-access** beats waiting in silence for testimonials.

### Short answers

| Question | Answer |
|----------|--------|
| Must I finish development before IG? | **Yes** — that is your flow. Complete dev checklist, then IG. |
| Can I post on IG right after code is written? | **Not yet** — run `MANUAL_TEST.md` and deploy first. |
| Should IG be the only channel? | **No** — add link in bio + DM **3 real couples** for Phase 0b. |
| When does Paystack go live publicly? | After Phase 0b go (≥2 yes to ₦10k), set `PAYMENTS_DISABLED=0`. |

---

## How to market and get visibility (after development)

> **Start this section only after** the [development checklist](#development-complete--checklist-do-this-before-ig) is complete.

### Week 1 — IG + warm outreach

1. Create **IG account** + bio; link to hosted app or landing.  
2. Post **#1** (problem hook) from `PHASE_0b_PITCH.md`.  
3. **List 10 people** who married in the last 12 months (Abuja/Lagos). Message **3** using Version A.  
4. Ask each: *“Know one couple still procrastinating on thank-yous?”*  
5. Optional **₦15k done-for-you** for one tired couple — first case study.

### Week 2 — semi-warm

6. Posts **#2 and #3** on IG.  
7. Ask church wedding committee / aso-ebi admin: *“Can I share this once for newlyweds?”*  
8. Put landing link in WhatsApp status for 7 days.

### After first paying user — credibility assets

7. Screenshot (blurred) of checklist / export — *“220 guests, done in one afternoon.”*  
8. One quote: *“Worth ₦10k so my aunties stop side-eyeing me.”*  
9. Add quote to landing; replace placeholder in `PHASE_0b_PITCH.md`.

### What to skip for now

- Paid Meta ads (need proof + creative first)  
- MC/planner B2B (not in scope for v1)  
- TikTok daily reels  
- Building a second product (guest games) before comms validates

---

## How long to gain credibility?

For this product, credibility is **narrow and fast**:

| Milestone | Timeline | What it buys you |
|-----------|----------|------------------|
| 3 conversations | **Week 1** | Willingness-to-pay signal |
| 1 couple uses it (paid or pilot) | **Week 2–3** | Real workflow proof |
| 2 couples say yes to ₦10k | **Phase 0b go** | Permission to public launch |
| 2 testimonials + 1 screenshot | **Week 4** | Enough for strangers to trust ₦10k |

You do **not** need 6 months, press coverage, or 1,000 followers. Nigerian wedding buyers trust: **friend referral + “this couple used it” + clear price + WhatsApp support**.

Credibility = **social proof from people like them**, not a polished brand.

---

## Balance: credibility vs speed

> **Launch the *conversation* fast. Launch the *product* only after someone pays or strongly commits.**

| Fast (do now) | Wait (until proof) |
|---------------|-------------------|
| Landing page + WhatsApp outreach | Hosted public app |
| “Early access — first 10 couples” framing | “Nigeria’s #1 wedding platform” claims |
| Manual done-for-you for 1–2 couples | Paid ads |
| Honest FAQ (“you send from your WhatsApp”) | Fake testimonials |
| ₦10k flat, one offer | Tiers, upsells, rebrand |

**“Early access” IS credibility** when you’re honest: *“I built this because every newlywed I know is stuck on thank-yous. Testing with Abuja/Lagos couples first.”*

---

## Suggested timeline (dev first → then IG)

| Phase | Action |
|-------|--------|
| **A — Dev** | `MANUAL_TEST.md` §P0+P1 → deploy hosted app → Paystack keys in `.env` |
| **B — Week 1 marketing** | Create IG + post #1; DM 3 couples (Version A) |
| **B — Week 2 marketing** | Posts #2–#3; follow up non-replies |
| **0b gate** | 3 conversations → record go/no-go in `PHASE_0b_PITCH.md` |
| **C — If go** | `PAYMENTS_DISABLED=0`; bio link = live checkout |
| **Launch** | Landing + IG + WhatsApp support for paying couples |

---

## Bottom line

**Flow:** Development complete → IG + marketing → Phase 0b go → Paystack live.

The problem is real and the price is simple. **Don’t post on IG until you’ve run the product end-to-end yourself** (`MANUAL_TEST.md` + hosted URL). Then use IG + 3 couple DMs to confirm ₦10k works.

| Launch type | What it includes |
|-------------|------------------|
| **Development sign-off** | Automated tests + `MANUAL_TEST.md` + hosted app |
| **Marketing launch** | IG account + 3 posts + landing + 3 couple DMs |
| **Full commercial launch** | Phase 0b go + `PAYMENTS_DISABLED=0` |

---

## Next actions (in order)

1. Run [`MANUAL_TEST.md`](./MANUAL_TEST.md) §P0+P1 (development sign-off)  
2. Deploy hosted app; add URL to notes for IG bio  
3. Create IG account + bio; post caption #1 from `PHASE_0b_PITCH.md`  
4. Publish landing (optional if app URL is enough)  
5. DM 3 couples (Version A) — same week as first IG post  
6. After Phase 0b go: `PAYMENTS_DISABLED=0`
