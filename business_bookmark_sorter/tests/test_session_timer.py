"""BB-TIMED-1 Phase 2 — session timer with fake clock."""

from __future__ import annotations

from business_bookmark_sorter.session_timer import SessionTimer, format_remaining


class FakeClock:
    def __init__(self, start: float = 1000.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def test_format_remaining():
    assert format_remaining(0) == "0:00"
    assert format_remaining(65) == "1:05"
    assert format_remaining(3661) == "1:01:01"


def test_countdown_and_expiry():
    clock = FakeClock()
    timer = SessionTimer(60, clock=clock)
    timer.start()
    assert not timer.is_expired()
    assert abs(timer.remaining_seconds() - 60) < 0.01
    clock.advance(30)
    assert abs(timer.remaining_seconds() - 30) < 0.01
    clock.advance(40)
    assert timer.is_expired()
    assert timer.remaining_seconds() == 0


def test_pause_freezes_countdown():
    clock = FakeClock()
    timer = SessionTimer(100, clock=clock)
    timer.start()
    clock.advance(20)
    timer.pause()
    clock.advance(50)
    assert abs(timer.remaining_seconds() - 80) < 0.01
    timer.resume()
    clock.advance(10)
    assert abs(timer.remaining_seconds() - 70) < 0.01


def test_extend_while_running():
    clock = FakeClock()
    timer = SessionTimer(60, clock=clock)
    timer.start()
    clock.advance(50)
    timer.extend(30)
    assert abs(timer.remaining_seconds() - 40) < 0.01


def test_extend_after_expiry_restarts():
    clock = FakeClock()
    timer = SessionTimer(10, clock=clock)
    timer.start()
    clock.advance(15)
    assert timer.is_expired()
    timer.extend(300)  # 5 minutes
    assert not timer.is_expired()
    assert abs(timer.remaining_seconds() - 300) < 0.01


def test_restart_from_settings():
    clock = FakeClock()
    timer = SessionTimer(60, clock=clock)
    timer.start()
    clock.advance(40)
    timer.restart(120)
    assert abs(timer.remaining_seconds() - 120) < 0.01
