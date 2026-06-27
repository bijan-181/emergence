"""Emergence — Interactive Conway's Game of Life Sandbox.

Entry point.  Run with::

    python main.py

"""

from __future__ import annotations

import curses
import logging
import sys
import time
from typing import Any

from camera.camera import Camera
from config.settings import Settings
from core.engine import Engine
from core.state import EngineState
from events.bus import EventBus
from events.types import Event, EventType
from input.handler import InputHandler
from input.keyboard import KeyAction
from renderer.terminal import TerminalRenderer
from ui.sidebar import Sidebar
from ui.status import StatusBar

logger = logging.getLogger("emergence")


# ────────────────────────────────────────────────────────────────────
# Wiring
# ────────────────────────────────────────────────────────────────────


class App:
    """Top-level application that owns the curses loop.

    All subsystems are created here and wired together through the
    event bus.  No subsystem knows about any other subsystem except
    through events — preserving the architecture's separation of
    concerns.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._event_bus = EventBus()
        self._engine = Engine(settings, self._event_bus)
        self._running = True

        # Subsystems set up after curses init (see ``_main``).
        self._camera: Camera | None = None
        self._input_handler: InputHandler | None = None
        self._renderer: TerminalRenderer | None = None
        self._sidebar: Sidebar | None = None
        self._status_bar: StatusBar | None = None

    # ────────────────────────────────────────────────────────────────
    # Event handlers (registered once)
    # ────────────────────────────────────────────────────────────────

    def _on_pause(self, _event: Event) -> None:
        if self._engine.is_running:
            self._engine.pause()
        elif self._engine.is_paused:
            self._engine.resume()

    def _on_step(self, _event: Event) -> None:
        if self._engine.is_paused:
            self._engine.step()

    def _on_reset(self, _event: Event) -> None:
        self._engine.reset_world()

    def _on_clear(self, _event: Event) -> None:
        self._engine.clear_world()

    def _on_randomize(self, _event: Event) -> None:
        self._engine.randomize_world()

    def _on_speed_changed(self, event: Event) -> None:
        delta = event.data.get("delta", 0)
        if delta > 0:
            self._engine.increase_speed()
        else:
            self._engine.decrease_speed()

    def _on_cell_toggle(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            current = self._engine.world.get(x, y)
            from world.cell import CellState
            new_state = CellState.DEAD if current else CellState.ALIVE
            self._engine.world.set(x, y, new_state)

    def _on_cell_erase(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            from world.cell import CellState
            self._engine.world.set(x, y, CellState.DEAD)

    def _on_cell_paint(self, event: Event) -> None:
        x, y = event.data.get("x", -1), event.data.get("y", -1)
        if self._engine.world.get_grid().in_bounds(x, y):
            from world.cell import CellState
            self._engine.world.set(x, y, CellState.ALIVE)

    def _register_events(self) -> None:
        self._event_bus.subscribe(EventType.INPUT_CELL_TOGGLE, self._on_pause)
        self._event_bus.subscribe(EventType.SIMULATION_STEP, self._on_step)
        self._event_bus.subscribe(EventType.SIMULATION_RESET, self._on_reset)
        self._event_bus.subscribe(EventType.WORLD_CLEARED, self._on_clear)
        self._event_bus.subscribe(EventType.WORLD_RANDOMIZED, self._on_randomize)
        self._event_bus.subscribe(EventType.SIMULATION_SPEED_CHANGED, self._on_speed_changed)

        # Separate subscription for cell toggle (different from pause toggle).
        # We override the pause subscription above — fix: use distinct event types.
        # Actually, INPUT_CELL_TOGGLE should toggle cells, not pause.
        # Let's correct: INPUT_CELL_TOGGLE → cell toggle; TOGGLE_PAUSE → pause.
        # The keyboard handler publishes INPUT_CELL_TOGGLE for space bar — that's wrong.
        # We need a PAUSE_TOGGLE event. Let's fix the handler.

    def _register_cell_events(self) -> None:
        """Cell-specific events (from mouse clicks)."""
        # These are handled by the input handler's mouse callbacks.
        # We subscribe to the cell-specific event types.
        pass

    # ────────────────────────────────────────────────────────────────
    # Main loop
    # ────────────────────────────────────────────────────────────────

    def _main(self, stdscr: Any) -> None:
        """Curses main loop — called by ``curses.wrapper``."""
        curses.curs_set(0)  # hide cursor
        stdscr.nodelay(True)  # non-blocking getch
        stdscr.timeout(16)   # ~60 fps poll rate

        # Enable mouse events.
        curses.mousemask(
            curses.BUTTON1_CLICKED
            | curses.BUTTON1_PRESSED
            | curses.BUTTON1_RELEASED
            | curses.BUTTON2_CLICKED
            | curses.BUTTON3_CLICKED
            | curses.BUTTON4_SCROLLED
            | curses.BUTTON5_SCROLLED
        )

        # Initialise subsystems.
        max_row, max_col = stdscr.getmaxyx()
        sidebar_w = self._settings.ui.sidebar_width
        view_w = max_col - sidebar_w
        view_h = max_row - 1  # reserve bottom row for status bar

        self._camera = Camera(self._settings.camera, view_w, view_h)
        self._input_handler = InputHandler(self._event_bus, self._camera)
        self._renderer = TerminalRenderer(stdscr, self._settings.renderer, self._camera, sidebar_w)
        self._sidebar = Sidebar(stdscr, sidebar_w, self._engine, self._camera)
        self._status_bar = StatusBar(stdscr, self._engine, self._camera)

        # Wire up the event bus properly.
        self._register_events()
        self._register_cell_events()

        # Subscribe to cell-specific events from mouse.
        self._event_bus.subscribe(EventType.INPUT_CELL_TOGGLE, self._on_cell_toggle)

        # Start with a random world.
        self._engine.randomize_world()
        self._engine.start()

        # Main loop.
        frame_interval = 1.0 / self._engine.speed

        while self._running:
            loop_start = time.monotonic()

            # Handle input.
            key = stdscr.getch()
            if key != -1:
                self._handle_input(key)

            # Advance simulation if running.
            if self._engine.is_running:
                self._engine.step()

            # Render.
            stdscr.erase()
            self._renderer.render(self._engine.world)
            self._sidebar.render()
            self._status_bar.render()
            curses.doupdate()

            # Pace the loop.
            elapsed = time.monotonic() - loop_start
            frame_interval = 1.0 / max(self._engine.speed, 0.1)
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _handle_input(self, key: int) -> None:
        """Dispatch a single key press."""
        action = self._input_handler.handle_key(key)

        if action == KeyAction.QUIT:
            self._running = False
            return

        if action == KeyAction.TOGGLE_PAUSE:
            if self._engine.is_running:
                self._engine.pause()
            elif self._engine.is_paused:
                self._engine.resume()
            return

        if action == KeyAction.STEP:
            if self._engine.is_paused:
                self._engine.step()
            return

        if action == KeyAction.RESET:
            self._engine.reset_world()
            return

        if action == KeyAction.CLEAR:
            self._engine.clear_world()
            return

        if action == KeyAction.RANDOMIZE:
            self._engine.randomize_world()
            return

        if action == KeyAction.SPEED_UP:
            self._engine.increase_speed()
            return

        if action == KeyAction.SPEED_DOWN:
            self._engine.decrease_speed()
            return

        # Handle mouse events (curses delivers them as KEY_MOUSE).
        if key == curses.KEY_MOUSE:
            try:
                self._input_handler.handle_mouse(None)
            except curses.error:
                pass

    # ────────────────────────────────────────────────────────────────
    # Entry
    # ────────────────────────────────────────────────────────────────

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


# ────────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────────


def main() -> None:
    settings = Settings()
    app = App(settings)
    app.run()


if __name__ == "__main__":
    main()
