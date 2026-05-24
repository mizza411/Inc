"""
Pipeline monitoring and alerts (Phase 4.3).

Checks for schedule misses, quality drops, and batch pipeline failures.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from database.youtube_schema import YouTubeDatabase

logger = logging.getLogger(__name__)


@dataclass
class PipelineAlert:
    category: str
    severity: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringReport:
    checked_at: str
    alert_count: int
    critical_count: int
    warning_count: int
    alerts: List[PipelineAlert]
    export_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["alerts"] = [asdict(a) for a in self.alerts]
        return data

    @property
    def healthy(self) -> bool:
        return self.critical_count == 0 and self.warning_count == 0


class PipelineMonitor:
    """Scan DB state and launch manifests for operational issues."""

    def __init__(
        self,
        db_path: Optional[Union[str, Path]] = None,
        exports_dir: Optional[Union[str, Path]] = None,
        min_quality_score: float = 0.75,
        avg_quality_floor: float = 0.80,
    ):
        base = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path or base / "data" / "youtube_business.db")
        self.exports_dir = Path(exports_dir or base / "exports" / "monitoring")
        self.launch_batches_dir = base / "exports" / "launch_batches"
        self.min_quality_score = min_quality_score
        self.avg_quality_floor = avg_quality_floor
        self.db = YouTubeDatabase(str(self.db_path))

    def check_all(self) -> MonitoringReport:
        alerts: List[PipelineAlert] = []
        alerts.extend(self._check_schedule_misses())
        alerts.extend(self._check_quality_drops())
        alerts.extend(self._check_pipeline_failures())

        critical = sum(1 for a in alerts if a.severity == "critical")
        warnings = sum(1 for a in alerts if a.severity == "warning")
        export_path = self._export(alerts, critical, warnings)

        return MonitoringReport(
            checked_at=datetime.now().isoformat(),
            alert_count=len(alerts),
            critical_count=critical,
            warning_count=warnings,
            alerts=alerts,
            export_path=str(export_path),
        )

    def _check_schedule_misses(self) -> List[PipelineAlert]:
        alerts: List[PipelineAlert] = []
        today = date.today().isoformat()
        planned = self.db.list_schedule(status="planned", limit=200)
        overdue = [row for row in planned if str(row.get("scheduled_date", "")) < today]

        for row in overdue:
            alerts.append(
                PipelineAlert(
                    category="schedule_miss",
                    severity="warning",
                    message=f"Overdue planned slot: {row.get('topic_title')}",
                    details={
                        "schedule_id": row.get("id"),
                        "scheduled_date": row.get("scheduled_date"),
                        "niche": row.get("content_niche"),
                    },
                )
            )

        due_today = [row for row in planned if str(row.get("scheduled_date", "")) == today]
        if len(due_today) >= 3:
            alerts.append(
                PipelineAlert(
                    category="schedule_load",
                    severity="info",
                    message=f"{len(due_today)} slot(s) due today — run schedule run-due",
                    details={"due_count": len(due_today)},
                )
            )

        return alerts

    def _check_quality_drops(self) -> List[PipelineAlert]:
        alerts: List[PipelineAlert] = []
        summary = self.db.get_content_quality_summary()
        avg_quality = summary.get("avg_quality")

        if avg_quality is not None:
            avg = float(avg_quality)
            if avg < self.avg_quality_floor:
                alerts.append(
                    PipelineAlert(
                        category="quality_drop",
                        severity="critical" if avg < self.min_quality_score else "warning",
                        message=f"Average content quality below floor ({avg:.2f} < {self.avg_quality_floor:.2f})",
                        details={"avg_quality": avg, "video_count": summary.get("video_count")},
                    )
                )

        for video in self.db.list_videos(limit=25):
            score = video.get("high_effort_score")
            if score is None:
                continue
            value = float(score)
            if value < self.min_quality_score:
                alerts.append(
                    PipelineAlert(
                        category="quality_drop",
                        severity="warning",
                        message=f"Low quality score for video: {video.get('title')}",
                        details={
                            "video_id": video.get("id"),
                            "score": value,
                            "threshold": self.min_quality_score,
                        },
                    )
                )

        return alerts

    def _check_pipeline_failures(self) -> List[PipelineAlert]:
        alerts: List[PipelineAlert] = []
        if not self.launch_batches_dir.is_dir():
            return alerts

        manifests = sorted(self.launch_batches_dir.glob("*.json"), reverse=True)[:10]
        for path in manifests:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                alerts.append(
                    PipelineAlert(
                        category="pipeline_failure",
                        severity="warning",
                        message=f"Could not read launch manifest: {path.name}",
                        details={"error": str(exc)},
                    )
                )
                continue

            failures = int(data.get("failure_count") or 0)
            if failures > 0:
                alerts.append(
                    PipelineAlert(
                        category="pipeline_failure",
                        severity="critical",
                        message=f"Launch batch had {failures} failure(s): {data.get('batch_id', path.stem)}",
                        details={
                            "batch_id": data.get("batch_id"),
                            "manifest": str(path),
                            "failure_count": failures,
                            "success_count": data.get("success_count"),
                        },
                    )
                )

            for topic in data.get("topics", []):
                if topic.get("status") == "failed" or topic.get("success") is False:
                    alerts.append(
                        PipelineAlert(
                            category="pipeline_failure",
                            severity="critical",
                            message=f"Pipeline failed for topic: {topic.get('topic')}",
                            details={
                                "batch_id": data.get("batch_id"),
                                "index": topic.get("index"),
                                "error": topic.get("error"),
                            },
                        )
                    )

        return alerts

    def _export(
        self,
        alerts: List[PipelineAlert],
        critical: int,
        warnings: int,
    ) -> Path:
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.exports_dir / f"monitoring_report_{stamp}.json"
        payload = {
            "checked_at": datetime.now().isoformat(),
            "database": str(self.db_path),
            "alert_count": len(alerts),
            "critical_count": critical,
            "warning_count": warnings,
            "healthy": critical == 0 and warnings == 0,
            "alerts": [asdict(a) for a in alerts],
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Monitoring report exported to %s", path)
        return path

    def close(self) -> None:
        self.db.close()
