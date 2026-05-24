"""
Content performance tracking for the YouTube automation pipeline.

Records pre-publish quality scores at creation time and YouTube metrics
(views, retention, etc.) when imported manually or via API later.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from core.content_validator import HighEffortContentValidator
from database.youtube_schema import YouTubeDatabase

logger = logging.getLogger(__name__)


class ContentPerformanceTracker:
    """Track content quality at creation and YouTube performance over time."""

    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        base = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path or base / "data" / "youtube_business.db")
        self.db = YouTubeDatabase(str(self.db_path))
        self.validator = HighEffortContentValidator()

    def track_created_video(
        self,
        topic: str,
        context: str,
        script: Any,
        extra_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Persist a newly generated video plus pre-publish quality analytics.

        Returns video_id, validation score, and any validation issues.
        """
        script_data = self._script_to_dict(script)
        validation = self.validator.validate_video_script(script_data)

        metadata = {
            "topic": topic,
            "context": context,
            "trending_terms": script_data.get("trending_terms", []),
            "language_blends": script_data.get("language_blends", []),
            "validation_score": validation.score,
            "validation_issues": validation.issues,
            **(extra_metadata or {}),
        }

        video_id = self.db.insert_video(
            {
                "youtube_id": None,
                "title": script_data.get("title", topic),
                "description": script_data.get("description", ""),
                "channel_id": "",
                "content_niche": context,
                "language_blending_score": min(
                    1.0, len(script_data.get("language_blends", [])) / 5.0
                ),
                "high_effort_score": validation.score,
                "target_duration_minutes": script_data.get("estimated_duration", 8),
                "actual_duration_minutes": script_data.get("estimated_duration", 8),
                "status": "draft",
                "thumbnail_path": "",
                "video_file_path": "",
                "script_file_path": "",
                "metadata_json": json.dumps(metadata),
            }
        )

        self.db.insert_content_analytics(
            video_id,
            {
                "content_quality_score": validation.score,
                "engagement_score": validation.score,
                "viral_potential_score": min(
                    1.0, len(script_data.get("trending_terms", [])) / 8.0
                ),
                "monetization_readiness_score": validation.score,
                "high_effort_compliance": {
                    "is_valid": validation.is_valid,
                    "issues": validation.issues,
                },
                "improvement_suggestions": validation.recommendations,
            },
        )

        logger.info("Tracked video id=%s title=%s score=%.2f", video_id, topic, validation.score)
        return {
            "video_id": video_id,
            "validation_score": validation.score,
            "validation_passed": validation.is_valid,
            "issues": validation.issues,
        }

    def record_youtube_metrics(self, video_id: int, metrics: Dict[str, Any]) -> None:
        """Upsert daily YouTube performance metrics for a video."""
        self.db.update_video_performance(video_id, metrics)

    def import_metrics_file(self, path: Union[str, Path]) -> int:
        """
        Import performance rows from JSON.

        Expected format: list of objects with video_id and metric fields,
        or a single object with a "records" array.
        """
        path = Path(path)
        with path.open(encoding="utf-8") as f:
            payload = json.load(f)

        records = payload if isinstance(payload, list) else payload.get("records", [])
        count = 0
        for row in records:
            video_id = row.get("video_id")
            if not video_id:
                logger.warning("Skipping row without video_id: %s", row)
                continue
            self.record_youtube_metrics(int(video_id), row)
            count += 1
        return count

    def get_summary(self) -> Dict[str, Any]:
        """Combined pre-publish quality and YouTube performance overview."""
        quality = self.db.get_content_quality_summary()
        top_videos = self.db.get_top_performing_videos(limit=5)
        recent = self.db.list_videos(limit=10)

        return {
            "generated_at": datetime.now().isoformat(),
            "database": str(self.db_path),
            "content_quality": quality,
            "top_performing_videos": top_videos,
            "recent_videos": recent,
        }

    def export_summary(self, exports_dir: Optional[Path] = None) -> Path:
        """Write performance summary JSON to exports/."""
        base = exports_dir or Path(__file__).resolve().parent.parent / "exports"
        base.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = base / f"performance_summary_{stamp}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(self.get_summary(), f, indent=2, default=str)
        return path

    def close(self) -> None:
        self.db.close()

    def _script_to_dict(self, script: Any) -> Dict[str, Any]:
        if isinstance(script, dict):
            return script
        if is_dataclass(script):
            data = asdict(script)
            if isinstance(data.get("generated_date"), datetime):
                data["generated_date"] = data["generated_date"].isoformat()
            return data
        return {"title": str(script)}
