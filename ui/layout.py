"""Layout engine — dynamically computes UI region geometry.

All panel dimensions are derived from the current terminal size.
No hardcoded positions; every region is recalculated when the
terminal is resized.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Region:
    """A rectangular region within the terminal.

    Coordinates are (row, col) with (0, 0) at top-left.
    """

    row: int
    col: int
    height: int
    width: int


class Layout:
    """Computes the geometry of all UI panels from terminal dimensions.

    Layout (assuming ``status_height=1``)::

        ┌──────────────────┬────────────┐
        │                  │            │
        │   simulation     │  sidebar   │
        │                  │            │
        ├──────────────────┴────────────┤
        │          status bar           │
        └────────────────────────────────┘

    Parameters:
        sidebar_width: Desired sidebar width in columns.
        status_height: Desired status bar height in rows.
    """

    def __init__(self, sidebar_width: int = 32, status_height: int = 1) -> None:
        self._sidebar_width = sidebar_width
        self._status_height = status_height

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def sidebar_width(self) -> int:
        return self._sidebar_width

    @property
    def status_height(self) -> int:
        return self._status_height

    # ------------------------------------------------------------------
    # Region computation
    # ------------------------------------------------------------------

    def compute(self, terminal_rows: int, terminal_cols: int) -> dict[str, Region]:
        """Return named regions for the current terminal size.

        Returns:
            Dict with keys ``"sim"``, ``"sidebar"``, ``"status"``.
        """
        sb_w = min(self._sidebar_width, max(1, terminal_cols - 1))
        st_h = min(self._status_height, max(1, terminal_rows - 1))

        sim_w = max(1, terminal_cols - sb_w)
        sim_h = max(1, terminal_rows - st_h)

        return {
            "sim": Region(row=0, col=0, height=sim_h, width=sim_w),
            "sidebar": Region(row=0, col=sim_w, height=sim_h, width=sb_w),
            "status": Region(row=sim_h, col=0, height=st_h, width=terminal_cols),
        }

    def simulation_width(self, terminal_cols: int) -> int:
        """Return the simulation area width for a given terminal width."""
        sb_w = min(self._sidebar_width, max(1, terminal_cols - 1))
        return max(1, terminal_cols - sb_w)

    def simulation_height(self, terminal_rows: int) -> int:
        """Return the simulation area height for a given terminal height."""
        st_h = min(self._status_height, max(1, terminal_rows - 1))
        return max(1, terminal_rows - st_h)
