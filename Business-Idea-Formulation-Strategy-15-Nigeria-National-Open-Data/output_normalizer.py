"""
Phase 4 helpers for Strategy 15 output normalization.
"""

from pathlib import Path
import re
from typing import Dict, List, Tuple


ANALYSIS_COLUMNS: List[str] = [
    "Proposed domain (not verified)",
    "Problem Identified",
    "Potential Digital Solution",
    "Estimated daily sales",
    "Actualization strategy",
    "Target Audience",
    "Problem it solves",
    "Competition Analysis",
    "Estimated Costs (in dollars)",
    "Funding Sources (provide links to possible investors and VCs)",
    "No-code Tools to build solution",
    "How to test the viability of the idea",
    "Potential Challenges",
    "Solution to those potential challenges",
    "landing page platform",
    "Monetization Strategy",
    "Market Size and Growth Potential",
    "Technical Expertise and Skill Requirements",
    "Partnerships and Collaboration",
    "Timeline",
    "Key Performance Indicators (KPIs)",
    "Team Requirements",
    "Time to Market",
    "Required Skills",
    "Risks and Mitigation",
    "Scalability",
    "Social Impact",
]


PROVENANCE_COLUMNS: List[str] = [
    "Statistical indicator (or metric)",
    "Period (as published)",
    "Source (organization + URL or file name)",
    "Gaps / limitations (optional)",
]


def _pipe_escape(value: str) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def _split_markdown_row(line: str) -> List[str]:
    row = line.strip()
    if not row.startswith("|"):
        return []
    if row.endswith("|"):
        row = row[:-1]
    if row.startswith("|"):
        row = row[1:]
    # Split on unescaped pipes only.
    parts = re.split(r"(?<!\\)\|", row)
    return [p.replace("\\|", "|").strip() for p in parts]


def _is_separator_row(cells: List[str]) -> bool:
    if not cells:
        return False
    for c in cells:
        c2 = c.replace(":", "").replace("-", "").strip()
        if c2:
            return False
    return True


def _canonical_map(headers: List[str]) -> Dict[str, str]:
    return {h.strip().lower(): h for h in headers}


def parse_markdown_table(table_path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Parse the first markdown table in a file.
    Returns (headers, rows).
    """
    lines = table_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    table_lines = [ln for ln in lines if ln.strip().startswith("|")]
    if len(table_lines) < 2:
        return [], []

    headers = _split_markdown_row(table_lines[0])
    if not headers:
        return [], []

    start_idx = 1
    # Skip markdown separator row if present.
    sep_cells = _split_markdown_row(table_lines[1])
    if _is_separator_row(sep_cells):
        start_idx = 2

    rows: List[Dict[str, str]] = []
    for ln in table_lines[start_idx:]:
        cells = _split_markdown_row(ln)
        if not cells:
            continue
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        elif len(cells) > len(headers):
            cells = cells[: len(headers)]
        rows.append({headers[i]: cells[i] for i in range(len(headers))})

    return headers, rows


def _record_to_phase4_row(rec: Dict[str, str]) -> Dict[str, str]:
    row: Dict[str, str] = {
        PROVENANCE_COLUMNS[0]: rec.get("indicator", ""),
        PROVENANCE_COLUMNS[1]: rec.get("period", ""),
        PROVENANCE_COLUMNS[2]: rec.get("source", ""),
        PROVENANCE_COLUMNS[3]: rec.get("gaps", "N/A"),
    }
    for i, col in enumerate(ANALYSIS_COLUMNS):
        row[col] = "TBD" if i == 0 else ""
    return row


def merge_response_rows_into_phase4(
    base_records: List[Dict[str, str]],
    response_headers: List[str],
    response_rows: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """
    Merge Prompt 1b response rows into the normalized Strategy 15 schema.
    Row mapping is index-based by default (safe and deterministic).
    """
    merged = [_record_to_phase4_row(r) for r in base_records]
    if not response_rows:
        return merged

    response_header_map = _canonical_map(response_headers)
    lower_to_col = {k: v for k, v in response_header_map.items()}

    for i, out_row in enumerate(merged):
        if i >= len(response_rows):
            break
        src = response_rows[i]

        for col in ANALYSIS_COLUMNS:
            key = col.strip().lower()
            if key in lower_to_col:
                raw_value = src.get(lower_to_col[key], "").strip()
                if raw_value:
                    out_row[col] = raw_value

    return merged


def render_full_phase4_markdown(rows: List[Dict[str, str]], out_path: Path) -> None:
    headers = PROVENANCE_COLUMNS + ANALYSIS_COLUMNS
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "|" + "|".join(["---"] * len(headers)) + "|"

    lines: List[str] = []
    lines.append("# Strategy 15 Phase 4 Normalized Table")
    lines.append("")
    lines.append(header_line)
    lines.append(sep_line)
    for row in rows:
        values = [_pipe_escape(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(values) + " |")
    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def render_phase4_markdown_table(records: List[Dict[str, str]], out_path: Path) -> None:
    """
    Phase 4.1:
    Build a deterministic 1b-style markdown scaffold where provenance columns
    are pre-filled from validated records and analysis columns are placeholders.
    """
    headers = PROVENANCE_COLUMNS + ANALYSIS_COLUMNS
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "|" + "|".join(["---"] * len(headers)) + "|"

    lines: List[str] = []
    lines.append("# Strategy 15 Phase 4 Normalized Table Scaffold")
    lines.append("")
    lines.append("Provenance fields are pre-filled from validated inputs.")
    lines.append("Fill remaining analysis columns after running Prompt 1a/1b.")
    lines.append("")
    lines.append(header_line)
    lines.append(sep_line)

    for rec in records:
        row_dict = _record_to_phase4_row(rec)
        row_values = [_pipe_escape(row_dict.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(row_values) + " |")

    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

