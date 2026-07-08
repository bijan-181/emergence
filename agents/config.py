"""Agent system configuration."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PerceptionConfig:
    """Perception channel configuration."""

    local_radius: int = 50
    history_buffer_size: int = 10
    enable_global_view: bool = True
    enable_target_view: bool = True
    enable_history: bool = True


@dataclass
class ActionConfig:
    """Action space configuration."""

    max_actions_per_step: int = 1
    enable_modify_cell: bool = True
    enable_modify_region: bool = True
    enable_signal: bool = False
    enable_wait: bool = True


@dataclass
class AgentConfig:
    """Agent system configuration."""

    perception: PerceptionConfig = field(default_factory=PerceptionConfig)
    action: ActionConfig = field(default_factory=ActionConfig)
    max_agents: int = 100
    default_agent_type: str = "REACTIVE"
    agent_step_enabled: bool = True
