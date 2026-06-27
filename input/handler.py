"""Unified input handler — dispatches mouse and keyboard events."""

from __future__ import annotations

import curses
import logging
from typing import TYPE_CHECKING

from events.bus import EventBus
from events.types import Event, EventType
from input.keyboard import KeyAction, build_default_bindings
from input.mouse import MouseButton, MouseAction

if TYPE_CHECKING:
    from camera.camera import Camera

logger = logging.getLogger(__name__)


class InputHandler:
    """Process raw terminal input and publish corresponding events.

    Parameters:
        event_bus: Shared event bus.
        camera: Camera for coordinate conversion.
    """

    def __init__(self, event_bus: EventBus, camera: Camera) -> None:
        self._event_bus = event_bus
        self._camera = camera
        self._key_bindings = build_default_bindings(curses)
        self._dragging = False
        self._drag_button: MouseButton | None = None
        self._last_tool: str = "paint"

    # ------------------------------------------------------------------
    # Keyboard
    # ------------------------------------------------------------------

    def handle_key(self, key: int) -> KeyAction | None:
        """Translate a curses key code to a high-level action.

        Returns the :class:`KeyAction` if the key was recognised,
        ``None`` otherwise.
        """
        action = self._key_bindings.get(key)
        if action is None:
            return None

        logger.debug("Key pressed: %s", action.name)
        return action

    # ------------------------------------------------------------------
    # Mouse
    # ------------------------------------------------------------------

    @staticmethod
    def _is_scroll_up(bstate: int) -> bool:
        if hasattr(curses, "BUTTON4_SCROLLED"):
            return bool(bstate & curses.BUTTON4_SCROLLED)
        return bool(bstate & curses.BUTTON4_CLICKED)

    @staticmethod
    def _is_scroll_down(bstate: int) -> bool:
        if hasattr(curses, "BUTTON5_SCROLLED"):
            return bool(bstate & curses.BUTTON5_SCROLLED)
        return bool(bstate & curses.BUTTON5_CLICKED)

    def handle_mouse(self, event: curses.flushinp | object) -> None:
        """Process a curses mouse event and publish the appropriate event."""
        _, mx, my, _, bstate = curses.getmouse()

        # Determine button from bstate bitmask.
        button: MouseButton | None = None
        action_type: MouseAction | None = None

        if bstate & curses.BUTTON1_CLICKED:
            button = MouseButton.LEFT
            action_type = MouseAction.CLICK
        elif bstate & curses.BUTTON1_PRESSED:
            button = MouseButton.LEFT
            action_type = MouseAction.DRAG_START
            self._dragging = True
            self._drag_button = button
        elif bstate & curses.BUTTON1_RELEASED:
            button = MouseButton.LEFT
            action_type = MouseAction.DRAG_END
            self._dragging = False
            self._drag_button = None
        elif bstate & curses.BUTTON3_CLICKED:
            button = MouseButton.RIGHT
            action_type = MouseAction.CLICK
        elif bstate & curses.BUTTON2_CLICKED:
            button = MouseButton.MIDDLE
            action_type = MouseAction.CLICK
        elif self._is_scroll_up(bstate):
            button = MouseButton.WHEEL_UP
            action_type = MouseAction.SCROLL
        elif self._is_scroll_down(bstate):
            button = MouseButton.WHEEL_DOWN
            action_type = MouseAction.SCROLL

        if button is None or action_type is None:
            return

        world_pos = self._camera.screen_to_world(mx, my)

        if button == MouseButton.WHEEL_UP:
            self._camera.zoom_in()
            return
        if button == MouseButton.WHEEL_DOWN:
            self._camera.zoom_out()
            return

        if button == MouseButton.MIDDLE:
            # Middle-click drag → pan
            if action_type == MouseAction.DRAG_START:
                self._dragging = True
                self._drag_button = MouseButton.MIDDLE
            elif action_type == MouseAction.DRAG_END:
                self._dragging = False
                self._drag_button = None
            return

        if action_type == MouseAction.CLICK:
            if button == MouseButton.LEFT:
                self._event_bus.publish(
                    Event(EventType.INPUT_CELL_TOGGLE, {"x": world_pos.x, "y": world_pos.y})
                )
            elif button == MouseButton.RIGHT:
                self._event_bus.publish(
                    Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
                )
        elif action_type in (MouseAction.DRAG_START, MouseAction.DRAG_CONTINUE):
            if button == MouseButton.LEFT:
                self._event_bus.publish(
                    Event(EventType.INPUT_CELL_PAINT, {"x": world_pos.x, "y": world_pos.y})
                )
