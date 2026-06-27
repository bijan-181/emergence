"""Tests for the world module."""

from __future__ import annotations

import numpy as np
import pytest

from world.cell import CellState
from world.grid import Grid
from world.world import World


class TestGrid:
    """Tests for :class:`Grid`."""

    def test_creation(self) -> None:
        g = Grid(10, 8)
        assert g.width == 10
        assert g.height == 8
        assert g.alive_count() == 0

    def test_invalid_dimensions(self) -> None:
        with pytest.raises(ValueError):
            Grid(0, 5)
        with pytest.raises(ValueError):
            Grid(5, -1)

    def test_get_set(self) -> None:
        g = Grid(5, 5)
        assert g.get(2, 3) == CellState.DEAD
        g.set(2, 3, CellState.ALIVE)
        assert g.get(2, 3) == CellState.ALIVE

    def test_clear(self) -> None:
        g = Grid(5, 5)
        g.set(1, 1, CellState.ALIVE)
        g.set(3, 3, CellState.ALIVE)
        assert g.alive_count() == 2
        g.clear()
        assert g.alive_count() == 0

    def test_randomize(self) -> None:
        g = Grid(100, 100)
        g.randomize(0.5, np.random.default_rng(42))
        count = g.alive_count()
        # With 50% ratio on 10000 cells, expect roughly 5000.
        assert 4000 < count < 6000

    def test_copy(self) -> None:
        g = Grid(5, 5)
        g.set(1, 1, CellState.ALIVE)
        g2 = g.copy()
        g2.set(1, 1, CellState.DEAD)
        assert g.get(1, 1) == CellState.ALIVE
        assert g2.get(1, 1) == CellState.DEAD

    def test_in_bounds(self) -> None:
        g = Grid(10, 10)
        assert g.in_bounds(0, 0)
        assert g.in_bounds(9, 9)
        assert not g.in_bounds(-1, 0)
        assert not g.in_bounds(10, 5)

    def test_set_array(self) -> None:
        g = Grid(3, 3)
        arr = np.ones((3, 3), dtype=np.uint8)
        g.set_array(arr)
        assert g.alive_count() == 9

    def test_set_array_wrong_shape(self) -> None:
        g = Grid(3, 3)
        with pytest.raises(ValueError):
            g.set_array(np.zeros((5, 5), dtype=np.uint8))


class TestWorld:
    """Tests for :class:`World`."""

    def test_creation(self) -> None:
        w = World(20, 15)
        assert w.width == 20
        assert w.height == 15
        assert w.generation == 0
        assert w.alive_count() == 0

    def test_get_set(self) -> None:
        w = World(10, 10)
        w.set(5, 5, CellState.ALIVE)
        assert w.get(5, 5) == CellState.ALIVE

    def test_clear(self) -> None:
        w = World(10, 10)
        w.set(3, 3, CellState.ALIVE)
        w.clear()
        assert w.alive_count() == 0

    def test_randomize(self) -> None:
        w = World(50, 50)
        w.randomize(0.3, seed=42)
        assert w.alive_count() > 0

    def test_generation_advance(self) -> None:
        w = World(5, 5)
        assert w.generation == 0
        w.advance_generation()
        assert w.generation == 1
        w.advance_generation()
        assert w.generation == 2

    def test_generation_reset(self) -> None:
        w = World(5, 5)
        w.advance_generation()
        w.advance_generation()
        w.reset_generation()
        assert w.generation == 0

    def test_snapshot_restore(self) -> None:
        w = World(5, 5)
        w.set(2, 2, CellState.ALIVE)
        snap = w.snapshot()
        w.clear()
        assert w.alive_count() == 0
        w.restore(snap)
        assert w.get(2, 2) == CellState.ALIVE

    def test_repr(self) -> None:
        w = World(10, 10)
        r = repr(w)
        assert "10x10" in r
        assert "gen=0" in r
