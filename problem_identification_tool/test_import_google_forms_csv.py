#!/usr/bin/env python3
"""Tests for Google Forms CSV import (Phase C1)."""

import json
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from import_google_forms_csv import import_csv_file, import_csv  # noqa: E402


FIXTURE = Path(__file__).resolve().parent / "imports" / "fixtures" / "google_forms_ill_pay_to_sample.csv"


class TestGoogleFormsImport(unittest.TestCase):
    def test_import_sample_csv(self):
        payload = import_csv_file(FIXTURE)
        self.assertEqual(payload["source"], "google_forms_import")
        self.assertEqual(payload["questionnaire_id"], "ill_pay_to_v1")
        self.assertEqual(payload["response_count"], 2)
        self.assertIn("q1_email", payload["column_map"])
        self.assertIn("q2_problem", payload["column_map"])

        first = payload["responses"][0]
        self.assertEqual(first["responses"]["q1_email"], "ada@example.com")
        self.assertIn("suppliers", first["responses"]["q2_problem"].lower())
        self.assertEqual(first["source"], "google_forms_import")
        self.assertEqual(first["questionnaire_id"], "ill_pay_to_v1")

    def test_subscription_row_maps_price_field(self):
        payload = import_csv_file(FIXTURE)
        second = payload["responses"][1]
        self.assertEqual(second["responses"]["q3_tried_solutions"], "No")
        self.assertIn("3000", second["responses"]["q7_subscription_fee"])

    def test_rejects_csv_without_required_columns(self):
        bad_csv = "Timestamp,Notes\n7/1/2026,something\n"
        with self.assertRaises(ValueError):
            import_csv(bad_csv)

    def test_output_is_valid_json_shape(self):
        payload = import_csv_file(FIXTURE)
        encoded = json.dumps(payload)
        decoded = json.loads(encoded)
        self.assertEqual(decoded["response_count"], len(decoded["responses"]))


if __name__ == "__main__":
    unittest.main()
