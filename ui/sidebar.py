"""Right sidebar — displays simulation information."""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from renderer.colors import BOLD, DIM, FG_BRIGHT_CYAN, FG_BRIGHT_GREEN, FG_BRIGHT_YELLOW, FG_CYAN, FG_GREEN, FG_YELLOW, RESET

if TYPE_CHECKING:
    from core.engine import Engine
    from camera.camera import Camera


class Sidebar:
    """Fixed panel on the right side of the terminal.

    Parameters:
        win: The curses window to draw into.
        width: Width in columns.
        engine: Simulation engine for status data.
        camera: Camera for viewport data.
    """

    def __init__(
        self,
        win: "curses.window",
        width: int,
        engine: Engine,
        camera: Camera,
    ) -> None:
        self._win = win
        self._width = width
        self._engine = engine
        self._camera = camera
        self._current_tool: str = "paint"

    def set_tool(self, tool: str) -> None:
        """Update the currently active tool name."""
        self._current_tool = tool

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> None:
        """Draw the sidebar contents."""
        max_row, max_col = self._win.getmaxyx()
        x_start = max_col - self._width

        sections = self._build_sections()
        row = 0

        for title, lines in sections:
            if row >= max_row:
                break
            # Section title
            header = f" {title} "
            try:
                self._win.addnstr(
                    row, x_start, header.ljust(self._width - 1), self._width - 1,
                    curses.A_BOLD | curses.A_REVERSE,
                )
            except curses.error:
                pass
            row += 1

            for line in lines:
                if row >= max_row:
                    break
                try:
                    self._win.addnstr(row, x_start, f" {line}".ljust(self._width - 1), self._width - 1)
                except curses.error:
                    pass
                row += 1

            row += 1  # blank line between sections

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------

    def _build_sections(self) -> list[tuple[str, list[str]]]:
        e = self._engine
        cam = self._camera
        state_str = "RUNNING" if e.is_running else ("PAUSED" if e.is_paused else "IDLE")

        return [
            ("Simulation", [
                f"Generation:   {e.generation}",
                f"State:        {state_str}",
                f"FPS:          {e.fps:.1f}",
                f"Speed:        {e.speed:.1f} gen/s",
            ]),
            ("World", [
                f"Alive cells:  {e.alive_count}",
                f"Dimensions:   {e.world.width}x{e.world.height}",
            ]),
            ("Camera", [
                f"Zoom:         {cam.zoom:.2f}x",
                f"Offset:       ({cam.offset_x:.0f}, {cam.offset_y:.0f})",
                f"Visible:      {cam.visible_width_cells()}x{cam.visible_height_cells()}",
            ]),
            ("Tool", [
                f"Current:      {self._current_tool}",
            ]),
            ("Shortcuts", [
                "Space  Pause/Resume",
                "N      Next generation",
                "R      Reset world",
                "C      Clear world",
                "G      Randomize",
                "+/-    Speed +/-",
                "0      Reset zoom",
                "Arrows Pan",
                "ESC    Quit",
                "LClick Toggle cell",
                "RClick Erase cell",
                "Drag   Paint",
                "Scroll Zoom",
                "MMouse Pan",
            ]),
            ("Future", [
                "  [Agent status]",
                "  [Target info]",
                "  [Evolution]",
                "  [Metrics]",
            ]),
        ]
