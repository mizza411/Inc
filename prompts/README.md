# prompts/

Canonical Cursor agent prompts for Inc Hub workflows.

## Formulation (task.md §14 — Pass 1 / Pass 2)

| Pass | File | When to paste | Owns |
|------|------|---------------|------|
| **1 — Discover** | `agent_formulation_run.txt` | First | Strategies, invent, score, dedup, rank, Best ideas, execution summary. Hub Phase 5 **Agent formulation run** (pinned) loads this file. |
| **2 — Pack** | `agent_formulation_pack.txt` | Second (same dated `.md`) | Fixed idea-card subheads (**Regulatory**, **Competitors / alternatives**, …) then Docx **once**. Hub card: **Agent formulation pack (Pass 2)**. |

**Run order:** Pass 1 → draft `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` → Pass 2 → packed `.md` → one-shot `.docx`.

**Contract (required reading before editing):** `FORMULATION_PASS_CONTRACT.md`

**Cloud Automations (task.md §19 — daily unattended Pass 1→2):** `CLOUD_FORMULATION_AUTOMATIONS.md`  
(Hub clipboard Start remains the **manual override**; do not fuse Pass 1+2.)

**Note:** After §14 Phase 2, Discover no longer owns Docx convert/open—always finish with Pass 2 when you need uniform cards + Word.

- Edit prompts **here** — do not hardcode wording in launcher Python.
- Discover includes Strategy **12 GUEMF dual-mode** (Mode A + Mode B) per `task.md` §13.

## Other

- **`abuja_area_opportunity_scan.txt`** — agent-only Abuja corridor/area opportunity scan (no app build; paste into Cursor chat to run). Not wired to Inc Hub yet.

Agent run outputs live in **`agent-business-idea-runs/outputs/`** (see `agent-business-idea-runs/README.md`). Area-scan runs write `abuja_area_opportunities_YYYYMMDD.md` there.
