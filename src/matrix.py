#!/usr/bin/env python

from six.moves import range

class Matrix:

    def __init__(self, start_x, start_y, width, height):
        matrix = {}
        for x in range(start_x, start_x + width):
            matrix[x] = {}
            for y in range(start_y, start_y + height):
                matrix[x][y] = None
        self.matrix = matrix

    def update(self, x, y, color):
        if self.exist_axis(x, y):
            self.matrix[x][y] = color

    def exist_axis(self, x, y):
        try:
            self.matrix[x][y]
        except (IndexError, KeyError):
            return False
        return True

    def get_color(self, x, y):
        if self.exist_axis(x, y):
            return self.matrix[x][y]

        return None
