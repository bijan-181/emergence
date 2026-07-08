"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from config.settings import Settings
from events.bus import EventBus
from world.grid import Grid
from world.world import World


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture
def small_grid() -> Grid:
    """5×5 grid."""
    return Grid(5, 5)


@pytest.fixture
def small_world() -> World:
    """5×5 world."""
    return World(5, 5)


@pytest.fixture
def medium_world() -> World:
    """200×200 world (default size)."""
    return World(200, 200)
