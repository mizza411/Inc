# Agent business-idea formulation runs

Dedicated home for **multi-strategy Cursor agent runs** (strategies **1**, 5, 6, 7, 9, 11–15; skip 2, 3, 4, 8, 10).

Per-strategy scripts stay in their folders (`Strategy-1-Business-Variation/`, `Business-Idea-Formulation-Strategy-*/`). This folder holds **inputs**, **outputs**, and the **shared fetch runner**.

## Layout

```
agent-business-idea-runs/
├── README.md                 ← this file
├── agent_strategy_run.py     ← RSS + OWID + S1 discovery + S6/S7 (S15 skipped by default)
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
| `strategy_1_discovery` | Agent-native web research guidance + optional `discovery_leads` from RSS / Product Hunt / StartupList (**not** proven complaints) |
| `strategy_1_run` | Optional collector subprocess; **skipped** unless `--with-strategy1-run` (URL-cited `--inputs`) |
| `strategy_5_9_rss` | News RSS |
| `strategy_6_startup_directory` | StartupList Africa snippet |
| `strategy_7_trending` | Product Hunt RSS |
| `strategy_12_run` | Optional GUEMF filter subprocess; **skipped** unless `--with-strategy12` (pre-scored `--inputs`; Mode B aid only) |
| `strategy_14_owid` | OurWorldInData snippets |
| `strategy_15_run` | Optional; skipped unless `--with-strategy15` |

**Removed (§11 Phase C):** `strategy_1_seeds` (no local seed snapshot).

Failures on any block are logged inside that key and **do not** abort the fetch.

Optional Strategy 1 collector run:

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy1-run
```

Optional Strategy 15 subprocess (may hang on clipboard prompts):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy15
```

Optional Strategy 12 GUEMF non-interactive (Mode B aid; does **not** replace Mode A synthesis):

```powershell
python agent-business-idea-runs/agent_strategy_run.py --with-strategy12
```

Explicit fetch-only:

```powershell
python agent-business-idea-runs/agent_strategy_run.py --fetch-only
```

## Strategy 1 (agent synthesis) — always online

- **Formula:** Successful Business + Recurring Complaint = Profitable Variation
- **Not** Strategy 6 (niche combination) or Strategy 7 (trending adaptation)
- **Primary:** agent-native web research (`strategy_1_discovery.primary`)
- **Optional leads:** `discovery_leads` from this fetch — starting points only; verify online and cite URLs
- **Citations required** on every S1-traced idea: source name, title/quote, **URL**, date when available
- **Forbidden:** archived `seed_businesses.json`, removed `strategy_1_seeds`, canned `example_complaints`, AI-invented gaps without URLs
- **CLI:** `--non-interactive --inputs` with `success_url` + `source_url`
- If online discovery fails: mark **blocked** / **synthesized** with missing-citation note — continue the run
- Execution summary status values: `ran` / `synthesized` / `skipped` / `blocked`

## Strategy 12 (GUEMF) — dual-mode required

Contract: `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/README.md` (Mode A + Mode B). Backlog: `task.md` §13.

| Mode | Required in agent runs? | What to produce |
|------|-------------------------|-----------------|
| **A — Standalone** | **Yes** | Prompt-1a-style GUEMF problem discovery → Nigeria ideas with **primary / S12** strategy trace (same ranked table) |
| **B — Overlay** | **Yes** | GUEMF **1–5** per criterion + composite (max 25) on ideas from **other** strategies |

- Incomplete S12 = Mode B table columns only (historical “Applied in ranked table” anti-pattern).
- Execution summary must note **both** Mode A and Mode B legs.
- Optional CLI aid (does not replace Mode A synthesis):  
  `python Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/problem_filter.py --non-interactive --inputs …`  
  (complete `criteria_scores` required; see strategy `fixtures/INPUTS_SCHEMA.md`). Soft-fail / timeout → agent synthesizes.
- Optional fetch key: `strategy_12_run` via `agent_strategy_run.py --with-strategy12` (default **skipped**; Mode B aid only).

Prompt: `prompts/agent_formulation_run.txt`

## Agent output path

New formulation runs should write:

- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md`
- `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.docx`

## Dedup sources (unchanged)

- `past_business_ideas.md` (repo root)
- `agent-business-idea-runs/outputs/business_ideas_*.md`
- Strategy-folder `past_business_ideas.md` and strategy-local `business_ideas_*.md`
