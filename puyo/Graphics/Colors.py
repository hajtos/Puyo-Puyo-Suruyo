from collections import namedtuple

ColorStruct = namedtuple("Colors", "BLACK, GREY, WHITE, DARKTURQUOISE, \
    GREEN, LIGHTGREEN, RED, BLUE, YELLOW, PURPLE, ORANGE")


COLORS = ColorStruct(
    #COLOR = (R, G, B)
    BLACK=(0, 0, 0),
    GREY=(127, 127, 127),
    WHITE=(255, 255, 255),
    DARKTURQUOISE=(3, 54, 73),
    GREEN=(0, 204, 0),
    LIGHTGREEN=(100, 255, 100),
    RED=(255, 0, 0),
    BLUE=(0, 127, 255),
    YELLOW=(255, 255, 0),
    PURPLE=(127, 0, 255),
    ORANGE=(255, 127, 0)
)
