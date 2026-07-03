#!/usr/bin/env python3
"""Tests for Strategy 3 sharing utilities integration (Phase B3)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_DIR))

from sharing_utilities import (  # noqa: E402
    DEFAULT_SURVEY_ID,
    SharingUtilities,
    build_tracked_survey_url,
)


class TestSharingStrategy3(unittest.TestCase):
    def test_build_tracked_survey_url_matches_strategy3_pattern(self):
        url = build_tracked_survey_url(
            "https://example.com/index.html",
            survey_id=DEFAULT_SURVEY_ID,
            ref="jane_doe",
            utm_source="jane_doe",
        )
        self.assertIn("survey=ill_pay_to_v1", url)
        self.assertIn("ref=jane_doe", url)
        self.assertIn("utm_source=jane_doe", url)
        self.assertIn("utm_medium=strategy3", url)

    def test_create_distributor_url(self):
        utilities = SharingUtilities(config_file=str(Path(tempfile.gettempdir()) / "missing_sharing_config.json"))
        url = utilities.create_distributor_url("ada_lovelace")
        self.assertIn("ref=ada_lovelace", url)

    def test_generate_strategy3_distributor_kit(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "distributor_registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "survey_id": "ill_pay_to_v1",
                        "distributors": [
                            {
                                "id": "test_user",
                                "name": "Test User",
                                "channel": "WhatsApp",
                                "payout_terms": "100 NGN",
                                "link": "",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            utilities = SharingUtilities(config_file=str(Path(tmp) / "cfg.json"))
            kit = utilities.generate_strategy3_distributor_kit(str(registry))
            self.assertEqual(kit["kit_type"], "strategy3_distributors")
            self.assertEqual(len(kit["distributors"]), 1)
            self.assertIn("ref=test_user", kit["distributors"][0]["link"])
            self.assertIn("whatsapp", kit["distributors"][0]["sharing_links"])

    def test_create_utm_url_backward_compatible(self):
        utilities = SharingUtilities(config_file=str(Path(tempfile.gettempdir()) / "missing_sharing_config2.json"))
        url = utilities.create_utm_url("email", "newsletter", "problem_research")
        self.assertIn("utm_source=email", url)
        self.assertNotIn("ref=", url)


if __name__ == "__main__":
    unittest.main()
