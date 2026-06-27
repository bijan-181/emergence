"""Cell state and properties."""

from __future__ import annotations

from enum import IntEnum


class CellState(IntEnum):
    """Binary cell states.

    Uses ``IntEnum`` so cells can be compared with plain integers
    and used as array indices.
    """

    DEAD = 0
    ALIVE = 1
