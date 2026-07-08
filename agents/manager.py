"""Agent lifecycle manager — orchestrates the perceive/decide/act cycle."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from agents.base import Agent
from events.bus import EventBus
from events.types import Event, EventType

if TYPE_CHECKING:
    import numpy as np

    from agents.actions import Action
    from world.world import World

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages a collection of agents and their interaction with the world.

    Parameters:
        event_bus: Shared event bus.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._agents: list[Agent] = []
        self._pending_actions: list[Action] = []
        self._world: World | None = None
        self._target: np.ndarray | None = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def register(self, agent: Agent) -> None:
        """Add an agent to the managed collection."""
        self._agents.append(agent)
        self._event_bus.publish(
            Event(
                EventType.AGENT_CREATED,
                {
                    "agent_id": agent.agent_id,
                    "agent_type": agent.agent_type.name,
                },
            )
        )
        logger.info("Agent registered: %s", agent.agent_id)

    def unregister(self, agent_id: str) -> None:
        """Remove an agent by ID."""
        self._agents = [a for a in self._agents if a.agent_id != agent_id]
        self._event_bus.publish(
            Event(EventType.AGENT_DESTROYED, {"agent_id": agent_id})
        )
        logger.info("Agent unregistered: %s", agent_id)

    def set_world(self, world: World) -> None:
        """Bind the manager to a world instance."""
        self._world = world

    def set_target(self, target: np.ndarray | None) -> None:
        """Update the current target pattern for all agents."""
        self._target = target
        for agent in self._agents:
            if hasattr(agent, "set_target"):
                agent.set_target(target)

    @property
    def agents(self) -> list[Agent]:
        return list(self._agents)

    # ------------------------------------------------------------------
    # Generation step
    # ------------------------------------------------------------------

    def step(self, world: World) -> None:
        """Run one full perceive -> decide -> apply cycle for all agents.

        Called by the Engine during the generation cycle.
        """
        if not self._agents or world is None:
            return

        self._pending_actions.clear()

        for agent in self._agents:
            action = agent.act(world, self._target)
            self._pending_actions.append(action)

            self._event_bus.publish(
                Event(
                    EventType.AGENT_DECISION,
                    {
                        "agent_id": agent.agent_id,
                        "action_type": action.action_type.name,
                    },
                )
            )

        self._apply_actions(world)

    def _apply_actions(self, world: World) -> None:
        """Apply all pending actions and publish results."""
        for action in self._pending_actions:
            action.apply(world, self._event_bus)
            self._event_bus.publish(
                Event(
                    EventType.AGENT_ACTION,
                    {
                        "agent_id": action.agent_id,
                        "action_type": action.action_type.name,
                    },
                )
            )

        self._pending_actions.clear()
