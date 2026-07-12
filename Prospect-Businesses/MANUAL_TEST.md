# Prospect-Businesses — Manual test

**Policy:** [.cursor/rules/deferred-manual-testing.mdc](../.cursor/rules/deferred-manual-testing.mdc)  
**Task tracker:** [.cursor/rules/task.md](../.cursor/rules/task.md) §4 Prospect + Current Priority §12

## Manual tests (you)

**None required** for v1 sign-off.

| Concern | Automated where |
|---------|-----------------|
| Hub Formulated card | `inc_launcher/tests/test_config.py` · see also `inc_launcher/MANUAL_TEST.md` §H |
| Sorter `prospects` route | `business_bookmark_sorter/tests/test_prospect_route.py` |
| Graduation to Started | Policy only — you must explicitly approve; not a UI test |

Optional Hub glance after tray restart: `inc_launcher/MANUAL_TEST.md` §H.
