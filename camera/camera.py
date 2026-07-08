"""Camera — viewport control with pan, zoom, and coordinate conversion.

The camera is decoupled from the renderer.  It maps between *world
coordinates* (cell positions) and *screen coordinates* (terminal
column / row).

The camera enforces world boundaries: the viewport never shows
negative coordinates or extends beyond the world edges.
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
        world_width: Width of the world in cells.
        world_height: Height of the world in cells.
    """

    def __init__(
        self,
        cfg: CameraConfig,
        view_width: int,
        view_height: int,
        world_width: int = 200,
        world_height: int = 200,
        cell_width: int = 1,
    ) -> None:
        self._cfg = cfg
        self._zoom: float = cfg.default_zoom
        self._offset_x: float = 0.0
        self._offset_y: float = 0.0
        self._view_width = view_width
        self._view_height = view_height
        self._world_width = world_width
        self._world_height = world_height
        self._cell_width = cell_width

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

    @property
    def world_width(self) -> int:
        return self._world_width

    @property
    def world_height(self) -> int:
        return self._world_height

    # ------------------------------------------------------------------
    # Viewport management
    # ------------------------------------------------------------------

    def resize(self, width: int, height: int) -> None:
        """Update the viewport dimensions (e.g. on terminal resize)."""
        self._view_width = width
        self._view_height = height
        self._clamp()

    def set_world_size(self, width: int, height: int) -> None:
        """Update the world dimensions."""
        self._world_width = width
        self._world_height = height
        self._clamp()

    def zoom_in(self) -> None:
        """Increase zoom level."""
        self._zoom = min(self._zoom + self._cfg.zoom_step, self._cfg.max_zoom)
        self._clamp()

    def zoom_out(self) -> None:
        """Decrease zoom level."""
        self._zoom = max(self._zoom - self._cfg.zoom_step, self._cfg.min_zoom)
        self._clamp()

    def reset_zoom(self) -> None:
        """Reset zoom to default (1.0)."""
        self._zoom = self._cfg.default_zoom
        self._clamp()

    def pan(self, dx: int, dy: int) -> None:
        """Shift the viewport by (*dx*, *dy*) world cells."""
        self._offset_x += dx
        self._offset_y += dy
        self._clamp()

    def center_on(self, x: float, y: float) -> None:
        """Center the viewport on world position (*x*, *y*)."""
        self._offset_x = x - self._view_width / (2 * self._zoom)
        self._offset_y = y - self._view_height / (2 * self._zoom)
        self._clamp()

    # ------------------------------------------------------------------
    # Boundary clamping
    # ------------------------------------------------------------------

    def _clamp(self) -> None:
        """Clamp camera offset to world boundaries.

        Ensures the viewport never shows negative coordinates or
        extends beyond the world edges.
        """
        visible_w = self._view_width / self._cell_width / self._zoom
        visible_h = self._view_height / self._zoom

        max_x = max(0.0, self._world_width - visible_w)
        max_y = max(0.0, self._world_height - visible_h)

        self._offset_x = max(0.0, min(self._offset_x, max_x))
        self._offset_y = max(0.0, min(self._offset_y, max_y))

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
        wx = int(col / self._cell_width / self._zoom + self._offset_x)
        wy = int(row / self._zoom + self._offset_y)
        return WorldPos(wx, wy)

    # ------------------------------------------------------------------
    # Visible region
    # ------------------------------------------------------------------

    def visible_bounds(self) -> tuple[int, int, int, int]:
        """Return ``(x_start, y_start, x_end, y_end)`` of visible world cells.

        The bounds are *exclusive* on the end (suitable for ``range()``).
        Values are clamped to the world.
        """
        x_start = max(0, int(self._offset_x))
        y_start = max(0, int(self._offset_y))
        x_end = min(self._world_width, int(self._offset_x + self._view_width / self._cell_width / self._zoom))
        y_end = min(self._world_height, int(self._offset_y + self._view_height / self._zoom))
        return x_start, y_start, x_end, y_end

    def visible_width_cells(self) -> int:
        """Number of world cells visible horizontally."""
        return max(1, int(self._view_width / self._cell_width / self._zoom))

    def visible_height_cells(self) -> int:
        """Number of world cells visible vertically."""
        return max(1, int(self._view_height / self._zoom))
