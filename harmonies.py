#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
color harmonies:
1 -> complementary color (+180º in hsl)
2 -> analogous (fix set of 2/4 colors to start):
        . +30 , +60
        . -30 , -60
3 -> triad: colors are evenly spaced (+120, -120)
4 -> split-complementary
        use analogous to complementary color
        c -> -30, +30
5 -> rectangle (tetradic): four colors split into
        two complementary pairs
        (color1, color2) -> (comp_1, comp_2)
6 -> square : four colors evenly distributed
        +90º,+180,+270

---------------------------------------------------------
INPUT)
1. hexstring
defaults : rgb(255,255,255) hls(0,0,1) rel (0,0,100) abs #white
"""

import colorsys
import re


# ------------------------------------------------
# conversion functions
# ------------------------------------------------


def isColor(colorStr):
    """
    Test if the color string is in the required format
    :param colorStr color string format #xxxxxx
    :rtype: boolean
    """
    if len(colorStr) != 7:
        return False
    if re.search(r"#[a-fA-F0-9]{6}", colorStr):
        return True


def hexToTuple(colorStr):
    """
       Hexadecimal color string to rgb tuple.
       :param colorStr color string format #xxxxxx
    """
    if not isColor(colorStr):
        raise ValueError("Hexadecimal string color format must be like #ff00ff")

    # string: #00ff00
    red = int(colorStr[1:3], 16)
    green = int(colorStr[3:5], 16)
    blue = int(colorStr[5:], 16)
    return red, green, blue


def rgbRelative(rgbcolor):
    """
    rgb absolute to relative
    :param rgbcolor tuple (0-255,0-255,0-255)
    """
    base = 255.0
    return tuple([round(i / base, 4) for i in rgbcolor])


def rgbAbsolute(rgbcolor):
    """
    rgb relative to rgb absolute
    :param rgbcolor relative tuple (0-1.0, 0-1.0, 0-1.0)
    """
    base = 255
    return tuple([(round(i * base)) for i in rgbcolor])


def hslRelative(hslcolor):
    """
    hsl absolute to hsl relative
    :param hslcolor absolute tuple (0-360, 0-100, 0-100)
    """
    return round(hslcolor[0] / 360.0, 4), round(hslcolor[1] / 100.0, 4), round(hslcolor[2] / 100.0, 4)


def hslAbsolute(hslcolor):
    """
    hsl relative to hsl absolute
    :param hslcolor relative tuple (0-1.0, 0-1.0, 0-1.0)
    """

    return round(hslcolor[0] * 360, 2), round(hslcolor[1] * 100, 2), round(hslcolor[2] * 100)


def hexColor(rgbcolor):
    """
    Return a hexadecimal color string from a rgb tuple
    :param rgbcolor rgb tuple (0-255, 0-255, 0-255)
    """
    # convert to int : compatibility with python2.x
    return '#' + ''.join(['{:02x}'.format(int(i)) for i in rgbcolor])


def rgbToHsl(rgbcolor):
    """
    Rgb to Hsl using colorsys
    :param rgbcolor tuple (0-255, 0-255, 0-255)
    """
    # from rgb absolute color to hsl absolute color
    rgb = rgbRelative(rgbcolor)
    # watch in colorsys is h-l-s
    hsl = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    hAbs = hslAbsolute((hsl[0], hsl[2], hsl[1]))
    return hAbs


def hslToRgb(hslcolor):
    """
    Hsl to Rgb using colorsys
    :param hslcolor tuple (0-360, 0-100, 0-100)
    """
    # from hls absolute color to rgb absolute
    hls = hslRelative(hslcolor)
    # ! watch in colorys is h-l-s but tuple comes in hsl
    rgb = colorsys.hls_to_rgb(hls[0], hls[2], hls[1])
    rAbs = rgbAbsolute(rgb)
    return rAbs


# -------------------------------------
# harmonies functions
# -------------------------------------
# color params are passed as absolute hsl

def complementary(color):
    """
    Get complementary color in hsl
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    """
    position = (color[0] + 180) % 360
    return position, color[1], color[2]


def splitComplementary(color):
    """
    Get the two colors adjacent to the complementary.
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    """
    first = (color[0] + 150) % 360, color[1], color[2]
    second = (color[0] + 210) % 360, color[1], color[2]
    return first, second


def analogous(color, colors=2):
    """
    Get a set of adjacent colors: 2 or 4
    Colors are considered to be separated by 30º
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    :param colors int 2 or 4
    """
    one = (color[0] + 30) % 360, color[1], color[2]
    two = (color[0] - 30) % 360, color[1], color[2]
    three = (color[0] + 60) % 360, color[1], color[2]
    four = (color[0] - 60) % 360, color[1], color[2]
    if colors == 2:
        return one, two
    else:
        return one, two, three, four


def triadic(color):
    """
    Get a triad of evenly distributed colors:
    the original + two more
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    """
    one = (color[0] + 120) % 360, color[1], color[2]
    two = (color[0] + 240) % 360, color[1], color[2]
    return one, two


def tetradic(color):
    """
    Get four colors evenly distributed:
    the original + three more
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    """
    one = (color[0] + 90) % 360, color[1], color[2]
    two = (color[0] + 180) % 360, color[1], color[2]
    three = (color[0] + 270) % 360, color[1], color[2]
    return one, two, three


def doubleComplementary(colorOne, colorTwo):
    return complementary(colorOne), complementary(colorTwo)


# ----------------------------------------------------------
# monochromatic functions
# ----------------------------------------------------------

def desaturate(color, percent=10):
    return color[0], (color[1] - percent) % 100, color[2]


def saturate(color, percent=10):
    return color[0], (color[1] + percent) % 100, color[2]


def lighter(color, percent=10):
    """
    Get a lighter tone. Default = 10%
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    :param percent int 0-99
    """
    return color[0], color[1], (color[2] + percent) % 100


def darker(color, percent=10):
    """
    Get a darker tone. Default = 10%.
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    :param percent int 0-99
    """
    return color[0], color[1], (color[2] - percent) % 100


def mono(color, percent=10):
    """
    Get four tints-shades from color.
    Assumed percent = 10%. Also it won't return black or white,
    keep turning the wheel.
    :param color tuple in hsl absolute values (0-360,0-100,0-100)
    :param percent int 0-99
    """

    return lighter(color, percent), lighter(color, percent * 2), darker(color, percent), darker(color, percent * 2)
