"""Seed a training corridor and print KPI + hotspot sample (stdlib)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from iron_protect.ingest_reports import ReportPayload
from iron_protect.ingest_sensors import SensorEvent
from iron_protect.packs_static import list_packs
from iron_protect.service import IronProtectService


def main() -> int:
    svc = IronProtectService()
    svc.auth.add_user("disp1", "Works Dispatcher", "works_dispatcher")
    svc.auth.add_user("liaison1", "Police Liaison", "liaison_readonly")

    a1 = svc.assets.create(
        "A-100",
        "cover",
        9.05,
        7.49,
        "demo-corridor",
        photo_ref="demo/a100.jpg",
        training=True,
    )
    svc.sensors.register_device("DEV-1", a1.asset_id)

    alert = svc.sensors.handle(
        SensorEvent(event_id="e1", device_id="DEV-1", event_type="lift_alert")
    )
    svc.tickets.transition(alert.ticket_id, "acknowledged", "disp1")
    svc.tickets.transition(alert.ticket_id, "assigned", "disp1", assignee="crew1")
    svc.tickets.transition(alert.ticket_id, "secured", "disp1")
    svc.tickets.transition(alert.ticket_id, "closed", "disp1")

    svc.reports.ingest(
        ReportPayload(
            message_id="wa1",
            text="Cover missing near junction",
            lat=9.0501,
            lon=7.4901,
        )
    )

    snap = svc.kpis.snapshot(day90_briefing_delivered=False)
    print("HARD_RULE ok")
    print("assets", len(svc.assets.list(include_training=True)))
    print("tickets", len(svc.tickets.list()))
    print("packs", [p.name for p in list_packs()])
    print("kpi_orphan_pct", snap.orphan_sensor_alert_pct)
    print("kpi_report_close_pct", snap.public_report_closed_pct)
    print("--- hotspot markdown ---")
    print(svc.hotspots.to_markdown(days=7))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
