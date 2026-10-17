"""Inc tray lifecycle file log."""

from __future__ import annotations

from pathlib import Path

from inc_launcher.lifecycle_log import LOG_PATH, append_lifecycle, lifecycle_log_path


def test_lifecycle_log_path_is_under_package():
    path = lifecycle_log_path()
    assert path == LOG_PATH
    assert path.name == "tray_lifecycle.log"
    assert path.is_absolute()
    assert path.parent.name == "inc_launcher"


def test_append_lifecycle_writes_breadcrumb(tmp_path: Path):
    log = tmp_path / "tray_lifecycle.log"
    append_lifecycle("starting handoff=no", log_path=log)
    append_lifecycle("Restart selected - shutting down", log_path=log)
    append_lifecycle("Restart handoff spawn ok - exiting for replacement", log_path=log)
    append_lifecycle("shutting down", log_path=log)
    text = log.read_text(encoding="utf-8")
    assert "starting handoff=no" in text
    assert "Restart selected - shutting down" in text
    assert "Restart handoff spawn ok - exiting for replacement" in text
    assert "shutting down" in text
    assert "pid=" in text
