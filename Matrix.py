#!/usr/bin/env python

class Matrix:

    def __init__(self, iterator, start_x, start_y):
        self.matrix = self.setup_matrix(iterator, start_x, start_y)

    def setup_matrix(iterator, start_x, start_y):
        map = {}
        for x in xrange(((start_x - (7 + iterator)) * 64, (iterator + start_x + 8) * 64):
            map[x] = {}
            for y in xrange((start_y - (7 + iterator)) * 64, (iterator + start_y + 8) * 64)):
                map[x][y] = None
        return map

    def update(self, x, y, color):
        if self.exist_axis(x, y):
            self.map[x][y] = color

    def exist_axis(self, x, y):
        try:
            self.map[x][y]
        except IndexError:
            return False
        return True