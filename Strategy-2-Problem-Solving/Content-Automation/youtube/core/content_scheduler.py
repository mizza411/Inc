"""
Automated content scheduling for the YouTube pipeline.

Builds a publish calendar from trending topics and runs due items through
the existing create_complete_video workflow.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from database.youtube_schema import YouTubeDatabase

logger = logging.getLogger(__name__)

NICHE_TO_CONTEXT = {
    "music": "music",
    "entertainment": "culture",
    "culture": "culture",
    "news": "culture",
    "technology": "technology",
    "sports": "culture",
    "general": "culture",
    "lifestyle": "lifestyle",
}


class ContentScheduler:
    """Plan and execute scheduled video creation slots."""

    def __init__(
        self,
        db_path: Optional[Union[str, Path]] = None,
        topic_analyzer: Optional[Any] = None,
        uploads_per_week: int = 3,
        target_duration_minutes: int = 8,
    ):
        base = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path or base / "data" / "youtube_business.db")
        self.db = YouTubeDatabase(str(self.db_path))
        self.topic_analyzer = topic_analyzer
        self.uploads_per_week = max(1, min(uploads_per_week, 7))
        self.target_duration_minutes = target_duration_minutes

    def generate_plan(
        self,
        days_ahead: int = 14,
        clear_existing_planned: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Create schedule rows from trending topics for the next N days.

        Default cadence: 3 uploads/week on Mon/Wed/Fri-style spacing.
        """
        if clear_existing_planned:
            for row in self.db.list_schedule(status="planned"):
                self.db.update_schedule_status(row["id"], "cancelled")

        topics = self._collect_topic_candidates()
        slot_dates = self._build_slot_dates(date.today(), days_ahead)
        created: List[Dict[str, Any]] = []

        for idx, slot_date in enumerate(slot_dates):
            topic = topics[idx % len(topics)]
            niche = topic.get("category", "general")
            context = NICHE_TO_CONTEXT.get(niche, "culture")
            item = {
                "scheduled_date": slot_date.isoformat(),
                "content_niche": niche,
                "topic_title": topic["title"],
                "target_duration_minutes": self.target_duration_minutes,
                "priority_level": "high" if idx < self.uploads_per_week else "normal",
                "status": "planned",
                "assigned_automation_workflow": "create_complete_video",
                "context": context,
            }
            item["id"] = self.db.insert_schedule_item(item)
            created.append(item)

        logger.info("Generated %s scheduled slots over %s days", len(created), days_ahead)
        return created

    def list_upcoming(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List planned schedule items from today onward."""
        today = date.today().isoformat()
        rows = self.db.list_schedule(status="planned", from_date=today, limit=limit)
        return rows

    def run_due(
        self,
        create_fn: Callable[[str, str, int], Dict[str, Any]],
        for_date: Optional[str] = None,
        dry_run: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Run create_complete_video for items due on or before for_date.

        create_fn signature: (topic, context, target_minutes) -> result dict
        """
        due = self.db.get_due_schedule_items(for_date)
        results: List[Dict[str, Any]] = []

        for row in due:
            topic = row["topic_title"]
            niche = row.get("content_niche") or "general"
            context = NICHE_TO_CONTEXT.get(niche, "culture")
            minutes = row.get("target_duration_minutes") or self.target_duration_minutes

            if dry_run:
                results.append(
                    {
                        "schedule_id": row["id"],
                        "topic": topic,
                        "context": context,
                        "dry_run": True,
                    }
                )
                continue

            outcome = create_fn(topic, context, int(minutes))
            status = "completed" if outcome.get("success") else "failed"
            self.db.update_schedule_status(row["id"], status)
            results.append(
                {
                    "schedule_id": row["id"],
                    "topic": topic,
                    "status": status,
                    "result": outcome,
                }
            )

        return results

    def export_plan(self, exports_dir: Optional[Path] = None) -> Path:
        """Export upcoming planned schedule to JSON."""
        base = exports_dir or Path(__file__).resolve().parent.parent / "exports"
        base.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = base / f"content_schedule_{stamp}.json"
        payload = {
            "generated_at": datetime.now().isoformat(),
            "uploads_per_week": self.uploads_per_week,
            "planned": self.list_upcoming(limit=100),
        }
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)
        return path

    def close(self) -> None:
        self.db.close()

    def _build_slot_dates(self, start: date, days_ahead: int) -> List[date]:
        """Mon/Wed/Fri-style slots within the planning window."""
        offsets = [0, 2, 4][: self.uploads_per_week]
        dates: List[date] = []
        end = start + timedelta(days=days_ahead)

        week_start = start
        while week_start <= end:
            for offset in offsets:
                slot = week_start + timedelta(days=offset)
                if start <= slot <= end:
                    dates.append(slot)
            week_start += timedelta(days=7)

        return dates

    def _collect_topic_candidates(self) -> List[Dict[str, str]]:
        if self.topic_analyzer:
            try:
                report = self.topic_analyzer.analyze()
                if report.video_ideas:
                    return [
                        {
                            "title": idea["title"],
                            "category": idea.get("category", "general"),
                        }
                        for idea in report.video_ideas
                    ]
                if report.top_picks:
                    return [
                        {"title": t.query, "category": t.category}
                        for t in report.top_picks
                    ]
            except Exception as exc:
                logger.warning("Trend topic fill failed, using fallback: %s", exc)

        return [
            {"title": "Afrobeats trends explained", "category": "music"},
            {"title": "Nigerian culture moments this week", "category": "culture"},
            {"title": "Lagos lifestyle and tech", "category": "technology"},
            {"title": "Nollywood and entertainment news", "category": "entertainment"},
            {"title": "Cost of living Nigeria update", "category": "news"},
        ]
