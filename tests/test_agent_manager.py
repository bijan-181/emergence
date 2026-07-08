"""Tests for agents/manager.py — AgentManager."""

from __future__ import annotations

import numpy as np

from agents.base import AgentType
from agents.manager import AgentManager
from agents.reactive import ReactiveAgent
from events.types import EventType


class TestAgentManager:
    def test_register(self, agent_manager, reactive_agent) -> None:
        agent_manager.register(reactive_agent)
        assert len(agent_manager.agents) == 1
        assert agent_manager.agents[0].agent_id == "test-agent"

    def test_unregister(self, agent_manager, reactive_agent) -> None:
        agent_manager.register(reactive_agent)
        agent_manager.unregister("test-agent")
        assert len(agent_manager.agents) == 0

    def test_set_world(self, agent_manager, small_world) -> None:
        agent_manager.set_world(small_world)
        assert agent_manager._world is small_world

    def test_set_target(self, agent_manager, reactive_agent) -> None:
        agent_manager.register(reactive_agent)
        target = np.ones((5, 5), dtype=np.uint8)
        agent_manager.set_target(target)
        assert agent_manager._target is target
        assert reactive_agent._target is target

    def test_step_no_agents(self, agent_manager, small_world) -> None:
        agent_manager.step(small_world)

    def test_step_with_agents(self, agent_manager, small_world) -> None:
        agent = ReactiveAgent("a1", position=(2, 2), local_radius=2)
        agent_manager.register(agent)
        small_world.clear()
        target = np.ones((5, 5), dtype=np.uint8)
        agent_manager.set_target(target)
        agent_manager.step(small_world)

    def test_register_publishes_event(self, agent_manager, event_bus, reactive_agent) -> None:
        events = []
        event_bus.subscribe(EventType.AGENT_CREATED, lambda e: events.append(e))
        agent_manager.register(reactive_agent)
        assert len(events) == 1
        assert events[0].data["agent_id"] == "test-agent"

    def test_unregister_publishes_event(self, agent_manager, event_bus, reactive_agent) -> None:
        agent_manager.register(reactive_agent)
        events = []
        event_bus.subscribe(EventType.AGENT_DESTROYED, lambda e: events.append(e))
        agent_manager.unregister("test-agent")
        assert len(events) == 1
