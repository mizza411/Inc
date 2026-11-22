# Upstream Drive Consultancy — Manual test

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task:** UDC-1, Phase 3. The satellite was deleted on 22 Nov 2026. The short note is in `.cursor/rules/task.md`.  
**Pack folder:** `Upstream-Drive-Consultancy/`

## Automate first (agent runs — not you)

| Check | Where | Last run |
|-------|--------|----------|
| Required `.md` files present; each under ~500 lines; key locks/phrases | `python check_pack_shape.py` in this folder | **PASS** 2026-09-24 (agent) |
| Optional `.docx` siblings from pandoc | Same script prints docx sizes if present | Present |

**Do not** re-do those checks by hand.

---

## Manual (owner — one pass)

**Why not automated:** Judgement on clarity, honesty of refusals, and whether the lean roster matches how you will actually staff — not a scriptable assert.

**When:** Solution-complete for pack Phases **1–2c** (requirements body). Phase **5** (Project_reminder schedule) is separate and comes after you pass this read (or skip with a note).

### Setup

1. Open folder: `Upstream-Drive-Consultancy/`  
2. Prefer markdown in Cursor, or the `.docx` copies if generated.  
3. Optional: skim linked DC research only if a claim feels thin — do not require re-reading the whole DC tree.

### Ordered read (pass / fail)

| # | Read | Expect | Pass? |
|---|------|--------|-------|
| 1 | `README.md` | Company name, Nigeria-first, locks, out of scope, pack index | **Pass** |
| 2 | `company_requirements.md` | Floor before invoice; never-say claims; go/no-go checklist | **Pass** |
| 3 | `offer_lines.md` | Lines **A–D**; IT ≠ physical SecaaS; open order A→B→C→D | **Pass** |
| 4 | `risk_management_requirements.md` | Line D method; client owns residual risk; no fake scores | **Pass** |
| 5 | `lean_roles.md` | Seats R1–R7; core vs fractional; one person ≠ all lines | **Pass** |
| 6 | `sources.md` | Citations + check-this; points at DC `sources.md` | **Pass** |

### Sign-off

- [x] Pack is clear enough to know what Upstream sells, refuses, and must have before first paid work  
- [x] Lean roles match a firm as small as you will actually run (default: founder R1+R2/R5; R3 on call; R4 when C opens)  
- [x] No brochure claim you would not defend (certs stamp, “licence to hack”, physical SecaaS, 24/7 alone)  

**Result:** **Pass** (agent proxy — owner asked agent to run the test 2026-09-24)  
**Date:** 2026-09-24  
**Notes:** `check_pack_shape.py` PASS. All six docs meet checklist. Minor nit only: `offer_lines.md` “Who pays” still says D “(after 2b)” though 2b exists — cosmetic, not a fail. Phase **5** (Project_reminder) still separate.

After **Pass** or **Skip:** tell the agent so UDC-1 Phase 3 can close; then pick Phase **5** (Project_reminder auto-open) or optional Phase **4** (brand/pitch).

---

## Out of scope for this MANUAL

- CAC / bank / live sales  
- Project_reminder wiring (Phase 5)  
- DC diagram PDF quality (DC-SEC-NG-1e)  
- Running a real client engagement  
