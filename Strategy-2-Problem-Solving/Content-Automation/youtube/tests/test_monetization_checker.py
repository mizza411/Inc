"""Tests for monetization application checker (Phase 4.6)."""

import json
from pathlib import Path

from database.monetization_checker import MonetizationChecker, YPP_SUBSCRIBERS, YPP_WATCH_HOURS
from database.youtube_schema import YouTubeDatabase


def _seed_video(db_path: Path, score: float = 0.9, duration: int = 8) -> int:
    db = YouTubeDatabase(str(db_path))
    vid = db.insert_video(
        {
            "title": "Eligible Video",
            "description": "",
            "channel_id": "",
            "content_niche": "culture",
            "high_effort_score": score,
            "target_duration_minutes": duration,
            "actual_duration_minutes": duration,
            "status": "draft",
        }
    )
    db.insert_content_analytics(
        vid,
        {
            "content_quality_score": score,
            "engagement_score": score,
            "monetization_readiness_score": score,
        },
    )
    db.close()
    return vid


def test_monetization_system_checklist(tmp_path: Path):
    checker = MonetizationChecker(
        db_path=tmp_path / "m.db",
        exports_dir=tmp_path / "out",
    )
    report = checker.assess()
    assert report.system_ready is True
    assert "8+ minute videos" in report.system_checklist
    checker.close()


def test_monetization_detects_eligible_content(tmp_path: Path):
    db_path = tmp_path / "m.db"
    _seed_video(db_path)
    checker = MonetizationChecker(db_path=db_path, exports_dir=tmp_path / "out")
    report = checker.assess()
    assert report.content_eligible_count >= 1
    checker.close()


def test_monetization_blockers_without_ypp_metrics(tmp_path: Path):
    db_path = tmp_path / "m.db"
    _seed_video(db_path)
    metrics = tmp_path / "metrics.json"
    metrics.write_text(
        json.dumps({"subscribers": 0, "watch_hours_12mo": 0}),
        encoding="utf-8",
    )
    checker = MonetizationChecker(
        db_path=db_path,
        metrics_path=metrics,
        exports_dir=tmp_path / "out",
    )
    report = checker.assess()
    assert report.ready_to_apply is False
    assert any("Subscribers" in b for b in report.blockers)
    checker.close()


def test_monetization_ready_when_metrics_met(tmp_path: Path):
    db_path = tmp_path / "m.db"
    for i in range(10):
        _seed_video(db_path, score=0.95)

    metrics = tmp_path / "metrics.json"
    metrics.write_text(
        json.dumps(
            {
                "subscribers": YPP_SUBSCRIBERS,
                "watch_hours_12mo": YPP_WATCH_HOURS,
                "two_factor_enabled": True,
                "adsense_linked": False,
            }
        ),
        encoding="utf-8",
    )
    checker = MonetizationChecker(
        db_path=db_path,
        metrics_path=metrics,
        exports_dir=tmp_path / "out",
    )
    report = checker.assess()
    assert report.ypp_eligible is True
    assert report.content_eligible_count >= 10
    assert Path(report.export_path).is_file()
    checker.close()
