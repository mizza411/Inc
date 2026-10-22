"""AUTO-NAR-09 — isolation / path allowlist checks."""

from __future__ import annotations

from .paths import INC_ROOT, PACKAGE_DIR


REQUIRED_PACKAGE_FILES = (
    "README.md",
    "ask_people_ask_owners_playbook.md",
    "config.example.json",
    "MANUAL_TEST.md",
    "config_loader.py",
    "rotate.py",
    "ask_log.py",
    "status_report.py",
    "openers.py",
    "hub_nudge.py",
    "build_docx.py",
    "pr_launcher.py",
    "cli.py",
)

CROSS_LINK_MARKER = "NET-ASK-REMIND-1"
STRATEGY3_README = (
    INC_ROOT
    / "Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification"
    / "README.md"
)
STRATEGY4_README = (
    INC_ROOT
    / "Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection"
    / "README.md"
)
LAUNCHER_CONFIG = INC_ROOT / "inc_launcher" / "launcher_config.json"

FORBIDDEN_ARTIFACTS = (
    PACKAGE_DIR / "inc_hub_hook.py",
    PACKAGE_DIR / "detached_toast.py",
)


def run_isolation_checks() -> list[str]:
    """Return list of error strings; empty means pass."""
    errors: list[str] = []

    for name in REQUIRED_PACKAGE_FILES:
        path = PACKAGE_DIR / name
        if not path.is_file():
            errors.append(f"missing package file: {name}")

    for readme in (STRATEGY3_README, STRATEGY4_README):
        if not readme.is_file():
            errors.append(f"missing strategy README: {readme}")
            continue
        text = readme.read_text(encoding="utf-8")
        if CROSS_LINK_MARKER not in text:
            errors.append(f"cross-link marker missing in {readme.name}")

    for path in FORBIDDEN_ARTIFACTS:
        if path.exists():
            errors.append(f"isolation: unexpected artifact {path.name}")

    for py in PACKAGE_DIR.glob("*.py"):
        src = py.read_text(encoding="utf-8")
        for bad in ("tegrid_re_gtm", "field_intelligence_radar", "inc_launcher"):
            if f"import {bad}" in src or f"from {bad}" in src:
                errors.append(f"{py.name} imports {bad} (not allowed)")

    if LAUNCHER_CONFIG.is_file():
        raw = LAUNCHER_CONFIG.read_text(encoding="utf-8")
        if '"network_ask_remind"' not in raw:
            errors.append("launcher_config missing network_ask_remind card")
        if '"network_ask_mwf"' not in raw:
            errors.append("launcher_config missing network_ask_mwf schedule")
        if "agent_formulation_run" not in raw:
            errors.append("launcher_config lost agent_formulation_run (regression)")
    else:
        errors.append("inc_launcher/launcher_config.json missing")

    return errors
