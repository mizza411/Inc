"""Pilot KPI counters aligned to PHASE_1_REQUIREMENTS / gov proposal."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .tickets import TicketService

DEFAULT_ACK_MINUTES = 30
DEFAULT_SECURE_HOURS = 4
DEFAULT_REPORT_CLOSE_PCT = 90.0
DEFAULT_ORPHAN_PCT = 5.0


@dataclass
class KpiSnapshot:
    alert_ack_median_minutes: float | None
    alert_ack_within_sla_pct: float | None
    secure_median_hours: float | None
    secure_within_sla_pct: float | None
    public_report_closed_pct: float | None
    orphan_sensor_alert_pct: float | None
    day90_briefing_delivered: bool
    pass_ack_sla: bool | None
    pass_secure_sla: bool | None
    pass_report_close: bool | None
    pass_orphan: bool | None


class KpiService:
    def __init__(self, tickets: TicketService) -> None:
        self.tickets = tickets

    def snapshot(self, *, day90_briefing_delivered: bool = False) -> KpiSnapshot:
        tickets = self.tickets.list()
        sensor = [t for t in tickets if t.kind == "sensor_alert"]
        reports = [t for t in tickets if t.kind == "public_report"]

        ack_mins = []
        for t in sensor:
            if t.acknowledged_at:
                ack_mins.append(
                    _minutes(t.created_at, t.acknowledged_at)
                )
        orphan = [t for t in sensor if not t.acknowledged_at]

        secure_hours = []
        for t in tickets:
            if t.secured_at and t.confirmed_missing_at:
                secure_hours.append(
                    _hours(t.confirmed_missing_at, t.secured_at)
                )

        closed_reports = [t for t in reports if t.state == "closed"]
        report_pct = (
            (100.0 * len(closed_reports) / len(reports)) if reports else None
        )
        orphan_pct = (
            (100.0 * len(orphan) / len(sensor)) if sensor else None
        )
        ack_sla_pct = (
            (
                100.0
                * sum(1 for m in ack_mins if m <= DEFAULT_ACK_MINUTES)
                / len(ack_mins)
            )
            if ack_mins
            else None
        )
        secure_sla_pct = (
            (
                100.0
                * sum(1 for h in secure_hours if h <= DEFAULT_SECURE_HOURS)
                / len(secure_hours)
            )
            if secure_hours
            else None
        )

        return KpiSnapshot(
            alert_ack_median_minutes=_median(ack_mins),
            alert_ack_within_sla_pct=ack_sla_pct,
            secure_median_hours=_median(secure_hours),
            secure_within_sla_pct=secure_sla_pct,
            public_report_closed_pct=report_pct,
            orphan_sensor_alert_pct=orphan_pct,
            day90_briefing_delivered=day90_briefing_delivered,
            pass_ack_sla=(
                None if ack_sla_pct is None else ack_sla_pct >= 95.0
            ),
            pass_secure_sla=(
                None if secure_sla_pct is None else secure_sla_pct >= 95.0
            ),
            pass_report_close=(
                None
                if report_pct is None
                else report_pct >= DEFAULT_REPORT_CLOSE_PCT
            ),
            pass_orphan=(
                None
                if orphan_pct is None
                else orphan_pct <= DEFAULT_ORPHAN_PCT
            ),
        )


def _parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


def _minutes(start: str, end: str) -> float:
    return (_parse(end) - _parse(start)).total_seconds() / 60.0


def _hours(start: str, end: str) -> float:
    return (_parse(end) - _parse(start)).total_seconds() / 3600.0


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0
