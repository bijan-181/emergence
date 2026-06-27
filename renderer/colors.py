"""Color definitions for terminal rendering via curses color pairs.

All colors are defined as curses attribute values, not raw ANSI
escape sequences.  ANSI codes corrupt curses' internal state and
must never be used inside a curses application.

Pair IDs are allocated here; :func:`init_colors` must be called
after ``curses.initscr()`` before using any ``PAIR_*`` constants.
"""

from __future__ import annotations

import curses

# ── Pair IDs (stable, never re-used) ──────────────────────────────
_PID_ALIVE_BG = 1
_PID_DEAD_BG = 2
_PID_SIDEBAR_TITLE = 3
_PID_SIDEBAR_VALUE = 4
_PID_STATUS_BAR = 5


def init_colors() -> None:
    """Initialize the curses color palette.  Call once after ``initscr``."""
    curses.start_color()
    curses.use_default_colors()

    _init = [
        (_PID_ALIVE_BG, -1, curses.COLOR_GREEN),
        (_PID_DEAD_BG, -1, 235),
        (_PID_SIDEBAR_TITLE, curses.COLOR_CYAN, -1),
        (_PID_SIDEBAR_VALUE, curses.COLOR_YELLOW, -1),
        (_PID_STATUS_BAR, curses.COLOR_WHITE, curses.COLOR_BLUE),
    ]
    for pid, fg, bg in _init:
        try:
            curses.init_pair(pid, fg, bg)
        except curses.error:
            pass  # terminal may not support 256 colors


# ── Attribute accessors (safe to call after init_colors) ──────────

def PAIR_ALIVE_BG() -> int:
    """Green background for alive cells."""
    return curses.color_pair(_PID_ALIVE_BG)


def PAIR_DEAD_BG() -> int:
    """Dark-gray background for dead cells."""
    return curses.color_pair(_PID_DEAD_BG)


def PAIR_SIDEBAR_TITLE() -> int:
    """Bold cyan for sidebar section headers."""
    return curses.color_pair(_PID_SIDEBAR_TITLE) | curses.A_BOLD


def PAIR_SIDEBAR_VALUE() -> int:
    """Yellow for sidebar data values."""
    return curses.color_pair(_PID_SIDEBAR_VALUE)


def PAIR_STATUS_BAR() -> int:
    """White-on-blue for the status bar."""
    return curses.color_pair(_PID_STATUS_BAR) | curses.A_BOLD
