"""World container — the heart of Emergence."""

from __future__ import annotations

import numpy as np

from world.boundary import BoundaryMode
from world.cell import CellState
from world.grid import Grid


class World:
    """A persistent two-dimensional cellular world.

    The world is created once and never reset.  Every modification
    accumulates — the current state encodes the entire history.

    Parameters:
        width: Number of columns.
        height: Number of rows.
        boundary: Edge behaviour (default: toroidal).
    """

    def __init__(
        self,
        width: int,
        height: int,
        boundary: BoundaryMode = BoundaryMode.TOROIDAL,
    ) -> None:
        self.width = width
        self.height = height
        self.boundary = boundary
        self.generation: int = 0
        self._grid = Grid(width, height)

    # ------------------------------------------------------------------
    # State access (delegates to Grid)
    # ------------------------------------------------------------------

    def get(self, x: int, y: int) -> CellState:
        """Return the state of cell at (*x*, *y*)."""
        return self._grid.get(x, y)

    def set(self, x: int, y: int, state: CellState) -> None:
        """Set the state of cell at (*x*, *y*)."""
        self._grid.set(x, y, state)

    def get_grid(self) -> Grid:
        """Return the underlying grid (for physics computation)."""
        return self._grid

    def alive_count(self) -> int:
        """Return the total number of alive cells."""
        return self._grid.alive_count()

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Kill every cell in the world."""
        self._grid.clear()

    def randomize(self, alive_ratio: float = 0.3, seed: int | None = None) -> None:
        """Fill the world randomly.

        Parameters:
            alive_ratio: Fraction of alive cells.
            seed: Optional RNG seed for reproducibility.
        """
        rng = np.random.default_rng(seed)
        self._grid.randomize(alive_ratio, rng)

    def randomize_from_config(self, alive_ratio: float = 0.3, seed: int | None = None) -> None:
        """Randomize using a fresh RNG (alias for clarity)."""
        self.randomize(alive_ratio, seed)

    # ------------------------------------------------------------------
    # Generation management
    # ------------------------------------------------------------------

    def advance_generation(self) -> None:
        """Increment the generation counter."""
        self.generation += 1

    def reset_generation(self) -> None:
        """Reset the generation counter to zero."""
        self.generation = 0

    # ------------------------------------------------------------------
    # Snapshot / history
    # ------------------------------------------------------------------

    def snapshot(self) -> np.ndarray:
        """Return an independent copy of the current grid state."""
        return self._grid.get_array().copy()

    def restore(self, state: np.ndarray) -> None:
        """Restore the grid from a previously captured snapshot."""
        self._grid.set_array(state)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"World({self.width}x{self.height}, "
            f"gen={self.generation}, alive={self.alive_count()})"
        )
