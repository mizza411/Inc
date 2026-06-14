# Post-Wedding Comms Pack — MVP

WhatsApp-first post-wedding gratitude and vendor wrap-up for Nigerian couples.  
**Strategy one-pager:** [`../post-wedding-comms-pack.md`](../post-wedding-comms-pack.md)

---

## Problem (validated)

Couples delay thank-yous for weeks; guest lists are large; messages should reference **gifts/spray**; **WhatsApp** beats email for local family. Vendors rarely get formal thanks or review links.

Sources: [The Knot Real Weddings Study](https://www.theknot.com/content/real-weddings-study), [WeddingWire thank-you guide](https://www.weddingwire.com/wedding-ideas/how-to-write-wedding-thank-you-cards), [r/weddingplanning](https://www.reddit.com/r/weddingplanning/comments/8w7k2d/how_do_you_handle_thank_you_notes/).

---

## Product scope (repositioned Jun 2026)

| Module | Phase 1 | Phase 2 |
|--------|---------|---------|
| Guest thank-yous (AI + review) | ✓ | |
| Gift/spray merge fields | ✓ | |
| WhatsApp copy-export | ✓ | |
| WhatsApp Business API send | | ✓ |
| Vendor thank-you + review links | ✓ | |
| Progress checklist | ✓ | |
| Email (diaspora only) | ✓ | |
| CSV import | ✓ | |
| Guest-link import | | ✓ |
| Printable PDF (print-shop affiliate) | | ✓ |

**Out of scope:** MC/planner subscriptions, live event features.

---

## Who pays

- **Couple (B2C)** — **₦10,000 flat** per wedding (self-serve via Paystack)
- **Print shop** — affiliate only, optional  

---

## Current MVP (`app.py`)

Streamlit app with **Guests** and **Vendors** tabs:

1. Upload CSV (guest: Name + Phone; legacy Name + Email supported)
2. Generate guest messages via OpenAI Chat Completions (or apply vendor templates)
3. Review/edit; set status Pending / Sent / Skipped
4. Export CSV with WhatsApp links or copy-paste text
5. Optional: SendGrid email for rows with Email (diaspora)

**Modules:** `csv_schema.py`, `prompts.py`, `generation.py`, `whatsapp_export.py`, `email_send.py`, `paystack_client.py`, `payment_ui.py`, `webhook_server.py`
**Run locally:**

```bash
cd Strategy-2-Problem-Solving/post-wedding-comms-pack
pip install -r requirements.txt
# .env: OPENAI_API_KEY (optional: SENDGRID_API_KEY, SENDER_EMAIL, OPENAI_MODEL)
python -m streamlit run app.py
```

**Sample CSVs:** `samples/guests_sample.csv`, `samples/vendors_sample.csv`  
**Automated tests:** `python test_p0_flow.py` · `python -m unittest test_paystack.py`  
**Manual UI (once at v1 sign-off):** [`MANUAL_TEST.md`](MANUAL_TEST.md)  
**Phase 0b validation copy:** [`PHASE_0b_PITCH.md`](PHASE_0b_PITCH.md)

Copy `.env.example` → `.env`. Default `PAYMENTS_DISABLED=1` unlocks all features for dev.

**Webhook server (separate process):**

```bash
python webhook_server.py
```

---

## Dev roadmap (align to strategy)

### P0 — Nigeria-usable MVP
- [x] Replace `text-davinci-003` with Chat Completions API
- [x] CSV schema: `Name`, `Phone`, `GiftOrSpray`, `Relationship`, `Email` (optional)
- [x] Prompt templates with gift/relationship context
- [x] “Copy to WhatsApp” batch export (no API cost)
- [x] Vendor list + separate templates (thank-you, review request)
- [x] Checklist UI: pending / sent / skipped

### P1 — Monetization (Paystack)
- [x] Paystack one-time unlock per wedding (sidebar pay + verify reference)
- [x] Paystack webhook + optional basic auth (`webhook_server.py`)
- [ ] (Optional v1.x) WhatsApp Business API or local BSP integration

### P2 — Stack integration
- [ ] Import from guest engagement export
- [ ] Printable PDF export for print affiliates
- [ ] English + Yoruba/Igbo/Hausa/Pidgin template picker

---

## Validation before P1

Wizard-of-Oz with 3 couples: test **₦10k self-serve** willingness-to-pay; optional **₦15k done-for-you** pilot. Proceed to public launch only if ≥2 say yes to ₦10k app.

---

## Tech stack (target)

| Layer | Choice |
|-------|--------|
| UI | Streamlit (MVP) → simple web app later |
| AI | OpenAI Chat Completions |
| Email | SendGrid (diaspora) |
| WhatsApp | Copy-export → Twilio/BSP |
| Payments | Paystack |
| Hosting | Netlify/Railway or similar |

---

## Privacy

- Guest/vendor PII only for message generation and send
- Auto-delete event data after 90 days (configurable)
- [NDPR](https://ndpr.nitda.gov.ng/) — consent checkbox at upload

---

## Related docs

- Guest engagement (pre/day-of): `../wedding-games-icebreakers-app.md`
- Wedding niche analysis: `../established-business-wedding-niche-analysis.md`
