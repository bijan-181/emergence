"""Color definitions for terminal rendering."""

from __future__ import annotations

# ANSI colour codes (standard 8-colour palette).
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Foreground
FG_BLACK = "\033[30m"
FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_BLUE = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN = "\033[36m"
FG_WHITE = "\033[37m"
FG_BRIGHT_GREEN = "\033[92m"
FG_BRIGHT_YELLOW = "\033[93m"
FG_BRIGHT_CYAN = "\033[96m"

# Background
BG_BLACK = "\033[40m"
BG_GREEN = "\033[42m"
BG_DARK_GREEN = "\033[48;5;22m"
BG_DARK_GRAY = "\033[48;5;235m"
BG_LIGHT_GRAY = "\033[48;5;240m"


def colored(text: str, fg: str = "", bg: str = "") -> str:
    """Wrap *text* in ANSI colour escape sequences."""
    parts: list[str] = []
    if fg:
        parts.append(fg)
    if bg:
        parts.append(bg)
    if parts:
        return f"{''.join(parts)}{text}{RESET}"
    return text
