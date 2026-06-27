"""Status bar — bottom line of the terminal."""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from renderer.colors import DIM, FG_BRIGHT_GREEN, RESET

if TYPE_CHECKING:
    from core.engine import Engine
    from camera.camera import Camera


class StatusBar:
    """One-line status display at the bottom of the terminal.

    Parameters:
        win: The curses window to draw into.
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
        """Draw the status bar at the bottom row."""
        max_row, max_col = self._win.getmaxyx()
        row = max_row - 1

        e = self._engine
        cam = self._camera

        parts = [
            f"Gen: {e.generation}",
            f"Alive: {e.alive_count}",
            f"Speed: {e.speed:.1f}",
            f"Zoom: {cam.zoom:.1f}x",
        ]

        text = "  │  ".join(parts)

        try:
            self._win.addnstr(row, 0, text.ljust(max_col - 1), max_col - 1, curses.A_REVERSE)
        except curses.error:
            pass
