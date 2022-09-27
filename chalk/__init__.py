import copy
import re
from typing import Callable, TypeVar, cast

from .colors import ANSI256, RGB
from .config import Level
from .control_sequences import CS, BgColor, CSPair, FgColor
from .conversions import ansi256_to_ansi16, rgb_to_ansi16, rgb_to_ansi256
from .term import supports_color
from .types import Symbol

Self = TypeVar("Self", bound="Chalk")


class Chalk:
    def __init__(self, level: Level) -> None:
        self._level = Symbol(level)
        self._visible = False
        self._cs_pairs: list[CSPair] = []

    def __call__(self, *values: object, sep: str = " ") -> str:
        string = sep.join(map(str, values))
        if string == "":
            return ""

        level = self.level

        if self._visible and level == Level.NO_COLORS:
            return ""

        cs_pairs: list[CSPair] = []

        if level != Level.NO_COLORS:
            for cs in self._cs_pairs:
                if isinstance(cs, BgColor | FgColor):
                    color, color_type = cs.color, type(cs.color)
                    ansi16: Callable[[int], BgColor | FgColor]
                    ansi256: Callable[[int], BgColor | FgColor]
                    if isinstance(cs, BgColor):
                        ansi16, ansi256 = CS.bg_ansi16, CS.bg_ansi256
                    else:
                        ansi16, ansi256 = CS.ansi16, CS.ansi256
                    if level == Level.ANSI16 and color_type == RGB:
                        cs = ansi16(rgb_to_ansi16(*color.tuple))
                    elif level == Level.ANSI16 and color_type == ANSI256:
                        cs = ansi16(ansi256_to_ansi16(color.code))
                    elif level == Level.ANSI256 and color_type == RGB:
                        cs = ansi256(rgb_to_ansi256(*color.tuple))
                cs_pairs.append(cs)

        for i in reversed(cs_pairs):
            string = string.replace(i.close, i.close + i.open)

        cs_open = "".join(i.open for i in cs_pairs)
        cs_close = "".join(i.close for i in reversed(cs_pairs))

        output = (
            cs_open + re.sub(r"(\n|\r\n)", rf"{cs_close}\1{cs_open}", string) + cs_close
        )

        return output

    def _set(self, cs: CSPair | None = None, visible: bool | None = None) -> Self:
        obj = copy.copy(self)
        if cs:
            obj._cs_pairs = obj._cs_pairs + [cs]
        if visible:
            obj._visible = visible
        return cast(Self, obj)

    @property
    def level(self) -> Level:
        return self._level.get()

    @level.setter
    def level(self, value: Level) -> None:
        self._level.set(value)

    @property
    def reset(self) -> Self:
        return self._set(cs=CS.reset)

    @property
    def bold(self) -> Self:
        return self._set(cs=CS.bold)

    @property
    def dim(self) -> Self:
        return self._set(cs=CS.dim)

    @property
    def italic(self) -> Self:
        return self._set(cs=CS.italic)

    @property
    def underline(self) -> Self:
        return self._set(cs=CS.underline)

    @property
    def overline(self) -> Self:
        return self._set(cs=CS.overline)

    @property
    def inverse(self) -> Self:
        return self._set(cs=CS.inverse)

    @property
    def hidden(self) -> Self:
        return self._set(cs=CS.hidden)

    @property
    def strikethrough(self) -> Self:
        return self._set(cs=CS.strikethrough)

    @property
    def black(self) -> Self:
        return self._set(cs=CS.black)

    @property
    def red(self) -> Self:
        return self._set(cs=CS.red)

    @property
    def green(self) -> Self:
        return self._set(cs=CS.green)

    @property
    def yellow(self) -> Self:
        return self._set(cs=CS.yellow)

    @property
    def blue(self) -> Self:
        return self._set(cs=CS.blue)

    @property
    def magenta(self) -> Self:
        return self._set(cs=CS.magenta)

    @property
    def cyan(self) -> Self:
        return self._set(cs=CS.cyan)

    @property
    def white(self) -> Self:
        return self._set(cs=CS.white)

    @property
    def gray(self) -> Self:
        return self._set(cs=CS.gray)

    @property
    def grey(self) -> Self:
        return self._set(cs=CS.grey)

    @property
    def black_bright(self) -> Self:
        return self._set(cs=CS.black_bright)

    @property
    def red_bright(self) -> Self:
        return self._set(cs=CS.red_bright)

    @property
    def green_bright(self) -> Self:
        return self._set(cs=CS.green_bright)

    @property
    def yellow_bright(self) -> Self:
        return self._set(cs=CS.yellow_bright)

    @property
    def blue_bright(self) -> Self:
        return self._set(cs=CS.blue_bright)

    @property
    def magenta_bright(self) -> Self:
        return self._set(cs=CS.magenta_bright)

    @property
    def cyan_bright(self) -> Self:
        return self._set(cs=CS.cyan_bright)

    @property
    def white_bright(self) -> Self:
        return self._set(cs=CS.white_bright)

    @property
    def bg_black(self) -> Self:
        return self._set(cs=CS.bg_black)

    @property
    def bg_red(self) -> Self:
        return self._set(cs=CS.bg_red)

    @property
    def bg_green(self) -> Self:
        return self._set(cs=CS.bg_green)

    @property
    def bg_yellow(self) -> Self:
        return self._set(cs=CS.bg_yellow)

    @property
    def bg_blue(self) -> Self:
        return self._set(cs=CS.bg_blue)

    @property
    def bg_magenta(self) -> Self:
        return self._set(cs=CS.bg_magenta)

    @property
    def bg_cyan(self) -> Self:
        return self._set(cs=CS.bg_cyan)

    @property
    def bg_white(self) -> Self:
        return self._set(cs=CS.bg_white)

    @property
    def bg_gray(self) -> Self:
        return self._set(cs=CS.bg_gray)

    @property
    def bg_grey(self) -> Self:
        return self._set(cs=CS.bg_grey)

    @property
    def bg_black_bright(self) -> Self:
        return self._set(cs=CS.bg_black_bright)

    @property
    def bg_red_bright(self) -> Self:
        return self._set(cs=CS.bg_red_bright)

    @property
    def bg_green_bright(self) -> Self:
        return self._set(cs=CS.bg_green_bright)

    @property
    def bg_yellow_bright(self) -> Self:
        return self._set(cs=CS.bg_yellow_bright)

    @property
    def bg_blue_bright(self) -> Self:
        return self._set(cs=CS.bg_blue_bright)

    @property
    def bg_magenta_bright(self) -> Self:
        return self._set(cs=CS.bg_magenta_bright)

    @property
    def bg_cyan_bright(self) -> Self:
        return self._set(cs=CS.bg_cyan_bright)

    @property
    def bg_white_bright(self) -> Self:
        return self._set(cs=CS.bg_white_bright)

    @property
    def visible(self) -> Self:
        return self._set(visible=True)

    def ansi256(self, code: int) -> Self:
        return self._set(cs=CS.ansi256(code))

    def hex(self, hex: str) -> Self:
        return self._set(cs=CS.hex(hex))

    def rgb(self, red: int, green: int, blue: int) -> Self:
        return self._set(cs=CS.rgb(red, green, blue))

    def bg_ansi256(self, code: int) -> Self:
        return self._set(cs=CS.bg_ansi256(code))

    def bg_hex(self, hex: str) -> Self:
        return self._set(cs=CS.bg_hex(hex))

    def bg_rgb(self, red: int, green: int, blue: int) -> Self:
        return self._set(cs=CS.bg_rgb(red, green, blue))


chalk = Chalk(level=supports_color())
