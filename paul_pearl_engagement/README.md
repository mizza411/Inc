# Paul Pearl/Upstream Drive engagement (Inc)

**PAUL-PEARL-TRAY-INC-1.** One product: the existing Upstream engagement tray, renamed.  
Opens **only** `Upstream-Drive-Consultancy/offer_lines.docx` (not the whole pack).  
Owner-facing title: **Paul Pearl/Upstream Drive**. Product home = **Inc** (not project_reminder).

| Event | Behaviour |
|-------|-----------|
| Tray start | Opens `offer_lines.docx` and the main window if `startup_open_docx` |
| Weekday slots | Default **10:00** and **17:00** (config). Opens the Word file and the main window |
| Tray menu | Open offer lines / Open Paul Pearl note / Show main window / Settings… / Restart / Exit |

## Run

```text
pythonw paul_pearl_engagement_tray_launcher.py
```

Auto-launch: Project Manager key `paul_pearl_engagement_tray` (owner ask 22 Nov 2026). Not an Inc Hub card.  
The old Project Reminder key `upstream_drive_engagement_tray` stays disabled so the retired stub does not start beside this tray.  
When this tray starts, it opens `offer_lines.docx` and the main window. Weekday slots stay 10:00 and 17:00 and open both. Settings stays on the menu only.

## Config

Storage file: `paul_pearl_schedule_config.json` beside this README (not an owner hand-edit path — Settings later if needed).  
Example: `paul_pearl_schedule_config.example.json`.

## Lifecycle log

`paul_pearl_engagement.log` in this folder (absolute path). Breadcrumbs: starting, tray Exit / Restart selected, shutting down. Each time the offer sheet opens, one line is `opened offer_lines.docx`. The date and time are at the start of that line.

## Settings

Tray **Show main window** opens the small main UI. **Settings…** is a separate stub (read-only schedule summary for now).  
Window position/size is remembered for each. Do not hand-edit JSON for day-to-day settings.

Hover/action text for menu rows lives in `menu_labels.py` (pystray has no tooltip API on Windows).

## Smoke

```text
python paul_pearl_engagement/test_paul_pearl_engagement_smoke.py
```

Does **not** start Project Manager. Does **not** require the old project_reminder tray.
