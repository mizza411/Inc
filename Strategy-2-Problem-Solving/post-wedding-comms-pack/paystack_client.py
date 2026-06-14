"""Paystack initialize + verify API client."""

from __future__ import annotations

import os
import secrets
import time
from typing import Any

import requests

PAYSTACK_BASE = "https://api.paystack.co"


def _secret_key() -> str | None:
    key = os.getenv("PAYSTACK_SECRET_KEY", "").strip()
    return key or None


def payments_configured() -> bool:
    return _secret_key() is not None and os.getenv("PAYMENTS_DISABLED", "").lower() not in (
        "1",
        "true",
        "yes",
    )


def default_amount_kobo() -> int:
    return int(os.getenv("PAYSTACK_AMOUNT_KOBO", "1000000"))


def generate_reference() -> str:
    return f"PWC_{int(time.time())}_{secrets.token_hex(4)}"


def initialize_transaction(
    email: str,
    *,
    amount_kobo: int | None = None,
    callback_url: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, str | None]:
    secret = _secret_key()
    if not secret:
        return None, "PAYSTACK_SECRET_KEY not configured."

    email = email.strip()
    if not email or "@" not in email:
        return None, "Valid email required for Paystack."

    payload: dict[str, Any] = {
        "email": email,
        "amount": amount_kobo if amount_kobo is not None else default_amount_kobo(),
        "reference": generate_reference(),
        "currency": os.getenv("PAYSTACK_CURRENCY", "NGN"),
        "metadata": metadata or {"product": "post-wedding-comms-pack"},
    }
    cb = callback_url or os.getenv("PAYSTACK_CALLBACK_URL", "").strip()
    if cb:
        payload["callback_url"] = cb

    try:
        resp = requests.post(
            f"{PAYSTACK_BASE}/transaction/initialize",
            json=payload,
            headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"},
            timeout=30,
        )
        body = resp.json()
        if not resp.ok or not body.get("status"):
            msg = body.get("message", resp.text)
            return None, f"Paystack initialize failed: {msg}"
        data = body["data"]
        return {
            "authorization_url": data["authorization_url"],
            "access_code": data.get("access_code"),
            "reference": data["reference"],
            "amount_kobo": payload["amount"],
        }, None
    except requests.RequestException as exc:
        return None, str(exc)


def verify_transaction(reference: str) -> tuple[dict[str, Any] | None, str | None]:
    secret = _secret_key()
    if not secret:
        return None, "PAYSTACK_SECRET_KEY not configured."

    reference = reference.strip()
    if not reference:
        return None, "Payment reference is required."

    try:
        resp = requests.get(
            f"{PAYSTACK_BASE}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {secret}"},
            timeout=30,
        )
        body = resp.json()
        if not resp.ok or not body.get("status"):
            msg = body.get("message", resp.text)
            return None, f"Paystack verify failed: {msg}"
        data = body["data"]
        if data.get("status") != "success":
            return None, f"Payment status: {data.get('status', 'unknown')}"
        return {
            "reference": data["reference"],
            "amount": data.get("amount"),
            "currency": data.get("currency"),
            "email": (data.get("customer") or {}).get("email"),
            "paid_at": data.get("paid_at"),
        }, None
    except requests.RequestException as exc:
        return None, str(exc)
