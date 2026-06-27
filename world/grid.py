"""Two-dimensional grid of cells."""

from __future__ import annotations

import numpy as np

from world.cell import CellState


class Grid:
    """A fixed-size two-dimensional array of cells.

    The grid stores cell states in a NumPy array for efficient
    vectorized computation.  It is the data backbone of the
    :class:`~world.world.World`.

    Parameters:
        width: Number of columns.
        height: Number of rows.
    """

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"Grid dimensions must be positive, got {width}x{height}")
        self.width = width
        self.height = height
        self._cells: np.ndarray = np.zeros((height, width), dtype=np.uint8)

    # ------------------------------------------------------------------
    # State access
    # ------------------------------------------------------------------

    def get(self, x: int, y: int) -> CellState:
        """Return the state of the cell at (*x*, *y*)."""
        return CellState(int(self._cells[y, x]))

    def set(self, x: int, y: int, state: CellState) -> None:
        """Set the state of the cell at (*x*, *y*)."""
        self._cells[y, x] = state

    def get_array(self) -> np.ndarray:
        """Return a *view* of the underlying NumPy array (read-only use)."""
        return self._cells

    def set_array(self, array: np.ndarray) -> None:
        """Replace the entire grid contents."""
        if array.shape != (self.height, self.width):
            raise ValueError(
                f"Array shape {array.shape} does not match grid "
                f"({self.height}, {self.width})"
            )
        self._cells = array.astype(np.uint8)

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Set every cell to *DEAD*."""
        self._cells[:] = CellState.DEAD

    def randomize(self, alive_ratio: float = 0.3, rng: np.random.Generator | None = None) -> None:
        """Fill the grid randomly.

        Parameters:
            alive_ratio: Fraction of cells that should be alive.
            rng: Optional NumPy random generator for reproducibility.
        """
        if rng is None:
            rng = np.random.default_rng()
        self._cells = (rng.random((self.height, self.width)) < alive_ratio).astype(np.uint8)

    def alive_count(self) -> int:
        """Return the number of alive cells."""
        return int(np.count_nonzero(self._cells))

    def copy(self) -> Grid:
        """Return an independent deep copy of this grid."""
        new = Grid(self.width, self.height)
        new._cells = self._cells.copy()
        return new

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def in_bounds(self, x: int, y: int) -> bool:
        """Return ``True`` if (*x*, *y*) lies inside the grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def __repr__(self) -> str:
        return f"Grid({self.width}x{self.height}, alive={self.alive_count()})"
