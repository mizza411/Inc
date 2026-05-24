"""Manual/automated smoke test for Inc Hub (run: python -m inc_launcher.tests.smoke_hub)."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from inc_launcher.actions import run_action
from inc_launcher.config import INC_ROOT, load_config, list_pillars, resolve_path
from inc_launcher.hub_window import HubController
from inc_launcher.recent import list_pinned, load_recent, record_recent
from inc_launcher.tray_app import build_menu


def main() -> int:
    errors: list[str] = []
    cfg = load_config()
    pillars = list_pillars(cfg)
    print(f"[OK] Config: {len(pillars)} pillars")

    for pillar in pillars:
        n = len(pillar.get("items", []))
        print(f"     {pillar.get('id')}: {n} items")

    pinned = list_pinned(cfg)
    print(f"[OK] Pinned: {len(pinned)} items")
    for p in pinned:
        print(f"     - {p.get('label')}")

    paths_to_check = [
        "Started-Businesses",
        ".cursor/rules/task.md",
        "problem_identification_tool/web/index.html",
        "abuja_lead_generator",
    ]
    for rel in paths_to_check:
        path = resolve_path(rel)
        ok = path.is_dir() or path.is_file()
        status = "OK" if ok else "MISSING"
        print(f"[{status}] Path: {rel}")
        if not ok:
            errors.append(f"Missing path: {rel}")

    record_recent(
        {"label": "Smoke test entry", "action": "folder", "path": "."},
        pillar_id="established",
    )
    recent = load_recent()
    if not recent or recent[0].get("label") != "Smoke test entry":
        errors.append("Recent items not recorded correctly")
    else:
        print(f"[OK] Recent: top item = {recent[0]['label']}")

    try:
        menu = build_menu(cfg)
        if menu is None:
            errors.append("Tray menu build returned None")
        else:
            print("[OK] Tray menu builds")
    except Exception as exc:
        errors.append(f"Tray menu build failed: {exc}")

    # Hub window: open briefly on background thread, then close
    print("[..] Hub window: open 2s then close...")
    controller = HubController()
    done = threading.Event()

    def _open_and_check():
        try:
            controller.show(cfg)
            time.sleep(2)
            if controller._window is None:
                errors.append("Hub window was not created")
            elif controller._queue is not None:
                controller._queue.put("hide")
                time.sleep(0.3)
        except Exception as exc:
            errors.append(f"Hub window failed: {exc}")
        finally:
            done.set()

    t = threading.Thread(target=_open_and_check, daemon=True)
    t.start()
    if not done.wait(timeout=15):
        errors.append("Hub window timed out")
    else:
        print("[OK] Hub window opened and closed")

    # Safe action: resolve only (do not open Explorer in CI)
    task_path = resolve_path(".cursor/rules/task.md")
    if not task_path.is_file():
        errors.append("task.md not found for action smoke")
    else:
        print(f"[OK] Action target exists: task.md")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\n=== SMOKE TEST PASSED ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
