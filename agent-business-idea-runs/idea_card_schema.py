#!/usr/bin/env python3
"""Validate packed idea cards in business_ideas_*.md (§14 Phase 3).

Read-only: does not edit files or call Docx export.
Soft aid — run after Pass 2 Pack, before Docx. Not wired into Hub or agent_strategy_run.

Usage (from repo root):
  python agent-business-idea-runs/idea_card_schema.py path/to/business_ideas_YYYYMMDD.md
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Incomplete Pass 2 hard gate (FORMULATION_PASS_CONTRACT.md)
REQUIRED_LABELS = (
    "Solution",
    "Target",
    "MVP cost",
    "Regulatory",
    "Competitors / alternatives",
)

# Problem spine: either Problem / Problem / trend, or S1 Formula
PROBLEM_SPINE = ("Problem", "Problem / trend", "Formula")

# Optional for fuller pack (reported as warnings when --strict-full)
OPTIONAL_LABELS = (
    "GUEMF",
    "Commercial viability",
    "Dedup",
    "Founder fit",
)

IDEA_DETAILS_RE = re.compile(
    r"^##\s+Idea details\s*$", re.IGNORECASE | re.MULTILINE
)
# Stop at next ## of same/next level that is not idea subheading
NEXT_H2_RE = re.compile(r"^##\s+\S", re.MULTILINE)
CARD_HEAD_RE = re.compile(r"^###\s+\d+\.\s+.+$", re.MULTILINE)
LABEL_RE = re.compile(
    r"^\s*[-*]?\s*\*\*(.+?):\*\*",
    re.MULTILINE,
)


@dataclass
class IdeaCardResult:
    title: str
    missing_required: list[str] = field(default_factory=list)
    missing_optional: list[str] = field(default_factory=list)
    has_problem_spine: bool = False

    @property
    def ok(self) -> bool:
        return not self.missing_required and self.has_problem_spine


@dataclass
class ValidationReport:
    path: Path
    ideas: list[IdeaCardResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors and all(i.ok for i in self.ideas) and bool(self.ideas)


def _normalize_label(raw: str) -> str:
    return re.sub(r"\s+", " ", raw.strip())


def _labels_in_body(body: str) -> set[str]:
    found: set[str] = set()
    for m in LABEL_RE.finditer(body):
        found.add(_normalize_label(m.group(1)))
    return found


def _label_present(labels: set[str], wanted: str) -> bool:
    w = wanted.lower()
    for lab in labels:
        if lab.lower() == w:
            return True
        # allow "MVP" if contract says MVP cost and file has MVP: as short form? No — require MVP cost
        if w == "competitors / alternatives" and lab.lower().startswith("competitors"):
            return True
        if w == "mvp cost" and lab.lower() in ("mvp cost", "mvp"):
            return True
    return False


def _has_problem_spine(labels: set[str]) -> bool:
    for spine in PROBLEM_SPINE:
        if _label_present(labels, spine):
            return True
    # Mode A sometimes leads with Mode A GUEMF + Evidence — still need Problem or Formula
    return False


def extract_idea_details_section(text: str) -> str | None:
    m = IDEA_DETAILS_RE.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    n = NEXT_H2_RE.search(rest)
    return rest[: n.start()] if n else rest


def split_cards(details: str) -> list[tuple[str, str]]:
    heads = list(CARD_HEAD_RE.finditer(details))
    if not heads:
        return []
    cards: list[tuple[str, str]] = []
    for i, h in enumerate(heads):
        title = h.group(0).strip()
        body_start = h.end()
        body_end = heads[i + 1].start() if i + 1 < len(heads) else len(details)
        cards.append((title, details[body_start:body_end]))
    return cards


def validate_markdown(text: str, path: Path | None = None) -> ValidationReport:
    report = ValidationReport(path=path or Path("<memory>"))
    details = extract_idea_details_section(text)
    if details is None:
        report.errors.append("missing ## Idea details section")
        return report
    cards = split_cards(details)
    if not cards:
        report.errors.append("no ### N. idea cards under Idea details")
        return report
    for title, body in cards:
        labels = _labels_in_body(body)
        card = IdeaCardResult(title=title, has_problem_spine=_has_problem_spine(labels))
        for req in REQUIRED_LABELS:
            if not _label_present(labels, req):
                card.missing_required.append(req)
        if not card.has_problem_spine:
            card.missing_required.append("Problem|Problem / trend|Formula")
        for opt in OPTIONAL_LABELS:
            if not _label_present(labels, opt):
                # GUEMF may appear as "GUEMF (Mode B)" etc.
                if opt == "GUEMF" and any(lab.upper().startswith("GUEMF") for lab in labels):
                    continue
                if opt == "Founder fit" and any(
                    "founder" in lab.lower() for lab in labels
                ):
                    continue
                card.missing_optional.append(opt)
        report.ideas.append(card)
    return report


def validate_path(path: Path) -> ValidationReport:
    text = path.read_text(encoding="utf-8")
    return validate_markdown(text, path=path)


def format_report(report: ValidationReport, *, show_optional: bool = False) -> str:
    lines: list[str] = [f"idea_card_schema: {report.path}"]
    if report.errors:
        for e in report.errors:
            lines.append(f"  ERROR: {e}")
    for idea in report.ideas:
        status = "OK" if idea.ok else "FAIL"
        lines.append(f"  [{status}] {idea.title}")
        if idea.missing_required:
            lines.append(f"    missing required: {', '.join(idea.missing_required)}")
        if show_optional and idea.missing_optional:
            lines.append(f"    missing optional: {', '.join(idea.missing_optional)}")
    if report.ok:
        lines.append(f"  PASS ({len(report.ideas)} ideas)")
    else:
        lines.append("  FAIL")
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate idea-card labels in a formulation markdown (Pass 2 aid)."
    )
    parser.add_argument("markdown", type=Path, help="Path to business_ideas_*.md")
    parser.add_argument(
        "--strict-full",
        action="store_true",
        help="Also fail on missing optional labels (GUEMF, commercial viability, …)",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    path: Path = args.markdown
    if not path.is_file():
        print(f"idea_card_schema: file not found: {path}", file=sys.stderr)
        return 2
    report = validate_path(path)
    if args.strict_full:
        for idea in report.ideas:
            # promote optional misses into required for exit code
            if idea.missing_optional:
                idea.missing_required.extend(
                    f"optional:{x}" for x in idea.missing_optional
                )
    print(format_report(report, show_optional=True))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
