# Wedding Guest Engagement (Repositioned)
## Crowd participation for couples & event centres — not MC tooling

**Status:** Strategy one-pager (Jun 2026)  
**Previous angle:** B2C “wedding games app” with couple quizzes — **retired** (MCs already own live quizzes; MCs unlikely to pay for software).

---

## One-line pitch

A **WhatsApp-friendly guest link** (no app download) that runs **pre-wedding, day-of, and post-wedding** participation — photo challenges, live polls, scavenger tasks, and a shared guest gallery — **paid for by the couple** or bundled by **event centres** as a venue amenity.

---

## What we are / are not

| We are | We are not |
|--------|------------|
| Guest participation **infrastructure** (festival “crowd app” logic) | A couple-quiz app competing with the MC |
| Pre-event hype + post-event memories + async inclusion | An MC B2B product (MCs won’t pay — out of scope) |
| QR / WhatsApp link → mobile web (PWA) | Native iOS/Android app store launch (Phase 1) |
| Output couples keep: gallery, votes, messages, guest list enrichment | Live entertainment or onsite hosting |

**Festival import:** Coachella-style crowd participation **without** replacing the main-stage host. The MC keeps the mic; guests use their phones for things the MC cannot scale to 200 people.

---

## Who pays (explicit)

### Primary — **Couples (B2C)**
- One-time **per-wedding fee** (e.g. ₦25,000–₦75,000) for a branded guest link + dashboard.
- Sold via Instagram/TikTok, wedding planners (referral only — planner does not need to pay), aso-ebi group chats, event-centre “add this package” upsell.
- **Why couples pay:** tangible keepsakes (gallery, guest messages, leaderboard screenshots), diaspora inclusion, less chaos than chasing 150 guests manually.

### Secondary — **Event centres & halls (B2B venue)**
- Venue buys **white-label or co-branded** guest links included in hall rental tiers (“Scan at our entrance”).
- **Why venues pay:** differentiation vs other halls, marketing asset, foot-traffic capture at registry-adjacent or high-traffic centres — **not** the same buyer psychology as MCs.
- Revenue: monthly seat fee or per-event wholesale (couple still sees venue branding).

### Not in scope — **MCs**
- No MC subscription, no “MC toolkit” sales motion.
- MCs may **announce** the link once; they are distribution, not customer.

### Optional channel — **Photographers / videographers (affiliate)**
- Upsell “guest photo challenge + gallery” alongside coverage; rev-share, not B2B license.

---

## Moments we own (MC gap)

MCs dominate **live reception entertainment**. We own everything else:

| Moment | Features | MC overlap |
|--------|----------|------------|
| **2–4 weeks before** | Predictions, childhood photo match, family-team points (bride vs groom side), blessing submissions | None |
| **Day-of (async)** | Live polls (“which outfit change next?”), text-in well-wishes (moderated), photo scavenger (QR at hall/registry) | Low — MC reads results if they want |
| **Day-of (inclusion)** | Back-table guests, elders, introverts vote without standing up; diaspora same link | None |
| **After event** | Guess-who game, gallery unlock, export for thank-you notes / recap | None |

**Deliberately excluded:** verbal couple quiz, dance-off hosting, spray hype — MC territory.

---

## Core product (MVP)

1. **Couple setup (15 min)** — names, date, photo, 5 auto-generated prompts from a short form.
2. **Guest link** — one URL; works in WhatsApp in-app browser; no login (nickname only).
3. **Three modules only:**
   - **Live poll** — one question at a time, bar chart on couple’s phone (optional cast to TV).
   - **Photo challenge** — 3 tasks (e.g. “you + aso-ebi”, “oldest guest selfie”); auto gallery.
   - **Digital guestbook** — voice note, text, or photo; moderated queue.
4. **Couple dashboard** — downloads, guest count, export CSV for thank-you pipeline (`post-wedding-comms-pack/`).

**Phase 2 (only after validation):** multi-day timelines (traditional + white wedding), event-centre white-label, prize draw automation.

---

## Delivery & Nigeria constraints

- **WhatsApp-first:** link shared in family groups; no app store friction.
- **Lightweight PWA:** works on 3G; offline queue for submissions if hall Wi‑Fi fails.
- **QR at door:** event centre / registry-area standee → same guest link (foot-traffic wedge).
- **Payment:** Paystack/Flutterwave one-time; optional venue wholesale invoice.

---

## Revenue model

| Tier | Buyer | Price signal | Includes |
|------|-------|--------------|----------|
| **Guest Link Basic** | Couple | ₦25,000–₦40,000 | Polls + guestbook + export |
| **Guest Link Plus** | Couple | ₦50,000–₦75,000 | + photo challenges + gallery + pre-event week |
| **Venue Pack** | Event centre | ₦30,000–₦100,000/mo | White-label links, N events/mo, hall QR kit |

No subscription for couples unless post-launch retention proves demand.

---

## Validation (minimal, no big build)

1. **Landing page** — “Guest link for your wedding (not another MC quiz)” + waitlist.
2. **Wizard-of-Oz weekend** — Google Form + WhatsApp broadcast + manual gallery (Canva/Google Drive); charge 1–2 couples ₦15k–25k pilot.
3. **One event centre conversation** — would they put a QR on the door if you handle tech?
4. **Success metrics:** ≥40% of invited guests open link; ≥20% submit something; couple would recommend.

Kill criteria: couples say “MC already enough” **and** won’t pay even ₦15k.

---

## Costs (revised — PWA-first)

| Item | Low | High |
|------|-----|------|
| PWA + backend MVP | ₦400,000 | ₦1,200,000 |
| Design / QR kit for venues | ₦50,000 | ₦150,000 |
| Hosting (monthly) | ₦10,000 | ₦40,000 |

**Avoid Phase 1:** native apps (₦800k–3M), MC sales outreach, complex gamification economies.

---

## Fit with existing wedding work

| Asset | Integration |
|-------|-------------|
| `post-wedding-comms-pack/` | Guest CSV + messages feed post-wedding comms MVP |
| `wedding-photo-booth-business.md` | Photo challenges overlap — partner or merge later |
| `established-business-wedding-niche-analysis.md` | Marketplace can list “guest link” as add-on |
| Festival import matrix | Crowd app + second screen **for guests**, not MC SaaS |

---

## Summary

**Don’t sell games to MCs.** Sell a **guest participation link** to **couples** (memory + inclusion + export) and optionally **event centres** (amenity + foot traffic). Compete on **pre/post, async, and scale** — not on couple quizzes at the reception.
