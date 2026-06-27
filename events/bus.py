"""Publish / subscribe event bus."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from events.types import Event, EventType

Handler = Callable[[Event], None]


class EventBus:
    """Decoupled publish / subscribe message bus.

    Components never call each other directly — they publish
    ``Event`` objects that other components subscribe to.
    """

    def __init__(self) -> None:
        self._handlers: dict[EventType, list[Handler]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def subscribe(self, event_type: EventType, handler: Handler) -> None:
        """Register *handler* to be called when *event_type* is published."""
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: EventType, handler: Handler) -> None:
        """Remove a previously registered *handler*."""
        try:
            self._handlers[event_type].remove(handler)
        except ValueError:
            pass

    def publish(self, event: Event) -> None:
        """Dispatch *event* to all registered handlers for its type."""
        for handler in self._handlers[event.type]:
            handler(event)

    def clear(self) -> None:
        """Remove all subscriptions."""
        self._handlers.clear()
