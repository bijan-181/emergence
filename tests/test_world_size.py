"""Tests for world size configuration."""

from __future__ import annotations

from config.settings import Settings, WorldConfig
from world.grid import Grid
from world.world import World


class TestWorldSizeConfiguration:
    """Tests for world size configuration and large world support."""

    def test_default_world_size(self) -> None:
        s = Settings()
        assert s.world.width == 200
        assert s.world.height == 200

    def test_custom_world_size(self) -> None:
        wc = WorldConfig(width=500, height=500)
        assert wc.width == 500
        assert wc.height == 500

    def test_world_creation_with_config(self) -> None:
        s = Settings()
        w = World(s.world.width, s.world.height)
        assert w.width == 200
        assert w.height == 200

    def test_grid_creation_large(self) -> None:
        g = Grid(500, 500)
        assert g.width == 500
        assert g.height == 500
        assert g.alive_count() == 0

    def test_grid_creation_1000x1000(self) -> None:
        g = Grid(1000, 1000)
        assert g.width == 1000
        assert g.height == 1000

    def test_world_randomize_large(self) -> None:
        w = World(500, 500)
        w.randomize(0.3, seed=42)
        assert w.alive_count() > 0

    def test_world_operations_on_large_grid(self) -> None:
        w = World(500, 500)
        w.set(250, 250, 1)
        assert w.get(250, 250).value == 1
        w.clear()
        assert w.alive_count() == 0

    def test_grid_in_bounds_large(self) -> None:
        g = Grid(1000, 1000)
        assert g.in_bounds(0, 0)
        assert g.in_bounds(999, 999)
        assert not g.in_bounds(1000, 0)
        assert not g.in_bounds(0, 1000)
        assert not g.in_bounds(-1, 0)
