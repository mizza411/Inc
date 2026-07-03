#!/usr/bin/env python3
"""Smoke tests for Strategy 3 distributor link generator (Phase B1)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STRATEGY_DIR))

from distributor_links import (  # noqa: E402
    DistributorLinkManager,
    build_distributor_link,
    slugify,
)


class TestDistributorLinks(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Jane Doe"), "jane_doe")
        self.assertEqual(slugify("  O'Brien & Co. "), "o_brien_co")

    def test_build_distributor_link_has_tracking_params(self):
        url = build_distributor_link("jane_doe")
        self.assertIn("survey=ill_pay_to_v1", url)
        self.assertIn("ref=jane_doe", url)
        self.assertIn("utm_source=jane_doe", url)
        self.assertIn("utm_medium=strategy3", url)
        self.assertIn("utm_campaign=ill_pay_to", url)

    def test_add_and_list_distributor(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = DistributorLinkManager(strategy_dir=Path(tmp))
            record = manager.add_distributor(
                name="Test User",
                channel="WhatsApp",
                payout_terms="100 NGN per response",
            )
            self.assertEqual(record["id"], "test_user")
            self.assertIn("ref=test_user", record["link"])

            listed = manager.list_distributors()
            self.assertEqual(len(listed), 1)
            self.assertEqual(listed[0]["name"], "Test User")

            registry_path = Path(tmp) / "distributor_registry.json"
            self.assertTrue(registry_path.exists())
            data = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertEqual(len(data["distributors"]), 1)

    def test_outreach_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            templates_src = STRATEGY_DIR / "distributor_message_templates.txt"
            (tmp_path / "distributor_message_templates.txt").write_text(
                templates_src.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            manager = DistributorLinkManager(strategy_dir=tmp_path)
            manager.add_distributor(
                name="Ada Lovelace",
                channel="Email",
                payout_terms="500 NGN each",
            )
            out_path = manager.generate_outreach_file()
            content = out_path.read_text(encoding="utf-8")
            self.assertIn("Ada Lovelace", content)
            self.assertIn("ref=ada_lovelace", content)
            self.assertIn("500 NGN each", content)


if __name__ == "__main__":
    unittest.main()
