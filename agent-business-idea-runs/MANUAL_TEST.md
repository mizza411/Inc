# MANUAL_TEST — agent-business-idea-runs (formulation pack / schema)

Automate-first for **task.md §14** (Phases 0–5). No remaining user manual steps for packaging v1.

| Check | Automated command |
|-------|-------------------|
| Pack + Discover prompt markers | `python -m pytest agent-business-idea-runs/tests/test_formulation_pack_prompt.py -q` |
| Idea-card schema | `python -m pytest agent-business-idea-runs/tests/test_idea_card_schema.py -q` |
| CLI validator | `python agent-business-idea-runs/idea_card_schema.py agent-business-idea-runs/fixtures/idea_cards_good.md` (expect exit 0) |
| §13 Discover dual-mode | `python -m pytest Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/test_strategy12_prompt_dual_mode.py -q` |
| Hub Pass 1+2 cards | `python -m pytest inc_launcher/tests/test_config.py inc_launcher/tests/test_agent_run.py -q` |
| Phase 5 modal (needs working Tk) | `python -m pytest inc_launcher/tests/test_phase5_signoff.py -q -k "not tray_restart"` |

**§14 Phase 5 proof (2026-07-15):** Pass 2 packed `outputs/business_ideas_20260715.md` → `idea_card_schema.py` **PASS (12 ideas)** → one-shot Docx OK.

**Hub:** Formulated **Agent formulation run** (Pass 1, pinned) + **Agent formulation pack (Pass 2)**.

**Why not automated:** Cursor chat **Enter** to send (same deferred Hub §G).
