"""Boundary behavior for the world grid."""

from __future__ import annotations

from enum import Enum, auto


class BoundaryMode(Enum):
    """Strategy for handling cells at the world edge."""

    TOROIDAL = auto()  # wrap-around (default)
    FIXED = auto()     # cells outside are always dead


def wrap_coord(coord: int, size: int) -> int:
    """Wrap *coord* into ``[0, size)`` using toroidal topology."""
    return coord % size
