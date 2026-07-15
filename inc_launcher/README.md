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

Action types: `folder`, `file`, `url`, `command`, `cursor`, `agent_run`.

## Phase 5 — Agent formulation run

**Front door** for the Cursor agent formulation workflow (strategies **1**, 5, 6, 7, 9, 11–15). **Not** the `run_all_strategies.py` CLI menu.

| Step | What happens |
|------|----------------|
| Hub or tray → **Agent formulation run** | Opens/focuses **Inc Hub** and shows **Option B** confirmation modal (Pass **1** Discover) |
| Hub → **Agent formulation pack (Pass 2)** | Same flow with `prompts/agent_formulation_pack.txt` (card schema → Docx once) |
| **Start** | Loads the card’s `prompt_path` (default Discover) → clipboard → opens Cursor on repo → auto-paste (~8s) if `pyautogui` installed |
| **Not now** | Dismisses modal; nothing runs |
| You | Focus Cursor chat if needed → **Enter** to send |

**Config** (`launcher_config.json`, Formulated ideas pillar):

```json
{
  "id": "agent_formulation_run",
  "label": "Agent formulation run",
  "action": "agent_run",
  "pinned": true
}
```

Pass 2 (additive; not pinned — Discover stays primary):

```json
{
  "id": "agent_formulation_pack",
  "label": "Agent formulation pack (Pass 2)",
  "action": "agent_run",
  "prompt_path": "prompts/agent_formulation_pack.txt",
  "modal_title": "Ready for Pass 2 pack?",
  "modal_bullets": ["…"]
}
```

Optional keys on the item: `prompt_path`, `paste_delay_sec` (default 8), `auto_paste` (default true), `modal_title`, `modal_bullets`.

**Edit prompts** under `prompts/` — not in Python. See `task.md` §14.

Legacy CLI runner remains as **Run all strategies (CLI menu)**.

Manual sign-off: `MANUAL_TEST.md` §G.

## Tests

```powershell
cd C:\dev\Inc
python -m pytest inc_launcher/tests -q
python -m inc_launcher.tests.smoke_hub
```
