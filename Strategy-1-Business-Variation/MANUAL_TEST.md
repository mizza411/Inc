# Strategy 1 — Manual test file

**Status (2026-07-12):** **CLOSED for v1.** Former Hub / runner / playbook sign-off steps are **automated**.  
**Your action required:** **None** for Strategy 1 v1.

## Automated coverage (agent/CI — not you)

```powershell
cd Strategy-1-Business-Variation
python test_signoff_automated.py
python test_phase6_regression.py
```

| Former manual step | Automated by |
|--------------------|--------------|
| A Hub Formulated “Run Strategy 1” | `test_signoff_automated.py` + `inc_launcher/tests/test_config.py` |
| B Established folder + gadget cards | same |
| C Master runner menu (1 / 2 verbal / 5) | `test_signoff_automated.py` stdin menu |
| D Playbook steps still present | `test_signoff_automated.py` structural markers |

## Remaining manual (none for v1)

**No remaining manual steps.** Do not block deleting the delivery chat on a Hub click-through.

If a future GUI-only regression cannot be scripted, add it below with **Why not automated**.
