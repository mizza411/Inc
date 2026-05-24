# Inc Tray Icon Launcher

Windows **tray icon** (notification area) for `C:\dev\Inc`. Right-click the icon for **4 pillars** and quick actions.

## Install

```powershell
cd C:\dev\Inc\inc_launcher
pip install -r requirements.txt
```

## Run

```powershell
python tray_app.py
```

The icon appears near the clock. **Right-click** for the menu.

## Four pillars

| Menu | Opens |
|------|--------|
| My Established business ideas | Started businesses, Strategy 1, YouTube status |
| My leads | Abuja lead generator |
| Formulated ideas | run_all_strategies, business ideas files, research |
| Problem identification | Problem ID tool, problem finder, strategies |

Global: Open Inc workspace, task.md, Cursor.

## Customize

Edit `launcher_config.json` — add pillars or items without changing Python code.

Action types: `folder`, `file`, `url`, `command`, `cursor`.

## Phase 2 (planned)

Super main hub window — same 4 pillars as a full launcher UI.
