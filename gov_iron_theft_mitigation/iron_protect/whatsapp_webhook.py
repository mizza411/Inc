"""WhatsApp-shaped webhook stub (pilot). Not live Meta credentials."""

from __future__ import annotations

from typing import Any

from .ingest_reports import ReportPayload

# Documented stub token for local / pilot demos. Not a production secret store.
STUB_VERIFY_TOKEN = "iron-protect-pilot-stub"


class WebhookError(ValueError):
    pass


def verify_stub_token(provided: str | None) -> None:
    if provided != STUB_VERIFY_TOKEN:
        raise WebhookError("invalid stub token")


def parse_stub_payload(body: dict[str, Any]) -> ReportPayload:
    """
    Accept either a flat pilot JSON or a tiny WhatsApp Cloud-like slice.

    Flat:
      {"message_id": "...", "text": "...", "lat": 9.0, "lon": 7.0}

    Nested stub:
      {"entry":[{"changes":[{"value":{"messages":[{
          "id":"...","type":"text","text":{"body":"..."},
          "location":{"latitude":9.0,"longitude":7.0}
      }]}}]}]}
    """
    if "message_id" in body and "text" in body:
        return ReportPayload(
            message_id=str(body["message_id"]),
            text=str(body["text"]),
            lat=_opt_float(body.get("lat")),
            lon=_opt_float(body.get("lon")),
        )
    try:
        msg = body["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError, TypeError) as exc:
        raise WebhookError("unrecognized webhook shape") from exc

    message_id = str(msg.get("id") or "")
    if not message_id:
        raise WebhookError("missing message id")

    text = ""
    if msg.get("type") == "text":
        text = str((msg.get("text") or {}).get("body") or "")
    elif msg.get("type") == "location":
        text = str(msg.get("text") or "location report")
    else:
        text = str(msg.get("text") or body.get("text") or "citizen report")

    lat = lon = None
    loc = msg.get("location") or {}
    if "latitude" in loc:
        lat = _opt_float(loc.get("latitude"))
        lon = _opt_float(loc.get("longitude"))

    if not text.strip():
        text = "citizen report (empty body)"

    return ReportPayload(message_id=message_id, text=text, lat=lat, lon=lon)


def _opt_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)
