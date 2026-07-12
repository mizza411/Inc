"""Strategy 1 seed businesses — RETIRED (§11 Phase B).

Live intake uses URL-cited --inputs / interactive paste in complaint_intake.py.
Archived copy: _archive/seed_businesses.json
"""

from __future__ import annotations

from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
ARCHIVED_SEEDS_PATH = STRATEGY_DIR / "_archive" / "seed_businesses.json"
# Kept for import compatibility; do not use as live input.
DEFAULT_SEEDS_PATH = ARCHIVED_SEEDS_PATH


def load_seeds(*_args, **_kwargs):
    raise RuntimeError(
        "seed_businesses.json is retired (task §11 Phase B). "
        "Use --non-interactive --inputs <json> with success_url + complaint source_url, "
        "or run interactively and paste http(s) URLs. "
        f"Archive (reference only): {ARCHIVED_SEEDS_PATH}"
    )


def find_seed_by_id(*_args, **_kwargs):
    raise RuntimeError("seed lookup retired — use URL-cited --inputs instead")


def find_seed_by_name(*_args, **_kwargs):
    raise RuntimeError("seed lookup retired — use URL-cited --inputs instead")
