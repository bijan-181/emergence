"""Perception channels — how agents observe the world."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from world.world import World


# ------------------------------------------------------------------
# Data containers for each view
# ------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LocalView:
    """Cells within a rectangular region around the agent."""

    cells: np.ndarray
    center: tuple[int, int]
    offset: tuple[int, int]
    radius: int


@dataclass(frozen=True, slots=True)
class GlobalView:
    """Full world state snapshot."""

    cells: np.ndarray
    generation: int
    alive_count: int


@dataclass(frozen=True, slots=True)
class TargetView:
    """Current target pattern and alignment info."""

    pattern: np.ndarray
    offset: tuple[int, int]
    is_loaded: bool


@dataclass(frozen=True, slots=True)
class HistoryView:
    """Rolling window of past local views."""

    frames: tuple[np.ndarray, ...]
    generation: int


# ------------------------------------------------------------------
# Perception container
# ------------------------------------------------------------------


@dataclass
class Perception:
    """Aggregate perception assembled from multiple channels."""

    local: LocalView | None = None
    global_view: GlobalView | None = None
    target: TargetView | None = None
    history: HistoryView | None = None
    generation: int = 0


# ------------------------------------------------------------------
# Channel interfaces
# ------------------------------------------------------------------


class PerceptionChannel(ABC):
    """Abstract perception channel."""

    @abstractmethod
    def observe(self, world: World, agent_pos: tuple[int, int]) -> object:
        """Return a channel-specific view."""
        ...


class LocalPerception(PerceptionChannel):
    """Extract a rectangular neighborhood around the agent.

    Parameters:
        radius: Half-width of the square view (view is 2r+1 x 2r+1).
    """

    def __init__(self, radius: int = 50) -> None:
        self.radius = radius

    def observe(self, world: World, agent_pos: tuple[int, int]) -> LocalView:
        cx, cy = agent_pos
        grid = world.get_grid()
        r = self.radius

        xs = [(cx + dx) % grid.width for dx in range(-r, r + 1)]
        ys = [(cy + dy) % grid.height for dy in range(-r, r + 1)]

        cells = np.empty((len(ys), len(xs)), dtype=np.uint8)
        for j, wy in enumerate(ys):
            for i, wx in enumerate(xs):
                cells[j, i] = int(grid.get(wx, wy))

        return LocalView(
            cells=cells,
            center=(cx, cy),
            offset=((cx - r) % grid.width, (cy - r) % grid.height),
            radius=r,
        )


class GlobalPerception(PerceptionChannel):
    """Snapshot of the entire world grid."""

    def observe(self, world: World, agent_pos: tuple[int, int]) -> GlobalView:
        return GlobalView(
            cells=world.snapshot(),
            generation=world.generation,
            alive_count=world.alive_count(),
        )


class TargetPerception(PerceptionChannel):
    """Observe the current target pattern (None-safe)."""

    def __init__(self, target: np.ndarray | None = None) -> None:
        self._target = target

    def set_target(self, target: np.ndarray | None) -> None:
        self._target = target

    def observe(self, world: World, agent_pos: tuple[int, int]) -> TargetView:
        if self._target is None:
            return TargetView(
                pattern=np.array([], dtype=np.uint8),
                offset=(0, 0),
                is_loaded=False,
            )
        return TargetView(
            pattern=self._target,
            offset=(0, 0),
            is_loaded=True,
        )


class HistoryPerception(PerceptionChannel):
    """Maintain a rolling buffer of past local views."""

    def __init__(self, max_frames: int = 10, radius: int = 50) -> None:
        self._max_frames = max_frames
        self._local = LocalPerception(radius)
        self._buffer: list[np.ndarray] = []

    def observe(self, world: World, agent_pos: tuple[int, int]) -> HistoryView:
        local = self._local.observe(world, agent_pos)
        self._buffer.insert(0, local.cells.copy())
        if len(self._buffer) > self._max_frames:
            self._buffer.pop()
        return HistoryView(
            frames=tuple(self._buffer),
            generation=world.generation,
        )
