"""Runtime configuration management.

Configuration sources (in priority order):
  1. Runtime overrides (programmatic)
  2. Configuration file (TOML)
  3. Defaults
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorldConfig:
    """World configuration."""

    width: int = 80
    height: int = 24
    initial_alive_ratio: float = 0.3


@dataclass
class SimulationConfig:
    """Simulation configuration."""

    target_fps: int = 10
    min_speed: float = 0.1
    max_speed: float = 60.0
    speed_step: float = 1.0
    default_speed: float = 10.0


@dataclass
class CameraConfig:
    """Camera configuration."""

    min_zoom: float = 0.25
    max_zoom: float = 8.0
    zoom_step: float = 0.25
    default_zoom: float = 1.0
    pan_step: int = 5


@dataclass
class RendererConfig:
    """Renderer configuration."""

    alive_char: str = "█"
    dead_char: str = " "
    cell_width: int = 2
    use_color: bool = True


@dataclass
class UIConfig:
    """UI configuration."""

    sidebar_width: int = 32
    status_height: int = 1


@dataclass
class Settings:
    """Top-level configuration container.

    Aggregates every subsystem's configuration into one object that
    is passed to the components that need it.
    """

    world: WorldConfig = field(default_factory=WorldConfig)
    simulation: SimulationConfig = field(default_factory=SimulationConfig)
    camera: CameraConfig = field(default_factory=CameraConfig)
    renderer: RendererConfig = field(default_factory=RendererConfig)
    ui: UIConfig = field(default_factory=UIConfig)
