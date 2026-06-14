"""Automated tests for Paystack payment modules (mocked HTTP)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import payment_store
import paystack_client
import unlock
from webhook_server import app as webhook_app


class PaystackClientTests(unittest.TestCase):
    def test_payments_disabled_when_no_key(self):
        with patch.dict(os.environ, {"PAYSTACK_SECRET_KEY": "", "PAYMENTS_DISABLED": ""}, clear=False):
            self.assertFalse(paystack_client.payments_configured())

    def test_payments_disabled_flag(self):
        with patch.dict(
            os.environ,
            {"PAYSTACK_SECRET_KEY": "sk_test_x", "PAYMENTS_DISABLED": "true"},
            clear=False,
        ):
            self.assertFalse(paystack_client.payments_configured())

    @patch("paystack_client.requests.post")
    def test_initialize_success(self, mock_post):
        mock_post.return_value = MagicMock(
            ok=True,
            json=lambda: {
                "status": True,
                "data": {
                    "authorization_url": "https://checkout.paystack.com/abc",
                    "access_code": "acc",
                    "reference": "PWC_test_1",
                },
            },
        )
        with patch.dict(os.environ, {"PAYSTACK_SECRET_KEY": "sk_test_x"}, clear=False):
            data, err = paystack_client.initialize_transaction("couple@example.com")
        self.assertIsNone(err)
        self.assertEqual(data["reference"], "PWC_test_1")

    @patch("paystack_client.requests.get")
    def test_verify_success(self, mock_get):
        mock_get.return_value = MagicMock(
            ok=True,
            json=lambda: {
                "status": True,
                "data": {
                    "status": "success",
                    "reference": "PWC_test_1",
                    "amount": 2500000,
                    "currency": "NGN",
                    "customer": {"email": "couple@example.com"},
                    "paid_at": "2026-06-14T12:00:00.000Z",
                },
            },
        )
        with patch.dict(os.environ, {"PAYSTACK_SECRET_KEY": "sk_test_x"}, clear=False):
            data, err = paystack_client.verify_transaction("PWC_test_1")
        self.assertIsNone(err)
        self.assertEqual(data["reference"], "PWC_test_1")


class PaymentStoreTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._store = Path(self._tmpdir.name) / "verified.json"
        self._env_patch = patch.dict(
            os.environ, {"PAYMENT_STORE_PATH": str(self._store)}, clear=False
        )
        self._env_patch.start()

    def tearDown(self):
        self._env_patch.stop()
        self._tmpdir.cleanup()

    def test_record_and_check_reference(self):
        payment_store.record_verified_payment({"reference": "REF123", "email": "a@b.com"})
        self.assertTrue(payment_store.is_reference_verified("REF123"))
        self.assertFalse(payment_store.is_reference_verified("OTHER"))


class UnlockTests(unittest.TestCase):
    def test_unlock_when_payments_disabled(self):
        with patch.dict(os.environ, {"PAYMENTS_DISABLED": "1"}, clear=False):
            self.assertFalse(unlock.payments_required())
            self.assertTrue(unlock.is_unlocked({}))

    @patch("unlock.verify_transaction")
    def test_try_unlock_records_payment(self, mock_verify):
        mock_verify.return_value = (
            {"reference": "REF999", "amount": 2500000, "email": "x@y.com"},
            None,
        )
        with patch.dict(
            os.environ,
            {"PAYSTACK_SECRET_KEY": "sk_test", "PAYMENTS_DISABLED": "", "PAYMENT_STORE_PATH": ""},
            clear=False,
        ):
            with tempfile.TemporaryDirectory() as td:
                store = Path(td) / "v.json"
                with patch.dict(os.environ, {"PAYMENT_STORE_PATH": str(store)}, clear=False):
                    ok, err = unlock.try_unlock_with_reference("REF999")
                    self.assertTrue(ok)
                    self.assertIsNone(err)
                    self.assertTrue(payment_store.is_reference_verified("REF999"))


class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.client = webhook_app.test_client()
        self._tmpdir = tempfile.TemporaryDirectory()
        self._store = Path(self._tmpdir.name) / "verified.json"
        patch.dict(os.environ, {"PAYMENT_STORE_PATH": str(self._store)}, clear=False).start()

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)

    def test_webhook_charge_success(self):
        payload = {
            "event": "charge.success",
            "data": {
                "reference": "WH_REF_1",
                "amount": 2500000,
                "currency": "NGN",
                "customer": {"email": "c@d.com"},
            },
        }
        with patch.dict(os.environ, {"PAYSTACK_WEBHOOK_STRICT": ""}, clear=False):
            resp = self.client.post(
                "/paystack/webhook",
                data=json.dumps(payload),
                content_type="application/json",
            )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(payment_store.is_reference_verified("WH_REF_1"))


if __name__ == "__main__":
    unittest.main()
