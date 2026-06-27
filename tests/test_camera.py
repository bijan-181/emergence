"""Tests for the camera module."""

from __future__ import annotations

from camera.camera import Camera
from config.settings import CameraConfig


class TestCamera:
    """Tests for :class:`Camera`."""

    def _make(self, vw: int = 80, vh: int = 24) -> Camera:
        return Camera(CameraConfig(), vw, vh)

    def test_initial_state(self) -> None:
        cam = self._make()
        assert cam.zoom == 1.0
        assert cam.offset_x == 0.0
        assert cam.offset_y == 0.0

    def test_zoom_in(self) -> None:
        cam = self._make()
        cam.zoom_in()
        assert cam.zoom == 1.25

    def test_zoom_out(self) -> None:
        cam = self._make()
        cam.zoom_out()
        assert cam.zoom == 0.75

    def test_zoom_bounds(self) -> None:
        cam = self._make()
        # Zoom all the way out.
        for _ in range(20):
            cam.zoom_out()
        assert cam.zoom >= CameraConfig().min_zoom

        # Zoom all the way in.
        for _ in range(20):
            cam.zoom_in()
        assert cam.zoom <= CameraConfig().max_zoom

    def test_reset_zoom(self) -> None:
        cam = self._make()
        cam.zoom_in()
        cam.zoom_in()
        cam.reset_zoom()
        assert cam.zoom == 1.0

    def test_pan(self) -> None:
        cam = self._make()
        cam.pan(5, 3)
        assert cam.offset_x == 5.0
        assert cam.offset_y == 3.0

    def test_world_to_screen(self) -> None:
        cam = self._make()
        sp = cam.world_to_screen(10, 5)
        assert sp.col == 10
        assert sp.row == 5

    def test_screen_to_world(self) -> None:
        cam = self._make()
        wp = cam.screen_to_world(10, 5)
        assert wp.x == 10
        assert wp.y == 5

    def test_roundtrip(self) -> None:
        """world_to_screen and screen_to_world should be inverses at zoom=1."""
        cam = self._make()
        for x, y in [(0, 0), (5, 3), (79, 23)]:
            sp = cam.world_to_screen(x, y)
            wp = cam.screen_to_world(sp.col, sp.row)
            assert wp.x == x
            assert wp.y == y

    def test_visible_bounds(self) -> None:
        cam = self._make()
        x0, y0, x1, y1 = cam.visible_bounds()
        assert x0 == 0
        assert y0 == 0
        assert x1 == 80
        assert y1 == 24

    def test_visible_cells_with_zoom(self) -> None:
        cam = self._make()
        cam.zoom_in()  # 1.25x
        w = cam.visible_width_cells()
        h = cam.visible_height_cells()
        assert w < 80
        assert h < 24

    def test_resize(self) -> None:
        cam = self._make()
        cam.resize(120, 40)
        assert cam.view_width == 120
        assert cam.view_height == 40

    def test_center_on(self) -> None:
        cam = self._make()
        cam.center_on(40, 12)
        # After centering, the center of the view should be near (40, 12).
        sp = cam.world_to_screen(40, 12)
        assert 35 <= sp.col <= 45
        assert 8 <= sp.row <= 16
