"""Tests for agents/base.py — Agent ABC and AgentType."""

from __future__ import annotations

import numpy as np
import pytest

from agents.base import Agent, AgentState, AgentType
from agents.actions import Wait
from agents.perception import Perception


class DummyAgent(Agent):
    """Minimal concrete agent for testing the ABC."""

    def perceive(self, world, target):
        return Perception(generation=world.generation)

    def decide(self, perception):
        return Wait(agent_id=self.agent_id)


class TestAgentType:
    def test_all_types_exist(self) -> None:
        assert hasattr(AgentType, "REACTIVE")
        assert hasattr(AgentType, "DELIBERATIVE")
        assert hasattr(AgentType, "LEARNING")
        assert hasattr(AgentType, "SOCIAL")
        assert hasattr(AgentType, "META")

    def test_reactive_is_default(self) -> None:
        assert AgentType.REACTIVE.value == 1


class TestAgentState:
    def test_defaults(self) -> None:
        state = AgentState()
        assert state.position == (0, 0)
        assert state.generation_created == 0
        assert state.total_actions == 0
        assert state.total_reward == 0.0


class TestAgent:
    def test_init(self, small_world) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE, (5, 5))
        assert agent.agent_id == "a1"
        assert agent.agent_type == AgentType.REACTIVE
        assert agent.position == (5, 5)

    def test_state_property(self) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE, (3, 7))
        assert agent.state.position == (3, 7)

    def test_act_increments_actions(self, small_world) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE)
        action = agent.act(small_world, None)
        assert isinstance(action, Wait)
        assert agent.state.total_actions == 1

    def test_act_multiple_times(self, small_world) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE)
        for _ in range(5):
            agent.act(small_world, None)
        assert agent.state.total_actions == 5

    def test_reward(self) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE)
        agent.reward(1.5)
        agent.reward(0.5)
        assert agent.state.total_reward == 2.0

    def test_repr(self) -> None:
        agent = DummyAgent("a1", AgentType.REACTIVE, (1, 2))
        r = repr(agent)
        assert "DummyAgent" in r
        assert "a1" in r
        assert "REACTIVE" in r

    def test_abstract_cannot_instantiate(self) -> None:
        with pytest.raises(TypeError):
            Agent("a1", AgentType.REACTIVE)  # type: ignore[abstract]
