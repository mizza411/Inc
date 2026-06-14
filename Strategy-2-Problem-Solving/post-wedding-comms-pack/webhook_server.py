"""Paystack webhook server (run separately from Streamlit).

Usage:
  python webhook_server.py
  # POST https://your-host/paystack/webhook  (configure in Paystack dashboard)
"""

from __future__ import annotations

import hashlib
import hmac
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request

from payment_store import record_verified_payment

load_dotenv()

app = Flask(__name__)


def _check_basic_auth() -> bool:
    user = os.getenv("WEBHOOK_BASIC_USER", "").strip()
    password = os.getenv("WEBHOOK_BASIC_PASSWORD", "").strip()
    if not user or not password:
        return True
    auth = request.authorization
    return bool(auth and auth.username == user and auth.password == password)


def require_webhook_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not _check_basic_auth():
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return wrapped


def _verify_paystack_signature(body: bytes, signature: str) -> bool:
    secret = os.getenv("PAYSTACK_SECRET_KEY", "").strip()
    if not secret or not signature:
        return not os.getenv("PAYSTACK_WEBHOOK_STRICT", "").lower() in ("1", "true", "yes")
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha512).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.post("/paystack/webhook")
@require_webhook_auth
def paystack_webhook():
    body = request.get_data()
    signature = request.headers.get("x-paystack-signature", "")
    if not _verify_paystack_signature(body, signature):
        return {"error": "Invalid signature"}, 401

    event = request.get_json(silent=True) or {}
    if event.get("event") == "charge.success":
        data = event.get("data") or {}
        record_verified_payment(
            {
                "reference": data.get("reference"),
                "email": (data.get("customer") or {}).get("email"),
                "amount": data.get("amount"),
                "currency": data.get("currency"),
                "source": "webhook",
            }
        )
    return "OK", 200


if __name__ == "__main__":
    port = int(os.getenv("WEBHOOK_PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=False)
