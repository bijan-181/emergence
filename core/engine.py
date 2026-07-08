"""Main simulation engine — the central coordinator.

The engine orchestrates the generation cycle but delegates all
computation to specialised subsystems (World, Rules, EventBus).
"""

from __future__ import annotations

import logging
import time
from typing import Callable

from config.settings import Settings
from core.rules import GameOfLifeRules
from core.state import EngineState
from events.bus import EventBus
from events.types import Event, EventType
from world.world import World

logger = logging.getLogger(__name__)


class Engine:
    """Simulation engine that drives the world's evolution.

    Parameters:
        settings: Application configuration.
        event_bus: Shared event bus for inter-component communication.
    """

    def __init__(self, settings: Settings, event_bus: EventBus) -> None:
        self._settings = settings
        self._event_bus = event_bus
        self._state = EngineState.IDLE
        self._world = World(
            settings.world.width,
            settings.world.height,
        )
        self._speed: float = settings.simulation.default_speed
        self._on_generation_callback: Callable[[], None] | None = None
        self._step_times: list[float] = []
        self._last_step_time: float = 0.0
        self._max_samples = 60

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def state(self) -> EngineState:
        return self._state

    @property
    def world(self) -> World:
        return self._world

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def tps(self) -> float:
        """Measured simulation ticks per second (rolling average)."""
        if not self._step_times:
            return 0.0
        avg_dt = sum(self._step_times) / len(self._step_times)
        return 1.0 / max(avg_dt, 0.0001)

    @property
    def generation(self) -> int:
        return self._world.generation

    @property
    def alive_count(self) -> int:
        return self._world.alive_count()

    @property
    def is_running(self) -> bool:
        return self._state == EngineState.RUNNING

    @property
    def is_paused(self) -> bool:
        return self._state == EngineState.PAUSED

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def set_on_generation(self, callback: Callable[[], None]) -> None:
        """Register a callback invoked after each generation advances."""
        self._on_generation_callback = callback

    def start(self) -> None:
        """Start the simulation."""
        if self._state == EngineState.RUNNING:
            return
        self._state = EngineState.RUNNING
        self._last_step_time = 0.0
        self._step_times.clear()
        logger.info("Engine started")
        self._event_bus.publish(Event(EventType.ENGINE_STARTED))

    def pause(self) -> None:
        """Pause the simulation."""
        if self._state != EngineState.RUNNING:
            return
        self._state = EngineState.PAUSED
        logger.info("Engine paused")
        self._event_bus.publish(Event(EventType.ENGINE_PAUSED))

    def resume(self) -> None:
        """Resume a paused simulation."""
        if self._state != EngineState.PAUSED:
            return
        self._state = EngineState.RUNNING
        self._last_step_time = 0.0
        self._step_times.clear()
        logger.info("Engine resumed")
        self._event_bus.publish(Event(EventType.ENGINE_RESUMED))

    def step(self) -> None:
        """Advance exactly one generation (regardless of running state)."""
        self._advance_one_generation()
        self._track_step_time()
        logger.debug("Single step → gen %d", self._world.generation)

    def stop(self) -> None:
        """Stop the simulation."""
        self._state = EngineState.STOPPED
        logger.info("Engine stopped")
        self._event_bus.publish(Event(EventType.ENGINE_SHUTDOWN))

    # ------------------------------------------------------------------
    # World commands
    # ------------------------------------------------------------------

    def clear_world(self) -> None:
        """Kill every cell."""
        self._world.clear()
        logger.info("World cleared")
        self._event_bus.publish(Event(EventType.WORLD_CLEARED))
        self._notify_generation()

    def randomize_world(self, seed: int | None = None) -> None:
        """Randomize the world."""
        self._world.randomize(self._settings.world.initial_alive_ratio, seed)
        logger.info("World randomized (alive=%d)", self._world.alive_count())
        self._event_bus.publish(Event(EventType.WORLD_RANDOMIZED))
        self._notify_generation()

    def reset_world(self) -> None:
        """Clear the world and reset generation counter."""
        self._world.clear()
        self._world.reset_generation()
        self._step_times.clear()
        self._last_step_time = 0.0
        logger.info("World reset")
        self._event_bus.publish(Event(EventType.SIMULATION_RESET))
        self._notify_generation()

    # ------------------------------------------------------------------
    # Speed control
    # ------------------------------------------------------------------

    def set_speed(self, speed: float) -> None:
        """Set the simulation speed (generations per second)."""
        self._speed = max(
            self._settings.simulation.min_speed,
            min(speed, self._settings.simulation.max_speed),
        )
        logger.debug("Speed set to %.1f", self._speed)

    def increase_speed(self) -> None:
        self.set_speed(self._speed + self._settings.simulation.speed_step)

    def decrease_speed(self) -> None:
        self.set_speed(self._speed - self._settings.simulation.speed_step)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _track_step_time(self) -> None:
        """Record the time between simulation steps for TPS measurement."""
        now = time.monotonic()
        if self._last_step_time > 0:
            dt = now - self._last_step_time
            self._step_times.append(dt)
            if len(self._step_times) > self._max_samples:
                self._step_times.pop(0)
        self._last_step_time = now

    def _advance_one_generation(self) -> None:
        """Compute the next generation and commit it."""
        self._event_bus.publish(Event(EventType.GENERATION_BEGIN))
        next_cells = GameOfLifeRules.compute_next(self._world.get_grid())
        self._world.get_grid().set_array(next_cells)
        self._world.advance_generation()
        self._event_bus.publish(Event(EventType.GENERATION_END))
        if self._on_generation_callback:
            self._on_generation_callback()

    def _notify_generation(self) -> None:
        """Notify listeners that the world state changed (outside normal cycle)."""
        if self._on_generation_callback:
            self._on_generation_callback()
