# Formulation Pass 1 / Pass 2 — Contract, inventory & acceptance

Docs-only artifact for **task.md §14 Phase 0** (2026-07-15).  
**No runtime behavior changes** in Phase 0: do not edit `agent_formulation_run.txt`, Hub config, strategy scripts, or `agent_strategy_run.py`.

Authoritative backlog: `.cursor/rules/task.md` → Current Priority **§14** + Notes **§14**.

---

## 0.1 — Idea-card contract (Pass ownership)

### Pass jobs

| Pass | File (target layout) | Owns | Does **not** own |
|------|----------------------|------|------------------|
| **1 — Discover** | `prompts/agent_formulation_run.txt` (trim in Phase 2; hub default) | Fetch/strategy work, invent, score, dedup, rank, Best ideas, ranked table, viability snapshot, execution summary, next-validation dates | Identical per-idea formatting; Docx convert/open |
| **2 — Pack** | `prompts/agent_formulation_pack.txt` (**add in Phase 1**) | Rewrite every ranked idea to the fixed card below; Best ideas ↔ packed details; Docx **once** after cards pass | New invent/re-rank by default; strategy CLIs; Hub (until Phase 4) |

**Run order (after Phase 1+):** paste Pass 1 → draft `.md` → paste Pass 2 → packed `.md` → one-shot Docx. Same path: `agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.md` (+ `.docx`).

### Required subheads (every ranked idea, same order)

Use these **exact / near-exact** labels so Word distribution stays stable:

1. **Problem** — or **Problem / trend**; for S1 use **Formula** (+ citations) as the problem spine  
2. **Solution**  
3. **Target**  
4. **MVP cost**  
5. **Regulatory** — required on every card (not only the viability table)  
6. **Competitors / alternatives** — 2–4 named products/agencies or DIY patterns; **each** with one “why Nigeria buyer might still choose this” line; no fake companies or fake pricing  
7. **GUEMF** — Mode A rationale *or* Mode B scores (G/U/E/M/F + composite; agent scale 1–5, max 25)  
8. **Commercial viability** (short)  
9. **Dedup** (short)  
10. **Founder fit** (short)

### Strategy add-ons (extra lines; never replace the list above)

| Trace | Extra (keep shared list) |
|-------|--------------------------|
| **S1** | Formula (successful business + recurring complaint + variation); success signal/citation; complaint citations with URL (title/date/quote when available) |
| **S12 Mode A** (primary `S12`) | Mode A GUEMF one-liners + evidence URL(s) |
| Any | **Strategy trace** in heading or a dedicated bullet |

### Incomplete Pass 2

Any ranked idea missing **Regulatory**, **Competitors / alternatives** block, **Solution**, **Target**, or **MVP cost** → Pass 2 incomplete. Fill from Pass 1 evidence; do not invent fake competitors.

### File-level skeleton (both passes agree)

1. Header / strategies / dedup  
2. Best ideas (top 3–5)  
3. Ranked table (full set + GUEMF)  
4. Commercial viability snapshot (recommended scan table even if cards also have viability)  
5. Idea details (packed cards after Pass 2)  
6. Explicitly not re-proposed  
7. Execution summary  
8. Next validation steps  
9. Docx status placeholder → Pass 2 converts once  

### Locked gates (Pass 1 must keep — §11 / §13)

- S1: online discovery + citeable URLs; no `seed_businesses.json` as sole evidence  
- S12: Mode A (≥2 ideas with **primary** S12) + Mode B overlay 1–5; mid-hop `→ S12` alone ≠ Mode A  
- Soft-fail: S1/S6/S7/S12 aids must not abort the whole run  

---

## 0.2 — Inventory: who loads `agent_formulation_run.txt` today

Paths that **must keep working** through Phases 1–2 (Hub default unchanged until Phase 4). Snapshot: **2026-07-15**.

### Runtime / Hub (break if path renamed without Phase 4)

| Surface | Path | Behavior |
|---------|------|----------|
| Default constant | `inc_launcher/agent_run.py` → `DEFAULT_PROMPT_PATH` | `"prompts/agent_formulation_run.txt"` |
| Action dispatch | `inc_launcher/actions.py` | Falls back to same path if item omits `prompt_path` |
| Hub card | `inc_launcher/launcher_config.json` → `id: agent_formulation_run` | `action: agent_run`, **pinned**; no explicit `prompt_path` → uses default |
| Load helper | `inc_launcher/agent_run.load_agent_prompt` | Reads file from Inc root |

### Automated asserts (must stay green when trimming Pass 1)

| Test | Asserts against prompt file |
|------|----------------------------|
| `Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering/test_strategy12_prompt_dual_mode.py` | §13 Mode A/B markers in `agent_formulation_run.txt` |
| `Strategy-1-Business-Variation/test_phase4_agent_smoke.py` | S1 include / cite rules |
| `Strategy-1-Business-Variation/test_phase6_regression.py` | Reads prompt text as part of regression |
| `inc_launcher/tests/test_agent_run.py` | Loads default / configured prompt path |
| `inc_launcher/tests/test_phase5_signoff.py` | `DEFAULT_PROMPT_PATH` exists; card pinned |
| `inc_launcher/tests/test_config.py` | Formulated pillar has `agent_formulation_run` |

### Docs / pointers (update in later phases; do not break links silently)

| Doc | Mentions |
|-----|----------|
| `prompts/README.md` | Canonical Hub formulation prompt |
| `agent-business-idea-runs/README.md` | Prompt path |
| `inc_launcher/README.md` | Edit `agent_formulation_run.txt`; Start loads that file |
| `Strategy-1-Business-Variation/README.md` | Agent runs use that prompt |
| `.cursor/rules/task.md` | Hub Phase 5 + §11/§13/§14 |

### Explicitly **not** loaders of the prompt body

| Surface | Note |
|---------|------|
| `agent-business-idea-runs/agent_strategy_run.py` | Fetch JSON only; does not read prompt text |
| `run_all_strategies.py` / strategy CLIs | Interactive menus; independent of Hub prompt file |
| `abuja_area_opportunity_scan.txt` | Separate prompt; out of scope for §14 |

### Phase 0 deliberately unchanged

- `prompts/agent_formulation_run.txt` body — **unchanged**  
- Hub `launcher_config.json` — **unchanged**  
- No `agent_formulation_pack.txt` yet (Phase 1)

---

## 0.3 — Acceptance sketch (Phases 1–5)

Executable checklist — what “green” means. Phase 0 ships this sketch only.

### Phase 1 — Add pack prompt (discover unchanged) ✅ (2026-07-15)

- [x] `prompts/agent_formulation_pack.txt` exists  
- [x] Pack text requires **Regulatory**, **Competitors / alternatives**, incomplete rule, Docx once after pack  
- [x] `prompts/README.md` names Pass 1 vs Pass 2 + run order  
- [x] Static smoke `agent-business-idea-runs/tests/test_formulation_pack_prompt.py`; **§13** dual-mode prompt smoke still passes  
- [x] Hub still single-card → discover file only; discover body **unchanged**

### Phase 2 — Slim discover (Docx deferred) ✅ (2026-07-15)

- [x] Discover prompt ends with explicit “Pass 2 pack required before Docx” + pack filename  
- [x] §11 S1 + §13 Mode A/B markers still present (S12 + pack smokes green)  
- [x] `agent-business-idea-runs/README.md` documents two-pass workflow  
- [x] Discover no longer owns one-shot Docx as the primary duty of Pass 1

### Phase 3 — Optional schema validator (deferrable) ✅ (2026-07-15)

- [x] Read-only validator under `agent-business-idea-runs/` (`idea_card_schema.py`)  
- [x] Fixture good/bad md + pytest  
- [x] Not wired into Hub Start; does not abort fetch  
- [x] Documented in agent README + pack prompt (optional before Docx)

### Phase 4 — Hub second card (deferrable) ✅ (2026-07-15)

- [x] Primary `agent_formulation_run` unchanged (discover)  
- [x] New card/id → `agent_formulation_pack.txt`  
- [x] Inc launcher Phase 5 / config tests green  

### Phase 5 — Sign-off ✅ (2026-07-15)

- [x] Cross-READMEs aligned (`prompts/`, `agent-business-idea-runs/`, Hub README)  
- [x] `MANUAL_TEST.md` automate-first (Cursor Enter only leftover)  
- [x] Regression: pack asserts + §13 dual-mode + schema + Hub config/agent_run  
- [x] Proof: Pass 2 pack of `business_ideas_20260715.md` → schema PASS (12) → Docx once  

### Minimal v1

Phases **0–5** complete (prompt split + validator + Hub Pass 2 + proof).


---

## Phase 0 definition of done

- [x] **0.1** Idea-card contract (this file §0.1)  
- [x] **0.2** Inventory (this file §0.2)  
- [x] **0.3** Acceptance sketch (this file §0.3)  
- [x] `prompts/README.md` points here  
- [x] Zero edits to Hub, discover prompt body, strategy scripts, `agent_strategy_run.py`

**Shipped:** 2026-07-15  
**Next:** §14 **CLOSED**. Hub leave-as-is (two cards = two agent runs). Meta paste drafts live in `task.md` Notes §14 close-out. Optional later: modal “Run N of 2” / tray intervals (new task when approved).

