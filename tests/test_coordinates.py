"""Tests for coordinate mapping between screen and world space."""

from __future__ import annotations

from camera.camera import Camera, ScreenPos, WorldPos
from config.settings import CameraConfig


class TestCoordinateMapping:
    """Tests for screen ↔ world coordinate conversion."""

    def _make(self, vw: int = 80, vh: int = 24, ww: int = 200, wh: int = 200) -> Camera:
        return Camera(CameraConfig(), vw, vh, ww, wh)

    def test_origin_mapping(self) -> None:
        cam = self._make()
        sp = cam.world_to_screen(0, 0)
        assert sp.col == 0
        assert sp.row == 0

    def test_origin_inverse(self) -> None:
        cam = self._make()
        wp = cam.screen_to_world(0, 0)
        assert wp.x == 0
        assert wp.y == 0

    def test_pan_offset_affects_mapping(self) -> None:
        cam = self._make()
        cam.pan(10, 5)
        sp = cam.world_to_screen(10, 5)
        assert sp.col == 0
        assert sp.row == 0

    def test_zoom_affects_mapping(self) -> None:
        cam = self._make()
        cam.zoom_in()  # 1.25x
        sp = cam.world_to_screen(10, 10)
        # At 1.25x zoom, world (10,10) should be at screen (12, 12)
        assert sp.col == 12
        assert sp.row == 12

    def test_roundtrip_with_offset(self) -> None:
        cam = self._make()
        cam.pan(20, 10)
        for wx, wy in [(0, 0), (25, 15), (50, 30)]:
            sp = cam.world_to_screen(wx, wy)
            wp = cam.screen_to_world(sp.col, sp.row)
            assert wp.x == wx
            assert wp.y == wy

    def test_roundtrip_with_zoom(self) -> None:
        cam = self._make()
        cam.zoom_in()
        cam.zoom_in()
        for wx, wy in [(10, 10), (50, 50), (100, 100)]:
            sp = cam.world_to_screen(wx, wy)
            wp = cam.screen_to_world(sp.col, sp.row)
            assert abs(wp.x - wx) <= 1
            assert abs(wp.y - wy) <= 1

    def test_screen_pos_dataclass(self) -> None:
        sp = ScreenPos(col=10, row=20)
        assert sp.col == 10
        assert sp.row == 20

    def test_world_pos_dataclass(self) -> None:
        wp = WorldPos(x=5, y=3)
        assert wp.x == 5
        assert wp.y == 3
