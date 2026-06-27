"""Engine state machine."""

from __future__ import annotations

from enum import Enum, auto


class EngineState(Enum):
    """Lifecycle states of the simulation engine."""

    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    STEPPING = auto()
    STOPPED = auto()
