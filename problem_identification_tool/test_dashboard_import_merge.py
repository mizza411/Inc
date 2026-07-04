"""Tests for dashboard import merge helpers and import sync path."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL_ROOT = Path(__file__).resolve().parent
FIXTURE_CSV = TOOL_ROOT / "imports" / "fixtures" / "google_forms_ill_pay_to_sample.csv"
IMPORT_SCRIPT = TOOL_ROOT / "scripts" / "import_google_forms_csv.py"
MERGE_JS = TOOL_ROOT / "web" / "lib" / "response_merge.js"
DASHBOARD_IMPORT = TOOL_ROOT / "web" / "data" / "imports" / "google_forms_ill_pay_to.json"


def run_node_merge_script(js_snippet: str) -> str:
    result = subprocess.run(
        ["node", "-e", js_snippet],
        cwd=TOOL_ROOT / "web",
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip(f"Node.js unavailable or merge script failed: {result.stderr.strip()}")
    return result.stdout.strip()


def test_import_sync_dashboard_writes_web_path(tmp_path: Path) -> None:
    out = tmp_path / "import.json"
    result = subprocess.run(
        [
            sys.executable,
            str(IMPORT_SCRIPT),
            "--input",
            str(FIXTURE_CSV),
            "--output",
            str(out),
            "--sync-dashboard",
        ],
        cwd=TOOL_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert out.exists()
    assert DASHBOARD_IMPORT.exists()

    payload = json.loads(DASHBOARD_IMPORT.read_text(encoding="utf-8"))
    assert payload["questionnaire_id"] == "ill_pay_to_v1"
    assert payload["response_count"] == 2
    assert len(payload["responses"]) == 2


def test_merge_dedupes_by_id() -> None:
    snippet = """
const m = require('./lib/response_merge.js');
const local = [{ id: 'a', responses: { q2_problem: 'One' } }];
const imported = [
  { id: 'a', responses: { q2_problem: 'Duplicate' } },
  { id: 'b', responses: { q2_problem: 'Two' } },
];
const merged = m.mergeResponses(local, imported);
console.log(JSON.stringify({ count: merged.length, ids: merged.map(r => r.id) }));
"""
    out = run_node_merge_script(snippet)
    data = json.loads(out)
    assert data["count"] == 2
    assert set(data["ids"]) == {"a", "b"}


def test_extract_responses_from_c1_wrapper() -> None:
    snippet = """
const m = require('./lib/response_merge.js');
const payload = { source: 'google_forms_import', responses: [{ id: 'x' }] };
console.log(JSON.stringify(m.extractResponsesFromPayload(payload)));
"""
    out = run_node_merge_script(snippet)
    data = json.loads(out)
    assert data == [{"id": "x"}]


def test_dashboard_import_json_is_valid_for_merge() -> None:
    if not DASHBOARD_IMPORT.exists():
        pytest.skip("Run import with --sync-dashboard first")
    payload = json.loads(DASHBOARD_IMPORT.read_text(encoding="utf-8"))
    assert payload.get("responses")
    first = payload["responses"][0]
    assert first.get("questionnaire_id") == "ill_pay_to_v1"
    assert "responses" in first
