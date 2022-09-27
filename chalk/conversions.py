import math
import re

from .types import u8


def rgb_to_ansi256(red: u8, green: u8, blue: u8) -> u8:
    if red == green and green == blue:
        if red < 8:
            return 16

        if red > 248:
            return 231

        return round(((red - 8) / 247) * 24) + 232

    return (
        16
        + (36 * round(red / 255 * 5))
        + (6 * round(green / 255 * 5))
        + round(blue / 255 * 5)
    )


def rgb_to_ansi16(red: u8, green: u8, blue: u8) -> u8:
    return ansi256_to_ansi16(rgb_to_ansi256(red, green, blue))


def ansi256_to_ansi16(code: u8) -> u8:
    if code < 8:
        return 30 + code

    if code < 16:
        return 90 + (code - 8)

    red: int
    green: int
    blue: int

    if code >= 232:
        red = (((code - 232) * 10) + 8) // 255
        green = red
        blue = red
    else:
        code -= 16

        remainder = code % 36

        red = math.floor(code / 36) // 5
        green = math.floor(remainder / 6) // 5
        blue = (remainder % 6) // 5

    value = max(red, green, blue) * 2

    if value == 0:
        return 30

    result = 30 + (round(blue) << 2) | (round(green) << 1) | round(red)

    if value == 2:
        result += 60

    return result


def hex_to_rgb(hex: str) -> tuple[u8, u8, u8]:
    matches = re.match(r"#(?P<color>[a-f\d]{6}|[a-f\d]{3})", hex, re.IGNORECASE)
    if matches is None:
        raise ValueError(f"Invalid color: {hex}")

    color = matches.group("color")

    if len(color) == 3:
        color = "".join(character * 2 for character in color)

    integer = int(color, 16)

    return (
        (integer >> 16) & 0xFF,
        (integer >> 8) & 0xFF,
        integer & 0xFF,
    )
