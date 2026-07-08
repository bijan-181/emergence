"""Tests for the clock module."""

from __future__ import annotations

import time

from core.clock import Clock


class TestClock:
    """Tests for :class:`Clock`."""

    def test_initial_fps(self) -> None:
        c = Clock(60)
        assert c.fps == 60.0

    def test_target_fps(self) -> None:
        c = Clock(30)
        assert c.target_fps == 30

    def test_frame_interval(self) -> None:
        c = Clock(20)
        assert c.frame_interval == 0.05

    def test_tick_measures_fps(self) -> None:
        c = Clock(60)
        c.tick()
        time.sleep(0.02)
        c.tick()
        time.sleep(0.02)
        c.tick()
        # Should measure roughly 50 fps (20ms per frame)
        assert 30 < c.fps < 80

    def test_reset(self) -> None:
        c = Clock(60)
        c.tick()
        time.sleep(0.01)
        c.tick()
        c.reset()
        assert c.fps == 60.0

    def test_fps_returns_target_before_enough_samples(self) -> None:
        c = Clock(30)
        c.tick()
        # Only 1 sample, should return target
        assert c.fps == 30.0
