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
        sim_offset_col: Column offset of the simulation area (sidebar width).
                        Mouse x-coordinates are adjusted by this value
                        before being passed to the camera.
    """

    def __init__(
        self,
        event_bus: EventBus,
        camera: Camera,
        sim_offset_col: int = 0,
    ) -> None:
        self._event_bus = event_bus
        self._camera = camera
        self._sim_offset_col = sim_offset_col
        self._key_bindings = build_default_bindings(curses)
        self._dragging = False
        self._drag_button: MouseButton | None = None
        self._last_mx: int = 0
        self._last_my: int = 0

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

    def _screen_to_world(self, mx: int, my: int):
        """Convert raw screen coordinates to world coordinates.

        Adjusts *mx* by the simulation area offset so that clicks
        inside the sidebar are ignored (negative resulting x).
        """
        adj_col = mx - self._sim_offset_col
        return self._camera.screen_to_world(adj_col, my)

    def handle_mouse(self) -> None:
        """Process a curses mouse event and publish the appropriate event."""
        _, mx, my, _, bstate = curses.getmouse()

        # Ignore clicks that land in the sidebar region.
        if mx >= self._sim_offset_col and not (
            self._is_scroll_up(bstate)
            or self._is_scroll_down(bstate)
            or (bstate & curses.BUTTON2_CLICKED)
            or (bstate & curses.BUTTON2_PRESSED)
        ):
            return

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
        elif bstate & curses.BUTTON2_PRESSED:
            button = MouseButton.MIDDLE
            action_type = MouseAction.DRAG_START
            self._dragging = True
            self._drag_button = MouseButton.MIDDLE
            self._last_mx = mx
            self._last_my = my
            return
        elif bstate & curses.BUTTON2_RELEASED:
            button = MouseButton.MIDDLE
            action_type = MouseAction.DRAG_END
            self._dragging = False
            self._drag_button = None
            return
        elif self._is_scroll_up(bstate):
            button = MouseButton.WHEEL_UP
            action_type = MouseAction.SCROLL
        elif self._is_scroll_down(bstate):
            button = MouseButton.WHEEL_DOWN
            action_type = MouseAction.SCROLL

        if button is None or action_type is None:
            return

        # Scroll → zoom (handled immediately, no world coordinates needed).
        if button == MouseButton.WHEEL_UP:
            self._camera.zoom_in()
            return
        if button == MouseButton.WHEEL_DOWN:
            self._camera.zoom_out()
            return

        # Middle-button drag → pan.
        if button == MouseButton.MIDDLE and action_type == MouseAction.DRAG_END:
            self._dragging = False
            self._drag_button = None
            return

        # Left-button click → toggle cell.
        if action_type == MouseAction.CLICK and button == MouseButton.LEFT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_TOGGLE, {"x": world_pos.x, "y": world_pos.y})
            )
            return

        # Right-button click → erase cell.
        if action_type == MouseAction.CLICK and button == MouseButton.RIGHT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
            )
            return

        # Left-button drag → paint.
        if button == MouseButton.LEFT and action_type in (
            MouseAction.DRAG_START,
            MouseAction.DRAG_CONTINUE,
        ):
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_PAINT, {"x": world_pos.x, "y": world_pos.y})
            )
            return

    # ------------------------------------------------------------------
    # Continuous input (called each frame for held buttons)
    # ------------------------------------------------------------------

    def poll_drag(self) -> None:
        """Emit drag-continue events for currently held mouse buttons.

        Curses only delivers press/release events; continuous drag
        requires polling ``getmouse()`` each frame while a button
        is held.
        """
        if not self._dragging or self._drag_button is None:
            return

        try:
            _, mx, my, _, _ = curses.getmouse()
        except curses.error:
            return

        if self._drag_button == MouseButton.LEFT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_PAINT, {"x": world_pos.x, "y": world_pos.y})
            )
        elif self._drag_button == MouseButton.MIDDLE:
            # Pan by the delta from last position (screen pixels).
            dx = self._last_mx - mx
            dy = self._last_my - my
            self._camera.pan(dx, dy)

        self._last_mx = mx
        self._last_my = my
