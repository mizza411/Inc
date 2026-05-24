"""
Launch system orchestration and post-launch performance monitoring (Phase 4.5).

Runs pre-flight checks, generates dashboard + performance exports, and writes
a combined launch status report.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

logger = logging.getLogger(__name__)


@dataclass
class GoLiveReport:
    launched_at: str
    system_status: str
    channel_name: str
    monitoring_healthy: bool
    alert_count: int
    dashboard_path: str
    performance_export: str
    monitoring_export: str
    schedule_slots_planned: int
    videos_tracked: int
    avg_quality_score: Optional[float]
    export_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LaunchController:
    """Coordinate go-live steps: verify, monitor, dashboard, performance snapshot."""

    def __init__(self, system: Any, exports_dir: Optional[Union[str, Path]] = None):
        base = Path(__file__).resolve().parent.parent
        self.system = system
        self.exports_dir = Path(exports_dir or base / "exports" / "launch_status")

    def go_live(
        self,
        skip_monitor: bool = False,
        plan_schedule: bool = True,
        schedule_days: int = 14,
    ) -> GoLiveReport:
        """
        Execute launch sequence and return a combined status report.

        Raises RuntimeError if system is not operational or monitoring fails.
        """
        status = self.system.get_system_status()
        sys_state = status.get("status", "unknown")
        if sys_state not in ("operational", "warning"):
            raise RuntimeError(f"System not ready for launch (status={sys_state})")

        monitoring_healthy = True
        alert_count = 0
        monitoring_export = ""

        if not skip_monitor:
            monitor_report = self.system.pipeline_monitor.check_all()
            monitoring_healthy = monitor_report.healthy
            alert_count = monitor_report.alert_count
            monitoring_export = monitor_report.export_path
            if not monitoring_healthy:
                raise RuntimeError(
                    f"Monitoring alerts block launch "
                    f"(critical={monitor_report.critical_count}, "
                    f"warning={monitor_report.warning_count})"
                )

        dashboard_path = str(self.system.analytics_dashboard.generate_html())
        performance_export = str(self.system.performance_tracker.export_summary())
        perf = self.system.performance_tracker.get_summary()
        quality = perf.get("content_quality") or {}

        schedule_planned = 0
        if plan_schedule:
            upcoming = self.system.content_scheduler.list_upcoming(limit=1)
            if not upcoming:
                created = self.system.content_scheduler.generate_plan(days_ahead=schedule_days)
                schedule_planned = len(created)
            else:
                schedule_planned = len(
                    self.system.content_scheduler.list_upcoming(limit=50)
                )

        launched_at = datetime.now().isoformat()
        channel = status.get("settings", {}).get("youtube", {}).get("channel_name", "")

        report = GoLiveReport(
            launched_at=launched_at,
            system_status=sys_state,
            channel_name=channel,
            monitoring_healthy=monitoring_healthy,
            alert_count=alert_count,
            dashboard_path=dashboard_path,
            performance_export=performance_export,
            monitoring_export=monitoring_export,
            schedule_slots_planned=schedule_planned,
            videos_tracked=int(quality.get("video_count") or 0),
            avg_quality_score=(
                float(quality["avg_quality"])
                if quality.get("avg_quality") is not None
                else None
            ),
            export_path="",
        )

        export_path = self._export(report, status, perf)
        report.export_path = str(export_path)
        logger.info("Go-live complete; report at %s", export_path)
        return report

    def _export(
        self,
        report: GoLiveReport,
        system_status: Dict[str, Any],
        performance: Dict[str, Any],
    ) -> Path:
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.exports_dir / f"go_live_{stamp}.json"
        payload = {
            **report.to_dict(),
            "monetization_checklist": system_status.get("monetization_checklist", {}),
            "components": system_status.get("components", {}),
            "performance_snapshot": performance,
        }
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return path
