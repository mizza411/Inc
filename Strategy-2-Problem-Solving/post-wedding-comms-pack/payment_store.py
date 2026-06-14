"""Persist verified Paystack references (webhook + manual verify)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parent / "data" / "verified_payments.json"


def _store_path() -> Path:
    raw = os.getenv("PAYMENT_STORE_PATH", "").strip()
    return Path(raw) if raw else DEFAULT_STORE


def _load() -> list[dict]:
    path = _store_path()
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(records: list[dict]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def is_reference_verified(reference: str) -> bool:
    reference = reference.strip()
    return any(r.get("reference") == reference for r in _load())


def record_verified_payment(record: dict) -> None:
    reference = record.get("reference", "").strip()
    if not reference:
        return
    records = _load()
    if any(r.get("reference") == reference for r in records):
        return
    entry = {
        "reference": reference,
        "email": record.get("email"),
        "amount": record.get("amount"),
        "currency": record.get("currency", "NGN"),
        "verified_at": record.get("verified_at")
        or datetime.now(timezone.utc).isoformat(),
        "source": record.get("source", "verify"),
    }
    records.append(entry)
    _save(records)
