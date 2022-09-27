from enum import IntEnum


class Level(IntEnum):
    NO_COLORS = 0
    ANSI16 = 1
    ANSI256 = 2
    TRUECOLOR = 3
