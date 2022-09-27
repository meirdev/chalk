import os
import re

from .config import Level


def supports_color() -> Level:
    level = Level.NO_COLORS

    force_color = os.environ.get("FORCE_COLOR", "")
    if force_color:
        match force_color:
            case "0":
                level = Level.NO_COLORS
            case "1":
                level = Level.ANSI16
            case "2":
                level = Level.ANSI256
            case "3":
                level = Level.TRUECOLOR
        return level

    color_term = os.environ.get("COLORTERM", "")
    if color_term:
        level = Level.ANSI16
    if re.search(r"truecolor|24bit", color_term, re.IGNORECASE):
        level = Level.TRUECOLOR

    term = os.environ.get("TERM", "")
    if re.search(r"256color", term, re.IGNORECASE):
        level = Level.ANSI256

    return level
