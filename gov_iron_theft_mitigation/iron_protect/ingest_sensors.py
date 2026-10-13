"""Sensor alert intake for pilot devices. Ops visibility only."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from .assets import AssetRegister
from .store import JsonStore
from .tickets import TicketService


@dataclass
class Device:
    device_id: str
    asset_id: str
    last_heartbeat_at: str
    online: bool = True


@dataclass
class SensorEvent:
    event_id: str
    device_id: str
    event_type: str  # lift_alert | heartbeat | offline
    at: str | None = None


class SensorIngest:
    def __init__(
        self,
        store: JsonStore,
        assets: AssetRegister,
        tickets: TicketService,
    ) -> None:
        self.store = store
        self.assets = assets
        self.tickets = tickets

    def register_device(self, device_id: str, asset_id: str) -> Device:
        self.assets.get(asset_id)  # must exist
        if any(d["device_id"] == device_id for d in self.store.section("devices")):
            raise ValueError(f"device exists: {device_id}")
        device = Device(
            device_id=device_id,
            asset_id=asset_id,
            last_heartbeat_at=_utc_now(),
            online=True,
        )
        rows = self.store.section("devices")
        rows.append(asdict(device))
        self.store.replace_section("devices", rows)
        return device

    def handle(self, event: SensorEvent):
        device = self._get_device(event.device_id)
        at = event.at or _utc_now()
        if event.event_type == "heartbeat":
            return self._heartbeat(device, at)
        if event.event_type == "offline":
            return self._mark_offline(device, at, event.event_id)
        if event.event_type == "lift_alert":
            return self._lift_alert(device, at, event.event_id)
        raise ValueError(f"unknown event_type: {event.event_type}")

    def list_offline(self) -> list[Device]:
        return [
            self._from_row(r)
            for r in self.store.section("devices")
            if not r.get("online", True)
        ]

    def _heartbeat(self, device: Device, at: str) -> Device:
        return self._write_device(
            device.device_id,
            last_heartbeat_at=at,
            online=True,
        )

    def _mark_offline(self, device: Device, at: str, event_id: str):
        self._write_device(device.device_id, last_heartbeat_at=at, online=False)
        return self.tickets.create(
            f"off-{event_id}",
            "device_offline",
            asset_id=device.asset_id,
            text=f"device_offline:{device.device_id}",
        )

    def _lift_alert(self, device: Device, at: str, event_id: str):
        self.assets.update_status(device.asset_id, "missing")
        return self.tickets.create(
            f"sns-{event_id}",
            "sensor_alert",
            asset_id=device.asset_id,
            text=f"lift_alert:{device.device_id}",
            confirmed_missing=True,
        )

    def _get_device(self, device_id: str) -> Device:
        for row in self.store.section("devices"):
            if row["device_id"] == device_id:
                return self._from_row(row)
        raise KeyError(device_id)

    def _write_device(self, device_id: str, **fields) -> Device:
        rows = self.store.section("devices")
        for row in rows:
            if row["device_id"] == device_id:
                row.update(fields)
                self.store.replace_section("devices", rows)
                return self._from_row(row)
        raise KeyError(device_id)

    @staticmethod
    def _from_row(row: dict) -> Device:
        return Device(
            device_id=row["device_id"],
            asset_id=row["asset_id"],
            last_heartbeat_at=row["last_heartbeat_at"],
            online=bool(row.get("online", True)),
        )


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
