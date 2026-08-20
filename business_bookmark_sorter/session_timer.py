"""Timed review session countdown (BB-TIMED-1 Phase 2).

Pure logic — no tkinter. Injectable clock for tests.
"""

from __future__ import annotations

import time
from typing import Callable, Optional

Clock = Callable[[], float]


class SessionTimer:
    """Countdown for one filing slot."""

    def __init__(
        self,
        duration_seconds: int,
        *,
        clock: Optional[Clock] = None,
    ) -> None:
        if duration_seconds < 1:
            duration_seconds = 1
        self._duration = int(duration_seconds)
        self._clock: Clock = clock or time.monotonic
        self._started_at: Optional[float] = None
        self._paused_at: Optional[float] = None
        self._paused_accumulated = 0.0
        self._running = False

    @property
    def duration_seconds(self) -> int:
        return self._duration

    @property
    def is_running(self) -> bool:
        return self._running and self._paused_at is None

    @property
    def is_paused(self) -> bool:
        return self._running and self._paused_at is not None

    def start(self, now: Optional[float] = None) -> None:
        t = self._clock() if now is None else now
        self._started_at = t
        self._paused_at = None
        self._paused_accumulated = 0.0
        self._running = True

    def pause(self, now: Optional[float] = None) -> None:
        if not self._running or self._paused_at is not None:
            return
        self._paused_at = self._clock() if now is None else now

    def resume(self, now: Optional[float] = None) -> None:
        if self._paused_at is None:
            return
        t = self._clock() if now is None else now
        self._paused_accumulated += t - self._paused_at
        self._paused_at = None

    def remaining_seconds(self, now: Optional[float] = None) -> float:
        if self._started_at is None:
            return float(self._duration)
        t = self._clock() if now is None else now
        if self._paused_at is not None:
            elapsed = (self._paused_at - self._started_at) - self._paused_accumulated
        else:
            elapsed = (t - self._started_at) - self._paused_accumulated
        left = self._duration - elapsed
        return left if left > 0 else 0.0

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self._started_at is None:
            return False
        return self.remaining_seconds(now) <= 0

    def extend(self, extra_seconds: int) -> None:
        """Add time to the slot (also restarts a finished session)."""
        if extra_seconds < 1:
            return
        if self.is_expired() or not self._running:
            # Fresh slice from now using remaining (0) + extension as new duration
            remaining = max(0.0, self.remaining_seconds())
            self._duration = int(remaining) + int(extra_seconds)
            if self._duration < 1:
                self._duration = int(extra_seconds)
            self.start()
            return
        self._duration += int(extra_seconds)

    def restart(self, duration_seconds: int, now: Optional[float] = None) -> None:
        if duration_seconds < 1:
            duration_seconds = 1
        self._duration = int(duration_seconds)
        self.start(now)


def format_remaining(seconds: float) -> str:
    """Format as M:SS or H:MM:SS."""
    total = max(0, int(seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
