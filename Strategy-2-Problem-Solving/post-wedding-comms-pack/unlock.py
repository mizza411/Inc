"""Payment unlock helpers for Streamlit session."""

from __future__ import annotations

from payment_store import is_reference_verified, record_verified_payment
from paystack_client import payments_configured, verify_transaction


def payments_required() -> bool:
    return payments_configured()


def is_unlocked(session: dict, *, reference: str | None = None) -> bool:
    if not payments_required():
        return True
    ref = reference or session.get("payment_reference") or session.get("unlocked_reference")
    if ref and (session.get("unlocked") or is_reference_verified(ref)):
        return True
    return bool(session.get("unlocked"))


def try_unlock_with_reference(reference: str) -> tuple[bool, str | None]:
    if not payments_required():
        return True, None
    if is_reference_verified(reference):
        return True, None
    result, err = verify_transaction(reference)
    if err:
        return False, err
    record_verified_payment({**result, "source": "verify_api"})
    return True, None
