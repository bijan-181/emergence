"""Tests for agents/config.py — AgentConfig."""

from __future__ import annotations

from agents.config import ActionConfig, AgentConfig, PerceptionConfig


class TestPerceptionConfig:
    def test_defaults(self) -> None:
        cfg = PerceptionConfig()
        assert cfg.local_radius == 50
        assert cfg.history_buffer_size == 10
        assert cfg.enable_global_view is True
        assert cfg.enable_target_view is True
        assert cfg.enable_history is True


class TestActionConfig:
    def test_defaults(self) -> None:
        cfg = ActionConfig()
        assert cfg.max_actions_per_step == 1
        assert cfg.enable_modify_cell is True
        assert cfg.enable_modify_region is True
        assert cfg.enable_signal is False
        assert cfg.enable_wait is True


class TestAgentConfig:
    def test_defaults(self) -> None:
        cfg = AgentConfig()
        assert cfg.max_agents == 100
        assert cfg.default_agent_type == "REACTIVE"
        assert cfg.agent_step_enabled is True
        assert isinstance(cfg.perception, PerceptionConfig)
        assert isinstance(cfg.action, ActionConfig)
