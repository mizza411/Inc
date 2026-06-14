# Post-Wedding Comms Pack — Manual test (run once at v1 sign-off)

**Do not run during incremental development.** The agent runs automated tests first (`python test_p0_flow.py`, etc.); only steps that **cannot** be automated live here.

**Automate-first policy:** [.cursor/rules/deferred-manual-testing.mdc](../../.cursor/rules/deferred-manual-testing.mdc) — manual items require a genuine automation attempt first.

**Run this file once when:** `task.md` §7 **v1 sign-off** milestone is reached:

| Milestone | Run these sections |
|-----------|-------------------|
| **v1.0 — soft launch** | §P0 only (after Phase 0b go) |
| **v1 — launch-ready** | §P0 + §P1 (after P1 Paystack shipped) |

See **v1 definition of done** in `.cursor/rules/task.md` §7.

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../../.cursor/rules/deferred-manual-testing.mdc)

---

## Before you start

### Agent/automated pre-check (should already be green)

```bash
cd Strategy-2-Problem-Solving/post-wedding-comms-pack
python test_p0_flow.py
```

Expected: `OK: guest + vendor CSV flow passed`

### Your prerequisites

- [ ] Python 3.11+ with deps: `pip install -r requirements.txt`
- [ ] Optional `.env` in this folder:
  - `OPENAI_API_KEY` — guest AI generate
  - `SENDGRID_API_KEY` + `SENDER_EMAIL` — diaspora email send
  - `OPENAI_MODEL` — optional (default `gpt-4o-mini`)
- [ ] P1 only (when built): Paystack test keys documented in README

### Start the app

```bash
cd Strategy-2-Problem-Solving/post-wedding-comms-pack
python -m streamlit run app.py
```

Open the Local URL shown (usually http://localhost:8501).

---

## P0 — Core UI (current build)

### A. Guests tab — sample upload

- [ ] Open **Guests** tab
- [ ] Upload `samples/guests_sample.csv`
- [ ] Confirm success toast and **3 guests** loaded
- [ ] Metrics show Total / Pending / Sent / Skipped

### B. Guests — AI generate (skip if no API key)

- [ ] Set **Sign-off names** in sidebar (e.g. `Ada & Emeka`)
- [ ] Click **Generate guest messages (AI)**
- [ ] Messages appear in expanders; gift/relationship context feels reasonable
- [ ] Edit one message; confirm it sticks after interacting with another expander

### C. Guests — checklist & export

- [ ] Change one guest **Status** to Sent, one to Skipped
- [ ] Filter by **Pending** — only pending rows show
- [ ] Download **export CSV** — open file; columns include `WhatsAppLink`
- [ ] First guest link starts with `https://wa.me/234` (not missing country code)
- [ ] Download **copy-paste text** — readable blocks per guest

### D. Guests — WhatsApp on phone (optional but recommended)

- [ ] Open one `wa.me` link on your phone
- [ ] WhatsApp opens with pre-filled message text

### E. Guests — legacy CSV (Name + Email only)

- [ ] Upload a tiny CSV: `Name,Email` / `Test User,test@example.com`
- [ ] App accepts it (Phone column empty)
- [ ] **Send email** button: only runs if SendGrid configured; otherwise clear error

### F. Vendors tab

- [ ] Upload `samples/vendors_sample.csv` — **2 vendors** load
- [ ] Click **Apply thank-you template to all** — messages populated
- [ ] Click **Apply review-request template to all** — review wording + link where present
- [ ] Download vendor export CSV and copy-paste text

---

## P1 — Monetization & send (add sections when built)

<!-- Agent: append checklist items here when Paystack / WhatsApp API ships -->

- [ ] _Not in build yet — skip until P1 complete_

---

## P2 — Integration (add sections when built)

- [ ] _Guest-link import — skip until P2_
- [ ] _PDF export — skip until P2_
- [ ] _Local language templates — skip until P2_

---

## Sign-off

| Area | Pass | Fail | Notes |
|------|------|------|-------|
| Guest upload & metrics | ☐ | ☐ | |
| AI messages (if tested) | ☐ | ☐ | |
| Status checklist & filter | ☐ | ☐ | |
| Export CSV / txt | ☐ | ☐ | |
| WhatsApp links (`234…`) | ☐ | ☐ | |
| Vendor templates & export | ☐ | ☐ | |
| P1 payment gate (if applicable) | ☐ | ☐ | |
| Overall v1 ready | ☐ | ☐ | |

**Tester:** _______________ **Date:** _______________

**Fail log (if any):**

```
```

---

## After pass

- Tick manual sign-off in `task.md` §7 if v1 criteria met
- Stage, commit, and push
- Phase 0b (real couples / WTP) is **business validation**, not this UI checklist
