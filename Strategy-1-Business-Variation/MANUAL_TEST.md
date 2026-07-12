# Strategy 1 — Manual test file

**Status (2026-07-12):** **CLOSED for v1 + §11 (always-online).** Sign-off is **automated**.  
**Your action required:** **None** for Strategy 1 formulation (v1 or §11).

## Automated coverage (agent/CI — not you)

```powershell
cd Strategy-1-Business-Variation
python test_signoff_automated.py
python test_phase11_signoff.py
python test_phase6_regression.py
```

| Former / §11 check | Automated by |
|--------------------|--------------|
| A Hub Formulated “Run Strategy 1” | `test_signoff_automated.py` + `inc_launcher/tests/test_config.py` |
| B Established folder + gadget cards | same |
| C Master runner menu (1 / 2 verbal / 5) | `test_signoff_automated.py` stdin menu |
| D Playbook steps still present | `test_signoff_automated.py` structural markers |
| §11 no live `seed_businesses.json` | `test_phase11_signoff.py` |
| §11 URL-cited collector + Prompt 1a | `test_phase11_signoff.py` |
| §11 `strategy_1_discovery` (no `strategy_1_seeds`) | `test_phase11_signoff.py` + Phase 4/6 |
| §11 Docx shows complaint source URL | `test_phase11_signoff.py` (`convert_md_to_docx` only — **does not open Word**) |

## Remaining manual (none)

**No remaining manual steps** for Strategy 1 v1 or §11 always-online retirement.

If a future GUI-only regression cannot be scripted, add it below with **Why not automated**.
