"""Camera — viewport control with pan, zoom, and coordinate conversion.

The camera is decoupled from the renderer.  It maps between *world
coordinates* (cell positions) and *screen coordinates* (terminal
column / row).

Future extension: support for infinite worlds by shifting the
visible window without modifying world state.
"""

from __future__ import annotations

from dataclasses import dataclass

from config.settings import CameraConfig


@dataclass(frozen=True, slots=True)
class ScreenPos:
    """A position in screen (terminal) space."""

    col: int
    row: int


@dataclass(frozen=True, slots=True)
class WorldPos:
    """A position in world (cell) space."""

    x: int
    y: int


class Camera:
    """Viewport that maps world cells to screen positions.

    Parameters:
        cfg: Camera configuration.
        view_width: Visible width in screen columns.
        view_height: Visible height in screen rows.
    """

    def __init__(self, cfg: CameraConfig, view_width: int, view_height: int) -> None:
        self._cfg = cfg
        self._zoom: float = cfg.default_zoom
        self._offset_x: float = 0.0
        self._offset_y: float = 0.0
        self._view_width = view_width
        self._view_height = view_height

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def zoom(self) -> float:
        return self._zoom

    @property
    def offset_x(self) -> float:
        return self._offset_x

    @property
    def offset_y(self) -> float:
        return self._offset_y

    @property
    def view_width(self) -> int:
        return self._view_width

    @property
    def view_height(self) -> int:
        return self._view_height

    # ------------------------------------------------------------------
    # Viewport management
    # ------------------------------------------------------------------

    def resize(self, width: int, height: int) -> None:
        """Update the viewport dimensions (e.g. on terminal resize)."""
        self._view_width = width
        self._view_height = height

    def zoom_in(self) -> None:
        """Increase zoom level."""
        self._zoom = min(self._zoom + self._cfg.zoom_step, self._cfg.max_zoom)

    def zoom_out(self) -> None:
        """Decrease zoom level."""
        self._zoom = max(self._zoom - self._cfg.zoom_step, self._cfg.min_zoom)

    def reset_zoom(self) -> None:
        """Reset zoom to default (1.0)."""
        self._zoom = self._cfg.default_zoom

    def pan(self, dx: int, dy: int) -> None:
        """Shift the viewport by (*dx*, *dy*) world cells."""
        self._offset_x += dx
        self._offset_y += dy

    def center_on(self, x: float, y: float) -> None:
        """Center the viewport on world position (*x*, *y*)."""
        self._offset_x = x - self._view_width / (2 * self._zoom)
        self._offset_y = y - self._view_height / (2 * self._zoom)

    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------

    def world_to_screen(self, wx: float, wy: float) -> ScreenPos:
        """Convert world coordinates to screen coordinates."""
        col = int((wx - self._offset_x) * self._zoom)
        row = int((wy - self._offset_y) * self._zoom)
        return ScreenPos(col, row)

    def screen_to_world(self, col: int, row: int) -> WorldPos:
        """Convert screen coordinates to world coordinates."""
        wx = int(col / self._zoom + self._offset_x)
        wy = int(row / self._zoom + self._offset_y)
        return WorldPos(wx, wy)

    # ------------------------------------------------------------------
    # Visible region
    # ------------------------------------------------------------------

    def visible_bounds(self) -> tuple[int, int, int, int]:
        """Return ``(x_start, y_start, x_end, y_end)`` of visible world cells.

        The bounds are *inclusive*.
        """
        x_start = max(0, int(self._offset_x))
        y_start = max(0, int(self._offset_y))
        x_end = int(self._offset_x + self._view_width / self._zoom)
        y_end = int(self._offset_y + self._view_height / self._zoom)
        return x_start, y_start, x_end, y_end

    def visible_width_cells(self) -> int:
        """Number of world cells visible horizontally."""
        return max(1, int(self._view_width / self._zoom))

    def visible_height_cells(self) -> int:
        """Number of world cells visible vertically."""
        return max(1, int(self._view_height / self._zoom))
