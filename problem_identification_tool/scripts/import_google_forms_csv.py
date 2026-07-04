#!/usr/bin/env python3
"""
Phase C1 — Import Google Forms CSV into ill_pay_to_v1 response JSON.

Does not modify the live survey or dashboard (C2 wires dashboard read path).

Usage:
    python scripts/import_google_forms_csv.py --input path/to/forms_export.csv
    python scripts/import_google_forms_csv.py --input export.csv --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QUESTIONNAIRE_ID = "ill_pay_to_v1"
SOURCE_TAG = "google_forms_import"

# Map ill_pay_to question ids -> substring hints for Google Forms CSV headers
FIELD_HINTS: dict[str, list[str]] = {
    "q1_email": ["email"],
    "q2_problem": ["problem", "pay to have solved"],
    "q3_tried_solutions": ["tried any existing solutions"],
    "q4_solutions_lacking": ["existing solutions lacking", "what were the existing"],
    "q5_payment_model": ["payment model do you prefer"],
    "q6_one_time_fee": ["one-time fee", "one time fee"],
    "q7_subscription_fee": ["subscription fee"],
    "q8_urgency": ["how urgent"],
}

TIMESTAMP_HINTS = ["timestamp", "time submitted", "date submitted"]


def normalize_header(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def match_column(headers: list[str], hints: list[str]) -> str | None:
    normalized = {h: normalize_header(h) for h in headers}
    for header, norm in normalized.items():
        for hint in hints:
            if hint in norm:
                return header
    return None


def build_column_map(headers: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for field_id, hints in FIELD_HINTS.items():
        column = match_column(headers, hints)
        if column:
            mapping[field_id] = column
    timestamp_col = match_column(headers, TIMESTAMP_HINTS)
    if timestamp_col:
        mapping["_timestamp"] = timestamp_col
    return mapping


def parse_google_timestamp(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return datetime.now(timezone.utc).isoformat()
    for fmt in (
        "%m/%d/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%d/%m/%Y %H:%M",
    ):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return value


def row_to_response(row: dict[str, str], column_map: dict[str, str], index: int) -> dict[str, Any]:
    responses: dict[str, str] = {}
    for field_id, column in column_map.items():
        if field_id.startswith("_"):
            continue
        responses[field_id] = (row.get(column) or "").strip()

    ts_column = column_map.get("_timestamp")
    timestamp = parse_google_timestamp(row.get(ts_column, "") if ts_column else "")

    return {
        "id": f"gf_import_{index}_{abs(hash(responses.get('q1_email', '') + responses.get('q2_problem', ''))) % 10**8}",
        "timestamp": timestamp,
        "questionnaire_id": QUESTIONNAIRE_ID,
        "ref": None,
        "source": SOURCE_TAG,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "responses": responses,
        "completion_time": 0,
        "user_agent": "google_forms_import",
        "anonymous": False,
    }


def import_csv(text: str) -> dict[str, Any]:
    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames:
        raise ValueError("CSV has no header row")

    headers = list(reader.fieldnames)
    column_map = build_column_map(headers)
    missing = [fid for fid in FIELD_HINTS if fid not in column_map]
    if "q1_email" in missing or "q2_problem" in missing:
        raise ValueError(
            f"CSV missing required columns (email and/or problem). "
            f"Mapped: {column_map}. Headers found: {headers}"
        )

    responses = []
    for index, row in enumerate(reader, start=1):
        if not any((v or "").strip() for v in row.values()):
            continue
        responses.append(row_to_response(row, column_map, index))

    return {
        "source": SOURCE_TAG,
        "questionnaire_id": QUESTIONNAIRE_ID,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "column_map": {k: v for k, v in column_map.items() if not k.startswith("_")},
        "response_count": len(responses),
        "responses": responses,
    }


def import_csv_file(input_path: Path) -> dict[str, Any]:
    text = input_path.read_text(encoding="utf-8-sig")
    return import_csv(text)


def main(argv: list[str] | None = None) -> int:
    tool_root = Path(__file__).resolve().parents[1]
    default_out = tool_root / "imports" / "google_forms_ill_pay_to.json"
    dashboard_out = tool_root / "web" / "data" / "imports" / "google_forms_ill_pay_to.json"

    parser = argparse.ArgumentParser(description="Import Google Forms CSV to ill_pay_to_v1 JSON")
    parser.add_argument("--input", "-i", required=True, help="Path to Google Forms CSV export")
    parser.add_argument("--output", "-o", default=str(default_out), help="Output JSON path")
    parser.add_argument(
        "--sync-dashboard",
        action="store_true",
        help="Also write JSON to web/data/imports/ for dashboard fetch on GitHub Pages",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print summary only")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        payload = import_csv_file(input_path)
    except (ValueError, csv.Error) as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        return 1

    print(f"Mapped columns: {payload['column_map']}")
    print(f"Imported {payload['response_count']} response(s)")

    if args.dry_run:
        return 0

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote: {output_path}")

    if args.sync_dashboard:
        dashboard_path = dashboard_out
        dashboard_path.parent.mkdir(parents=True, exist_ok=True)
        dashboard_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Synced dashboard import: {dashboard_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
