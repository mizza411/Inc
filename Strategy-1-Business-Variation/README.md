# Strategy 1: Business Variation & Complaint Fixing

## Overview

Turn **successful businesses + recurring complaints** into **differentiated variation** ideas.

**Formula:** `Successful Business + Recurring Complaint = Profitable Variation`

This is a **technical formulation strategy**. It is **not** Strategy 6 (niche combination) or Strategy 7 (trending adaptation).

**Intake (task §11 Phase B):** Always **online / URL-cited** — each business needs a `success_url`; each complaint needs a `source_url` (http/https). `seed_businesses.json` is **retired** (archive only under `_archive/`).

Gadget ops under `gadget-business/gadget-business-automation/` are a **separate** established-business tool — not this formulation entrypoint.

## Files

| File | Purpose |
|------|---------|
| `strategy-1-business-variation.md` | Full playbook (human steps) |
| `chatgpt_prompt_1a.txt` | Prompt 1a (variation hooks) |
| `chatgpt_prompt_1b.txt` | Prompt 1b (tabulation; S1 lead + S5-wide columns) |
| `chatgpt_prompt_1c.txt` | Prompt 1c (optional hardware/ops appendix) |
| `_archive/seed_businesses.json` | Retired seed list (reference only) |
| `business_variation_collector.py` | Entrypoint (interactive + `--non-interactive`) |
| `complaint_intake.py` / `variation_prompts.py` / `seeds.py` | Intake (URL-cited); `seeds.py` raises if called |
| `fixtures/sample_inputs.json` | URL-cited smoke fixture |

## Run

From repo root or this folder:

```bash
# Interactive — paste business success URL + complaint source URLs
python Strategy-1-Business-Variation/business_variation_collector.py

# Non-interactive (agent / smoke) — URL-cited inputs JSON
python Strategy-1-Business-Variation/business_variation_collector.py --non-interactive --inputs Strategy-1-Business-Variation/fixtures/sample_inputs.json

# File check only
python Strategy-1-Business-Variation/business_variation_collector.py --check-only
```

`--seed-ids` / `--seeds` are **rejected** (clear error).

Outputs (gitignored): `business_variation_YYYYMMDD_HHMMSS.json`, Prompt 1a payload, Prompt 1b scaffold.

```bash
python Strategy-1-Business-Variation/test_phase2_smoke.py
python Strategy-1-Business-Variation/test_phase3_runner_smoke.py
python Strategy-1-Business-Variation/test_phase4_agent_smoke.py
python Strategy-1-Business-Variation/test_phase11_signoff.py
python Strategy-1-Business-Variation/test_signoff_automated.py
python Strategy-1-Business-Variation/test_phase6_regression.py
```

**Master runner:** Strategy 1 is registered in `run_all_strategies.py` (active set `1, 3–7, 9, 11–15`). For non-interactive/agent use `--inputs` (interactive Hub/menu still prompts for URLs).

**Agent runs:** `prompts/agent_formulation_run.txt` requires online discovery + citeable URLs. Fetch JSON includes **`strategy_1_discovery`** (agent web research + optional leads). `strategy_1_seeds` removed (Phase C). Optional: `agent_strategy_run.py --with-strategy1-run` uses the URL-cited fixture.

**Inc Hub:** Formulated ideas → **Run Strategy 1 — Business Variation**. Established keeps **Strategy 1 folder** + **Gadget business automation** (ops only).

**Manual sign-off:** None required for v1 — see `MANUAL_TEST.md`.

## Requirements

Stdlib only for collector intake (URL format validation; no paid scrapers).
