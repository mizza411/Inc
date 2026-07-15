# Strategy 12 `--inputs` JSON schema (Phase 1)

Used with:

```bash
python problem_filter.py --non-interactive --inputs fixtures/sample_inputs.json
```

## Shapes accepted

1. Object with `problems` array (preferred), or  
2. Bare JSON array of problem objects.

## Problem object

| Field | Required | Description |
|-------|----------|-------------|
| `description` | **yes** | Non-empty string |
| `source` | no | Tag (e.g. `S5-News`) |
| `criteria_scores` | **yes** in non-interactive | All five GUEMF keys (or aliases) with **0/1** (or Y/N / true/false). **Missing keys → error** (no invented scores). Agent-style 1–5 values map: `>=4` → 1, else → 0 if not already 0/1. |

### Criteria keys (canonical)

- `Growing`
- `Urgent`
- `Expensive to Solve`
- `Mandatory`
- `Frequent`

Aliases also accepted: `g`/`u`/`e`/`m`/`f`, lowercase names, `expensive` → Expensive to Solve.

## Top-level optional fields

| Field | Description |
|-------|-------------|
| `select_min_score` | Default **4**. Auto-select original indices with `total_score >=` this for Prompt 1b file generation. |
| `selected_indices` | Optional 0-based indices overriding auto-select. |
| `strategy` | Documentation only (`12`). |

## Outputs

- Summary JSON: `high_value_problem_filtering_YYYYMMDD_HHMMSS.json` (or `--output`)
- If any problems selected: `chatgpt_strategy12_prompts.txt`
- Non-interactive never calls `input()` and does **not** auto-open files unless `--open` is passed.
