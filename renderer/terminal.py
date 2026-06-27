"""Terminal renderer — draws the world grid into curses.

The renderer is completely decoupled from the engine.  It reads
the world state (via a snapshot) and paints it to the terminal.
"""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from renderer.colors import BG_DARK_GRAY, BG_GREEN, FG_BRIGHT_GREEN, colored

if TYPE_CHECKING:
    from camera.camera import Camera
    from config.settings import RendererConfig
    from world.world import World


class TerminalRenderer:
    """Renders the world grid inside a curses window.

    Parameters:
        win: The curses window to draw into.
        cfg: Renderer configuration.
        camera: Camera for viewport mapping.
        sidebar_width: Columns reserved for the sidebar.
    """

    def __init__(
        self,
        win: "curses.window",
        cfg: RendererConfig,
        camera: Camera,
        sidebar_width: int = 0,
    ) -> None:
        self._win = win
        self._cfg = cfg
        self._camera = camera
        self._sidebar_width = sidebar_width

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, world: World) -> None:
        """Draw the visible portion of *world* to the terminal."""
        self._win.erase()
        grid = world.get_grid()
        x_start, y_start, x_end, y_end = self._camera.visible_bounds()

        # Clamp to world boundaries.
        x_start = max(0, min(x_start, grid.width))
        y_start = max(0, min(y_start, grid.height))
        x_end = max(0, min(x_end, grid.width))
        y_end = max(0, min(y_end, grid.height))

        max_row, max_col = self._win.getmaxyx()

        # Reserve rows for status bar at bottom.
        draw_rows = max_row - 1
        draw_cols = max_col - self._sidebar_width

        for wy in range(y_start, y_end):
            for wx in range(x_start, x_end):
                sp = self._camera.world_to_screen(wx, wy)
                if 0 <= sp.row < draw_rows and 0 <= sp.col < draw_cols:
                    cell = grid.get(wx, wy)
                    char = self._cfg.alive_char if cell else self._cfg.dead_char
                    if self._cfg.use_color and cell:
                        char = colored(char, fg=FG_BRIGHT_GREEN, bg=BG_GREEN)
                    elif self._cfg.use_color and not cell:
                        char = colored(char, bg=BG_DARK_GRAY)
                    try:
                        self._win.addstr(sp.row, sp.col * self._cfg.cell_width, char)
                    except curses.error:
                        pass  # cursor at edge of window

        self._win.noutrefresh()
