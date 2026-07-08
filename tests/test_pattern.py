"""Tests for agents/pattern.py — PatternGenerator."""

from __future__ import annotations

import numpy as np
import pytest

from agents.pattern import PatternFormat, PatternGenerator, TargetPattern


class TestPatternGenerator:
    def test_from_numpy(self, pattern_generator) -> None:
        arr = np.ones((5, 5), dtype=np.uint8)
        result = pattern_generator.load(arr)
        assert isinstance(result, TargetPattern)
        assert result.width == 5
        assert result.height == 5
        assert result.format == PatternFormat.NUMPY

    def test_from_numpy_rejects_3d(self, pattern_generator) -> None:
        arr = np.ones((3, 3, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="2D"):
            pattern_generator.load(arr)

    def test_from_text_file(self, pattern_generator, tmp_path) -> None:
        content = "###\n#.#\n###"
        f = tmp_path / "pattern.txt"
        f.write_text(content)
        result = pattern_generator.load(f)
        assert result.width == 3
        assert result.height == 3
        assert result.format == PatternFormat.ASCII
        assert result.matrix[0, 0] == 1
        assert result.matrix[1, 1] == 0

    def test_file_not_found(self, pattern_generator) -> None:
        with pytest.raises(FileNotFoundError):
            pattern_generator.load("/nonexistent/file.txt")

    def test_unsupported_format(self, pattern_generator, tmp_path) -> None:
        f = tmp_path / "pattern.xyz"
        f.write_text("data")
        with pytest.raises(ValueError, match="Unsupported"):
            pattern_generator.load(f)

    def test_from_text_string(self, pattern_generator) -> None:
        result = pattern_generator.from_text_string("HI", width=20, height=10)
        assert result.width == 20
        assert result.height == 10
        assert result.format == PatternFormat.TEXT
        assert result.matrix.sum() > 0

    def test_unsupported_type(self, pattern_generator) -> None:
        with pytest.raises(TypeError):
            pattern_generator.load(12345)  # type: ignore[arg-type]

    def test_default_threshold(self) -> None:
        pg = PatternGenerator(default_threshold=100)
        assert pg._threshold == 100
