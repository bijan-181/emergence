"""Pattern loading — text and image inputs to binary matrices."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import numpy as np


class PatternFormat(Enum):
    """Supported input formats."""

    TEXT = auto()
    IMAGE = auto()
    ASCII = auto()
    NUMPY = auto()


@dataclass(frozen=True, slots=True)
class TargetPattern:
    """A processed target pattern ready for agent use."""

    matrix: np.ndarray
    source: str
    format: PatternFormat
    width: int
    height: int


class PatternGenerator:
    """Convert user-provided inputs into TargetPattern objects.

    Supported inputs in Phase 2:
      - Text string -> rendered via PIL to bitmap, then binarized
      - Image file (PNG/JPG) -> loaded, resized, binarized
      - NumPy array -> validated and returned directly
      - Text file (# = alive, . = dead)
    """

    def __init__(self, default_threshold: int = 128) -> None:
        self._threshold = default_threshold

    def load(
        self, source: str | Path | np.ndarray, **kwargs: object
    ) -> TargetPattern:
        """Load a target pattern from various sources.

        Args:
            source: A file path (str/Path), a numpy array, or a text string.
            **kwargs: Format-specific options (width, height, threshold).

        Returns:
            A validated TargetPattern.
        """
        if isinstance(source, np.ndarray):
            return self._from_numpy(source, **kwargs)
        if isinstance(source, (str, Path)):
            return self._from_path(Path(source), **kwargs)
        raise TypeError(f"Unsupported source type: {type(source)}")

    def _from_numpy(self, arr: np.ndarray, **kwargs: object) -> TargetPattern:
        matrix = arr.astype(np.uint8)
        if matrix.ndim != 2:
            raise ValueError(f"Expected 2D array, got {matrix.ndim}D")
        return TargetPattern(
            matrix=matrix,
            source="<numpy>",
            format=PatternFormat.NUMPY,
            width=matrix.shape[1],
            height=matrix.shape[0],
        )

    def _from_path(self, path: Path, **kwargs: object) -> TargetPattern:
        if not path.exists():
            raise FileNotFoundError(f"Pattern file not found: {path}")
        suffix = path.suffix.lower()
        if suffix in (".png", ".jpg", ".jpeg", ".bmp", ".tiff"):
            return self._from_image(path, **kwargs)
        if suffix in (".txt",):
            return self._from_text_file(path, **kwargs)
        raise ValueError(f"Unsupported file format: {suffix}")

    def _from_image(self, path: Path, **kwargs: object) -> TargetPattern:
        """Load image -> grayscale -> threshold -> binary matrix."""
        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError(
                "Pillow is required for image loading: pip install Pillow"
            ) from e

        width = int(kwargs.get("width", 100))  # type: ignore[arg-type]
        height = int(kwargs.get("height", 100))  # type: ignore[arg-type]
        threshold = int(kwargs.get("threshold", self._threshold))  # type: ignore[arg-type]

        img = Image.open(path).convert("L").resize((width, height))
        arr = np.array(img)
        matrix = (arr >= threshold).astype(np.uint8)
        return TargetPattern(
            matrix=matrix,
            source=str(path),
            format=PatternFormat.IMAGE,
            width=width,
            height=height,
        )

    def _from_text_file(self, path: Path, **kwargs: object) -> TargetPattern:
        """Load a text file where '#' = alive, '.' = dead."""
        lines = path.read_text().strip().splitlines()
        height = len(lines)
        width = max(len(line) for line in lines) if lines else 0
        matrix = np.zeros((height, width), dtype=np.uint8)
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == "#":
                    matrix[y, x] = 1
        return TargetPattern(
            matrix=matrix,
            source=str(path),
            format=PatternFormat.ASCII,
            width=width,
            height=height,
        )

    def from_text_string(
        self, text: str, width: int = 100, height: int = 50
    ) -> TargetPattern:
        """Render a short text string to a binary pattern using a bitmap font."""
        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new("L", (width, height), color=0)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
                )
            except OSError:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = max(0, (width - tw) // 2)
            y = max(0, (height - th) // 2)
            draw.text((x, y), text, fill=255, font=font)
            arr = np.array(img)
            matrix = (arr >= 128).astype(np.uint8)
        except ImportError:
            matrix = np.zeros((height, width), dtype=np.uint8)
            for i, ch in enumerate(text[:width]):
                if ch != " ":
                    matrix[height // 2, i] = 1

        return TargetPattern(
            matrix=matrix,
            source=f"text:{text}",
            format=PatternFormat.TEXT,
            width=width,
            height=height,
        )
