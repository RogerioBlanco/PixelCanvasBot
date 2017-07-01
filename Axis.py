#!/usr/bin/env python

import math

class Axis:

    @staticmethod
    def get_centers(start_x, width, start_y, height):
        return (x - (x % 64)) / 64, (y - (y % 64)) / 64

    @staticmethod
    def calc_radius(start_x, width, start_y, height):
        radius_x = abs(((start_x + width) - start_x) / 960)
        radius_y = abs(((start_y + height) - start_y) / 960)
        radius = int(math.ceil(radius_x if radius_x >= radius_y else radius_y))
        return (radius if radius % 2 else radius + 1)

    @staticmethod
    def get_center_points(start_x, width, start_y, height):
        return ((start_x + width) + start_x) / 2, ((start_y + height) + start_y) / 2

    @staticmethod
    def get_iteration(radius):
        return int(math.ceil(radius / 2) * 15)
