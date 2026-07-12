# Agent business-idea formulation runs

Dedicated home for **multi-strategy Cursor agent runs** (strategies **1**, 5, 6, 7, 9, 11–15; skip 2, 3, 4, 8, 10).

Per-strategy scripts stay in their folders (`Strategy-1-Business-Variation/`, `Business-Idea-Formulation-Strategy-*/`). This folder holds **inputs**, **outputs**, and the **shared fetch runner**.

## Layout

```
agent-business-idea-runs/
├── README.md                 ← this file
├── agent_strategy_run.py     ← RSS + OWID + S1 seeds + S6/S7 (S15 skipped by default)
├── inputs/
│   └── agent_strategy_inputs_YYYYMMDD_HHMMSS.json
└── outputs/
    ├── business_ideas_YYYYMMDD.md
    └── business_ideas_YYYYMMDD.docx
```

## Run fetch (from repo root)

```powershell
$env:PYTHONIOENCODING='utf-8'
python agent-business-idea-runs/agent_strategy_run.py
```

Fetch JSON always includes (when available):

| Key | Content |
|-----|---------|
| `strategy_1_seeds` | Local `Strategy-1-Business-Variation/seed_businesses.json` snapshot (no network) |
| `strategy_1_run` | Optional collector subprocess; **skipped** unless `--with-strategy1-run` |
| `strategy_5_9_rss` | News RSS |
| `strategy_6_startup_directory` | StartupList Africa snippet |
| `strategy_7_trending` | Product Hunt RSS |
| `strategy_14_owid` | OurWorldInData snippets |
| `strategy_15_run` | Optional; skipped unless `--with-strategy15` |

Failures on any block are logged inside that key and **do not** abort the fetch.

Optional Strategy 1 collector run:

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy1-run
```

Optional Strategy 15 subprocess (may hang on clipboard prompts):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy15
```

Explicit fetch-only (skips Strategy 15 subprocess; S1 seeds still included):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --fetch-only
```

## Strategy 1 (agent synthesis)

- **Formula:** Successful Business + Recurring Complaint = Profitable Variation
- **Not** Strategy 6 (niche combination) or Strategy 7 (trending adaptation)
- Prefer `strategy_1_seeds` from fetch JSON; if missing/empty, synthesize and mark execution status **synthesized**
- Execution summary status values: `ran` / `synthesized` / `skipped` / `blocked`

## Agent output path

New formulation runs should write:

- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md`
- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.docx`

Prompt: `prompts/agent_formulation_run.txt`

## Dedup sources (unchanged)

- `past_business_ideas.md` (repo root)
- `agent-business-idea-runs/outputs/business_ideas_*.md`
- Strategy-folder `past_business_ideas.md` and strategy-local `business_ideas_*.md`
