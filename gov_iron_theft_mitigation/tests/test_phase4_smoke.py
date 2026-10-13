"""Phase 4 — WhatsApp stub parse + HTTP ops/webhook smoke."""

from __future__ import annotations

import json
import sys
import threading
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import app_web
from iron_protect.whatsapp_webhook import (
    STUB_VERIFY_TOKEN,
    WebhookError,
    parse_stub_payload,
    verify_stub_token,
)


class WebhookParseTests(unittest.TestCase):
    def test_flat_and_nested(self) -> None:
        flat = parse_stub_payload(
            {"message_id": "m1", "text": "hole", "lat": 9.0, "lon": 7.0}
        )
        self.assertEqual(flat.message_id, "m1")
        nested = parse_stub_payload(
            {
                "entry": [
                    {
                        "changes": [
                            {
                                "value": {
                                    "messages": [
                                        {
                                            "id": "wamid.1",
                                            "type": "text",
                                            "text": {"body": "Cover gone"},
                                            "location": {
                                                "latitude": 9.05,
                                                "longitude": 7.49,
                                            },
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(nested.message_id, "wamid.1")
        self.assertIn("Cover", nested.text)
        self.assertAlmostEqual(nested.lat or 0, 9.05)

    def test_bad_token(self) -> None:
        with self.assertRaises(WebhookError):
            verify_stub_token("nope")
        verify_stub_token(STUB_VERIFY_TOKEN)


class HttpPhase4Smoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app_web.reset_svc_for_tests(None)
        cls.httpd = HTTPServer(("127.0.0.1", 0), app_web.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()

    def _conn(self) -> HTTPConnection:
        return HTTPConnection("127.0.0.1", self.port, timeout=5)

    def test_health_and_ops_html(self) -> None:
        c = self._conn()
        c.request("GET", "/health")
        r = c.getresponse()
        body = json.loads(r.read().decode("utf-8"))
        self.assertEqual(r.status, 200)
        self.assertEqual(body.get("phase"), 4)
        c.request("GET", "/ops")
        r2 = c.getresponse()
        html = r2.read().decode("utf-8")
        self.assertEqual(r2.status, 200)
        self.assertIn("Public Iron Asset Protect", html)
        self.assertIn("Simulate WhatsApp", html)

    def test_webhook_creates_ticket(self) -> None:
        payload = {
            "message_id": "http-wa-1",
            "text": "Missing cover at junction",
            "lat": 9.05,
            "lon": 7.49,
        }
        raw = json.dumps(payload).encode("utf-8")
        c = self._conn()
        c.request(
            "POST",
            "/webhooks/whatsapp",
            body=raw,
            headers={
                "Content-Type": "application/json",
                "X-Stub-Token": STUB_VERIFY_TOKEN,
                "Content-Length": str(len(raw)),
            },
        )
        r = c.getresponse()
        data = json.loads(r.read().decode("utf-8"))
        self.assertEqual(r.status, 201)
        self.assertTrue(data.get("ok"))
        self.assertEqual(data["ticket"]["ticket_id"], "rpt-http-wa-1")

    def test_webhook_rejects_bad_token(self) -> None:
        raw = b'{"message_id":"x","text":"y"}'
        c = self._conn()
        c.request(
            "POST",
            "/webhooks/whatsapp",
            body=raw,
            headers={
                "Content-Type": "application/json",
                "X-Stub-Token": "wrong",
                "Content-Length": str(len(raw)),
            },
        )
        r = c.getresponse()
        self.assertEqual(r.status, 401)


if __name__ == "__main__":
    unittest.main()
