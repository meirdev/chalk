from abc import ABC

from .color_codes import Colors
from .types import u8


class BaseColor(ABC):
    pass


class ANSI16(BaseColor):
    def __init__(self, color: u8 | Colors) -> None:
        self.code = color


class ANSI256(BaseColor):
    def __init__(self, color: u8) -> None:
        self.code = color


class RGB(BaseColor):
    def __init__(self, red: u8, green: u8, blue: u8) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def tuple(self) -> tuple[u8, u8, u8]:
        return self.red, self.green, self.blue
