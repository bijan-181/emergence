"""Timing measurement and frame pacing.

The Clock is a passive measurement tool — it does not drive any
loop.  Callers decide when to call :meth:`tick` and
:meth:`sleep_until_next`.
"""

from __future__ import annotations

import time


class Clock:
    """Measures frames per second using a rolling window.

    Parameters:
        target_fps: Desired frames per second (used for
                    :meth:`sleep_until_next` pacing and as the
                    initial reported FPS before any ticks).
    """

    def __init__(self, target_fps: int = 10) -> None:
        self.target_fps = target_fps
        self._last_tick: float = 0.0
        self._frame_times: list[float] = []
        self._max_samples = 60

    @property
    def frame_interval(self) -> float:
        """Seconds between frames at the current target FPS."""
        return 1.0 / max(self.target_fps, 1)

    @property
    def fps(self) -> float:
        """Measured frames per second (rolling average).

        Returns ``target_fps`` until enough samples are collected.
        """
        if len(self._frame_times) < 2:
            return float(self.target_fps)
        return 1.0 / (sum(self._frame_times) / len(self._frame_times))

    def tick(self) -> None:
        """Record the time of this frame and update FPS measurement."""
        now = time.monotonic()
        if self._last_tick > 0:
            dt = now - self._last_tick
            self._frame_times.append(dt)
            if len(self._frame_times) > self._max_samples:
                self._frame_times.pop(0)
        self._last_tick = now

    def sleep_until_next(self) -> None:
        """Block until the next frame should occur."""
        remaining = self.frame_interval - self._elapsed_since_tick()
        if remaining > 0:
            time.sleep(remaining)

    def _elapsed_since_tick(self) -> float:
        if self._last_tick == 0:
            return 0.0
        return time.monotonic() - self._last_tick

    def reset(self) -> None:
        """Reset timing state."""
        self._last_tick = 0.0
        self._frame_times.clear()
