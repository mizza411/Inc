"""AUTO-NAR-08 — regenerate playbook .docx via pandoc."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from .paths import PACKAGE_DIR

PLAYBOOK_MD = PACKAGE_DIR / "ask_people_ask_owners_playbook.md"
PLAYBOOK_DOCX = PACKAGE_DIR / "ask_people_ask_owners_playbook.docx"
MIN_DOCX_BYTES = 500


def build_docx(*, check_only: bool = False) -> Path:
    if not PLAYBOOK_MD.is_file():
        raise FileNotFoundError(f"Missing playbook: {PLAYBOOK_MD}")
    if check_only:
        if not PLAYBOOK_DOCX.is_file():
            raise FileNotFoundError(f"Missing docx: {PLAYBOOK_DOCX}")
        size = PLAYBOOK_DOCX.stat().st_size
        if size < MIN_DOCX_BYTES:
            raise ValueError(f"docx too small ({size} bytes): {PLAYBOOK_DOCX}")
        return PLAYBOOK_DOCX

    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("pandoc not found on PATH")
    subprocess.run(
        [pandoc, str(PLAYBOOK_MD), "-o", str(PLAYBOOK_DOCX)],
        check=True,
    )
    size = PLAYBOOK_DOCX.stat().st_size
    if size < MIN_DOCX_BYTES:
        raise ValueError(f"docx too small after build ({size} bytes)")
    return PLAYBOOK_DOCX


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    check_only = "--check" in args
    try:
        path = build_docx(check_only=check_only)
    except (FileNotFoundError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK {'check' if check_only else 'build'}: {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
