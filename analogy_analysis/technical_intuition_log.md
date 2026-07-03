# Technical Intuition Log

## 2026-07-03 — Strategy 3 Phase B3: sharing_utilities ref/UTM wiring

**What we did**
- Extended `sharing_utilities.py` with `build_tracked_survey_url`, `create_distributor_url`, and `generate_strategy3_distributor_kit`.
- Added CLI flags `--distributor-ref` and `--strategy3-kit`; Strategy 3 `distributor_links.py sharing-kit` subcommand.
- `network_problem_collector.py --distributor` optionally saves a per-distributor social sharing kit.

**Why it matters**
Distributors get WhatsApp/LinkedIn-ready links from one registry; survey ref tracking stays consistent across tools.

**Intuition analogy**
Like connecting your affiliate dashboard to the same promo codes the checkout already reads — one attribution scheme, many share surfaces.

---

## 2026-07-03 — Strategy 3 Phase B2: optional distributor mode in collector

**What we did**
- Extended `network_problem_collector.py` with `--distributor` flag; classic `python network_problem_collector.py` unchanged.
- Integrated `DistributorLinkManager` for register → outreach → optional export sync → problem capture.
- Added `count_responses_by_ref`, export loader, and `test_network_problem_collector.py` (6 tests).

**Why it matters**
One CLI entry point now covers both classic network outreach and paid survey distribution without breaking the original workflow.

**Intuition analogy**
Like adding a "promoter mode" toggle to an existing CRM — same tool, different pipeline, default behavior untouched.

---

## 2026-07-03 — Strategy 3 Phase B1: paid distributor links (no collector changes)

**What we did**
- Added `distributor_links.py` in Strategy 3 folder — unique `ref`/UTM URLs for `ill_pay_to_v1`, local registry, outreach message generation.
- Added `distributor_brief.md`, `distributor_message_templates.txt`, example registry, and `test_distributor_links.py`.
- Left `network_problem_collector.py`, `sharing_utilities.py`, and live survey untouched (B2/B3 deferred).

**Why it matters**
Paid distribution can start immediately with tracked links and copy-paste outreach, without risking the live survey or the existing Strategy 3 CLI flow.

**Intuition analogy**
Like giving each promoter a unique discount code before rebuilding the whole checkout — attribution works on day one; deeper integration comes later.

---

## 2026-07-02 — “I'll pay to..” survey (Phase A) in Problem Identification Tool

**What we did**
- Added `ill_pay_to_v1` questionnaire (WTP, urgency, payment model, email) to both `web/data/` and `data/questionnaires.json`.
- Extended `questionnaire.js` with `email`/`short_text` types, `show_if` branching (2 rules), `?survey=` URL override, and `ref` capture on save.
- Kept `general_problems_v1` intact; dashboard reads both survey shapes without breaking older responses.

**Why it matters**
Strategy 3 can now share one flexible hosted survey instead of Google Forms, with conditional pricing questions and per-distributor tracking hooks—without forking the whole app.

**Intuition analogy**
Like swapping a paper comment card for a Typeform-style flow on your own domain: same questions as the Google Form, but you control branching, branding, and who gets credit for each reply.

---

## 2026-06-27 — Agent-orchestrated business idea formulation run

**What we did**
- Ran Strategies 4–7, 9, 11–15 without the interactive master runner (blocked on `input()` prompts).
- Pulled live Nairametrics/BusinessDay RSS headlines, World Bank Nigeria indicators, and OWID internet trend CSV.
- Applied each strategy’s prompt logic (news problems, niche combos, trending startup adaptation, personal problems from repo docs, GUEMF filter).
- Wrote consolidated output to `business_ideas_agent_run_20260627.md`.

**Why it matters**
The strategy scripts are designed for human-in-the-loop CLI sessions; an agent can substitute for ChatGPT Vision/manual paste steps by fetching public feeds and APIs, then producing the same Prompt 1a→1b idea hooks—except where sites block bots (Cloudflare on full articles).

**Intuition analogy**
Like running a Bloomberg terminal scrape plus a focus group in one pass: each “strategy” is a different lens on the same market, and the agent is the analyst who runs all lenses before the investment committee picks three names.
