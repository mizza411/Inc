# Paul Pearl/Upstream Drive engagement (Inc)

**PAUL-PEARL-TRAY-INC-1.** One product: the existing Upstream engagement tray, renamed.  
Opens **only** `Upstream-Drive-Consultancy/offer_lines.docx` (not the whole pack).  
Owner-facing title: **Paul Pearl/Upstream Drive**. Product home = **Inc** (not project_reminder).

| Event | Behaviour |
|-------|-----------|
| Tray start | Opens `offer_lines.docx` if `startup_open_docx` |
| Weekday slots | Default **10:00** and **17:00** (config) |
| Tray menu | Open offer lines / Open Paul Pearl note / Settings… / Restart / Exit |

## Run

```text
pythonw paul_pearl_engagement_tray_launcher.py
```

Auto-launch: **neither** Inc Hub nor Project Manager (owner lock 05/11/2026). Run manually with `pythonw` above.  
Legacy PR key `upstream_drive_engagement_tray` is **disabled** so it does not auto-start beside this tray.

## Config

Storage file: `paul_pearl_schedule_config.json` beside this README (not an owner hand-edit path — Settings later if needed).  
Example: `paul_pearl_schedule_config.example.json`.

## Lifecycle log

`paul_pearl_engagement.log` in this folder (absolute path). Breadcrumbs: starting, tray Exit / Restart selected, shutting down.

## Settings

Tray **Settings…** opens a stub window (read-only schedule summary for now).  
Window position/size is remembered. Do not hand-edit JSON for day-to-day settings.

Hover/action text for menu rows lives in `menu_labels.py` (pystray has no tooltip API on Windows).

## Smoke

```text
python paul_pearl_engagement/test_paul_pearl_engagement_smoke.py
```

Does **not** start Project Manager. Does **not** require the old project_reminder tray.
