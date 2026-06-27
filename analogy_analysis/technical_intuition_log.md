# Technical intuition log

## 2026-06-27 — Strategy 10 (ChatGPT Vision) retirement

**What we did**
- Removed Strategy 10 from `run_all_strategies.py` active scripts; added to `RETIRED_STRATEGIES` alongside Strategy 8.
- Archived `visual_content_analyzer_legacy.py`; stubbed `visual_content_analyzer.py`; added `DEPRECATED.md` and deprecated banners in README/playbook.
- Updated API docs, `run_all_strategies_README.md`, and `task.md` §7; added `_smoke_test_strategy10_retirement.py`.

**Why it matters**
- Manual ChatGPT Vision upload/paste did not meet the repo's automate-first policy; retiring keeps numbering stable while pointing users to Strategies 3–5 for real-estate/construction problem discovery.

**Intuition analogy**
- Like removing a fax-only intake desk from a digital clinic — the workflow still exists in the archive, but the front door now routes to channels that actually run on autopilot.

## 2026-06-14 — Post-Wedding Comms Pack P1 (Paystack)

**What we did**
- Added `paystack_client.py`, `payment_store.py`, `unlock.py`, `payment_ui.py`, `webhook_server.py`; gated AI/export/email behind one-time unlock.
- Automated: `test_paystack.py` (9 tests, mocked Paystack API + webhook). Dev mode: `PAYMENTS_DISABLED=1`.
- Updated MANUAL_TEST §P1 with “why not automated” for live Paystack only.

**Why it matters**
- v1 monetization without WhatsApp API; webhook + verify-reference covers Streamlit’s lack of native payment callbacks.

**Intuition analogy**
- Like Gumroad’s paywall on a download link — pay once, then the tool unlocks; webhook is the receipt filing cabinet.

## 2026-06-14 — Post-Wedding Comms Pack P0 (modular Streamlit MVP)

**What we did**
- Split `post-wedding-comms-pack/` into small modules: `csv_schema`, `prompts`, `generation`, `whatsapp_export`, `email_send`; thin `app.py` UI only.
- P0 features: Chat Completions (not legacy davinci), guest Phone/gift/relationship CSV, vendor templates, Pending/Sent/Skipped checklist, WhatsApp link export CSV/txt; optional SendGrid kept for diaspora.
- Updated README, strategy doc, and `task.md` Phase 1 (P0) — no changes outside this folder except those docs.

**Why it matters**
- Post-wedding comms is the lowest-stress wedding wedge (no event-day ops). Modular files keep future Paystack/WhatsApp API work isolated so P1 does not rewrite the UI.

**Intuition analogy**
- Like Mailchimp’s post-purchase “thank you” sequence, but scoped to one Nigerian wedding batch and exported through WhatsApp instead of a mailing list.
