"""Asset register CRUD and ID export."""

from __future__ import annotations

import csv
import io
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Literal

from .store import JsonStore

AssetType = Literal["cover", "railing", "barricade", "other"]
AssetStatus = Literal["present", "missing", "secured"]


@dataclass
class Asset:
    asset_id: str
    asset_type: AssetType
    lat: float
    lon: float
    corridor: str
    photo_ref: str
    public_mark: str
    status: AssetStatus
    last_check_at: str
    training: bool = False

    def to_row(self) -> dict:
        return asdict(self)


class AssetRegister:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def list(
        self,
        corridor: str | None = None,
        status: AssetStatus | None = None,
        include_training: bool = False,
    ) -> list[Asset]:
        out: list[Asset] = []
        for row in self.store.section("assets"):
            asset = self._from_row(row)
            if not include_training and asset.training:
                continue
            if corridor and asset.corridor != corridor:
                continue
            if status and asset.status != status:
                continue
            out.append(asset)
        return out

    def create(
        self,
        asset_id: str,
        asset_type: AssetType,
        lat: float,
        lon: float,
        corridor: str,
        photo_ref: str = "",
        public_mark: str | None = None,
        training: bool = False,
    ) -> Asset:
        if any(a.asset_id == asset_id for a in self.list(include_training=True)):
            raise ValueError(f"asset exists: {asset_id}")
        mark = public_mark or f"GOV-{asset_id}"
        now = _utc_now()
        asset = Asset(
            asset_id=asset_id,
            asset_type=asset_type,
            lat=lat,
            lon=lon,
            corridor=corridor,
            photo_ref=photo_ref,
            public_mark=mark,
            status="present",
            last_check_at=now,
            training=training,
        )
        rows = self.store.section("assets")
        rows.append(asset.to_row())
        self.store.replace_section("assets", rows)
        return asset

    def update_status(self, asset_id: str, status: AssetStatus) -> Asset:
        rows = self.store.section("assets")
        for row in rows:
            if row["asset_id"] == asset_id:
                row["status"] = status
                row["last_check_at"] = _utc_now()
                self.store.replace_section("assets", rows)
                return self._from_row(row)
        raise KeyError(asset_id)

    def get(self, asset_id: str) -> Asset:
        for a in self.list(include_training=True):
            if a.asset_id == asset_id:
                return a
        raise KeyError(asset_id)

    def export_csv(self, include_training: bool = False) -> str:
        buf = io.StringIO()
        writer = csv.DictWriter(
            buf,
            fieldnames=[
                "asset_id",
                "public_mark",
                "asset_type",
                "lat",
                "lon",
                "corridor",
                "status",
                "last_check_at",
            ],
        )
        writer.writeheader()
        for asset in self.list(include_training=include_training):
            writer.writerow(
                {
                    "asset_id": asset.asset_id,
                    "public_mark": asset.public_mark,
                    "asset_type": asset.asset_type,
                    "lat": asset.lat,
                    "lon": asset.lon,
                    "corridor": asset.corridor,
                    "status": asset.status,
                    "last_check_at": asset.last_check_at,
                }
            )
        return buf.getvalue()

    @staticmethod
    def _from_row(row: dict) -> Asset:
        return Asset(
            asset_id=row["asset_id"],
            asset_type=row["asset_type"],
            lat=float(row["lat"]),
            lon=float(row["lon"]),
            corridor=row["corridor"],
            photo_ref=row.get("photo_ref", ""),
            public_mark=row["public_mark"],
            status=row["status"],
            last_check_at=row["last_check_at"],
            training=bool(row.get("training", False)),
        )


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
