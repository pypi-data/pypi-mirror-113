"""
This module is designed to color the information displayed in the console.

import rainbow

rainbow.print("#F07427example #F4CA16print")
rainbow.print("example print", color="#CC397B")
print(rainbow.paint("Hello, world!", color="#318CE7"))

Colored line example: "#318CE7Hello #FECF3DWorld#309831!#r default colored text"
Use #xxxxx to set color
Use #r to reset color to console default
Flag #r automatically appends to end of string
"""

import re

OPEN_COLOR = "\033[38;2;{r};{g};{b}m"
CLOSE_COLOR = "\033[0m"


def hex_to_rgb(value: str) -> tuple:
    """
    This function converts hex color to rgb color.

    :param value: color in hex
    :return: tuple of rgb color
    """
    if (not value.startswith("#")) or (len(value) != 7):
        raise ValueError(f"value {value} is not a valid hex")
    try:
        return tuple(int(value.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"value {value} is not a valid hex")


def paint(string: str, color: str = None, ignore_errors: bool = False) -> str:
    """
    This function paints a string by pattern.

    :param string: the string to be colored
    :param color: default color
    :param ignore_errors: ignore errors
    :return: colored string
    """
    colors = list(set(re.findall(r"#[0-9a-fA-F]{6}", string)))

    try:
        hex_to_rgb(color)
        colors.append(color)
        string = color + string
    except ValueError as e:
        if not ignore_errors:
            raise e
    except AttributeError:
        pass

    for color in colors:
        r, g, b = hex_to_rgb(color)
        string = re.sub(color, OPEN_COLOR.format(r=r, g=g, b=b), string)

    string += "#r"
    string = re.sub(r"#r", CLOSE_COLOR, string)

    return string


def rainbow_print(*args, color: str = None, ignore_errors: bool = False, **kwargs):
    """
    This function works like print but in addition, it automatically color the lines.

    :param color: default color
    :param ignore_errors: ignore errors
    """

    print(" ".join(list(map(lambda value: paint(str(value), color=color, ignore_errors=ignore_errors), args))), **kwargs)
