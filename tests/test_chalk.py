from chalk import Chalk, chalk
from chalk.config import Level


def test_no_style():
    assert chalk("foo") == "foo"


def test_multiple_argument():
    assert chalk("hello", "world") == "hello world"


def test_cast_to_string():
    assert chalk(["hello", "world"], 123) == "['hello', 'world'] 123"


def test_style_string():
    assert chalk.underline("foo") == "\u001B[4mfoo\u001B[24m"
    assert chalk.red("foo") == "\u001B[31mfoo\u001B[39m"
    assert chalk.bg_red("foo") == "\u001B[41mfoo\u001B[49m"


def test_multiple_styles():
    assert (
        chalk.red.bg_green.underline("foo")
        == "\u001B[31m\u001B[42m\u001B[4mfoo\u001B[24m\u001B[49m\u001B[39m"
    )
    assert (
        chalk.underline.red.bg_green("foo")
        == "\u001B[4m\u001B[31m\u001B[42mfoo\u001B[49m\u001B[39m\u001B[24m"
    )


def test_nested_styles():
    assert (
        chalk.red("foo" + chalk.underline.bg_blue("bar") + "!")
        == "\u001B[31mfoo\u001B[4m\u001B[44mbar\u001B[49m\u001B[24m!\u001B[39m"
    )
    assert (
        chalk.red("a" + chalk.yellow("b" + chalk.green("c") + "b") + "c")
        == "\u001B[31ma\u001B[33mb\u001B[32mc\u001B[39m\u001B[31m\u001B[33mb\u001B[39m\u001B[31mc\u001B[39m"
    )


def test_style_precedent():
    assert (
        chalk.red.green.underline("foo")
        == "\u001B[31m\u001B[32m\u001B[4mfoo\u001B[24m\u001B[39m\u001B[39m"
    )


def test_empty_input():
    assert chalk.red() == ""
    assert chalk.red.blue.black() == ""


def test_line_breaks():
    assert (
        chalk.grey("hello\nworld")
        == "\u001B[90mhello\u001B[39m\n\u001B[90mworld\u001B[39m"
    )
    assert (
        chalk.grey("hello\r\nworld")
        == "\u001B[90mhello\u001B[39m\r\n\u001B[90mworld\u001B[39m"
    )


def test_convert_rgb_to_ansi16():
    assert (
        Chalk(level=Level.ANSI16).hex("#FF0000")("hello") == "\u001B[91mhello\u001B[39m"
    )
    assert (
        Chalk(level=Level.ANSI16).bg_hex("#FF0000")("hello")
        == "\u001B[101mhello\u001B[49m"
    )


def test_convert_rgb_to_ansi256():
    assert (
        Chalk(level=Level.ANSI256).hex("#FF0000")("hello")
        == "\u001B[38;5;196mhello\u001B[39m"
    )
    assert (
        Chalk(level=Level.ANSI256).bg_hex("#FF0000")("hello")
        == "\u001B[48;5;196mhello\u001B[49m"
    )
    assert (
        Chalk(level=Level.TRUECOLOR).bg_hex("#FF0000")("hello")
        == "\u001B[48;2;255;0;0mhello\u001B[49m"
    )


def test_no_colors():
    assert Chalk(level=Level.NO_COLORS).hex("#FF0000")("hello") == "hello"


def test_visible():
    assert Chalk(level=Level.TRUECOLOR).visible.red("foo") == "\u001B[31mfoo\u001B[39m"
    assert Chalk(level=Level.NO_COLORS).red.visible("foo") == ""


def test_level_propagate():
    chalk.level = Level.ANSI16
    assert chalk.red.level == Level.ANSI16
    chalk.red.level = Level.NO_COLORS
    assert chalk.level == Level.NO_COLORS
