# Cloud formulation Automations (task.md §19)

Docs-only guide for **Cursor Automations** that run Pass 1 / Pass 2 unattended.  
Does **not** replace Hub clipboard Start (manual override). Does **not** change strategy CLIs.

**Authoritative backlog:** `.cursor/rules/task.md` → Current Priority **§19** + Notes **§19**.  
**Card contract:** `FORMULATION_PASS_CONTRACT.md` (§14).  
**Phase 0 locks (2026-07-23):** Pass 1 **07:00** WAT · Pass 2 **11:00** WAT · open **PR** (owner merges) · **Cursor cloud** · **Docx in-repo only** · fetch prep = Phase 4.

---

## What to create (later phases — not this file’s job)

| Automation | Cron (WAT) | Prompt source | Must produce | Must not |
|------------|------------|---------------|--------------|----------|
| **A — Discover** | Daily **07:00** | `agent_formulation_run.txt` | `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` with `_PENDING_PASS_2_PACK_` | Pack cards; Docx; start Pass 2 |
| **B — Pack** | Daily **11:00** | `agent_formulation_pack.txt` + this contract | Same dated `.md` packed + `.docx` beside it | Invent/re-rank; new idea set; open Word on desktop |

**Soft gate (B):** If today’s draft is missing or not pending Pass 2 → **no-op** (exit cleanly). Do not invent content to fill the gap.

**Git (locked):** Open PR from branch like `formulation/auto-YYYYMMDD` → default branch. **Do not** push straight to `main`/`master`.

---

## Write / read scope (anti-break)

- **Write:** under `agent-business-idea-runs/` only (outputs + agreed PR).
- **Read-only:** strategy folders, `run_all_strategies.py`, Inc Hub launcher behavior.
- **Preserve:** §11 S1 online cites; §13 S12 Mode A (≥2 primary) + Mode B; §14 subheads on every packed idea.
- **Hub:** leave `agent_formulation_run` + `agent_formulation_pack` cards as manual override — do not delete or fuse.
- **Tray schedules:** do not hijack `daily_task_md` / `daily_inc_hub` / `problem_id_live_mwf` for this work.
- **Encoding:** prefer UTF-8; on any Windows-local helper, `PYTHONIOENCODING=utf-8`.

---

## Suggested Automation instruction spines

Copy intent (not a mega-prompt merge). Prefer pointing the cloud agent at the files below rather than pasting the whole prompt body into the Automation UI when the repo checkout is available.

### Run 1 of 2 (Automation A)

```
Inc formulation — AUTOMATION A (Pass 1 Discover only).
Follow prompts/agent_formulation_run.txt and prompts/FORMULATION_PASS_CONTRACT.md.
Write agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md (today’s date).
Do NOT pack cards. Do NOT convert/open Docx. Leave _PENDING_PASS_2_PACK_.
Stop when the draft .md is complete. Do not start Pass 2.
Read-only on strategy scripts; write under agent-business-idea-runs/ only.
Open a PR (formulation/auto-YYYYMMDD); do not push directly to main.
```

### Run 2 of 2 (Automation B)

```
Inc formulation — AUTOMATION B (Pass 2 Pack).
If today’s agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md is missing
or not pending Pass 2, stop with a short no-op note — do not invent ideas.
Otherwise follow prompts/agent_formulation_pack.txt on that same file.
Normalize every idea to §14 subheads (Regulatory + Competitors / alternatives on every idea).
Optional: python agent-business-idea-runs/idea_card_schema.py <that .md> — fix gaps before Word.
Then one-shot Docx convert in-repo only (do not open desktop Word).
Do not invent a new ranked set. Contract: prompts/FORMULATION_PASS_CONTRACT.md.
Open/update PR per Phase 0 git policy.
```

---

## Inventory (must exist on the Automation checkout branch)

| Path | Role |
|------|------|
| `prompts/agent_formulation_run.txt` | Pass 1 |
| `prompts/agent_formulation_pack.txt` | Pass 2 |
| `prompts/FORMULATION_PASS_CONTRACT.md` | Contract |
| `agent-business-idea-runs/idea_card_schema.py` | Optional schema before Docx |
| `prompts/CLOUD_FORMULATION_AUTOMATIONS.md` | This note |

Cloud agents only see **committed remote** files. Commit this note + any prompt edits before enabling Automations (Phase 2+).

---

## Rollback

If a run misbehaves: **pause/disable** the Automation in Cursor. Do not delete Hub cards or prompt files to “fix” a bad run.
