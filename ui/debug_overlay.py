"""Developer debug overlay — toggled with F1.

Displays runtime diagnostics over the simulation area without
interfering with the normal UI layout.
"""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING, Any

from renderer.colors import PAIR_STATUS_BAR as _pair_debug

if TYPE_CHECKING:
    from camera.camera import Camera
    from core.clock import Clock
    from core.engine import Engine
    from input.handler import InputHandler


class DebugOverlay:
    """Transparent overlay showing developer diagnostics.

    Parameters:
        engine: Simulation engine.
        camera: Camera for viewport data.
        input_handler: Input handler for mouse state.
        render_clock: Render clock for FPS measurement.
        world_width: World width in cells.
        world_height: World height in cells.
    """

    def __init__(
        self,
        engine: Engine,
        camera: Camera,
        input_handler: InputHandler,
        render_clock: Clock,
        world_width: int,
        world_height: int,
    ) -> None:
        self._engine = engine
        self._camera = camera
        self._input_handler = input_handler
        self._render_clock = render_clock
        self._world_width = world_width
        self._world_height = world_height

    def render(self, stdscr: Any) -> None:
        """Draw the debug overlay onto the main screen.

        Renders at the top-left corner of stdscr, floating above
        all subwindows.
        """
        lines = self._build_lines()
        attr = _pair_debug() | curses.A_REVERSE

        max_row, max_col = stdscr.getmaxyx()
        for i, line in enumerate(lines):
            if i + 1 >= max_row - 1:
                break
            padded = f" {line}".ljust(min(len(line) + 2, max_col - 2))
            try:
                stdscr.addnstr(i + 1, 1, padded, min(len(padded), max_col - 2), attr)
            except curses.error:
                pass

        stdscr.noutrefresh()

    def get_lines(self) -> list[str]:
        """Return the debug overlay content as a list of strings."""
        return self._build_lines()

    def _build_lines(self) -> list[str]:
        cam = self._camera
        e = self._engine
        mx, my = self._input_handler._last_mx, self._input_handler._last_my
        world_pos = cam.screen_to_world(mx, my)
        state_str = "RUNNING" if e.is_running else ("PAUSED" if e.is_paused else "IDLE")
        x0, y0, x1, y1 = cam.visible_bounds()

        return [
            "=== DEBUG OVERLAY (F1 to toggle) ===",
            f"Mouse screen:  ({mx}, {my})",
            f"Mouse world:   ({world_pos.x}, {world_pos.y})",
            f"Camera offset: ({cam.offset_x:.1f}, {cam.offset_y:.1f})",
            f"Camera bounds: ({x0}, {y0}) -> ({x1}, {y1})",
            f"Zoom level:    {cam.zoom:.2f}x",
            f"Viewport:      {cam.view_width}x{cam.view_height}",
            f"World size:    {self._world_width}x{self._world_height}",
            f"Render FPS:    {self._render_clock.fps:.1f}",
            f"Sim TPS:       {e.tps:.1f}",
            f"Sim state:     {state_str}",
            f"Generation:    {e.generation}",
            f"Alive cells:   {e.alive_count}",
            f"Speed:         {e.speed:.1f} gen/s",
            f"Dragging:      {self._input_handler._dragging}",
        ]
