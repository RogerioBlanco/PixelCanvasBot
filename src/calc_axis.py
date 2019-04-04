#!/usr/bin/env python

from __future__ import division
import math


class CalcAxis:

    @staticmethod
    def calc_centers_axis(middle_x, middle_y):
        return (middle_x - (middle_x % 64)) // 64, (middle_y - (middle_y % 64)) // 64

    @staticmethod
    def calc_max_chunks(start_x, width, start_y, height):
        chunks_x = width / 960.
        chunks_y = height / 960.
        max_chunks = int(math.ceil(radius_x if radius_x >= radius_y else radius_y))
        return (max_chunks if max_chunks % 2 else max_chunks + 1)

    @staticmethod
    def calc_middle_axis(start_x, width, start_y, height):
        return (2 * start_x + width) // 2, (2 * start_y + height) // 2

    @staticmethod
    def calc_iteration(max_chunks):
        return int(math.ceil(max_chunks / 2) * 15)
