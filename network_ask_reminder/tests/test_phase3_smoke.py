"""Phase 3 smokes: AUTO-NAR-03 Hub network_ask wiring (no live tray)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from inc_launcher.actions import run_action
from inc_launcher.config import load_config, list_pillars
from inc_launcher.option_b_actions import uses_option_b_modal
from inc_launcher.scheduled_nudges import find_menu_item_by_id
from network_ask_reminder.build_docx import PLAYBOOK_DOCX
from network_ask_reminder.hub_nudge import enrich_hub_item, run_network_ask_start
from network_ask_reminder.isolation import run_isolation_checks
from network_ask_reminder.paths import PACKAGE_DIR


class TestPhase3ConfigWiring(unittest.TestCase):
    def test_hub_card_and_schedule(self) -> None:
        config = load_config()
        problem = next(p for p in list_pillars(config) if p["id"] == "problem_identification")
        by_id = {i.get("id"): i for i in problem.get("items", []) if i.get("id")}
        self.assertIn("network_ask_remind", by_id)
        card = by_id["network_ask_remind"]
        self.assertEqual(card["action"], "network_ask")
        self.assertTrue(card.get("pinned"))

        resolved = find_menu_item_by_id(config, "network_ask_remind")
        self.assertIsNotNone(resolved)

    def test_formulation_card_untouched(self) -> None:
        config = load_config()
        formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
        by_id = {i.get("id"): i for i in formulated.get("items", []) if i.get("id")}
        self.assertEqual(by_id["agent_formulation_run"]["action"], "agent_run")
        self.assertTrue(by_id["agent_formulation_run"].get("pinned"))


class TestPhase3NudgeLogic(unittest.TestCase):
    def test_option_b_action_set(self) -> None:
        self.assertTrue(uses_option_b_modal("agent_run"))
        self.assertTrue(uses_option_b_modal("network_ask"))
        self.assertFalse(uses_option_b_modal("folder"))

    def test_enrich_has_today_copy(self) -> None:
        item = enrich_hub_item({"action": "network_ask", "label": "Ask"})
        self.assertEqual(item["action"], "network_ask")
        self.assertTrue(item["modal_title"])
        self.assertTrue(item["modal_bullets"])
        joined = " ".join(item["modal_bullets"]).lower()
        self.assertIn("never auto-messages", joined)

    def test_start_writes_openers_file(self) -> None:
        with patch("os.startfile"):
            with patch(
                "cursor_copy_helper.copy_to_clipboard",
                return_value=True,
            ):
                result = run_network_ask_start(PACKAGE_DIR.parent)
        self.assertIn(result["mode"], ("s3", "s4", "both"))
        openers = Path(result["openers_path"])
        self.assertTrue(openers.is_file())
        text = openers.read_text(encoding="utf-8")
        self.assertIn("copy/paste", text.lower())

    def test_start_opens_docx_not_markdown(self) -> None:
        with patch("os.startfile") as start:
            with patch(
                "cursor_copy_helper.copy_to_clipboard",
                return_value=True,
            ):
                result = run_network_ask_start(PACKAGE_DIR.parent)
        self.assertTrue(result["playbook_opened"])
        start.assert_called_once()
        opened = Path(start.call_args.args[0]).resolve()
        self.assertEqual(opened, PLAYBOOK_DOCX.resolve())
        self.assertEqual(opened.suffix.lower(), ".docx")
        self.assertTrue(Path(result["openers_path"]).is_file())

    def test_missing_docx_does_not_open_markdown(self) -> None:
        live_docx = PLAYBOOK_DOCX.resolve()
        self.assertTrue(live_docx.is_file())
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder) / "ask_people_ask_owners_playbook.docx"
            self.assertFalse(missing.exists())
            with patch("network_ask_reminder.hub_nudge.PLAYBOOK_DOCX", missing):
                with patch("os.startfile") as start:
                    with patch(
                        "cursor_copy_helper.copy_to_clipboard",
                        return_value=True,
                    ):
                        result = run_network_ask_start(PACKAGE_DIR.parent)
        self.assertFalse(result["playbook_opened"])
        start.assert_not_called()
        self.assertTrue(Path(result["openers_path"]).is_file())
        self.assertTrue(live_docx.is_file())

    def test_run_action_dispatches_network_ask(self) -> None:
        with patch("network_ask_reminder.hub_nudge.run_network_ask_start") as mock_run:
            run_action({"action": "network_ask", "label": "Ask"}, inc_root=PACKAGE_DIR.parent)
        mock_run.assert_called_once()

    def test_isolation_still_ok(self) -> None:
        errors = run_isolation_checks()
        self.assertEqual(errors, [], msg=errors)


if __name__ == "__main__":
    unittest.main()
