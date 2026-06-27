"""Simulation timing and control."""

from __future__ import annotations

import time


class Clock:
    """Controls simulation speed and provides timing information.

    The clock does **not** drive the main loop — the caller
    decides when to call :meth:`tick`.  This keeps the engine
    decoupled from any specific timing mechanism.

    Parameters:
        target_fps: Desired frames (generations) per second.
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
        """Measured frames per second (rolling average)."""
        if not self._frame_times:
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
