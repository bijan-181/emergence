"""Emergence — Interactive Conway's Game of Life Sandbox.

Entry point.  Run with::

    python main.py

"""

from __future__ import annotations

import curses
import logging
import os
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
from ui.debug_overlay import DebugOverlay
from ui.layout import Layout
from ui.sidebar import Sidebar
from ui.status import StatusBar
from world.cell import CellState

logger = logging.getLogger("emergence")


def _setup_logging() -> None:
    """Configure logging to write to a file, never to the terminal.

    During curses operation any output to stdout/stderr corrupts the
    screen.  Logs go to ``emergence.log`` in the working directory.
    """
    log_path = os.path.join(os.getcwd(), "emergence.log")
    handler = logging.FileHandler(log_path, mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    )
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)


class App:
    """Top-level application that owns the curses loop.

    Rendering architecture:

    - A :class:`~ui.layout.Layout` engine computes region geometry
      from the current terminal size — no hardcoded positions.
    - The terminal is divided into three non-overlapping subwindows
      (simulation, sidebar, status) via ``stdscr.subwin()``.
    - Each subsystem renders into its own subwindow independently.
    - A single ``curses.doupdate()`` flushes all subwindow changes
      to the physical terminal in one atomic operation.
    - On terminal resize (``KEY_RESIZE``), subwindows are destroyed
      and recreated; the camera viewport is updated to match.

    Timing architecture:

    - Render and simulation run on independent clocks.
    - Render FPS controls only how often the screen is repainted.
    - Simulation TPS controls only how often the Game of Life
      advances a generation.
    - Changing one never affects the other.
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
        self._debug_overlay: DebugOverlay | None = None
        self._render_clock = Clock(settings.simulation.render_fps)
        self._layout = Layout(
            sidebar_width=settings.ui.sidebar_width,
            status_height=settings.ui.status_height,
        )

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
    # Layout / subwindow management
    # ------------------------------------------------------------------

    def _build_panels(self, stdscr: Any) -> None:
        """(Re)create subwindows from the current terminal size.

        Called at startup and again on every ``KEY_RESIZE`` event.
        """
        max_row, max_col = stdscr.getmaxyx()
        regions = self._layout.compute(max_row, max_col)

        sim_r = regions["sim"]
        sb_r = regions["sidebar"]
        st_r = regions["status"]

        sim_win = stdscr.subwin(sim_r.height, sim_r.width, sim_r.row, sim_r.col)
        sidebar_win = stdscr.subwin(sb_r.height, sb_r.width, sb_r.row, sb_r.col)
        status_win = stdscr.subwin(st_r.height, st_r.width, st_r.row, st_r.col)

        self._camera = Camera(
            self._settings.camera, sim_r.width, sim_r.height,
            self._settings.world.width, self._settings.world.height,
            cell_width=self._settings.renderer.cell_width,
        )
        self._renderer = TerminalRenderer(sim_win, self._settings.renderer, self._camera)
        self._sidebar = Sidebar(sidebar_win, sb_r.width, self._engine, self._camera,
                                self._render_clock)
        self._status_bar = StatusBar(status_win, self._engine, self._camera)
        self._input_handler = InputHandler(
            self._event_bus, self._camera, sim_area_width=sim_r.width,
        )
        self._debug_overlay = DebugOverlay(
            self._engine, self._camera, self._input_handler,
            self._render_clock,
            self._settings.world.width, self._settings.world.height,
        )

    def _handle_resize(self, stdscr: Any) -> None:
        """Rebuild all panels after a terminal resize."""
        curses.endwin()
        stdscr.refresh()
        self._build_panels(stdscr)

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
        stdscr.timeout(0)

        init_colors()

        # Enable mouse events.
        mouse_mask = (
            curses.BUTTON1_CLICKED
            | curses.BUTTON1_PRESSED
            | curses.BUTTON1_RELEASED
            | curses.BUTTON2_CLICKED
            | curses.BUTTON2_PRESSED
            | curses.BUTTON2_RELEASED
            | curses.BUTTON3_CLICKED
            | curses.BUTTON3_PRESSED
            | curses.BUTTON3_RELEASED
        )
        if hasattr(curses, "BUTTON4_SCROLLED"):
            mouse_mask |= curses.BUTTON4_SCROLLED | curses.BUTTON5_SCROLLED
        else:
            mouse_mask |= curses.BUTTON4_CLICKED | curses.BUTTON5_CLICKED
        if hasattr(curses, "BUTTON4_PRESSED"):
            mouse_mask |= curses.BUTTON4_PRESSED | curses.BUTTON5_PRESSED
        if hasattr(curses, "REPORT_MOUSE_POSITION"):
            mouse_mask |= curses.REPORT_MOUSE_POSITION
        avail, old = curses.mousemask(mouse_mask)
        logger.info("mousemask: requested=%#x avail=%#x old=%#x", mouse_mask, avail, old)
        if avail == 0:
            logger.warning("Mouse events NOT supported by terminal – clicks will not work")

        # Build initial layout.
        self._build_panels(stdscr)

        # Subscribe mouse-cell events (these never re-enter the engine).
        self._event_bus.subscribe(EventType.INPUT_CELL_TOGGLE, self._on_cell_toggle)
        self._event_bus.subscribe(EventType.INPUT_CELL_ERASE, self._on_cell_erase)
        self._event_bus.subscribe(EventType.INPUT_CELL_PAINT, self._on_cell_paint)

        # Start with a random world.
        self._engine.randomize_world()
        self._engine.start()

        # Timing state for independent render/sim loops.
        render_fps = self._settings.simulation.render_fps
        last_render = time.monotonic()
        last_sim = time.monotonic()

        # ---- main loop ------------------------------------------------
        while self._running:
            now = time.monotonic()

            # 1. Input (non-blocking).
            key = stdscr.getch()
            while key != -1:
                self._handle_input(key, stdscr)
                if not self._running:
                    break
                key = stdscr.getch()

            # 1b. Continuous drag polling (held mouse buttons).
            self._input_handler.poll_drag()

            # 2. Simulation step (independent of render timing).
            sim_interval = 1.0 / max(self._engine.speed, 0.1)
            if self._engine.is_running and (now - last_sim) >= sim_interval:
                self._engine.step()
                last_sim = now

            # 3. Render (independent of simulation timing).
            render_interval = 1.0 / max(render_fps, 1)
            if (now - last_render) >= render_interval:
                self._render_clock.tick()
                self._renderer.render(self._engine.world)
                self._sidebar.render()
                self._status_bar.render()
                if self._debug_mode and self._debug_overlay is not None:
                    self._debug_overlay.render(stdscr)
                curses.doupdate()
                last_render = now

            # 4. Small sleep to prevent busy-waiting.
            time.sleep(0.001)

    # ------------------------------------------------------------------
    # Input dispatch
    # ------------------------------------------------------------------

    def _handle_input(self, key: int, stdscr: Any) -> None:
        """Dispatch a single key press or mouse event."""
        # Terminal resize.
        if key == curses.KEY_RESIZE:
            self._handle_resize(stdscr)
            return

        # Mouse events.
        if key == curses.KEY_MOUSE:
            logger.debug("KEY_MOUSE received")
            try:
                self._input_handler.handle_mouse()
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
        elif action == KeyAction.DEBUG_TOGGLE:
            self._debug_mode = not self._debug_mode
            logger.debug("Debug overlay: %s", "ON" if self._debug_mode else "OFF")

    # ------------------------------------------------------------------
    # Entry
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Launch the application."""
        _setup_logging()
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
