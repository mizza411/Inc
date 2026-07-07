# Agent business-idea formulation runs

Dedicated home for **multi-strategy Cursor agent runs** (strategies 5, 6, 7, 9, 11–15; skip 3, 4, 8, 10).

Per-strategy scripts stay in `Business-Idea-Formulation-Strategy-*/`. This folder holds **inputs**, **outputs**, and the **shared fetch runner**.

## Layout

```
agent-business-idea-runs/
├── README.md                 ← this file
├── agent_strategy_run.py     ← RSS + OWID fetch (Strategy 15 skipped by default)
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

Optional Strategy 15 subprocess (may hang on clipboard prompts):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy15
```

Explicit fetch-only (same as default—skips Strategy 15):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --fetch-only
```

## Agent output path

New formulation runs should write:

- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md`
- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.docx`

Prompt: `prompts/agent_formulation_run.txt`

## Dedup sources (unchanged)

- `past_business_ideas.md` (repo root)
- `agent-business-idea-runs/outputs/business_ideas_*.md`
- Strategy-folder `past_business_ideas.md` and strategy-local `business_ideas_*.md`
