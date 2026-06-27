"""Neighborhood computation for cellular automata."""

from __future__ import annotations

from typing import Iterator

from world.grid import Grid


def moore_offsets() -> list[tuple[int, int]]:
    """Return the eight relative positions of the Moore neighborhood."""
    return [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1),
    ]


def count_alive_neighbors(grid: Grid, x: int, y: int) -> int:
    """Count alive neighbors of the cell at (*x*, *y*) using toroidal wrapping."""
    count = 0
    for dx, dy in moore_offsets():
        nx = (x + dx) % grid.width
        ny = (y + dy) % grid.height
        if grid.get(nx, ny):
            count += 1
    return count


def iter_neighborhood(grid: Grid, x: int, y: int) -> Iterator[tuple[int, int, int]]:
    """Yield ``(nx, ny, state)`` for each neighbor of (*x*, *y*).

    Uses toroidal (wrap-around) boundary behavior.
    """
    for dx, dy in moore_offsets():
        nx = (x + dx) % grid.width
        ny = (y + dy) % grid.height
        yield nx, ny, int(grid.get(nx, ny))
