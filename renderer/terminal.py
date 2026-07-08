"""Terminal renderer — draws the world grid into a curses subwindow.

The renderer is completely decoupled from the engine.  It receives
a reference to a *subwindow* that covers only the simulation area
and paints cells into it using overwrite-only strategy (no erase).

Color is handled via curses color pairs initialized by
:func:`renderer.colors.init_colors`.
"""

from __future__ import annotations

import curses
from typing import TYPE_CHECKING

from renderer.colors import PAIR_ALIVE_BG as _pair_alive, PAIR_DEAD_BG as _pair_dead

if TYPE_CHECKING:
    from camera.camera import Camera
    from config.settings import RendererConfig
    from world.world import World


class TerminalRenderer:
    """Renders the world grid into a dedicated curses subwindow.

    Parameters:
        win: A subwindow covering the simulation area only.
        cfg: Renderer configuration.
        camera: Camera for viewport mapping.
    """

    def __init__(
        self,
        win: "curses.window",
        cfg: RendererConfig,
        camera: Camera,
    ) -> None:
        self._win = win
        self._cfg = cfg
        self._camera = camera

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, world: World) -> None:
        """Overwrite the visible portion of *world* into the subwindow.

        The window is cleared before drawing to prevent stale pixels
        after zoom or pan changes.
        """
        self._win.erase()
        grid = world.get_grid()
        x_start, y_start, x_end, y_end = self._camera.visible_bounds()

        x_start = max(0, min(x_start, grid.width))
        y_start = max(0, min(y_start, grid.height))
        x_end = max(0, min(x_end, grid.width))
        y_end = max(0, min(y_end, grid.height))

        max_row, max_col = self._win.getmaxyx()
        cell_w = self._cfg.cell_width

        for wy in range(y_start, y_end):
            for wx in range(x_start, x_end):
                sp = self._camera.world_to_screen(wx, wy)
                if 0 <= sp.row < max_row and 0 <= sp.col * cell_w < max_col:
                    alive = bool(grid.get(wx, wy))
                    attr = _pair_alive() if alive else _pair_dead()
                    char = self._cfg.alive_char if alive else self._cfg.dead_char
                    try:
                        self._win.addstr(sp.row, sp.col * cell_w, char * cell_w, attr)
                    except curses.error:
                        pass

        self._win.noutrefresh()
