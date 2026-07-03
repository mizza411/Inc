#!/usr/bin/env python3
"""Tests for Strategy 3 collector B2 integration (non-interactive)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

STRATEGY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STRATEGY_DIR))

from distributor_links import count_responses_by_ref, load_survey_responses_export  # noqa: E402
from network_problem_collector import NetworkProblemIdentifier, build_parser  # noqa: E402


class TestCollectorB2(unittest.TestCase):
    def test_default_parser_is_classic_mode(self):
        args = build_parser().parse_args([])
        self.assertFalse(args.distributor)

    def test_distributor_flag(self):
        args = build_parser().parse_args(["--distributor"])
        self.assertTrue(args.distributor)

    def test_count_responses_by_ref(self):
        sample = [
            {"ref": "jane_doe", "questionnaire_id": "ill_pay_to_v1"},
            {"ref": "jane_doe", "questionnaire_id": "ill_pay_to_v1"},
            {"ref": "ada_lovelace", "questionnaire_id": "ill_pay_to_v1"},
            {"questionnaire_id": "ill_pay_to_v1"},
        ]
        counts = count_responses_by_ref(sample)
        self.assertEqual(counts["jane_doe"], 2)
        self.assertEqual(counts["ada_lovelace"], 1)

    def test_load_survey_export_array_and_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            array_path = Path(tmp) / "array.json"
            array_path.write_text(json.dumps([{"ref": "a"}]), encoding="utf-8")
            self.assertEqual(len(load_survey_responses_export(array_path)), 1)

            wrap_path = Path(tmp) / "wrap.json"
            wrap_path.write_text(json.dumps({"responses": [{"ref": "b"}]}), encoding="utf-8")
            self.assertEqual(len(load_survey_responses_export(wrap_path)), 1)

    def test_save_data_includes_workflow_and_distributors(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            identifier = NetworkProblemIdentifier()
            identifier.strategy_dir = tmp_path
            identifier.workflow = "distributor"
            identifier.distributors = [{"id": "test_user", "name": "Test User", "link": "http://example.com"}]
            identifier.problems = [{"contact": "X", "problem": "Y", "frequency": "Daily", "urgency": "High",
                                    "current_solution": "", "willing_to_pay": "Yes"}]

            with patch("network_problem_collector.open_file_automatically"), patch("builtins.print"):
                identifier.save_data()

            output_files = list(tmp_path.glob("network_problems_*.json"))
            self.assertEqual(len(output_files), 1)
            saved = json.loads(output_files[0].read_text(encoding="utf-8"))
            self.assertEqual(saved["workflow"], "distributor")
            self.assertEqual(len(saved["distributors"]), 1)

    def test_classic_run_method_still_exists(self):
        identifier = NetworkProblemIdentifier()
        self.assertTrue(callable(identifier.run))
        self.assertTrue(callable(identifier.run_distributor))
        self.assertEqual(identifier.workflow, "classic")


if __name__ == "__main__":
    unittest.main()
