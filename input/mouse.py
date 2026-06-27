"""Mouse input processing."""

from __future__ import annotations

from enum import Enum, auto


class MouseButton(Enum):
    """Mouse button identifiers."""

    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()
    WHEEL_UP = auto()
    WHEEL_DOWN = auto()


class MouseAction(Enum):
    """Types of mouse interaction."""

    CLICK = auto()
    DRAG_START = auto()
    DRAG_CONTINUE = auto()
    DRAG_END = auto()
    SCROLL = auto()
