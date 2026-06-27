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
from core.clock import Clock
from core.engine import Engine
from events.bus import EventBus
from events.types import Event, EventType
from input.handler import InputHandler
from input.keyboard import KeyAction
from renderer.colors import init_colors
from renderer.terminal import TerminalRenderer
from ui.sidebar import Sidebar
from ui.status import StatusBar
from world.cell import CellState

logger = logging.getLogger("emergence")


class App:
    """Top-level application that owns the curses loop.

    Rendering architecture:

    - The terminal is divided into three non-overlapping subwindows:
      ``sim_win`` (left, simulation grid), ``sidebar_win`` (right),
      ``status_win`` (bottom row).
    - Each subsystem renders into its own subwindow independently.
    - A single ``curses.doupdate()`` flushes all subwindow changes
      to the physical terminal in one atomic operation — eliminating
      flicker caused by incremental screen updates.
    - No ``erase()`` is called on any window.  Every render pass
      overwrites cell positions unconditionally, which is both
      faster and flicker-free compared to clear-then-redraw.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._event_bus = EventBus()
        self._engine = Engine(settings, self._event_bus)
        self._running = True
        self._debug_mode = False

        self._camera: Camera | None = None
        self._input_handler: InputHandler | None = None
        self._renderer: TerminalRenderer | None = None
        self._sidebar: Sidebar | None = None
        self._status_bar: StatusBar | None = None
        self._clock: Clock | None = None

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
    # Layout
    # ------------------------------------------------------------------

    def _create_subwindows(self, stdscr: Any) -> None:
        """Split the terminal into three non-overlapping regions.

        Layout::

            ┌──────────────────┬────────────┐
            │                  │            │
            │   sim_win        │ sidebar_win│
            │   (grid)         │            │
            │                  │            │
            ├──────────────────┴────────────┤
            │          status_win            │
            └────────────────────────────────┘
        """
        max_row, max_col = stdscr.getmaxyx()
        sidebar_w = self._settings.ui.sidebar_width
        status_h = 1

        sim_w = max_col - sidebar_w
        sim_h = max_row - status_h

        # Ensure minimum sizes.
        sim_w = max(sim_w, 1)
        sim_h = max(sim_h, 1)
        sidebar_w = min(sidebar_w, max_col)
        status_h = min(status_h, max_row)

        sim_win = stdscr.subwin(sim_h, sim_w, 0, 0)
        sidebar_win = stdscr.subwin(sim_h, sidebar_w, 0, sim_w)
        status_win = stdscr.subwin(status_h, max_col, sim_h, 0)

        return sim_win, sidebar_win, status_win

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def _main(self, stdscr: Any) -> None:
        """Curses main loop — called by ``curses.wrapper``."""
        # Terminal initialisation.
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.nodelay(True)
        stdscr.timeout(0)  # non-blocking getch; we control timing ourselves

        init_colors()

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

        # Create subwindows.
        sim_win, sidebar_win, status_win = self._create_subwindows(stdscr)

        # Compute simulation viewport size.
        sim_h, sim_w = sim_win.getmaxyx()
        sidebar_w = sidebar_win.getmaxyx()[1]

        self._camera = Camera(self._settings.camera, sim_w, sim_h)
        self._input_handler = InputHandler(self._event_bus, self._camera)
        self._renderer = TerminalRenderer(sim_win, self._settings.renderer, self._camera)
        self._sidebar = Sidebar(sidebar_win, sidebar_w, self._engine, self._camera)
        self._status_bar = StatusBar(status_win, self._engine, self._camera)
        self._clock = Clock(self._settings.simulation.target_fps)

        # Subscribe mouse-cell events (these never re-enter the engine).
        self._event_bus.subscribe(EventType.INPUT_CELL_TOGGLE, self._on_cell_toggle)
        self._event_bus.subscribe(EventType.INPUT_CELL_ERASE, self._on_cell_erase)
        self._event_bus.subscribe(EventType.INPUT_CELL_PAINT, self._on_cell_paint)

        # Start with a random world.
        self._engine.randomize_world()
        self._engine.start()

        # ---- main loop ------------------------------------------------
        while self._running:
            self._clock.tick()

            # 1. Input (non-blocking).
            key = stdscr.getch()
            while key != -1:
                self._handle_input(key)
                if not self._running:
                    break
                key = stdscr.getch()

            # 2. Simulation step.
            if self._engine.is_running:
                self._engine.step()

            # 3. Render — each subwindow writes independently, then one
            #    atomic doupdate flushes everything.
            self._renderer.render(self._engine.world)
            self._sidebar.render()
            self._status_bar.render()
            curses.doupdate()

            # 4. Frame pacing.
            self._clock.sleep_until_next()

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
