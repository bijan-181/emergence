"""Tests for agents/perception.py — Perception channels."""

from __future__ import annotations

import numpy as np

from agents.perception import (
    GlobalPerception,
    HistoryPerception,
    LocalPerception,
    Perception,
    TargetPerception,
)


class TestLocalPerception:
    def test_shape(self, small_world) -> None:
        ch = LocalPerception(radius=2)
        view = ch.observe(small_world, (2, 2))
        assert view.cells.shape == (5, 5)

    def test_center_matches_world(self, small_world) -> None:
        from world.cell import CellState

        small_world.set(2, 2, CellState.ALIVE)
        ch = LocalPerception(radius=2)
        view = ch.observe(small_world, (2, 2))
        assert view.cells[2, 2] == 1

    def test_toroidal_wrapping(self, small_world) -> None:
        from world.cell import CellState

        small_world.set(0, 0, CellState.ALIVE)
        ch = LocalPerception(radius=2)
        view = ch.observe(small_world, (4, 4))
        assert view.cells[3, 3] == 1

    def test_offset(self, small_world) -> None:
        ch = LocalPerception(radius=2)
        view = ch.observe(small_world, (2, 2))
        assert view.offset == (0, 0)
        assert view.radius == 2
        assert view.center == (2, 2)


class TestGlobalPerception:
    def test_snapshot_matches_world(self, small_world) -> None:
        ch = GlobalPerception()
        view = ch.observe(small_world, (0, 0))
        assert np.array_equal(view.cells, small_world.snapshot())

    def test_generation(self, small_world) -> None:
        small_world.advance_generation()
        small_world.advance_generation()
        ch = GlobalPerception()
        view = ch.observe(small_world, (0, 0))
        assert view.generation == 2

    def test_alive_count(self, small_world) -> None:
        ch = GlobalPerception()
        view = ch.observe(small_world, (0, 0))
        assert view.alive_count == small_world.alive_count()


class TestTargetPerception:
    def test_none_target(self, small_world) -> None:
        ch = TargetPerception(None)
        view = ch.observe(small_world, (0, 0))
        assert view.is_loaded is False

    def test_loaded_target(self, small_world) -> None:
        target = np.ones((5, 5), dtype=np.uint8)
        ch = TargetPerception(target)
        view = ch.observe(small_world, (0, 0))
        assert view.is_loaded is True
        assert np.array_equal(view.pattern, target)

    def test_set_target(self, small_world) -> None:
        ch = TargetPerception(None)
        assert ch.observe(small_world, (0, 0)).is_loaded is False
        ch.set_target(np.ones((3, 3), dtype=np.uint8))
        assert ch.observe(small_world, (0, 0)).is_loaded is True


class TestHistoryPerception:
    def test_buffer_grows(self, small_world) -> None:
        ch = HistoryPerception(max_frames=3, radius=2)
        for _ in range(5):
            ch.observe(small_world, (2, 2))
        view = ch.observe(small_world, (2, 2))
        assert len(view.frames) == 3

    def test_generation_tracked(self, small_world) -> None:
        small_world.advance_generation()
        ch = HistoryPerception(max_frames=3, radius=2)
        view = ch.observe(small_world, (2, 2))
        assert view.generation == 1


class TestPerception:
    def test_aggregate(self, small_world) -> None:
        p = Perception(generation=42)
        assert p.generation == 42
        assert p.local is None
        assert p.global_view is None
        assert p.target is None
        assert p.history is None
