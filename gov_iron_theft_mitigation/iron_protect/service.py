"""Facade wiring all Phase 3 modules."""

from __future__ import annotations

from pathlib import Path

from .assets import AssetRegister
from .auth_roles import AuthService
from .hotspots import HotspotPack
from .ingest_reports import ReportIngest
from .ingest_sensors import SensorIngest
from .kpis import KpiService
from .store import JsonStore
from .tickets import TicketService


class IronProtectService:
    def __init__(self, data_path: Path | None = None) -> None:
        self.store = JsonStore(data_path)
        self.auth = AuthService(self.store)
        self.assets = AssetRegister(self.store)
        self.tickets = TicketService(self.store, self.auth)
        self.reports = ReportIngest(self.assets, self.tickets)
        self.sensors = SensorIngest(self.store, self.assets, self.tickets)
        self.hotspots = HotspotPack(self.assets, self.tickets)
        self.kpis = KpiService(self.tickets)
