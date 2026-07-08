"""Shared pytest fixtures."""

from __future__ import annotations

import numpy as np
import pytest

from agents.manager import AgentManager
from agents.metrics import AgentMetrics
from agents.pattern import PatternGenerator
from agents.reactive import ReactiveAgent
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


@pytest.fixture
def reactive_agent() -> ReactiveAgent:
    return ReactiveAgent(
        agent_id="test-agent",
        position=(10, 10),
        local_radius=5,
    )


@pytest.fixture
def agent_manager(event_bus: EventBus) -> AgentManager:
    return AgentManager(event_bus)


@pytest.fixture
def agent_metrics(event_bus: EventBus) -> AgentMetrics:
    return AgentMetrics(event_bus)


@pytest.fixture
def pattern_generator() -> PatternGenerator:
    return PatternGenerator()


@pytest.fixture
def sample_target() -> np.ndarray:
    """10×10 target pattern with a cross."""
    target = np.zeros((10, 10), dtype=np.uint8)
    target[4, 2:8] = 1
    target[2:8, 4] = 1
    return target
