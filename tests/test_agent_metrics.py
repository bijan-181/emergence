"""Tests for agents/metrics.py — AgentMetrics."""

from __future__ import annotations

from agents.metrics import AgentMetrics
from events.bus import EventBus
from events.types import Event, EventType


class TestAgentMetrics:
    def test_counts_actions(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "MODIFY_CELL"})
        )
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "MODIFY_CELL"})
        )
        stats = metrics.get_stats("a1")
        assert stats is not None
        assert stats.total_actions == 2
        assert stats.cell_modifications == 2

    def test_counts_waits(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "WAIT"})
        )
        stats = metrics.get_stats("a1")
        assert stats.wait_count == 1

    def test_rewards(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(
            Event(EventType.AGENT_REWARD, {"agent_id": "a1", "amount": 1.5})
        )
        event_bus.publish(
            Event(EventType.AGENT_REWARD, {"agent_id": "a1", "amount": 0.5})
        )
        stats = metrics.get_stats("a1")
        assert stats.total_reward == 2.0

    def test_reset(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "WAIT"})
        )
        metrics.reset()
        assert metrics.all_stats() == {}

    def test_created_destroyed(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(Event(EventType.AGENT_CREATED, {"agent_id": "a1"}))
        assert metrics.get_stats("a1") is not None
        event_bus.publish(Event(EventType.AGENT_DESTROYED, {"agent_id": "a1"}))
        assert metrics.get_stats("a1") is None

    def test_all_stats(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(Event(EventType.AGENT_CREATED, {"agent_id": "a1"}))
        event_bus.publish(Event(EventType.AGENT_CREATED, {"agent_id": "a2"}))
        all_stats = metrics.all_stats()
        assert "a1" in all_stats
        assert "a2" in all_stats

    def test_actions_by_type(self, event_bus) -> None:
        metrics = AgentMetrics(event_bus)
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "MODIFY_CELL"})
        )
        event_bus.publish(
            Event(EventType.AGENT_ACTION, {"agent_id": "a1", "action_type": "WAIT"})
        )
        stats = metrics.get_stats("a1")
        assert stats.actions_by_type["MODIFY_CELL"] == 1
        assert stats.actions_by_type["WAIT"] == 1
