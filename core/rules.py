"""Conway's Game of Life rules — the physics of the Emergence universe.

Rules (B3/S23):
  - Birth:        dead cell with exactly 3 alive neighbors → alive
  - Survival:     alive cell with 2 or 3 alive neighbors  → alive
  - Underpopulation: alive cell with < 2 alive neighbors   → dead
  - Overpopulation:  alive cell with > 3 alive neighbors   → dead

All cells update *simultaneously*.
"""

from __future__ import annotations

import numpy as np

from world.grid import Grid


class GameOfLifeRules:
    """Compute the next generation of a Game of Life grid.

    Uses a vectorised NumPy implementation for performance.
    """

    @staticmethod
    def compute_next(grid: Grid) -> np.ndarray:
        """Return a new array representing the next generation.

        Parameters:
            grid: The current world grid.

        Returns:
            A ``(height, width)`` ``uint8`` array with the next states.
        """
        cells = grid.get_array()
        h, w = cells.shape

        # Count alive neighbors for every cell via shift-and-add.
        # Toroidal wrapping is achieved by rolling the array.
        neighbors = np.zeros((h, w), dtype=np.uint8)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                neighbors += np.roll(np.roll(cells, dy, axis=0), dx, axis=1)

        # Apply B3/S23 rules via lookup.
        birth = (cells == 0) & (neighbors == 3)
        survive = (cells == 1) & ((neighbors == 2) | (neighbors == 3))

        next_cells = (birth | survive).astype(np.uint8)
        return next_cells
