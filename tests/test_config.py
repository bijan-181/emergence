"""Tests for the configuration module."""

from __future__ import annotations

from config.settings import CameraConfig, RendererConfig, Settings, SimulationConfig, WorldConfig


class TestSettings:
    """Tests for :class:`Settings`."""

    def test_defaults(self) -> None:
        s = Settings()
        assert s.world.width == 80
        assert s.world.height == 24
        assert s.simulation.target_fps == 10
        assert s.camera.default_zoom == 1.0

    def test_world_config(self) -> None:
        wc = WorldConfig(width=100, height=50)
        assert wc.width == 100
        assert wc.height == 50

    def test_simulation_config(self) -> None:
        sc = SimulationConfig(target_fps=30)
        assert sc.target_fps == 30

    def test_camera_config(self) -> None:
        cc = CameraConfig(min_zoom=0.5, max_zoom=4.0)
        assert cc.min_zoom == 0.5
        assert cc.max_zoom == 4.0

    def test_renderer_config(self) -> None:
        rc = RendererConfig(alive_char="O", dead_char=".")
        assert rc.alive_char == "O"
        assert rc.dead_char == "."
