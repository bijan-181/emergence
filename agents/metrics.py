"""Agent performance tracking."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from events.bus import EventBus
from events.types import Event, EventType


@dataclass
class AgentStats:
    """Per-agent statistics."""

    total_actions: int = 0
    cell_modifications: int = 0
    region_modifications: int = 0
    wait_count: int = 0
    total_reward: float = 0.0
    actions_by_type: dict[str, int] = field(
        default_factory=lambda: defaultdict(int)
    )


class AgentMetrics:
    """Collects and reports agent performance metrics.

    Subscribes to agent events and accumulates statistics.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._stats: dict[str, AgentStats] = defaultdict(AgentStats)
        self._event_bus = event_bus
        self._subscribe()

    def _subscribe(self) -> None:
        self._event_bus.subscribe(EventType.AGENT_ACTION, self._on_action)
        self._event_bus.subscribe(EventType.AGENT_REWARD, self._on_reward)
        self._event_bus.subscribe(EventType.AGENT_CREATED, self._on_created)
        self._event_bus.subscribe(
            EventType.AGENT_DESTROYED, self._on_destroyed
        )

    def _on_action(self, event: Event) -> None:
        agent_id = event.data.get("agent_id", "")
        action_type = event.data.get("action_type", "")
        stats = self._stats[agent_id]
        stats.total_actions += 1
        stats.actions_by_type[action_type] += 1
        if action_type == "MODIFY_CELL":
            stats.cell_modifications += 1
        elif action_type == "MODIFY_REGION":
            stats.region_modifications += 1
        elif action_type == "WAIT":
            stats.wait_count += 1

    def _on_reward(self, event: Event) -> None:
        agent_id = event.data.get("agent_id", "")
        amount = event.data.get("amount", 0.0)
        self._stats[agent_id].total_reward += amount

    def _on_created(self, event: Event) -> None:
        agent_id = event.data.get("agent_id", "")
        self._stats[agent_id] = AgentStats()

    def _on_destroyed(self, event: Event) -> None:
        agent_id = event.data.get("agent_id", "")
        self._stats.pop(agent_id, None)

    def get_stats(self, agent_id: str) -> AgentStats | None:
        return self._stats.get(agent_id)

    def all_stats(self) -> dict[str, AgentStats]:
        return dict(self._stats)

    def reset(self) -> None:
        self._stats.clear()
