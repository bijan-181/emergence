"""Tests for the camera module."""

from __future__ import annotations

from camera.camera import Camera
from config.settings import CameraConfig


class TestCamera:
    """Tests for :class:`Camera`."""

    def _make(self, vw: int = 80, vh: int = 24, ww: int = 200, wh: int = 200) -> Camera:
        return Camera(CameraConfig(), vw, vh, ww, wh)

    def test_initial_state(self) -> None:
        cam = self._make()
        assert cam.zoom == 1.0
        assert cam.offset_x == 0.0
        assert cam.offset_y == 0.0
        assert cam.world_width == 200
        assert cam.world_height == 200

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
        for _ in range(20):
            cam.zoom_out()
        assert cam.zoom >= CameraConfig().min_zoom

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
        sp = cam.world_to_screen(40, 12)
        assert 35 <= sp.col <= 45
        assert 8 <= sp.row <= 16


class TestCameraBoundaryClamping:
    """Tests for camera boundary clamping."""

    def _make(self, vw: int = 80, vh: int = 24, ww: int = 200, wh: int = 200) -> Camera:
        return Camera(CameraConfig(), vw, vh, ww, wh)

    def test_pan_clamps_to_origin(self) -> None:
        """Camera should not show negative coordinates."""
        cam = self._make()
        cam.pan(-100, -100)
        assert cam.offset_x >= 0
        assert cam.offset_y >= 0

    def test_pan_clamps_to_world_end(self) -> None:
        """Camera should not scroll beyond world edges."""
        cam = self._make()
        cam.pan(500, 500)
        # At zoom=1 with viewport 80x24, max offset is (200-80, 200-24) = (120, 176)
        assert cam.offset_x <= 200 - 80
        assert cam.offset_y <= 200 - 24

    def test_zoom_in_preserves_bounds(self) -> None:
        """Zooming in from a valid position should stay in bounds."""
        cam = self._make()
        cam.pan(100, 100)
        for _ in range(10):
            cam.zoom_in()
        assert cam.offset_x >= 0
        assert cam.offset_y >= 0

    def test_zoom_out_preserves_bounds(self) -> None:
        """Zooming out from a valid position should stay in bounds."""
        cam = self._make()
        cam.pan(50, 50)
        for _ in range(10):
            cam.zoom_out()
        assert cam.offset_x >= 0
        assert cam.offset_y >= 0

    def test_zoom_out_world_smaller_than_viewport(self) -> None:
        """When world is smaller than viewport, offset should stay at 0."""
        cam = self._make(vw=100, vh=100, ww=50, wh=50)
        cam.pan(10, 10)
        cam.zoom_out()
        cam.zoom_out()
        assert cam.offset_x == 0.0
        assert cam.offset_y == 0.0

    def test_visible_bounds_clamped_to_world(self) -> None:
        """Visible bounds should never exceed world dimensions."""
        cam = self._make()
        cam.pan(150, 150)
        x0, y0, x1, y1 = cam.visible_bounds()
        assert x0 >= 0
        assert y0 >= 0
        assert x1 <= 200
        assert y1 <= 200

    def test_center_on_clamped(self) -> None:
        """Centering near the edge should clamp to world bounds."""
        cam = self._make()
        cam.center_on(0, 0)
        assert cam.offset_x >= 0
        assert cam.offset_y >= 0

        cam.center_on(200, 200)
        assert cam.offset_x <= 200 - 80
        assert cam.offset_y <= 200 - 24

    def test_resize_reclamps(self) -> None:
        """Resizing the viewport should re-clamp the offset."""
        cam = self._make(vw=80, vh=24, ww=200, wh=200)
        cam.pan(150, 150)
        # Now resize to a larger viewport — offset should decrease.
        cam.resize(200, 200)
        assert cam.offset_x >= 0
        assert cam.offset_y >= 0

    def test_set_world_size_reclamps(self) -> None:
        """Changing world size should re-clamp the offset."""
        cam = self._make()
        cam.pan(150, 150)
        cam.set_world_size(100, 100)
        assert cam.offset_x <= 100 - 80
        assert cam.offset_y <= 100 - 24

    def test_no_negative_visible_bounds(self) -> None:
        """Visible bounds should never be negative."""
        cam = self._make()
        cam.pan(-50, -50)
        x0, y0, x1, y1 = cam.visible_bounds()
        assert x0 >= 0
        assert y0 >= 0
        assert x1 >= 0
        assert y1 >= 0

    def test_large_world(self) -> None:
        """Camera should work correctly with large worlds."""
        cam = self._make(vw=80, vh=24, ww=1000, wh=1000)
        cam.pan(500, 500)
        assert cam.offset_x == 500
        assert cam.offset_y == 500
        cam.pan(600, 600)
        # Max offset x = 1000 - 80 = 920, y = 1000 - 24 = 976
        assert cam.offset_x <= 920
        assert cam.offset_y <= 976
