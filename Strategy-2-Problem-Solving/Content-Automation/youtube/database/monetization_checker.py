"""
YouTube Partner Program (YPP) application readiness checker (Phase 4.6).

Evaluates system config, content quality in SQLite, and optional channel metrics
to produce an application checklist and export report.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from config.settings import Settings
from database.youtube_schema import YouTubeDatabase

logger = logging.getLogger(__name__)

YPP_SUBSCRIBERS = 1000
YPP_WATCH_HOURS = 4000

APPLICATION_STEPS = [
    "Produce 8+ minute high-effort videos (automated pipeline)",
    "Upload monetization-ready videos to YouTube channel",
    "Reach 1,000 subscribers",
    "Reach 4,000 valid public watch hours (last 12 months)",
    "Follow YouTube channel monetization policies",
    "Enable 2-Step Verification on Google account",
    "Apply in YouTube Studio → Earn → Apply",
    "Link or create AdSense account when approved",
]


@dataclass
class MonetizationApplicationReport:
    assessed_at: str
    system_checklist: Dict[str, bool]
    system_ready: bool
    content_eligible_count: int
    content_eligible_videos: List[Dict[str, Any]]
    channel_metrics: Dict[str, Any]
    ypp_eligible: bool
    application_steps: List[Dict[str, Any]]
    ready_to_apply: bool
    blockers: List[str] = field(default_factory=list)
    export_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MonetizationChecker:
    """Assess monetization application readiness for the YouTube automation pipeline."""

    def __init__(
        self,
        db_path: Optional[Union[str, Path]] = None,
        metrics_path: Optional[Union[str, Path]] = None,
        exports_dir: Optional[Union[str, Path]] = None,
    ):
        base = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path or base / "data" / "youtube_business.db")
        self.metrics_path = Path(metrics_path or base / "data" / "monetization_metrics.json")
        self.exports_dir = Path(exports_dir or base / "exports" / "monetization")
        self.settings = Settings()
        self.db = YouTubeDatabase(str(self.db_path))

    def assess(self) -> MonetizationApplicationReport:
        checklist = self.settings.get_monetization_checklist()
        system_ready = all(checklist.values())

        eligible = self._content_eligible_videos()
        metrics = self._load_channel_metrics()

        subs = int(metrics.get("subscribers") or 0)
        hours = float(metrics.get("watch_hours_12mo") or 0)
        ypp_eligible = subs >= YPP_SUBSCRIBERS and hours >= YPP_WATCH_HOURS

        steps = self._build_application_steps(
            system_ready, len(eligible), metrics, ypp_eligible
        )
        blockers = self._blockers(checklist, eligible, metrics, ypp_eligible)
        ready = system_ready and len(eligible) >= 1 and ypp_eligible and not blockers

        report = MonetizationApplicationReport(
            assessed_at=datetime.now().isoformat(),
            system_checklist=checklist,
            system_ready=system_ready,
            content_eligible_count=len(eligible),
            content_eligible_videos=eligible[:20],
            channel_metrics=metrics,
            ypp_eligible=ypp_eligible,
            application_steps=steps,
            ready_to_apply=ready,
            blockers=blockers,
        )
        report.export_path = str(self._export(report))
        return report

    def init_metrics_template(self) -> Path:
        """Create a template metrics file for manual YouTube Studio updates."""
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.metrics_path.is_file():
            template = {
                "subscribers": 0,
                "watch_hours_12mo": 0,
                "channel_url": "",
                "adsense_linked": False,
                "last_updated": None,
                "notes": "Update from YouTube Studio → Analytics after each week",
            }
            self.metrics_path.write_text(
                json.dumps(template, indent=2), encoding="utf-8"
            )
        return self.metrics_path

    def _content_eligible_videos(self, min_score: float = 0.8) -> List[Dict[str, Any]]:
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            SELECT id, title, high_effort_score, actual_duration_minutes,
                   content_niche, status, created_at
            FROM videos
            WHERE high_effort_score >= ?
              AND actual_duration_minutes >= 8
            ORDER BY high_effort_score DESC, created_at DESC
            """,
            (min_score,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def _load_channel_metrics(self) -> Dict[str, Any]:
        if not self.metrics_path.is_file():
            return {
                "subscribers": 0,
                "watch_hours_12mo": 0,
                "channel_url": "",
                "adsense_linked": False,
                "source": "default",
            }
        try:
            data = json.loads(self.metrics_path.read_text(encoding="utf-8"))
            data["source"] = str(self.metrics_path)
            return data
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not load metrics file: %s", exc)
            return {"subscribers": 0, "watch_hours_12mo": 0, "source": "error"}

    def _build_application_steps(
        self,
        system_ready: bool,
        eligible_count: int,
        metrics: Dict[str, Any],
        ypp_eligible: bool,
    ) -> List[Dict[str, Any]]:
        subs = int(metrics.get("subscribers") or 0)
        hours = float(metrics.get("watch_hours_12mo") or 0)
        statuses = [
            system_ready,
            eligible_count >= 10,
            subs >= YPP_SUBSCRIBERS,
            hours >= YPP_WATCH_HOURS,
            True,
            metrics.get("two_factor_enabled", False),
            metrics.get("application_submitted", False),
            metrics.get("adsense_linked", False),
        ]
        steps: List[Dict[str, Any]] = []
        for i, label in enumerate(APPLICATION_STEPS):
            done = statuses[i] if i < len(statuses) else False
            steps.append({"step": i + 1, "label": label, "completed": done})
        return steps

    def _blockers(
        self,
        checklist: Dict[str, bool],
        eligible: List[Dict],
        metrics: Dict[str, Any],
        ypp_eligible: bool,
    ) -> List[str]:
        blockers: List[str] = []
        for key, ok in checklist.items():
            if not ok:
                blockers.append(f"System config: {key}")

        if len(eligible) < 1:
            blockers.append("No content-eligible videos (need score≥0.8, duration≥8 min)")
        elif len(eligible) < 10:
            blockers.append(
                f"Only {len(eligible)} eligible video(s) — recommend 10+ before applying"
            )

        subs = int(metrics.get("subscribers") or 0)
        hours = float(metrics.get("watch_hours_12mo") or 0)
        if subs < YPP_SUBSCRIBERS:
            blockers.append(f"Subscribers {subs}/{YPP_SUBSCRIBERS}")
        if hours < YPP_WATCH_HOURS:
            blockers.append(f"Watch hours {hours:.0f}/{YPP_WATCH_HOURS}")

        if not metrics.get("two_factor_enabled"):
            blockers.append("Enable 2-Step Verification on Google account")

        return blockers

    def _export(self, report: MonetizationApplicationReport) -> Path:
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.exports_dir / f"monetization_application_{stamp}.json"
        path.write_text(
            json.dumps(report.to_dict(), indent=2, default=str),
            encoding="utf-8",
        )
        return path

    def close(self) -> None:
        self.db.close()
