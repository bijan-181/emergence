"""Tests for the debug overlay."""

from __future__ import annotations

from camera.camera import Camera
from config.settings import CameraConfig, Settings
from core.clock import Clock
from core.engine import Engine
from events.bus import EventBus
from input.handler import InputHandler
from ui.debug_overlay import DebugOverlay


class TestDebugOverlay:
    """Tests for :class:`DebugOverlay`."""

    def _make(self) -> tuple[DebugOverlay, Engine, InputHandler]:
        settings = Settings()
        bus = EventBus()
        engine = Engine(settings, bus)
        camera = Camera(CameraConfig(), 80, 24, 200, 200)
        handler = InputHandler(bus, camera, sim_area_width=80)
        render_clock = Clock(60)
        overlay = DebugOverlay(engine, camera, handler, render_clock, 200, 200)
        return overlay, engine, handler

    def test_get_lines_returns_list(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert isinstance(lines, list)
        assert len(lines) > 0

    def test_get_lines_contains_debug_header(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("DEBUG OVERLAY" in line for line in lines)

    def test_get_lines_contains_world_size(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("200x200" in line for line in lines)

    def test_get_lines_contains_render_fps(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("Render FPS" in line for line in lines)

    def test_get_lines_contains_sim_tps(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("Sim TPS" in line for line in lines)

    def test_get_lines_contains_camera_info(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("Camera offset" in line for line in lines)
        assert any("Zoom level" in line for line in lines)

    def test_get_lines_contains_mouse_info(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("Mouse screen" in line for line in lines)
        assert any("Mouse world" in line for line in lines)

    def test_get_lines_contains_sim_state(self) -> None:
        overlay, engine, _ = self._make()
        engine.start()
        lines = overlay.get_lines()
        assert any("RUNNING" in line for line in lines)

    def test_get_lines_shows_paused_state(self) -> None:
        overlay, engine, _ = self._make()
        engine.start()
        engine.pause()
        lines = overlay.get_lines()
        assert any("PAUSED" in line for line in lines)

    def test_get_lines_contains_viewport(self) -> None:
        overlay, _, _ = self._make()
        lines = overlay.get_lines()
        assert any("Viewport" in line for line in lines)
