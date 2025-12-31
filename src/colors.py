"""ANSI color codes for terminal output.

This module provides simple color formatting using ANSI escape codes.
No external dependencies required - uses only Python standard library.
"""

import os
import sys


class Colors:
    """ANSI color codes for terminal output."""

    # Check if terminal supports colors
    _SUPPORTS_COLOR = (
        hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    ) or 'TERM' in os.environ

    # Color codes
    RED = '\033[91m' if _SUPPORTS_COLOR else ''
    GREEN = '\033[92m' if _SUPPORTS_COLOR else ''
    YELLOW = '\033[93m' if _SUPPORTS_COLOR else ''
    BLUE = '\033[94m' if _SUPPORTS_COLOR else ''
    MAGENTA = '\033[95m' if _SUPPORTS_COLOR else ''
    CYAN = '\033[96m' if _SUPPORTS_COLOR else ''
    WHITE = '\033[97m' if _SUPPORTS_COLOR else ''

    # Styles
    BOLD = '\033[1m' if _SUPPORTS_COLOR else ''
    DIM = '\033[2m' if _SUPPORTS_COLOR else ''
    UNDERLINE = '\033[4m' if _SUPPORTS_COLOR else ''

    # Reset
    RESET = '\033[0m' if _SUPPORTS_COLOR else ''


def colorize(text: str, color: str) -> str:
    """Apply color to text.

    Args:
        text: Text to colorize.
        color: Color code from Colors class.

    Returns:
        Colored text with reset code.
    """
    if not Colors._SUPPORTS_COLOR:
        return text
    return f"{color}{text}{Colors.RESET}"


def success(text: str) -> str:
    """Format text as success message (green)."""
    return colorize(text, Colors.GREEN)


def error(text: str) -> str:
    """Format text as error message (red)."""
    return colorize(text, Colors.RED)


def info(text: str) -> str:
    """Format text as info message (cyan)."""
    return colorize(text, Colors.CYAN)


def warning(text: str) -> str:
    """Format text as warning message (yellow)."""
    return colorize(text, Colors.YELLOW)


def bold(text: str) -> str:
    """Format text as bold."""
    return colorize(text, Colors.BOLD)


def highlight(text: str) -> str:
    """Format text as highlighted (bold cyan)."""
    if not Colors._SUPPORTS_COLOR:
        return text
    return f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}"
