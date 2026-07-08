"""Abstract agent interface — the contract every agent must fulfil."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

    from agents.actions import Action
    from agents.perception import Perception
    from world.world import World


class AgentType(Enum):
    """Agent architecture categories."""

    REACTIVE = auto()
    DELIBERATIVE = auto()
    LEARNING = auto()
    SOCIAL = auto()
    META = auto()


@dataclass
class AgentState:
    """Mutable internal state carried across generations."""

    position: tuple[int, int] = (0, 0)
    generation_created: int = 0
    total_actions: int = 0
    total_reward: float = 0.0


class Agent(ABC):
    """Abstract base class for all agents.

    Every agent follows the perceive -> decide -> act cycle.
    Agents never modify the world directly — they return Action
    objects that the AgentManager applies.

    Parameters:
        agent_id: Unique identifier.
        agent_type: Architecture category.
        position: World coordinate the agent is anchored to.
    """

    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        position: tuple[int, int] = (0, 0),
    ) -> None:
        self.agent_id = agent_id
        self.agent_type = agent_type
        self._state = AgentState(
            position=position,
            generation_created=0,
        )

    @property
    def position(self) -> tuple[int, int]:
        return self._state.position

    @property
    def state(self) -> AgentState:
        return self._state

    @abstractmethod
    def perceive(self, world: World, target: np.ndarray | None) -> Perception:
        """Build a perception snapshot from the current world state."""
        ...

    @abstractmethod
    def decide(self, perception: Perception) -> Action:
        """Select an action based on the current perception."""
        ...

    def act(self, world: World, target: np.ndarray | None) -> Action:
        """Full perceive -> decide cycle. Called by AgentManager each generation."""
        perception = self.perceive(world, target)
        action = self.decide(perception)
        self._state.total_actions += 1
        return action

    def reward(self, amount: float) -> None:
        """Receive a reward signal. Override in learning agents."""
        self._state.total_reward += amount

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.agent_id!r}, "
            f"type={self.agent_type.name}, pos={self.position})"
        )
