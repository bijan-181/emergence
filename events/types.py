"""Event type definitions for the Emergence event system."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class EventType(Enum):
    """Core event types published by the simulation."""

    # Lifecycle events
    ENGINE_STARTED = auto()
    ENGINE_PAUSED = auto()
    ENGINE_RESUMED = auto()
    ENGINE_SHUTDOWN = auto()

    # Generation events
    GENERATION_BEGIN = auto()
    GENERATION_END = auto()

    # World events
    CELL_STATE_CHANGED = auto()
    WORLD_CLEARED = auto()
    WORLD_RANDOMIZED = auto()

    # Input events
    INPUT_CELL_TOGGLE = auto()
    INPUT_CELL_ERASE = auto()
    INPUT_CELL_PAINT = auto()
    INPUT_ZOOM = auto()
    INPUT_PAN = auto()

    # Control events
    SIMULATION_STEP = auto()
    SIMULATION_SPEED_CHANGED = auto()
    SIMULATION_RESET = auto()


@dataclass(frozen=True, slots=True)
class Event:
    """An immutable event payload.

    Attributes:
        type: The kind of event.
        data: Arbitrary payload carried by the event.
    """

    type: EventType
    data: dict[str, Any] = field(default_factory=dict)
