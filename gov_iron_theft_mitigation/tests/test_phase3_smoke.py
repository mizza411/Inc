"""Phase 3 automated smoke — domain modules + KPI math."""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from iron_protect.ingest_reports import ReportPayload
from iron_protect.ingest_sensors import SensorEvent
from iron_protect.packs_static import list_packs, read_pack
from iron_protect.service import IronProtectService
from iron_protect.tickets import TRANSITIONS


class Phase3Smoke(unittest.TestCase):
    def setUp(self) -> None:
        self.svc = IronProtectService()
        self.svc.auth.add_user("disp1", "Dispatcher", "works_dispatcher")
        self.svc.auth.add_user("ro1", "Liaison", "liaison_readonly")

    def test_asset_register_and_csv(self) -> None:
        a = self.svc.assets.create(
            "A1", "cover", 9.0, 7.0, "c1", training=True
        )
        self.assertEqual(a.public_mark, "GOV-A1")
        csv_text = self.svc.assets.export_csv(include_training=True)
        self.assertIn("A1", csv_text)
        self.assertIn("public_mark", csv_text)

    def test_ticket_state_machine_and_readonly(self) -> None:
        t = self.svc.tickets.create("T1", "public_report", text="hole")
        self.svc.tickets.transition("T1", "acknowledged", "disp1")
        with self.assertRaises(PermissionError):
            self.svc.tickets.transition("T1", "assigned", "ro1")
        self.svc.tickets.transition("T1", "assigned", "disp1")
        self.svc.tickets.transition("T1", "secured", "disp1")
        self.svc.tickets.transition("T1", "closed", "disp1")
        self.assertEqual(self.svc.tickets.get("T1").state, "closed")
        self.assertIn("closed", TRANSITIONS["secured"])

    def test_report_nearest_match(self) -> None:
        self.svc.assets.create("A2", "cover", 9.1, 7.2, "c2")
        ticket = self.svc.reports.ingest(
            ReportPayload("m1", "missing", lat=9.1001, lon=7.2001)
        )
        self.assertEqual(ticket.asset_id, "A2")
        self.assertEqual(ticket.kind, "public_report")

    def test_sensor_lift_and_offline(self) -> None:
        self.svc.assets.create("A3", "cover", 9.2, 7.3, "c3")
        self.svc.sensors.register_device("D1", "A3")
        alert = self.svc.sensors.handle(
            SensorEvent("e1", "D1", "lift_alert")
        )
        self.assertEqual(alert.kind, "sensor_alert")
        self.assertEqual(self.svc.assets.get("A3").status, "missing")
        self.svc.sensors.handle(SensorEvent("e2", "D1", "offline"))
        self.assertTrue(any(d.device_id == "D1" for d in self.svc.sensors.list_offline()))

    def test_kpi_orphan_and_ack(self) -> None:
        self.svc.assets.create("A4", "cover", 9.3, 7.4, "c4")
        self.svc.sensors.register_device("D2", "A4")
        alert = self.svc.sensors.handle(
            SensorEvent("e3", "D2", "lift_alert")
        )
        # orphan until ack
        snap0 = self.svc.kpis.snapshot()
        self.assertEqual(snap0.orphan_sensor_alert_pct, 100.0)
        self.svc.tickets.transition(alert.ticket_id, "acknowledged", "disp1")
        # backdate ack within 30 min by rewriting store row
        rows = self.svc.store.section("tickets")
        for row in rows:
            if row["ticket_id"] == alert.ticket_id:
                created = datetime.fromisoformat(row["created_at"])
                row["acknowledged_at"] = (
                    created + timedelta(minutes=10)
                ).isoformat()
        self.svc.store.replace_section("tickets", rows)
        snap1 = self.svc.kpis.snapshot()
        self.assertEqual(snap1.orphan_sensor_alert_pct, 0.0)
        self.assertIsNotNone(snap1.alert_ack_median_minutes)
        self.assertLessEqual(snap1.alert_ack_median_minutes or 999, 30)

    def test_hotspot_and_packs(self) -> None:
        self.svc.assets.create("A5", "barricade", 9.4, 7.5, "hot-c")
        self.svc.tickets.create(
            "T-hot", "public_report", asset_id="A5", text="x"
        )
        md = self.svc.hotspots.to_markdown()
        self.assertIn("hot-c", md)
        self.assertIn("bypass", md.lower())  # states no bypass
        packs = list_packs()
        self.assertEqual(len(packs), 2)
        notice = read_pack("yard_notice")
        self.assertIn("Do not buy", notice)

    def test_training_assets_hidden_by_default(self) -> None:
        self.svc.assets.create(
            "TR1", "cover", 1.0, 1.0, "train", training=True
        )
        self.assertEqual(len(self.svc.assets.list()), 0)
        self.assertEqual(len(self.svc.assets.list(include_training=True)), 1)


if __name__ == "__main__":
    unittest.main()
