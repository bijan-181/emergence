"""Emergence — Interactive Conway's Game of Life Sandbox.

Entry point.  Run with::

    python main.py

"""

from __future__ import annotations

import curses
import logging
import time
from typing import Any

from camera.camera import Camera
from config.settings import Settings
from core.engine import Engine
from events.bus import EventBus
from events.types import Event, EventType
from input.handler import InputHandler
from input.keyboard import KeyAction
from renderer.terminal import TerminalRenderer
from ui.sidebar import Sidebar
from ui.status import StatusBar
from world.cell import CellState

logger = logging.getLogger("emergence")


class App:
    """Top-level application that owns the curses loop.

    Keyboard actions are dispatched directly in ``_handle_input``
    (no event bus round-trip) to avoid re-entrant recursion.
    Mouse actions flow through the event bus because the input
    handler publishes them asynchronously.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._event_bus = EventBus()
        self._engine = Engine(settings, self._event_bus)
        self._running = True

        self._camera: Camera | None = None
        self._input_handler: InputHandler | None = None
        self._renderer: TerminalRenderer | None = None
        self._sidebar: Sidebar | None = None
        self._status_bar: StatusBar | None = None

    # ------------------------------------------------------------------
    # Mouse event handlers (via event bus — safe, no re-entrance)
    # ------------------------------------------------------------------

    def _on_cell_toggle(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            current = self._engine.world.get(x, y)
            self._engine.world.set(x, y, CellState.DEAD if current else CellState.ALIVE)

    def _on_cell_erase(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            self._engine.world.set(x, y, CellState.DEAD)

    def _on_cell_paint(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            self._engine.world.set(x, y, CellState.ALIVE)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def _main(self, stdscr: Any) -> None:
        """Curses main loop — called by ``curses.wrapper``."""
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(16)

        # Enable mouse events.
        mouse_mask = (
            curses.BUTTON1_CLICKED
            | curses.BUTTON1_PRESSED
            | curses.BUTTON1_RELEASED
            | curses.BUTTON2_CLICKED
            | curses.BUTTON3_CLICKED
        )
        if hasattr(curses, "BUTTON4_SCROLLED"):
            mouse_mask |= curses.BUTTON4_SCROLLED | curses.BUTTON5_SCROLLED
        else:
            mouse_mask |= curses.BUTTON4_CLICKED | curses.BUTTON5_CLICKED
        curses.mousemask(mouse_mask)

        # Initialise subsystems.
        max_row, max_col = stdscr.getmaxyx()
        sidebar_w = self._settings.ui.sidebar_width
        view_w = max_col - sidebar_w
        view_h = max_row - 1

        self._camera = Camera(self._settings.camera, view_w, view_h)
        self._input_handler = InputHandler(self._event_bus, self._camera)
        self._renderer = TerminalRenderer(stdscr, self._settings.renderer, self._camera, sidebar_w)
        self._sidebar = Sidebar(stdscr, sidebar_w, self._engine, self._camera)
        self._status_bar = StatusBar(stdscr, self._engine, self._camera)

        # Subscribe mouse-cell events (these never re-enter the engine).
        self._event_bus.subscribe(EventType.INPUT_CELL_TOGGLE, self._on_cell_toggle)
        self._event_bus.subscribe(EventType.INPUT_CELL_ERASE, self._on_cell_erase)
        self._event_bus.subscribe(EventType.INPUT_CELL_PAINT, self._on_cell_paint)

        # Start with a random world.
        self._engine.randomize_world()
        self._engine.start()

        # Main loop.
        while self._running:
            loop_start = time.monotonic()

            key = stdscr.getch()
            if key != -1:
                self._handle_input(key)

            if self._engine.is_running:
                self._engine.step()

            stdscr.erase()
            self._renderer.render(self._engine.world)
            self._sidebar.render()
            self._status_bar.render()
            curses.doupdate()

            elapsed = time.monotonic() - loop_start
            frame_interval = 1.0 / max(self._engine.speed, 0.1)
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    # ------------------------------------------------------------------
    # Input dispatch
    # ------------------------------------------------------------------

    def _handle_input(self, key: int) -> None:
        """Dispatch a single key press or mouse event."""
        # Mouse events.
        if key == curses.KEY_MOUSE:
            try:
                self._input_handler.handle_mouse(None)
            except curses.error:
                pass
            return

        # Keyboard shortcuts — dispatched directly, no event bus.
        action = self._input_handler.handle_key(key)
        if action is None:
            return

        if action == KeyAction.QUIT:
            self._running = False
        elif action == KeyAction.TOGGLE_PAUSE:
            if self._engine.is_running:
                self._engine.pause()
            elif self._engine.is_paused:
                self._engine.resume()
        elif action == KeyAction.STEP:
            if self._engine.is_paused:
                self._engine.step()
        elif action == KeyAction.RESET:
            self._engine.reset_world()
        elif action == KeyAction.CLEAR:
            self._engine.clear_world()
        elif action == KeyAction.RANDOMIZE:
            self._engine.randomize_world()
        elif action == KeyAction.SPEED_UP:
            self._engine.increase_speed()
        elif action == KeyAction.SPEED_DOWN:
            self._engine.decrease_speed()
        elif action == KeyAction.ZOOM_RESET:
            self._camera.reset_zoom()
        elif action == KeyAction.PAN_UP:
            self._camera.pan(0, -self._camera._cfg.pan_step)
        elif action == KeyAction.PAN_DOWN:
            self._camera.pan(0, self._camera._cfg.pan_step)
        elif action == KeyAction.PAN_LEFT:
            self._camera.pan(-self._camera._cfg.pan_step, 0)
        elif action == KeyAction.PAN_RIGHT:
            self._camera.pan(self._camera._cfg.pan_step, 0)

    # ------------------------------------------------------------------
    # Entry
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Launch the application."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        )
        logger.info("Emergence sandbox starting")
        try:
            curses.wrapper(self._main)
        except KeyboardInterrupt:
            pass
        finally:
            self._engine.stop()
            logger.info("Emergence sandbox stopped")


def main() -> None:
    settings = Settings()
    app = App(settings)
    app.run()


if __name__ == "__main__":
    main()
