"""Tests for agents/reactive.py — ReactiveAgent."""

from __future__ import annotations

import numpy as np

from agents.actions import ModifyCell, Wait
from agents.base import AgentType
from agents.perception import Perception
from agents.reactive import ReactiveAgent


class TestReactiveAgent:
    def test_init(self) -> None:
        agent = ReactiveAgent("r1", position=(5, 5), local_radius=3)
        assert agent.agent_id == "r1"
        assert agent.agent_type == AgentType.REACTIVE
        assert agent.position == (5, 5)

    def test_wait_without_target(self, small_world) -> None:
        agent = ReactiveAgent("r1", position=(2, 2), local_radius=2)
        action = agent.act(small_world, None)
        assert isinstance(action, Wait)

    def test_wait_when_target_empty(self, small_world) -> None:
        agent = ReactiveAgent("r1", position=(2, 2), local_radius=2)
        empty_target = np.zeros((5, 5), dtype=np.uint8)
        small_world.clear()
        action = agent.act(small_world, empty_target)
        assert isinstance(action, Wait)

    def test_modifies_with_target(self, small_world) -> None:
        agent = ReactiveAgent("r1", position=(2, 2), local_radius=2)
        target = np.ones((5, 5), dtype=np.uint8)
        small_world.clear()
        action = agent.act(small_world, target)
        assert isinstance(action, ModifyCell)

    def test_set_target(self) -> None:
        agent = ReactiveAgent("r1")
        new_target = np.ones((3, 3), dtype=np.uint8)
        agent.set_target(new_target, offset=(1, 1))
        assert agent._target is new_target
        assert agent._target_offset == (1, 1)

    def test_perceive_returns_perception(self, small_world) -> None:
        agent = ReactiveAgent("r1", position=(2, 2), local_radius=2)
        perception = agent.perceive(small_world, None)
        assert isinstance(perception, Perception)
        assert perception.local is not None
        assert perception.local.cells.shape == (5, 5)

    def test_repr(self) -> None:
        agent = ReactiveAgent("r1", position=(5, 5), local_radius=3)
        r = repr(agent)
        assert "ReactiveAgent" in r
        assert "r1" in r
