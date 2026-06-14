# Post-Wedding Comms Pack (Repositioned)
## WhatsApp-first gratitude + vendor wrap-up for couples — not planner/MC SaaS

**Status:** Strategy one-pager (Jun 2026)  
**Folder / MVP:** `post-wedding-comms-pack/`  
**Previous angle:** “Automated thank-you note generator” (email-first, planner white-label) — **retired** for Nigeria GTM.

---

## One-line pitch

A **one-time post-wedding dashboard** where couples upload a guest/vendor list, get **AI-drafted WhatsApp messages** (gift- and relationship-aware), review in bulk, and send or export — plus **vendor thank-yous and review requests** — without chasing 200 people manually.

---

## What we are / are not

| We are | We are not |
|--------|------------|
| **Post-event comms automation** (festival “thanks for coming + survey” layer) | Live reception entertainment (MC territory) |
| WhatsApp-first; email for diaspora only | Email-only thank-you tool |
| Guest gratitude + vendor wrap-up checklist | Generic bulk SMS blaster |
| Couple pays once per wedding | MC or planner subscription product |
| Import from CSV or guest-engagement export | Full wedding planning suite |

**Festival import:** After the main stage, organizers run email lists, fan surveys, and merch follow-ups. Nigerian weddings need the same **operational tail** — gratitude, vendor closure, reviews — not another mic moment.

---

## Who pays (explicit)

### Primary — **Couples (B2C)**
- One-time fee **1–8 weeks after** the wedding (e.g. ₦15,000–₦50,000).
- Sold when guilt peaks: Instagram “newlywed” content, church WhatsApp groups, friend referrals.
- **Why couples pay:** 150+ guests, spray/gift guilt, procrastination, fear of forgetting aunties.

### Optional channel — **Print shops (affiliate)**
- Export printable PDF/card layouts → local printer fulfills physical cards.
- You stay digital; no print ops.

### Not in scope — **MCs, planners (as buyers)**
- Planners/MCs may **refer**; they are not the customer (same rule as guest engagement product).
- No white-label planner SaaS in Phase 1.

---

## Problem (Nigeria-specific)

| Pain | Detail |
|------|--------|
| Volume | 100–400 guests across traditional, court, reception |
| Gift-linked thanks | Spray, envelopes, transfers — messages must reference amount/gift |
| Channel | **WhatsApp** reaches aunties; email does not |
| Vendor loose ends | Final payments, thank-yous, Google/Instagram reviews never sent |
| Timing | Couples are exhausted; task slips 2–12 weeks |
| ChatGPT gap | Drafts one note at a time; no bulk tracking or send |

Validated globally: ~80% of couples report post-wedding comms stress ([The Knot Real Weddings Study](https://www.theknot.com/content/real-weddings-study)).

---

## Product modules (MVP)

### 1. Guest gratitude
- CSV columns: `Name`, `Phone`, `GiftOrSpray`, `Relationship`, `EventAttended` (optional)
- AI drafts per guest (English + optional Yoruba/Igbo/Hausa/Pidgin template)
- Bulk review screen → schedule or copy-to-WhatsApp / WhatsApp Business API send
- Dashboard: sent / pending / skipped

### 2. Vendor wrap-up
- Separate list: photographer, caterer, hall, MC (as **recipient**, not buyer)
- Templates: final thank-you, payment confirmation, review link (Google/Instagram)
- Checklist — couple ticks off as done

### 3. Import / handoff
- Manual CSV upload (Phase 1)
- Export from `wedding-games-icebreakers-app.md` guest link (Phase 2)

**Phase 2 only:** physical mail partners, subscription plans, automated drip sequences.

---

## Delivery & Nigeria constraints

- **WhatsApp-first:** primary send path; SMS fallback; email for diaspora with addresses
- **Copy-paste mode (Phase 1):** generate messages + deep links — couple sends from personal WhatsApp if API costs bite
- **WhatsApp Business API (Phase 1b):** after validation, via Twilio or local BSP
- **Payment:** Paystack/Flutterwave one-time unlock per wedding
- **Privacy:** NDPR-aware; guest data deleted after N days (configurable)
- **Human in the loop:** always review before send — no fully autonomous blast

---

## Revenue model

| Tier | Buyer | Price signal | Includes |
|------|-------|--------------|----------|
| **Comms Basic** | Couple | ₦15,000–₦25,000 | Guest messages + export/copy (up to 100 recipients) |
| **Comms Plus** | Couple | ₦30,000–₦50,000 | + vendor module + gift merge + local language templates |
| **Print export add-on** | Couple | ₦5,000–₦10,000 | PDF card layout for printer affiliate |

No couple subscription unless repeat events (corporate/baby shower expansion later).

---

## Competition

| Alternative | Weakness vs us |
|-------------|----------------|
| ChatGPT manual | No bulk tracking, no gift fields, no send |
| Canva | Design only |
| Wedding planner (manual) | Expensive, not scalable |
| Generic SMS tools | No wedding tone or gift merge |
| MCs | **Do not do post-event thank-yous** |

**Moat:** Nigeria templates + gift/spray fields + WhatsApp workflow + checklist + guest-list import from engagement product.

---

## Validation (minimal)

1. **Landing page** — “Post-wedding WhatsApp thank-yous in one afternoon”
2. **Wizard-of-Oz** — 3 couples, CSV with phone + gift, you generate + they send; charge ₦10k–20k
3. **Success metrics:** ≥70% complete list; couple would pay ₦25k for self-serve; ≥1 referral
4. **Kill criteria:** “We only thank in person” + zero willingness to pay

---

## MVP code status

| Built (`app.py`) | Not built |
|------------------|-----------|
| Streamlit UI (Guests + Vendors tabs) | Paystack unlock |
| CSV Name + Phone (+ gift/relationship) | WhatsApp Business API auto-send |
| OpenAI Chat Completions | Guest-link import |
| Copy-to-WhatsApp export (CSV + txt) | Local language template picker |
| Vendor templates + checklist statuses | Printable PDF export |
| Optional SendGrid email (legacy/diaspora) | |

See `post-wedding-comms-pack/README.md` for dev next steps.

---

## Fit with wedding stack

| Asset | Integration |
|-------|-------------|
| `wedding-games-icebreakers-app.md` | Guest link export → comms import (post-event tail) |
| `established-business-wedding-niche-analysis.md` | Marketplace can list vendors for review links |
| `wedding-photo-booth-business.md` | Photographer affiliate for review upsell |

**Priority vs gamification:** Ship **post-event comms first** — clearer pain, no MC overlap, coded MVP already exists.

---

## Summary

**Don’t sell “AI thank-you notes.”** Sell **post-wedding comms done** — WhatsApp gratitude with gift context, vendor wrap-up, and a checklist — **paid once by the couple**, no planner/MC B2B.
