# Technical intuition log

## 2026-06-14 — Post-Wedding Comms Pack P0 (modular Streamlit MVP)

**What we did**
- Split `post-wedding-comms-pack/` into small modules: `csv_schema`, `prompts`, `generation`, `whatsapp_export`, `email_send`; thin `app.py` UI only.
- P0 features: Chat Completions (not legacy davinci), guest Phone/gift/relationship CSV, vendor templates, Pending/Sent/Skipped checklist, WhatsApp link export CSV/txt; optional SendGrid kept for diaspora.
- Updated README, strategy doc, and `task.md` Phase 1 (P0) — no changes outside this folder except those docs.

**Why it matters**
- Post-wedding comms is the lowest-stress wedding wedge (no event-day ops). Modular files keep future Paystack/WhatsApp API work isolated so P1 does not rewrite the UI.

**Intuition analogy**
- Like Mailchimp’s post-purchase “thank you” sequence, but scoped to one Nigerian wedding batch and exported through WhatsApp instead of a mailing list.
