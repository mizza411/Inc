# Local data (not in git)

This folder holds machine-local state for the bookmark sorter. **Do not commit** these files:

| File | Contents |
|------|----------|
| `queue.json` | Import/review queue (Chrome URLs, titles, folder paths, filing decisions) |
| `actions.log` | Review action audit log |
| `session_settings.json` | Timed-session prefs (minutes, auto-open toggle) — **BB-TIMED-1**; change via review Settings UI only |

A leftover `discover_report.json` may exist from the old `discover` command (discontinued 2026-08-19). Safe to delete locally; still gitignored.

Regenerate with `python -m business_bookmark_sorter import` (first time) and `review` from repo root.
