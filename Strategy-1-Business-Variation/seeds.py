"""Load Strategy 1 seed businesses from JSON (editable, not hardcoded forever)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

STRATEGY_DIR = Path(__file__).resolve().parent
DEFAULT_SEEDS_PATH = STRATEGY_DIR / "seed_businesses.json"


def load_seeds(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Return list of business dicts from seed_businesses.json (or override path)."""
    seeds_path = Path(path) if path else DEFAULT_SEEDS_PATH
    if not seeds_path.exists():
        raise FileNotFoundError(f"Seeds file not found: {seeds_path}")
    data = json.loads(seeds_path.read_text(encoding="utf-8"))
    businesses = data.get("businesses")
    if not isinstance(businesses, list):
        raise ValueError(f"Invalid seeds file (missing businesses list): {seeds_path}")
    return businesses


def find_seed_by_id(businesses: List[Dict[str, Any]], business_id: str) -> Optional[Dict[str, Any]]:
    key = business_id.strip().lower()
    for b in businesses:
        if str(b.get("id", "")).lower() == key:
            return b
    return None


def find_seed_by_name(businesses: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    key = name.strip().lower()
    for b in businesses:
        if str(b.get("name", "")).lower() == key:
            return b
    return None
