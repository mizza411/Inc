# Local data (not in git)

This folder holds machine-local state for the bookmark sorter. **Do not commit** these files:

| File | Contents |
|------|----------|
| `queue.json` | Import/review queue (Chrome URLs, titles, folder paths, filing decisions) |
| `discover_report.json` | Phase 0 discover sample output |
| `actions.log` | Review action audit log |

Regenerate with `python -m business_bookmark_sorter import` and `review` from repo root.
