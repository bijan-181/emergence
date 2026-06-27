"""Event system for component communication."""

from events.bus import EventBus
from events.types import Event, EventType

__all__ = ["EventBus", "Event", "EventType"]
