"""Tests for pipeline monitoring and alerts (Phase 4.3)."""

import json
from pathlib import Path

from core.pipeline_monitor import PipelineMonitor
from database.youtube_schema import YouTubeDatabase


def test_monitor_healthy_empty_db(tmp_path: Path):
    db_path = tmp_path / "monitor.db"
    monitor = PipelineMonitor(db_path=db_path, exports_dir=tmp_path / "monitoring")
    report = monitor.check_all()

    assert report.healthy is True
    assert report.alert_count == 0
    assert Path(report.export_path).is_file()
    monitor.close()


def test_monitor_detects_schedule_miss(tmp_path: Path):
    db_path = tmp_path / "sched.db"
    db = YouTubeDatabase(str(db_path))
    db.insert_schedule_item(
        {
            "scheduled_date": "2020-01-01",
            "content_niche": "music",
            "topic_title": "Stale Topic",
            "status": "planned",
        }
    )
    db.close()

    monitor = PipelineMonitor(db_path=db_path, exports_dir=tmp_path / "monitoring")
    report = monitor.check_all()

    categories = {a.category for a in report.alerts}
    assert "schedule_miss" in categories
    monitor.close()


def test_monitor_detects_pipeline_failure_manifest(tmp_path: Path):
    db_path = tmp_path / "mon.db"
    batches_dir = tmp_path / "launch_batches"
    batches_dir.mkdir()
    manifest = {
        "batch_id": "launch_test",
        "failure_count": 1,
        "success_count": 0,
        "topics": [
            {"index": 1, "topic": "Failed Topic", "status": "failed", "success": False, "error": "boom"},
        ],
    }
    (batches_dir / "launch_test.json").write_text(json.dumps(manifest), encoding="utf-8")

    monitor = PipelineMonitor(
        db_path=db_path,
        exports_dir=tmp_path / "monitoring",
    )
    monitor.launch_batches_dir = batches_dir
    report = monitor.check_all()

    assert any(a.category == "pipeline_failure" for a in report.alerts)
    assert report.critical_count >= 1
    monitor.close()


def test_monitor_detects_low_quality_video(tmp_path: Path):
    db_path = tmp_path / "quality.db"
    db = YouTubeDatabase(str(db_path))
    video_id = db.insert_video(
        {
            "title": "Low Quality Draft",
            "description": "",
            "channel_id": "",
            "content_niche": "culture",
            "high_effort_score": 0.55,
            "target_duration_minutes": 8,
            "actual_duration_minutes": 8,
            "status": "draft",
        }
    )
    db.insert_content_analytics(
        video_id,
        {"content_quality_score": 0.55, "engagement_score": 0.55, "monetization_readiness_score": 0.55},
    )
    db.close()

    monitor = PipelineMonitor(db_path=db_path, exports_dir=tmp_path / "monitoring")
    report = monitor.check_all()

    assert any(a.category == "quality_drop" for a in report.alerts)
    monitor.close()
