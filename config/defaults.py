"""Default configuration values."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorldDefaults:
    """Default world parameters."""

    width: int = 200
    height: int = 200
    initial_alive_ratio: float = 0.3


@dataclass(frozen=True, slots=True)
class SimulationDefaults:
    """Default simulation parameters."""

    target_fps: int = 10
    render_fps: int = 60
    min_speed: float = 0.1
    max_speed: float = 60.0
    speed_step: float = 1.0
    default_speed: float = 10.0


@dataclass(frozen=True, slots=True)
class CameraDefaults:
    """Default camera parameters."""

    min_zoom: float = 0.25
    max_zoom: float = 8.0
    zoom_step: float = 0.25
    default_zoom: float = 1.0
    pan_step: int = 5


@dataclass(frozen=True, slots=True)
class RendererDefaults:
    """Default renderer parameters."""

    alive_char: str = "█"
    dead_char: str = " "
    cell_width: int = 2
    use_color: bool = True


@dataclass(frozen=True, slots=True)
class UIDefaults:
    """Default UI parameters."""

    sidebar_width: int = 32
    status_height: int = 1
