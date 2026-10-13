"""Citizen report intake (WhatsApp / webhook shaped). No bypass content."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .assets import AssetRegister
from .tickets import TicketService


@dataclass
class ReportPayload:
    message_id: str
    text: str
    lat: float | None = None
    lon: float | None = None


class ReportIngest:
    """Maps a public report into a ticket, optionally nearest asset."""

    def __init__(self, assets: AssetRegister, tickets: TicketService) -> None:
        self.assets = assets
        self.tickets = tickets

    def ingest(self, payload: ReportPayload, *, match_radius_m: float = 150.0):
        asset_id = None
        if payload.lat is not None and payload.lon is not None:
            asset_id = self._nearest_asset_id(
                payload.lat, payload.lon, match_radius_m
            )
        ticket_id = f"rpt-{payload.message_id}"
        return self.tickets.create(
            ticket_id,
            "public_report",
            asset_id=asset_id,
            text=payload.text.strip(),
            confirmed_missing=asset_id is not None,
        )

    def _nearest_asset_id(
        self, lat: float, lon: float, radius_m: float
    ) -> str | None:
        best_id = None
        best_d = radius_m
        for asset in self.assets.list(include_training=True):
            d = _haversine_m(lat, lon, asset.lat, asset.lon)
            if d <= best_d:
                best_d = d
                best_id = asset.asset_id
        return best_id


def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))
