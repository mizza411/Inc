"""Tests for launch system go-live orchestration (Phase 4.5)."""

from pathlib import Path
from unittest.mock import MagicMock

from core.launch_controller import LaunchController


def _mock_system(tmp_path: Path, monitor_healthy: bool = True):
    system = MagicMock()
    system.get_system_status.return_value = {
        "status": "operational",
        "settings": {"youtube": {"channel_name": "Test Channel"}},
        "monetization_checklist": {"8+ minute videos": True},
        "components": {"pipeline_monitor": "ready"},
    }

    monitor_report = MagicMock()
    monitor_report.healthy = monitor_healthy
    monitor_report.alert_count = 0 if monitor_healthy else 2
    monitor_report.critical_count = 0
    monitor_report.warning_count = 0 if monitor_healthy else 2
    monitor_report.export_path = str(tmp_path / "monitor.json")
    system.pipeline_monitor.check_all.return_value = monitor_report

    system.analytics_dashboard.generate_html.return_value = tmp_path / "dash.html"
    system.performance_tracker.export_summary.return_value = tmp_path / "perf.json"
    system.performance_tracker.get_summary.return_value = {
        "content_quality": {"video_count": 3, "avg_quality": 0.91},
        "recent_videos": [],
    }
    system.content_scheduler.list_upcoming.return_value = [{"id": 1}]
    return system


def test_go_live_success(tmp_path: Path):
    controller = LaunchController(_mock_system(tmp_path), exports_dir=tmp_path / "launch")
    report = controller.go_live(skip_monitor=False, plan_schedule=False)

    assert report.system_status == "operational"
    assert report.monitoring_healthy is True
    assert report.videos_tracked == 3
    assert Path(report.export_path).is_file()


def test_go_live_blocks_on_monitor_alerts(tmp_path: Path):
    controller = LaunchController(
        _mock_system(tmp_path, monitor_healthy=False),
        exports_dir=tmp_path / "launch",
    )
    try:
        controller.go_live(skip_monitor=False)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "Monitoring alerts" in str(exc)


def test_go_live_skip_monitor(tmp_path: Path):
    controller = LaunchController(
        _mock_system(tmp_path, monitor_healthy=False),
        exports_dir=tmp_path / "launch",
    )
    report = controller.go_live(skip_monitor=True, plan_schedule=False)
    assert report.monitoring_healthy is True
