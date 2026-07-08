"""Status bar — bottom line of the terminal.

Renders into its own curses subwindow.
"""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from renderer.colors import PAIR_STATUS_BAR as _pair_status

if TYPE_CHECKING:
    from core.engine import Engine
    from camera.camera import Camera


class StatusBar:
    """One-line status display at the bottom of the terminal.

    Parameters:
        win: A subwindow covering the bottom row only.
        engine: Simulation engine for status data.
        camera: Camera for viewport data.
    """

    def __init__(
        self,
        win: "curses.window",
        engine: Engine,
        camera: Camera,
    ) -> None:
        self._win = win
        self._engine = engine
        self._camera = camera

    def render(self) -> None:
        """Draw the status bar into its subwindow."""
        max_row, max_col = self._win.getmaxyx()

        e = self._engine
        cam = self._camera

        parts = [
            f"Gen: {e.generation}",
            f"Alive: {e.alive_count}",
            f"Speed: {e.speed:.1f} gen/s",
            f"TPS: {e.tps:.1f}",
            f"Zoom: {cam.zoom:.1f}x",
        ]

        text = "  |  ".join(parts)

        try:
            self._win.addnstr(0, 0, text.ljust(max_col - 1), max_col - 1, _pair_status())
        except curses.error:
            pass

        self._win.noutrefresh()
