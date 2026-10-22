"""Phase 4 smokes: AUTO-NAR-04/08 (+ AUTO-NAR-05 skip note)."""

from __future__ import annotations

import unittest

from network_ask_reminder.build_docx import PLAYBOOK_DOCX, build_docx
from network_ask_reminder.pr_launcher import (
    LAUNCHER_KEY,
    validate_pr_launcher,
)
from network_ask_reminder.task_reminder_seed import SKIP_REASON, seed_status


class TestPhase4Docx(unittest.TestCase):
    def test_docx_exists_nonempty(self) -> None:
        path = build_docx(check_only=True)
        self.assertEqual(path, PLAYBOOK_DOCX)
        self.assertGreaterEqual(path.stat().st_size, 500)


class TestPhase4PrLauncher(unittest.TestCase):
    def test_launcher_entry_valid(self) -> None:
        errors = validate_pr_launcher()
        self.assertEqual(errors, [], msg=errors)

    def test_key_name(self) -> None:
        self.assertEqual(LAUNCHER_KEY, "ask_people_ask_owners_playbook")


class TestPhase4TaskReminderSkip(unittest.TestCase):
    def test_auto_nar_05_skipped_with_reason(self) -> None:
        status = seed_status()
        self.assertTrue(status.startswith("SKIPPED:"))
        self.assertIn("Task Reminder", SKIP_REASON)


if __name__ == "__main__":
    unittest.main()
