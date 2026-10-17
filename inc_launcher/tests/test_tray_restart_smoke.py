"""INC-TRAY-RESTART-1 Phase 2: live one-process Restart handoff smoke (Windows)."""

from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest

from inc_launcher.config import INC_ROOT
from inc_launcher.tray_app import _RESTART_SMOKE_ENV
from inc_launcher.tray_process_restart import spawn_detached

ROOT = INC_ROOT

_TRAY_MATCH = "inc_launcher\\.tray_app|inc_launcher/tray_app"


def _kill_tray_processes() -> None:
    if sys.platform != "win32":
        return
    script = (
        "Get-CimInstance Win32_Process -Filter \"name='python.exe' OR name='pythonw.exe'\" | "
        f"Where-Object {{ $_.CommandLine -match '{_TRAY_MATCH}' }} | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        timeout=30,
    )


def _tray_pids() -> list[int]:
    if sys.platform != "win32":
        return []
    script = (
        "$ids = @(); "
        "Get-CimInstance Win32_Process -Filter \"name='python.exe' OR name='pythonw.exe'\" | "
        f"Where-Object {{ $_.CommandLine -match '{_TRAY_MATCH}' }} | "
        "ForEach-Object { $ids += $_.ProcessId }; "
        "$ids -join ','"
    )
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    raw = (proc.stdout or "").strip()
    if not raw:
        return []
    out: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out


def test_spawn_strips_restart_smoke_env(tmp_path):
    seen: dict = {}

    def fake_popen(cmd, **kwargs):
        seen["env"] = dict(kwargs.get("env") or {})
        return object()

    os.environ[_RESTART_SMOKE_ENV] = "1"
    try:
        assert spawn_detached(
            [sys.executable, "-c", "pass"],
            cwd=tmp_path,
            popen=fake_popen,
        )
        assert _RESTART_SMOKE_ENV not in seen["env"]
    finally:
        os.environ.pop(_RESTART_SMOKE_ENV, None)


@pytest.mark.skipif(sys.platform != "win32", reason="tray lifecycle smoke is Windows-only")
def test_restart_smoke_leaves_one_tray_process():
    """Start tray with smoke env, auto-Restart, assert exactly one survivor."""
    _kill_tray_processes()
    time.sleep(0.5)
    assert _tray_pids() == []

    env = os.environ.copy()
    env[_RESTART_SMOKE_ENV] = "1"
    first = subprocess.Popen(
        [sys.executable, "-m", "inc_launcher.tray_app"],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    first_pid = first.pid
    try:
        deadline = time.time() + 20
        survivor: list[int] = []
        while time.time() < deadline:
            pids = _tray_pids()
            if first.poll() is not None and len(pids) == 1 and pids[0] != first_pid:
                survivor = pids
                break
            if first.poll() is not None and len(pids) == 1:
                # Replacement may reuse reporting briefly, accept single tray
                survivor = pids
                break
            time.sleep(0.4)

        assert first.poll() is not None, "Original tray should exit after Restart handoff"
        assert len(survivor) == 1, f"Expected one tray after Restart, got {survivor!r} / {_tray_pids()!r}"
        assert survivor[0] != first_pid, "Survivor must be the replacement process"
    finally:
        if first.poll() is None:
            first.terminate()
            try:
                first.wait(timeout=5)
            except subprocess.TimeoutExpired:
                first.kill()
        _kill_tray_processes()
        time.sleep(0.3)
        assert _tray_pids() == []
