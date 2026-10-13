"""Phase 4 ops desk + WhatsApp webhook stub (stdlib HTTP)."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from iron_protect.ingest_reports import ReportPayload
from iron_protect.service import IronProtectService
from iron_protect.web_ui import ops_body, page
from iron_protect.whatsapp_webhook import (
    STUB_VERIFY_TOKEN,
    WebhookError,
    parse_stub_payload,
    verify_stub_token,
)

_SVC: IronProtectService | None = None


def get_svc() -> IronProtectService:
    global _SVC
    if _SVC is None:
        data = ROOT / "data" / "pilot_demo.json"
        _SVC = IronProtectService(data)
        if not _SVC.auth.list_users():
            _SVC.auth.add_user("disp1", "Works Dispatcher", "works_dispatcher")
            _SVC.auth.add_user("ict1", "ICT Admin", "ict_admin")
            _SVC.auth.add_user("liaison1", "Liaison", "liaison_readonly")
    return _SVC


def reset_svc_for_tests(path: Path | None = None) -> IronProtectService:
    """Test helper: force a fresh in-memory or temp store."""
    global _SVC
    _SVC = IronProtectService(path)
    _SVC.auth.add_user("disp1", "Works Dispatcher", "works_dispatcher")
    return _SVC


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        svc = get_svc()
        if path == "/ops":
            self._ops("")
            return
        if path in {"/", "/health"}:
            body = {
                "ok": True,
                "service": "iron_protect",
                "phase": 4,
                "ops": "/ops",
                "webhook": "/webhooks/whatsapp",
            }
            self._send(200, json.dumps(body, indent=2).encode("utf-8") + b"\n", "application/json")
            return
        if path == "/assets":
            rows = [a.to_row() for a in svc.assets.list(include_training=True)]
            self._json(200, rows)
            return
        if path == "/tickets":
            self._json(200, [t.to_row() for t in svc.tickets.list()])
            return
        if path == "/kpis":
            self._json(200, svc.kpis.snapshot().__dict__)
            return
        if path == "/hotspots.md":
            self._send(
                200,
                svc.hotspots.to_markdown().encode("utf-8"),
                "text/markdown; charset=utf-8",
            )
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        svc = get_svc()

        if path == "/webhooks/whatsapp":
            try:
                verify_stub_token(self.headers.get("X-Stub-Token"))
                body = json.loads(raw.decode("utf-8") or "{}")
                payload = parse_stub_payload(body)
                ticket = svc.reports.ingest(payload)
                self._json(201, {"ok": True, "ticket": ticket.to_row()})
            except WebhookError as exc:
                self._json(401 if "token" in str(exc) else 400, {"ok": False, "error": str(exc)})
            except json.JSONDecodeError:
                self._json(400, {"ok": False, "error": "invalid json"})
            except Exception as exc:  # noqa: BLE001 — surface ops errors
                self._json(400, {"ok": False, "error": str(exc)})
            return

        if path == "/ops/simulate-wa":
            form = parse_qs(raw.decode("utf-8"))
            try:
                payload = ReportPayload(
                    message_id=_form(form, "message_id"),
                    text=_form(form, "text"),
                    lat=_form_float(form, "lat"),
                    lon=_form_float(form, "lon"),
                )
                ticket = svc.reports.ingest(payload)
                self._ops(f"Created ticket {ticket.ticket_id}")
            except Exception as exc:  # noqa: BLE001
                self._ops(f"Error: {exc}")
            return

        if path == "/ops/transition":
            form = parse_qs(raw.decode("utf-8"))
            try:
                tid = _form(form, "ticket_id")
                state = _form(form, "new_state")
                actor = _form(form, "actor") or "disp1"
                ticket = svc.tickets.transition(tid, state, actor)  # type: ignore[arg-type]
                self._ops(f"Ticket {ticket.ticket_id} -> {ticket.state}")
            except Exception as exc:  # noqa: BLE001
                self._ops(f"Error: {exc}")
            return

        if path == "/ops/seed-asset":
            form = parse_qs(raw.decode("utf-8"))
            try:
                asset = svc.assets.create(
                    _form(form, "asset_id"),
                    "cover",
                    float(_form(form, "lat") or "9.05"),
                    float(_form(form, "lon") or "7.49"),
                    _form(form, "corridor") or "pilot-corridor",
                    training=True,
                )
                self._ops(f"Seeded asset {asset.asset_id} mark {asset.public_mark}")
            except Exception as exc:  # noqa: BLE001
                self._ops(f"Error: {exc}")
            return

        self._json(404, {"error": "not_found"})

    def _ops(self, flash: str) -> None:
        svc = get_svc()
        snap = svc.kpis.snapshot().__dict__
        body = ops_body(
            flash=flash,
            tickets=[t.to_row() for t in svc.tickets.list()],
            assets=[a.to_row() for a in svc.assets.list(include_training=True)],
            kpis=snap,
        )
        html_doc = page("Ops — Iron Protect", body).encode("utf-8")
        self._send(200, html_doc, "text/html; charset=utf-8")

    def _json(self, code: int, obj: object) -> None:
        self._send(
            code,
            json.dumps(obj, indent=2).encode("utf-8") + b"\n",
            "application/json",
        )

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("web: " + (fmt % args) + "\n")

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _form(form: dict, key: str) -> str:
    vals = form.get(key) or [""]
    return (vals[0] or "").strip()


def _form_float(form: dict, key: str) -> float | None:
    raw = _form(form, key)
    if not raw:
        return None
    return float(raw)


def main() -> int:
    host, port = "127.0.0.1", 8765
    server = HTTPServer((host, port), Handler)
    print(f"iron_protect ops http://{host}:{port}/ops")
    print(f"webhook POST /webhooks/whatsapp  X-Stub-Token: {STUB_VERIFY_TOKEN}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
