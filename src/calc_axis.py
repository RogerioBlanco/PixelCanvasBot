#!/usr/bin/env python

from __future__ import division
import math


class CalcAxis:

    @staticmethod
    def calc_centers_axis(middle_x, middle_y):
        center_x = (middle_x - (middle_x % 64)) // 64
        center_y = (middle_y - (middle_y % 64)) // 64
        offset_x = center_x % 15
        offset_y = center_y % 15
        return center_x - offset_x, center_y - offset_y

    @staticmethod
    def calc_max_chunks(width, height):
        chunks_x = width / 960.
        chunks_y = height / 960.
        max_chunks = int(math.ceil(chunks_x if chunks_x >= chunks_y else chunks_y))
        return (max_chunks if max_chunks % 2 else max_chunks + 1)

    @staticmethod
    def calc_middle_axis(start_x, width, start_y, height):
        return (2 * start_x + width) // 2, (2 * start_y + height) // 2

    @staticmethod
    def calc_num_blocks(max_chunks):
        return int(math.ceil(max_chunks / 2) * 15)
