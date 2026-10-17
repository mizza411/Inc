"""Single-icon tray Restart helper (exit_before_spawn handoff).

Order when ``exit_before_spawn=True``: run ``before_exit`` (stop icon), then
spawn one replacement, then ``exit_fn``. On spawn failure after stop, log and
do not call ``exit_fn`` only when spawn-first mode is used. With
``exit_before_spawn``, a failed spawn after stop is logged (old icon already gone).

Inc uses ``module=`` relaunch (``pythonw -m inc_launcher.tray_app``).
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Sequence

logger = logging.getLogger(__name__)

# Never pass the Phase 2 self-test env into the replacement process (avoids Restart loop).
_SMOKE_ENV = "INC_LAUNCHER_RESTART_SMOKE"

MSG = {
    "ok": "Restart scheduled.",
    "no_target": "Restart failed: no script or module.",
    "spawn_fail": "Restart failed: could not start a new process.",
}


def messages_for(app_name: str = "app") -> dict[str, str]:
    label = (app_name or "app").strip() or "app"
    return {
        "ok": MSG["ok"],
        "no_target": f"Restart failed: {label} target missing.",
        "spawn_fail": f"Restart failed: could not start a new {label}.",
    }


def prefer_pythonw(executable: str | None = None) -> str:
    """Prefer ``pythonw.exe`` beside the current interpreter (Windows GUI)."""
    exe = executable or sys.executable
    path = Path(exe)
    if path.name.lower() == "pythonw.exe":
        return str(path)
    sibling = path.with_name("pythonw.exe")
    if sibling.is_file():
        return str(sibling)
    return str(path)


def build_relaunch_command(
    *,
    script: Path | None = None,
    module: str | None = None,
    executable: str | None = None,
    extra_args: Sequence[str] = (),
) -> list[str] | None:
    """Return argv for relaunch, or None if neither script nor module is usable."""
    exe = prefer_pythonw(executable)
    extras = [str(a) for a in extra_args]
    if module:
        return [exe, "-m", str(module), *extras]
    if script is None:
        return None
    script_path = Path(script)
    if not script_path.is_file():
        return None
    return [exe, str(script_path.resolve()), *extras]


def spawn_detached(
    cmd: Sequence[str],
    *,
    cwd: str | Path | None = None,
    popen: Callable[..., Any] | None = None,
) -> bool:
    """Start ``cmd`` detached so it survives current-process exit."""
    if not cmd:
        return False
    starter = popen or subprocess.Popen
    workdir = str(cwd) if cwd is not None else None
    creationflags = 0
    if sys.platform == "win32":
        creationflags = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(
            subprocess, "CREATE_NEW_PROCESS_GROUP", 0
        )
    try:
        child_env = os.environ.copy()
        child_env.pop(_SMOKE_ENV, None)
        kwargs: dict[str, Any] = {
            "close_fds": True,
            "creationflags": creationflags,
            "stdin": subprocess.DEVNULL,
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "env": child_env,
        }
        if workdir:
            kwargs["cwd"] = workdir
        starter(list(cmd), **kwargs)  # noqa: S603 — local argv from build_relaunch_command
        return True
    except OSError:
        logger.exception("tray restart spawn failed")
        return False


def restart_tray_process(
    *,
    script: Path | None = None,
    module: str | None = None,
    app_name: str = "app",
    executable: str | None = None,
    extra_args: Sequence[str] = (),
    cwd: str | Path | None = None,
    before_exit: Callable[[], None] | None = None,
    popen: Callable[..., Any] | None = None,
    exit_fn: Callable[[int], Any] | None = None,
    msg: Optional[Mapping[str, str]] = None,
    exit_before_spawn: bool = False,
) -> tuple[bool, str]:
    """
    Relaunch this tray, then exit.

    Pass ``exit_before_spawn=True`` so the old icon stops before the new
    process starts (Auto Scroll / INC-TRAY-RESTART-1 pattern).
    """
    texts = dict(msg) if msg is not None else messages_for(app_name)
    cmd = build_relaunch_command(
        script=script,
        module=module,
        executable=executable,
        extra_args=extra_args,
    )
    if cmd is None:
        return False, texts.get("no_target", MSG["no_target"])

    if cwd is not None:
        workdir: str | Path | None = cwd
    elif script is not None:
        workdir = Path(script).resolve().parent
    else:
        workdir = None

    def _run_before_exit() -> None:
        if before_exit is None:
            return
        try:
            before_exit()
        except Exception:
            logger.exception("tray restart before_exit failed")

    if exit_before_spawn:
        _run_before_exit()

    if not spawn_detached(cmd, cwd=workdir, popen=popen):
        if exit_before_spawn:
            logger.error("tray restart spawn failed after the old icon was stopped")
        return False, texts.get("spawn_fail", MSG["spawn_fail"])

    if not exit_before_spawn:
        _run_before_exit()

    stopper = exit_fn if exit_fn is not None else sys.exit
    try:
        stopper(0)
    except SystemExit:
        raise
    except Exception:
        logger.exception("tray restart exit_fn failed")
    return True, texts.get("ok", MSG["ok"])


__all__ = [
    "MSG",
    "build_relaunch_command",
    "messages_for",
    "prefer_pythonw",
    "restart_tray_process",
    "spawn_detached",
]
