# Strategy 3 — Paid Distributor Brief

Use this when paying someone with social capital to share the **I'll pay to..** survey.

**Survey (live):** https://mizza411.github.io/Inc/problem_identification_tool/web/index.html

---

## Who makes a good distributor?

- Someone you trust who knows operators, founders, or professionals
- Has an active WhatsApp group, LinkedIn network, or community channel
- Will share personally (not spam a massive list)

## Who should they share with?

**Good:** People with real, recurring business/work problems who would honestly say what they'd pay to fix.

**Avoid:** Random broadcast lists, incentive-only click farms, or people with no real problem to describe.

## What counts as a qualified response?

1. **Valid email** entered  
2. **Problem statement** — at least one clear sentence (not "N/A" or gibberish)  
3. **All required questions** answered seriously (urgency, payment preference, etc.)  
4. **Submitted via the distributor's unique link** (`ref=` in URL)

You decide payout; typical starting point: fixed fee per qualified response or a cap (e.g. first 10 qualified).

## How tracking works

Each distributor gets a unique link:

```
.../index.html?survey=ill_pay_to_v1&ref=jane_doe&utm_source=jane_doe&utm_medium=strategy3&utm_campaign=ill_pay_to
```

Responses saved in browser localStorage include the `ref` field. Phase B2 will wire the collector to count these; for now, export dashboard JSON and filter by `ref`.

## Commands (Phase B1)

From this folder:

```powershell
cd "C:\dev\Inc\Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification"

# Register a distributor + generate link
python distributor_links.py add --name "Jane Doe" --channel WhatsApp --payout "500 NGN per qualified response"

# List all distributors
python distributor_links.py list

# Generate outreach messages (fills templates)
python distributor_links.py outreach
```

Registry file: `distributor_registry.json` (local — not committed; see `distributor_registry.example.json`).

## Phases

| Phase | Status | Scope |
|-------|--------|--------|
| **B1** | Done | Link generator, templates, brief (this doc) |
| **B2** | Done | Optional `--distributor` mode in `network_problem_collector.py` |
| **B3** | Pending | Wire `sharing_utilities.py` ref/UTM with Strategy 3 |
