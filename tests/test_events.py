"""Tests for the event system."""

from __future__ import annotations

from events.bus import EventBus
from events.types import Event, EventType


class TestEventBus:
    """Tests for :class:`EventBus`."""

    def test_subscribe_publish(self) -> None:
        bus = EventBus()
        received: list[Event] = []
        bus.subscribe(EventType.ENGINE_STARTED, lambda e: received.append(e))
        event = Event(EventType.ENGINE_STARTED)
        bus.publish(event)
        assert len(received) == 1
        assert received[0] is event

    def test_multiple_handlers(self) -> None:
        bus = EventBus()
        count = {"a": 0, "b": 0}
        bus.subscribe(EventType.GENERATION_END, lambda e: count.__setitem__("a", count["a"] + 1))
        bus.subscribe(EventType.GENERATION_END, lambda e: count.__setitem__("b", count["b"] + 1))
        bus.publish(Event(EventType.GENERATION_END))
        assert count["a"] == 1
        assert count["b"] == 1

    def test_unsubscribe(self) -> None:
        bus = EventBus()
        count = {"n": 0}
        handler = lambda e: count.__setitem__("n", count["n"] + 1)
        bus.subscribe(EventType.GENERATION_END, handler)
        bus.publish(Event(EventType.GENERATION_END))
        assert count["n"] == 1
        bus.unsubscribe(EventType.GENERATION_END, handler)
        bus.publish(Event(EventType.GENERATION_END))
        assert count["n"] == 1  # unchanged

    def test_different_event_types(self) -> None:
        bus = EventBus()
        counts = {"a": 0, "b": 0}
        bus.subscribe(EventType.ENGINE_STARTED, lambda e: counts.__setitem__("a", counts["a"] + 1))
        bus.subscribe(EventType.ENGINE_PAUSED, lambda e: counts.__setitem__("b", counts["b"] + 1))
        bus.publish(Event(EventType.ENGINE_STARTED))
        assert counts["a"] == 1
        assert counts["b"] == 0

    def test_clear(self) -> None:
        bus = EventBus()
        count = {"n": 0}
        bus.subscribe(EventType.GENERATION_END, lambda e: count.__setitem__("n", count["n"] + 1))
        bus.clear()
        bus.publish(Event(EventType.GENERATION_END))
        assert count["n"] == 0

    def test_event_data(self) -> None:
        bus = EventBus()
        received: list[dict] = []
        bus.subscribe(EventType.INPUT_CELL_TOGGLE, lambda e: received.append(e.data))
        bus.publish(Event(EventType.INPUT_CELL_TOGGLE, {"x": 5, "y": 3}))
        assert received[0] == {"x": 5, "y": 3}
