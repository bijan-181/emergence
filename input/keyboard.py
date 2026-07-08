"""Keyboard shortcut definitions."""

from __future__ import annotations

from enum import Enum, auto


class KeyAction(Enum):
    """High-level actions triggered by keyboard shortcuts."""

    TOGGLE_PAUSE = auto()
    STEP = auto()
    RESET = auto()
    CLEAR = auto()
    RANDOMIZE = auto()
    SPEED_UP = auto()
    SPEED_DOWN = auto()
    ZOOM_RESET = auto()
    PAN_UP = auto()
    PAN_DOWN = auto()
    PAN_LEFT = auto()
    PAN_RIGHT = auto()
    DEBUG_TOGGLE = auto()
    QUIT = auto()


# Default key bindings (curses key codes → action).
# Maps are populated at runtime by the InputHandler because
# curses key constants are only available after ``initscr``.
DEFAULT_BINDINGS: dict[int, KeyAction] = {}


def build_default_bindings(curses_mod: object) -> dict[int, KeyAction]:
    """Build the default key → action mapping.

    Parameters:
        curses_mod: The ``curses`` module (passed in to avoid
                    importing curses at module level).
    """
    return {
        ord(" "): KeyAction.TOGGLE_PAUSE,
        ord("n"): KeyAction.STEP,
        ord("N"): KeyAction.STEP,
        ord("r"): KeyAction.RESET,
        ord("R"): KeyAction.RESET,
        ord("c"): KeyAction.CLEAR,
        ord("C"): KeyAction.CLEAR,
        ord("g"): KeyAction.RANDOMIZE,
        ord("G"): KeyAction.RANDOMIZE,
        ord("+"): KeyAction.SPEED_UP,
        ord("="): KeyAction.SPEED_UP,
        ord("-"): KeyAction.SPEED_DOWN,
        ord("0"): KeyAction.ZOOM_RESET,
        curses_mod.KEY_UP: KeyAction.PAN_UP,
        curses_mod.KEY_DOWN: KeyAction.PAN_DOWN,
        curses_mod.KEY_LEFT: KeyAction.PAN_LEFT,
        curses_mod.KEY_RIGHT: KeyAction.PAN_RIGHT,
        curses_mod.KEY_F1: KeyAction.DEBUG_TOGGLE,
        27: KeyAction.QUIT,  # ESC
    }
