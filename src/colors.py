#!/usr/bin/env python

import logging
import math
from copy import deepcopy

from .i18n import I18n

logger = logging.getLogger('bot')


class EnumColor:
    class Color(object):
        def __init__(self, index, name, rgba):
            self.name = name
            self.rgba = rgba
            self.index = index

        def __eq__(self, other):
            return self.name == other.name and self.rgba[0:3] == other.rgba[0:3]

        def __ne__(self, other):
            return not self.__eq__(other)

        @property
        def alpha(self):
            return self.rgba[3]

    ENUM = [
        Color(0, 'white', (255, 255, 255, 255)),
        Color(1, 'gainsboro', (228, 228, 228, 255)),
        Color(2, 'grey', (136, 136, 136, 255)),
        Color(3, 'nero', (34, 34, 34, 255)),
        Color(4, 'carnation pink', (255, 167, 209, 255)),
        Color(5, 'red', (229, 0, 0, 255)),
        Color(6, 'orange', (229, 149, 0, 255)),
        Color(7, 'brown', (160, 106, 66, 255)),
        Color(8, 'yellow', (229, 217, 0, 255)),
        Color(9, 'conifer', (148, 224, 68, 255)),
        Color(10, 'green', (2, 190, 1, 255)),
        Color(11, 'dark turquoise', (0, 211, 221, 255)),
        Color(12, 'pacific blue', (0, 131, 199, 255)),
        Color(13, 'blue', (0, 0, 234, 255)),
        Color(14, 'violet', (207, 110, 228, 255)),
        Color(15, 'purple', (130, 0, 128, 255)),
        Color(16, 'noncolor', (91, 9, 9, 255))
    ]

    @staticmethod
    def index(i):
        for color in EnumColor.ENUM:
            if i == color.index:
                return color
        # White is default color
        return EnumColor.ENUM[0]

    @staticmethod
    def rgba(rgba, silent=False, sensitive=1, brightness=0):
        for color in EnumColor.ENUM:
            if rgba[0:3] == color.rgba[0:3]:
                new_color = deepcopy(color)
                new_color.rgba = rgba
                return new_color

        # if that color is not in standard colors list
        diff_min = [(255, 255, 255), 1038366]  # sqrt(255*255 + 255*255 + 255*255) = 441.67295593 --> Default white

        for x in range(0,16):
            color = EnumColor.ENUM[x]
            # formula that sqrt( (x1 - x2)2 + (y1 - y2)2 + (z1 - z2)2 )

            diff_r = ((rgba[0] + brightness) - color.rgba[0]) * ((rgba[0] + brightness) - color.rgba[0])
            diff_g = ((rgba[1] + brightness) - color.rgba[1]) * ((rgba[1] + brightness) - color.rgba[1])
            diff_b = ((rgba[2] + brightness) - color.rgba[2]) * ((rgba[2] + brightness) - color.rgba[2])

            x = min(diff_r, diff_g, diff_b)
            z = max(diff_r, diff_g, diff_r)
            y = (diff_r + diff_g + diff_b) - (x + z)

            x = x / sensitive
            z = z * sensitive

            diffys = math.sqrt(x + y + z)

            if diffys < diff_min[1]:
                diff_min[1] = diffys
                diff_min[0] = color.rgba[0:3] + (rgba[3],)

        # return rounding colour

        if not silent:
            logger.debug(I18n.get(' %s colours rounded %s (%s) ') % (
            str(rgba), str(diff_min[0]), I18n.get(str(EnumColor.rgba(diff_min[0]).name), 'true')))
        return EnumColor.rgba(diff_min[0])
