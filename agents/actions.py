"""Action types — what agents can do to the world."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from events.bus import EventBus
    from world.world import World


class ActionType(Enum):
    """Categories of world modification."""

    MODIFY_CELL = auto()
    MODIFY_REGION = auto()
    SIGNAL = auto()
    WAIT = auto()


class Action(ABC):
    """An instruction to modify the world.

    Created by agents, applied by the AgentManager.
    """

    __slots__ = ("action_type", "agent_id")

    def __init__(self, action_type: ActionType, agent_id: str) -> None:
        self.action_type = action_type
        self.agent_id = agent_id

    @abstractmethod
    def apply(self, world: World, event_bus: EventBus) -> None:
        """Execute this action against the world."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(agent={self.agent_id!r})"


class ModifyCell(Action):
    """Set a single cell to a specific state."""

    __slots__ = ("x", "y", "alive")

    def __init__(
        self, x: int, y: int, alive: bool, agent_id: str = ""
    ) -> None:
        super().__init__(ActionType.MODIFY_CELL, agent_id)
        self.x = x
        self.y = y
        self.alive = alive

    def apply(self, world: World, event_bus: EventBus) -> None:
        from world.cell import CellState

        state = CellState.ALIVE if self.alive else CellState.DEAD
        world.set(self.x, self.y, state)


class ModifyRegion(Action):
    """Set a rectangular region of cells."""

    __slots__ = ("x1", "y1", "x2", "y2", "pattern")

    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        pattern: np.ndarray | None = None,
        agent_id: str = "",
    ) -> None:
        super().__init__(ActionType.MODIFY_REGION, agent_id)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.pattern = pattern

    def apply(self, world: World, event_bus: EventBus) -> None:
        from world.cell import CellState

        grid = world.get_grid()
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                if not grid.in_bounds(x, y):
                    continue
                if self.pattern is not None:
                    py = y - self.y1
                    px = x - self.x1
                    if (
                        py < self.pattern.shape[0]
                        and px < self.pattern.shape[1]
                    ):
                        state = (
                            CellState.ALIVE
                            if self.pattern[py, px]
                            else CellState.DEAD
                        )
                    else:
                        continue
                else:
                    state = CellState.ALIVE
                world.set(x, y, state)


class Signal(Action):
    """Broadcast information to other agents (Phase 5+ stub)."""

    __slots__ = ("channel", "message")

    def __init__(
        self,
        channel: str = "default",
        message: dict | None = None,
        agent_id: str = "",
    ) -> None:
        super().__init__(ActionType.SIGNAL, agent_id)
        self.channel = channel
        self.message = message or {}

    def apply(self, world: World, event_bus: EventBus) -> None:
        pass


class Wait(Action):
    """Observe without modifying the world."""

    def __init__(self, agent_id: str = "") -> None:
        super().__init__(ActionType.WAIT, agent_id)

    def apply(self, world: World, event_bus: EventBus) -> None:
        pass


class ActionSpace:
    """Defines the set of actions an agent can take.

    In Phase 2 this is a simple container. Phase 3+ will add
    sampling strategies for RL.
    """

    def __init__(self, enabled_types: list[ActionType] | None = None) -> None:
        self.enabled = enabled_types or list(ActionType)

    def is_enabled(self, action_type: ActionType) -> bool:
        return action_type in self.enabled

    def create_modify_cell(
        self, x: int, y: int, alive: bool, agent_id: str = ""
    ) -> ModifyCell:
        return ModifyCell(x, y, alive, agent_id)

    def create_modify_region(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        pattern: np.ndarray | None = None,
        agent_id: str = "",
    ) -> ModifyRegion:
        return ModifyRegion(x1, y1, x2, y2, pattern, agent_id)

    def create_signal(
        self, channel: str = "default", agent_id: str = ""
    ) -> Signal:
        return Signal(channel=channel, agent_id=agent_id)

    def create_wait(self, agent_id: str = "") -> Wait:
        return Wait(agent_id=agent_id)
