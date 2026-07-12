# Strategy 1 — Manual test file

**Status (2026-07-12):** Former Hub / runner / playbook sign-off steps are **automated**. You do **not** need to run anything manually for v1.

## Automated coverage (run these)

```powershell
cd Strategy-1-Business-Variation
python test_signoff_automated.py
python test_phase6_regression.py
```

| Former manual step | Now automated by |
|--------------------|------------------|
| A Hub Formulated “Run Strategy 1” | `test_signoff_automated.py` (config + path + collector non-interactive) + `inc_launcher/tests/test_config.py` |
| B Established folder + gadget cards | `test_signoff_automated.py` + `test_config.py` path resolve |
| C Master runner menu (1 / 2 verbal / 5) | `test_signoff_automated.py` stdin menu drive |
| D Playbook steps still present | `test_signoff_automated.py` structural markers |

## Remaining manual (none for v1)

**No remaining manual steps.** Physical tray icon pixel-click is intentionally not required — config + command target + menu stdin cover the same acceptance criteria without a human.

If a future GUI-only regression appears that cannot be scripted, add it below with **Why not automated**.
