"""Unified input handler — dispatches mouse and keyboard events."""

from __future__ import annotations

import curses
import logging
import time
from typing import TYPE_CHECKING

from events.bus import EventBus
from events.types import Event, EventType
from input.keyboard import KeyAction, build_default_bindings
from input.mouse import MouseButton, MouseAction

if TYPE_CHECKING:
    from camera.camera import Camera

logger = logging.getLogger(__name__)

CLICK_THRESHOLD = 10
CLICK_TIME_LIMIT = 0.3


class InputHandler:
    """Process raw terminal input and publish corresponding events.

    Parameters:
        event_bus: Shared event bus.
        camera: Camera for coordinate conversion.
        sim_area_width: Width of the simulation area in columns.
                        Mouse events beyond this column are in the sidebar.
    """

    def __init__(
        self,
        event_bus: EventBus,
        camera: Camera,
        sim_area_width: int = 80,
    ) -> None:
        self._event_bus = event_bus
        self._camera = camera
        self._sim_area_width = sim_area_width
        self._key_bindings = build_default_bindings(curses)
        self._dragging = False
        self._drag_confirmed = False
        self._drag_button: MouseButton | None = None
        self._last_mx: int = 0
        self._last_my: int = 0
        self._press_mx: int = 0
        self._press_my: int = 0
        self._press_time: float = 0.0

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
        mask = 0
        if hasattr(curses, "BUTTON4_SCROLLED"):
            mask |= curses.BUTTON4_SCROLLED
        if hasattr(curses, "BUTTON4_PRESSED"):
            mask |= curses.BUTTON4_PRESSED
        if not mask and hasattr(curses, "BUTTON4_CLICKED"):
            mask = curses.BUTTON4_CLICKED
        return bool(bstate & mask)

    @staticmethod
    def _is_scroll_down(bstate: int) -> bool:
        mask = 0
        if hasattr(curses, "BUTTON5_SCROLLED"):
            mask |= curses.BUTTON5_SCROLLED
        if hasattr(curses, "BUTTON5_PRESSED"):
            mask |= curses.BUTTON5_PRESSED
        if not mask and hasattr(curses, "BUTTON5_CLICKED"):
            mask = curses.BUTTON5_CLICKED
        return bool(bstate & mask)

    @staticmethod
    def _is_motion(bstate: int) -> bool:
        """Check if the event is a mouse motion event."""
        if hasattr(curses, "REPORT_MOUSE_POSITION"):
            return bool(bstate & curses.REPORT_MOUSE_POSITION)
        return False

    def _screen_to_world(self, mx: int, my: int):
        """Convert raw screen coordinates to world coordinates.

        The simulation area starts at column 0, so mx is used directly.
        """
        return self._camera.screen_to_world(mx, my)

    def handle_mouse(self) -> None:
        """Process a curses mouse event and publish the appropriate event."""
        try:
            _, mx, my, _, bstate = curses.getmouse()
        except curses.error as exc:
            logger.warning("getmouse() failed: %s", exc)
            return

        logger.debug("Mouse event: mx=%d my=%d bstate=0x%x", mx, my, bstate)

        # Handle scroll events (zoom) — always process regardless of position.
        if self._is_scroll_up(bstate):
            self._camera.zoom_in()
            logger.debug("Scroll up → zoom %.2f", self._camera.zoom)
            return
        if self._is_scroll_down(bstate):
            self._camera.zoom_out()
            logger.debug("Scroll down → zoom %.2f", self._camera.zoom)
            return

        # Handle motion events during drag.
        if self._is_motion(bstate) and self._dragging:
            self._handle_drag_motion(mx, my)
            return

        # --- Left button ---
        if bstate & curses.BUTTON1_PRESSED:
            self._dragging = True
            self._drag_confirmed = False
            self._drag_button = MouseButton.LEFT
            self._press_mx = mx
            self._press_my = my
            self._press_time = time.monotonic()
            self._last_mx = mx
            self._last_my = my
            return

        if bstate & curses.BUTTON1_RELEASED:
            if self._dragging and self._drag_button == MouseButton.LEFT:
                if not self._drag_confirmed:
                    dist = abs(mx - self._press_mx) + abs(my - self._press_my)
                    elapsed = time.monotonic() - self._press_time
                    if dist <= CLICK_THRESHOLD or elapsed < CLICK_TIME_LIMIT:
                        world_pos = self._screen_to_world(mx, my)
                        logger.debug("Left click at screen(%d,%d) → world(%d,%d)", mx, my, world_pos.x, world_pos.y)
                        self._event_bus.publish(
                            Event(EventType.INPUT_CELL_TOGGLE, {"x": world_pos.x, "y": world_pos.y})
                        )
                self._dragging = False
                self._drag_confirmed = False
                self._drag_button = None
            return

        if bstate & curses.BUTTON1_CLICKED:
            world_pos = self._screen_to_world(mx, my)
            logger.debug("Left click at screen(%d,%d) → world(%d,%d)", mx, my, world_pos.x, world_pos.y)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_TOGGLE, {"x": world_pos.x, "y": world_pos.y})
            )
            return

        # --- Right button ---
        if bstate & curses.BUTTON3_PRESSED:
            self._dragging = True
            self._drag_confirmed = False
            self._drag_button = MouseButton.RIGHT
            self._press_mx = mx
            self._press_my = my
            self._press_time = time.monotonic()
            self._last_mx = mx
            self._last_my = my
            return

        if bstate & curses.BUTTON3_RELEASED:
            if self._dragging and self._drag_button == MouseButton.RIGHT:
                if not self._drag_confirmed:
                    dist = abs(mx - self._press_mx) + abs(my - self._press_my)
                    elapsed = time.monotonic() - self._press_time
                    if dist <= CLICK_THRESHOLD or elapsed < CLICK_TIME_LIMIT:
                        world_pos = self._screen_to_world(mx, my)
                        logger.debug("Right click at screen(%d,%d) → world(%d,%d)", mx, my, world_pos.x, world_pos.y)
                        self._event_bus.publish(
                            Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
                        )
                self._dragging = False
                self._drag_confirmed = False
                self._drag_button = None
            return

        if bstate & curses.BUTTON3_CLICKED:
            world_pos = self._screen_to_world(mx, my)
            logger.debug("Right click at screen(%d,%d) → world(%d,%d)", mx, my, world_pos.x, world_pos.y)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
            )
            return

        # --- Middle button (pan) ---
        if bstate & curses.BUTTON2_PRESSED:
            self._dragging = True
            self._drag_confirmed = True
            self._drag_button = MouseButton.MIDDLE
            self._last_mx = mx
            self._last_my = my
            return

        if bstate & curses.BUTTON2_RELEASED:
            self._dragging = False
            self._drag_confirmed = False
            self._drag_button = None
            return

        if bstate & curses.BUTTON2_CLICKED:
            return

    def _handle_drag_motion(self, mx: int, my: int) -> None:
        """Handle mouse motion during an active drag."""
        if not self._drag_confirmed:
            dist = abs(mx - self._press_mx) + abs(my - self._press_my)
            elapsed = time.monotonic() - self._press_time
            if dist > CLICK_THRESHOLD and elapsed >= CLICK_TIME_LIMIT:
                self._drag_confirmed = True
                logger.debug("Drag confirmed from (%d,%d)", self._press_mx, self._press_my)
            else:
                return

        if self._drag_button == MouseButton.LEFT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_PAINT, {"x": world_pos.x, "y": world_pos.y})
            )
        elif self._drag_button == MouseButton.RIGHT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
            )
        elif self._drag_button == MouseButton.MIDDLE:
            dx = self._last_mx - mx
            dy = self._last_my - my
            if dx != 0 or dy != 0:
                self._camera.pan(dx, dy)

        self._last_mx = mx
        self._last_my = my

    # ------------------------------------------------------------------
    # Continuous input (called each frame for held buttons)
    # ------------------------------------------------------------------

    def poll_drag(self) -> None:
        """Emit drag-continue events for currently held mouse buttons.

        Curses only delivers press/release events; continuous drag
        requires polling ``getmouse()`` each frame while a button
        is held.  This is a fallback for terminals that don't
        support REPORT_MOUSE_POSITION.
        """
        if not self._dragging or self._drag_button is None:
            return

        try:
            _, mx, my, _, bstate = curses.getmouse()
        except curses.error:
            return

        if self._drag_button == MouseButton.LEFT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_PAINT, {"x": world_pos.x, "y": world_pos.y})
            )
        elif self._drag_button == MouseButton.RIGHT:
            world_pos = self._screen_to_world(mx, my)
            self._event_bus.publish(
                Event(EventType.INPUT_CELL_ERASE, {"x": world_pos.x, "y": world_pos.y})
            )
        elif self._drag_button == MouseButton.MIDDLE:
            dx = self._last_mx - mx
            dy = self._last_my - my
            if dx != 0 or dy != 0:
                self._camera.pan(dx, dy)

        self._last_mx = mx
        self._last_my = my
