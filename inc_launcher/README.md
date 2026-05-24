# Inc Tray Icon Launcher

Windows **tray icon** (notification area) for `C:\dev\Inc`. Right-click the icon for **pillars** and quick actions. **Left-click** (or choose **Open Inc Hub**) for the super main launcher window.

## Install

```powershell
cd C:\dev\Inc\inc_launcher
pip install -r requirements.txt
```

## Run

```powershell
python tray_app.py
```

Or from Inc root:

```powershell
python -m inc_launcher.tray_app
```

The icon appears near the clock.

| Interaction | Result |
|-------------|--------|
| **Left-click** icon | Opens **Inc Hub** window |
| **Right-click** icon | Tray menu (pillars + global actions) |
| **Open Inc Hub** (menu, default) | Same hub window |

## Pillars (config-driven)

Default pillars include Established ideas, Leads, Formulated ideas, Problem identification, and **Automation hub**. Add more in `launcher_config.json` — no Python changes needed.

## Inc Hub (Phase 2)

- Left sidebar: pillars from config
- Main area: launcher **grid** (labels + action type)
- **Pinned** items (`"pinned": true`) at the top
- **Recently opened** in `recent_items.json` (local, gitignored)

## Phase 3

| Feature | How |
|---------|-----|
| **5th+ pillar** | Add object under `"pillars"` in `launcher_config.json` |
| **Single instance** | `"settings.single_instance": true` — only one tray icon |
| **Start at login** | Right-click tray → **Start at Windows login** (toggle ON/OFF) |
| **Custom icon** | Place `assets/icon.png` or set `settings.icon_path` |

Global actions: Open Inc workspace, task.md, Cursor.

## Customize

Edit `launcher_config.json` — pillars, items, `"pinned": true`, `settings`.

Action types: `folder`, `file`, `url`, `command`, `cursor`.

## Tests

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests -q
python -m inc_launcher.tests.smoke_hub
```
