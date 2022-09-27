from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .color_codes import Colors
from .colors import ANSI16, ANSI256, RGB, BaseColor
from .conversions import hex_to_rgb
from .types import u8


def esc(code: str | int) -> str:
    return f"\u001B[{code}m"


class CSPair(ABC):
    @property
    @abstractmethod
    def open(self) -> str:
        ...

    @property
    @abstractmethod
    def close(self) -> str:
        ...


class Modifier(CSPair):
    def __init__(self, open_code: int, close_code: int) -> None:
        self._open_code = open_code
        self._close_code = close_code

    @property
    def open(self) -> str:
        return esc(self._open_code)

    @property
    def close(self) -> str:
        return esc(self._close_code)


T = TypeVar("T", bound=BaseColor)


class FgColor(Generic[T], CSPair):
    def __init__(self, color: T) -> None:
        self.color = color

    @property
    def open(self) -> str:
        if isinstance(self.color, ANSI16):
            return esc(self.color.code)
        elif isinstance(self.color, ANSI256):
            return esc(f"38;5;{self.color.code}")
        elif isinstance(self.color, RGB):
            return esc(f"38;2;{self.color.red};{self.color.green};{self.color.blue}")
        raise NotImplementedError

    @property
    def close(self) -> str:
        return esc(39)


class BgColor(Generic[T], CSPair):
    def __init__(self, color: T) -> None:
        self.color = color

    @property
    def open(self) -> str:
        if isinstance(self.color, ANSI16):
            return esc(self.color.code + 10)
        elif isinstance(self.color, ANSI256):
            return esc(f"48;5;{self.color.code}")
        elif isinstance(self.color, RGB):
            return esc(f"48;2;{self.color.red};{self.color.green};{self.color.blue}")
        raise NotImplementedError

    @property
    def close(self) -> str:
        return esc(49)


class CS:
    reset = Modifier(0, 0)
    bold = Modifier(1, 22)
    dim = Modifier(2, 22)
    italic = Modifier(3, 23)
    underline = Modifier(4, 24)
    overline = Modifier(53, 55)
    inverse = Modifier(7, 27)
    hidden = Modifier(8, 28)
    strikethrough = Modifier(9, 29)

    black = FgColor(ANSI16(Colors.BLACK))
    red = FgColor(ANSI16(Colors.RED))
    green = FgColor(ANSI16(Colors.GREEN))
    yellow = FgColor(ANSI16(Colors.YELLOW))
    blue = FgColor(ANSI16(Colors.BLUE))
    magenta = FgColor(ANSI16(Colors.MAGENTA))
    cyan = FgColor(ANSI16(Colors.CYAN))
    white = FgColor(ANSI16(Colors.WHITE))

    black_bright = FgColor(ANSI16(Colors.BRIGHT_BLACK))
    red_bright = FgColor(ANSI16(Colors.BRIGHT_RED))
    green_bright = FgColor(ANSI16(Colors.BRIGHT_GREEN))
    yellow_bright = FgColor(ANSI16(Colors.BRIGHT_YELLOW))
    blue_bright = FgColor(ANSI16(Colors.BRIGHT_BLUE))
    magenta_bright = FgColor(ANSI16(Colors.BRIGHT_MAGENTA))
    cyan_bright = FgColor(ANSI16(Colors.BRIGHT_CYAN))
    white_bright = FgColor(ANSI16(Colors.BRIGHT_WHITE))

    gray = black_bright
    grey = black_bright

    bg_black = BgColor(ANSI16(Colors.BLACK))
    bg_red = BgColor(ANSI16(Colors.RED))
    bg_green = BgColor(ANSI16(Colors.GREEN))
    bg_yellow = BgColor(ANSI16(Colors.YELLOW))
    bg_blue = BgColor(ANSI16(Colors.BLUE))
    bg_magenta = BgColor(ANSI16(Colors.MAGENTA))
    bg_cyan = BgColor(ANSI16(Colors.CYAN))
    bg_white = BgColor(ANSI16(Colors.WHITE))

    bg_black_bright = BgColor(ANSI16(Colors.BRIGHT_BLACK))
    bg_red_bright = BgColor(ANSI16(Colors.BRIGHT_RED))
    bg_green_bright = BgColor(ANSI16(Colors.BRIGHT_GREEN))
    bg_yellow_bright = BgColor(ANSI16(Colors.BRIGHT_YELLOW))
    bg_blue_bright = BgColor(ANSI16(Colors.BRIGHT_BLUE))
    bg_magenta_bright = BgColor(ANSI16(Colors.BRIGHT_MAGENTA))
    bg_cyan_bright = BgColor(ANSI16(Colors.BRIGHT_CYAN))
    bg_white_bright = BgColor(ANSI16(Colors.BRIGHT_WHITE))

    bg_gray = bg_black_bright
    bg_grey = bg_black_bright

    @staticmethod
    def ansi16(code: u8) -> FgColor:
        return FgColor(ANSI16(code))

    @staticmethod
    def ansi256(code: u8) -> FgColor:
        return FgColor(ANSI256(code))

    @staticmethod
    def hex(hex: str) -> FgColor:
        return FgColor(RGB(*hex_to_rgb(hex)))

    @staticmethod
    def rgb(red: u8, green: u8, blue: u8) -> FgColor:
        return FgColor(RGB(red, green, blue))

    @staticmethod
    def bg_ansi16(code: u8) -> BgColor:
        return BgColor(ANSI16(code))

    @staticmethod
    def bg_ansi256(code: u8) -> BgColor:
        return BgColor(ANSI256(code))

    @staticmethod
    def bg_hex(hex: str) -> BgColor:
        return BgColor(RGB(*hex_to_rgb(hex)))

    @staticmethod
    def bg_rgb(red: u8, green: u8, blue: u8) -> BgColor:
        return BgColor(RGB(red, green, blue))
