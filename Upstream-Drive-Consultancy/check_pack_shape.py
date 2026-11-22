"""Shape check for Upstream-Drive-Consultancy requirements pack (UDC-1)."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LINES = 500
REQUIRED = [
    "README.md",
    "company_requirements.md",
    "offer_lines.md",
    "risk_management_requirements.md",
    "lean_roles.md",
    "sources.md",
    "MANUAL_TEST.md",
    "brand_one_pager.md",
]

# phrase -> file that must contain it (substring, case-sensitive enough)
CUES: list[tuple[str, str]] = [
    ("Upstream Drive Consultancy", "README.md"),
    ("Nigeria-first", "README.md"),
    ("Physical security product", "README.md"),
    ("lean_roles.md", "README.md"),
    ("Professional indemnity", "company_requirements.md"),
    ("We certified you", "company_requirements.md"),
    ("Authorised testing", "offer_lines.md"),
    ("Risk management", "offer_lines.md"),
    ("residual risk", "risk_management_requirements.md"),
    ("R1 — Engagement lead", "lean_roles.md"),
    ("R3 — Authorised tester", "lean_roles.md"),
    ("check this", "sources.md"),
    ("Why not automated", "MANUAL_TEST.md"),
    ("brand_one_pager.md", "README.md"),
    ("What the firm refuses", "brand_one_pager.md"),
]


def main() -> int:
    errors: list[str] = []
    print(f"folder: {HERE}")

    for name in REQUIRED:
        path = HERE / name
        if not path.is_file():
            errors.append(f"missing {name}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        n = len(lines)
        print(f"  {n:4d}  {name}")
        if n > MAX_LINES:
            errors.append(f"{name} has {n} lines (max {MAX_LINES})")

    for phrase, name in CUES:
        text = (HERE / name).read_text(encoding="utf-8") if (HERE / name).is_file() else ""
        if phrase not in text:
            errors.append(f"{name} missing cue: {phrase!r}")

    # no slim terminology in pack body (owner: lean)
    for name in REQUIRED:
        path = HERE / name
        if not path.is_file():
            continue
        if "slim" in path.read_text(encoding="utf-8").lower():
            # allow MANUAL/history? none expected
            errors.append(f"{name} still contains 'slim' — use lean")

    docx = sorted(HERE.glob("*.docx"))
    if docx:
        print("docx:")
        for d in docx:
            print(f"  {d.name} ({d.stat().st_size // 1024} KB)")
    else:
        print("docx: (none yet)")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
