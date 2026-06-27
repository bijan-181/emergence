"""Tests for Game of Life rules."""

from __future__ import annotations

import numpy as np

from core.rules import GameOfLifeRules
from world.cell import CellState
from world.grid import Grid


class TestGameOfLifeRules:
    """Tests for :class:`GameOfLifeRules`."""

    def test_all_dead_stays_dead(self) -> None:
        """An empty world should stay empty."""
        g = Grid(10, 10)
        next_gen = GameOfLifeRules.compute_next(g)
        assert next_gen.sum() == 0

    def test_birth_with_three_neighbors(self) -> None:
        """A dead cell with exactly 3 alive neighbors should become alive."""
        g = Grid(5, 5)
        # Place a blinker horizontally.
        g.set(1, 2, CellState.ALIVE)
        g.set(2, 2, CellState.ALIVE)
        g.set(3, 2, CellState.ALIVE)

        next_gen = GameOfLifeRules.compute_next(g)
        # NumPy indexing: next_gen[y, x]
        # Horizontal blinker at row 2: cells (x=1,y=2), (x=2,y=2), (x=3,y=2)
        # Center (x=2,y=2) has 2 alive neighbors → survives.
        # Ends (x=1,y=2) and (x=3,y=2) have 1 neighbor each → die.
        # Cells above/below center: (x=2,y=1) and (x=2,y=3) each have 3 neighbors → birth.
        assert next_gen[2, 2] == 1  # center survives
        assert next_gen[2, 1] == 0  # left end dies
        assert next_gen[2, 3] == 0  # right end dies
        assert next_gen[1, 2] == 1  # above center born
        assert next_gen[3, 2] == 1  # below center born

    def test_blinker_oscillation(self) -> None:
        """A blinker should oscillate between horizontal and vertical."""
        g = Grid(5, 5)
        # Horizontal blinker.
        g.set(1, 2, CellState.ALIVE)
        g.set(2, 2, CellState.ALIVE)
        g.set(3, 2, CellState.ALIVE)

        # Step 1: becomes vertical.
        arr1 = GameOfLifeRules.compute_next(g)
        g.set_array(arr1)
        assert g.get(2, 1) == CellState.ALIVE
        assert g.get(2, 2) == CellState.ALIVE
        assert g.get(2, 3) == CellState.ALIVE

        # Step 2: returns to horizontal.
        arr2 = GameOfLifeRules.compute_next(g)
        g.set_array(arr2)
        assert g.get(1, 2) == CellState.ALIVE
        assert g.get(2, 2) == CellState.ALIVE
        assert g.get(3, 2) == CellState.ALIVE

    def test_block_still_life(self) -> None:
        """A 2×2 block should remain unchanged."""
        g = Grid(6, 6)
        g.set(2, 2, CellState.ALIVE)
        g.set(3, 2, CellState.ALIVE)
        g.set(2, 3, CellState.ALIVE)
        g.set(3, 3, CellState.ALIVE)

        arr = GameOfLifeRules.compute_next(g)
        # Block should survive: each cell has 3 neighbors.
        assert arr[2, 2] == 1
        assert arr[3, 2] == 1
        assert arr[2, 3] == 1
        assert arr[3, 3] == 1

    def test_overpopulation(self) -> None:
        """A cell with > 3 neighbors should die."""
        g = Grid(5, 5)
        # Fill center with a plus shape (center has 4 neighbors).
        g.set(2, 1, CellState.ALIVE)
        g.set(1, 2, CellState.ALIVE)
        g.set(2, 2, CellState.ALIVE)
        g.set(3, 2, CellState.ALIVE)
        g.set(2, 3, CellState.ALIVE)

        arr = GameOfLifeRules.compute_next(g)
        # Center (2,2) has 4 neighbors → dies.
        assert arr[2, 2] == 0

    def test_underpopulation(self) -> None:
        """A cell with < 2 neighbors should die."""
        g = Grid(5, 5)
        g.set(2, 2, CellState.ALIVE)  # alone

        arr = GameOfLifeRules.compute_next(g)
        assert arr[2, 2] == 0

    def test_toroidal_wrapping(self) -> None:
        """Neighbors should wrap around the edges (toroidal)."""
        g = Grid(5, 5)
        # Place alive cells at opposite corners to test wrapping.
        g.set(0, 0, CellState.ALIVE)
        g.set(4, 4, CellState.ALIVE)
        g.set(0, 4, CellState.ALIVE)

        arr = GameOfLifeRules.compute_next(g)
        # (0,0) should have neighbors at (4,4) and (0,4) via wrapping = 2 → survives.
        assert arr[0, 0] == 1

    def test_output_shape(self) -> None:
        """Output array should match grid dimensions."""
        g = Grid(20, 15)
        arr = GameOfLifeRules.compute_next(g)
        assert arr.shape == (15, 20)
