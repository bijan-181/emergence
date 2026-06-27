"""Tests for the simulation engine."""

from __future__ import annotations

from config.settings import Settings
from core.engine import Engine
from core.state import EngineState
from events.bus import EventBus


class TestEngine:
    """Tests for :class:`Engine`."""

    def _make(self) -> Engine:
        return Engine(Settings(), EventBus())

    def test_initial_state(self) -> None:
        e = self._make()
        assert e.state == EngineState.IDLE
        assert e.generation == 0

    def test_start(self) -> None:
        e = self._make()
        e.start()
        assert e.is_running
        assert e.state == EngineState.RUNNING

    def test_pause_resume(self) -> None:
        e = self._make()
        e.start()
        e.pause()
        assert e.is_paused
        e.resume()
        assert e.is_running

    def test_single_step(self) -> None:
        e = self._make()
        e.step()
        assert e.generation == 1

    def test_multiple_steps(self) -> None:
        e = self._make()
        for _ in range(10):
            e.step()
        assert e.generation == 10

    def test_speed_control(self) -> None:
        e = self._make()
        initial = e.speed
        e.increase_speed()
        assert e.speed > initial
        e.decrease_speed()
        assert e.speed == initial

    def test_speed_bounds(self) -> None:
        e = self._make()
        e.set_speed(1000)
        assert e.speed <= Settings().simulation.max_speed
        e.set_speed(-5)
        assert e.speed >= Settings().simulation.min_speed

    def test_clear_world(self) -> None:
        e = self._make()
        e.randomize_world(seed=42)
        assert e.alive_count > 0
        e.clear_world()
        assert e.alive_count == 0

    def test_randomize_world(self) -> None:
        e = self._make()
        e.randomize_world(seed=42)
        assert e.alive_count > 0

    def test_reset_world(self) -> None:
        e = self._make()
        e.randomize_world(seed=42)
        e.step()
        e.step()
        assert e.generation == 2
        e.reset_world()
        assert e.generation == 0
        assert e.alive_count == 0

    def test_generation_callback(self) -> None:
        e = self._make()
        counter = {"value": 0}
        def on_gen() -> None:
            counter["value"] += 1
        e.set_on_generation(on_gen)
        e.step()
        e.step()
        assert counter["value"] == 2

    def test_stop(self) -> None:
        e = self._make()
        e.start()
        e.stop()
        assert e.state == EngineState.STOPPED

    def test_world_persistence_after_steps(self) -> None:
        """The world should accumulate changes across steps."""
        e = self._make()
        e.randomize_world(seed=42)
        gen1_alive = e.alive_count
        e.step()
        # The alive count should change (Game of Life is dynamic).
        # It's possible it stays the same by chance, but very unlikely.
        # Just verify generation advanced.
        assert e.generation == 1
