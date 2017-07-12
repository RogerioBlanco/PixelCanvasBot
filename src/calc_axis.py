#!/usr/bin/env python

import math

class CalcAxis:

    @staticmethod
    def calc_centers_axis(middle_x, middle_y):
        return (middle_x - (middle_x % 64)) / 64, (middle_y - (middle_y % 64)) / 64

    @staticmethod
    def calc_radius(start_x, width, start_y, height):
        radius_x = ((start_x + width) - start_x) / 960.
        radius_y = ((start_y + height) - start_y) / 960.
        radius = int(math.ceil(radius_x if radius_x >= radius_y else radius_y))
        return (radius if radius % 2 else radius + 1)

    @staticmethod
    def calc_middle_axis(start_x, width, start_y, height):
        return ((start_x + width) + start_x) / 2, ((start_y + height) + start_y) / 2

    @staticmethod
    def calc_iteration(radius):
        return int(math.ceil(radius / 2) * 15)
