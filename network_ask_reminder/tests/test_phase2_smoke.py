"""Phase 2 smokes: AUTO-NAR-01/02/06/07/09/10."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from network_ask_reminder.ask_log import append_ask, read_asks
from network_ask_reminder.config_loader import ConfigError, load_config, validate_config
from network_ask_reminder.isolation import run_isolation_checks
from network_ask_reminder.openers import generate_openers
from network_ask_reminder.paths import CONFIG_EXAMPLE
from network_ask_reminder.rotate import day_prompt, select_mode
from network_ask_reminder.status_report import compute_status


class TestPhase2Config(unittest.TestCase):
    def test_example_config_loads(self) -> None:
        cfg = load_config(CONFIG_EXAMPLE)
        self.assertEqual(cfg["version"], 1)
        self.assertEqual(cfg["rotate_mode"], "alternate_s3_s4")
        self.assertEqual(cfg["cadence"]["days"], ["mon", "wed", "fri"])

    def test_invalid_rotate_rejected(self) -> None:
        raw = json.loads(CONFIG_EXAMPLE.read_text(encoding="utf-8"))
        raw["rotate_mode"] = "nope"
        with self.assertRaises(ConfigError):
            validate_config(raw)


class TestPhase2Rotate(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_config(CONFIG_EXAMPLE)

    def test_alternate_deterministic(self) -> None:
        # Fixed Monday / Wednesday in same ISO week should differ
        mon = date(2026, 8, 10)  # Monday
        wed = date(2026, 8, 12)  # Wednesday
        self.assertEqual(mon.weekday(), 0)
        self.assertEqual(wed.weekday(), 2)
        m1 = select_mode(self.cfg, mon)
        m2 = select_mode(self.cfg, wed)
        self.assertIn(m1, ("s3", "s4"))
        self.assertIn(m2, ("s3", "s4"))
        self.assertNotEqual(m1, m2)

    def test_both_mode(self) -> None:
        cfg = dict(self.cfg)
        cfg["rotate_mode"] = "both"
        dp = day_prompt(cfg, date(2026, 8, 10))
        self.assertEqual(dp.mode, "both")
        self.assertIn("[S3]", dp.prompt_text)
        self.assertIn("[S4]", dp.prompt_text)

    def test_same_date_stable(self) -> None:
        d = date(2026, 8, 14)  # Friday
        self.assertEqual(select_mode(self.cfg, d), select_mode(self.cfg, d))


class TestPhase2LogAndStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.cfg = load_config(CONFIG_EXAMPLE)

    def test_append_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ask_log.jsonl"
            append_ask(
                self.cfg,
                mode="s3",
                notes="Friend mentioned inventory chaos",
                role="classmate",
                log_path=log,
                when=datetime(2026, 8, 10, 10, 0, tzinfo=timezone.utc),
            )
            append_ask(
                self.cfg,
                mode="s4",
                notes="Shop owner: stockouts weekly",
                role="kiosk owner",
                log_path=log,
                when=datetime(2026, 8, 12, 11, 0, tzinfo=timezone.utc),
            )
            rows = read_asks(self.cfg, log)
            self.assertEqual(len(rows), 2)
            report = compute_status(
                self.cfg,
                today=date(2026, 8, 12),
                log_path=log,
            )
            self.assertEqual(report.ask_count, 2)
            self.assertEqual(report.last_mode, "s4")
            self.assertEqual(report.days_since_last, 0)
            self.assertGreaterEqual(report.streak_cadence_hits, 1)

    def test_empty_notes_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "ask_log.jsonl"
            with self.assertRaises(ValueError):
                append_ask(self.cfg, mode="s3", notes="  ", log_path=log)


class TestPhase2OpenersIsolation(unittest.TestCase):
    def test_openers_no_send_language(self) -> None:
        cfg = load_config(CONFIG_EXAMPLE)
        text = generate_openers(cfg, "both")
        self.assertIn("Strategy 3", text)
        self.assertIn("Strategy 4", text)
        self.assertIn("never sends", text.lower())

    def test_isolation_ok(self) -> None:
        errors = run_isolation_checks()
        self.assertEqual(errors, [], msg=errors)


if __name__ == "__main__":
    unittest.main()
