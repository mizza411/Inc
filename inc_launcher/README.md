# Inc Tray Icon Launcher

Windows **tray icon** (notification area) for `C:\dev\Inc`. Right-click the icon for **4 pillars** and quick actions. **Left-click** (or choose **Open Inc Hub**) for the super main launcher window.

## Install

```powershell
cd C:\dev\Inc\inc_launcher
pip install -r requirements.txt
```

## Run

```powershell
python tray_app.py
```

The icon appears near the clock.

| Interaction | Result |
|-------------|--------|
| **Left-click** icon | Opens **Inc Hub** window |
| **Right-click** icon | Tray menu (4 pillars + global actions) |
| **Open Inc Hub** (menu, default) | Same hub window |

## Inc Hub (Phase 2)

- Left sidebar: same **4 pillars** as the tray menu
- Main area: launcher **grid** (labels + action type from config)
- **Pinned** items (`"pinned": true` in config) show at the top
- **Recently opened** items tracked in `recent_items.json` (local, not committed)

## Four pillars

| Menu | Opens |
|------|--------|
| My Established business ideas | Started businesses, Strategy 1, YouTube status |
| My leads | Abuja lead generator |
| Formulated ideas | run_all_strategies, business ideas files, research |
| Problem identification | Problem ID tool, problem finder, strategies |

Global: Open Inc workspace, task.md, Cursor.

## Customize

Edit `launcher_config.json` — add pillars, items, or `"pinned": true` without changing Python code.

Action types: `folder`, `file`, `url`, `command`, `cursor`.

## Tests

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests -q
```

## Phase 3 (planned)

Add pillars via config only; optional login startup and single-instance lock.
