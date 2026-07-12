# Strategy 1: Business Variation & Complaint Fixing

## Overview

Turn **successful businesses + recurring complaints** into **differentiated variation** ideas.

**Formula:** `Successful Business + Recurring Complaint = Profitable Variation`

This is a **technical formulation strategy** (Phase 2 CLI). It is **not** Strategy 6 (niche combination) or Strategy 7 (trending adaptation).

Gadget ops under `gadget-business/gadget-business-automation/` are a **separate** established-business tool — not this formulation entrypoint.

## Files

| File | Purpose |
|------|---------|
| `strategy-1-business-variation.md` | Full playbook (human steps) |
| `chatgpt_prompt_1a.txt` | Prompt 1a (variation hooks) |
| `chatgpt_prompt_1b.txt` | Prompt 1b (tabulation; S1 lead + S5-wide columns) |
| `chatgpt_prompt_1c.txt` | Prompt 1c (optional hardware/ops appendix) |
| `seed_businesses.json` | Editable Nigeria-first seed businesses |
| `business_variation_collector.py` | Entrypoint (interactive + `--non-interactive`) |
| `seeds.py` / `complaint_intake.py` / `variation_prompts.py` | Modular helpers |
| `fixtures/sample_inputs.json` | Smoke fixture for non-interactive runs |

## Run

From repo root or this folder:

```bash
# Interactive
python Strategy-1-Business-Variation/business_variation_collector.py

# Non-interactive (agent / smoke) — inputs JSON
python Strategy-1-Business-Variation/business_variation_collector.py --non-interactive --inputs Strategy-1-Business-Variation/fixtures/sample_inputs.json

# Non-interactive — seed example complaints
python Strategy-1-Business-Variation/business_variation_collector.py --non-interactive --seed-ids jumia_food,bolt

# File check only
python Strategy-1-Business-Variation/business_variation_collector.py --check-only
```

Outputs (gitignored): `business_variation_YYYYMMDD_HHMMSS.json`, Prompt 1a payload, Prompt 1b scaffold.

```bash
python Strategy-1-Business-Variation/test_phase2_smoke.py
python Strategy-1-Business-Variation/test_phase3_runner_smoke.py
python Strategy-1-Business-Variation/test_phase4_agent_smoke.py
python Strategy-1-Business-Variation/test_phase6_regression.py
```

**Master runner:** Strategy 1 is registered in `run_all_strategies.py` (active set `1, 3–7, 9, 11–15`). Menu option 3 → `1` launches this script interactively; for agent/smoke use `--non-interactive` directly.

**Agent runs:** `prompts/agent_formulation_run.txt` includes Strategy 1; `agent-business-idea-runs/agent_strategy_run.py` writes `strategy_1_seeds` into fetch JSON.

**Inc Hub:** Formulated ideas → **Run Strategy 1 — Business Variation**. Established keeps **Strategy 1 folder** + **Gadget business automation** (ops only).

**Manual sign-off (once):** `MANUAL_TEST.md` — only Hub/menu/playbook steps not covered by automation.

## Requirements

Stdlib only for Phase 2.
