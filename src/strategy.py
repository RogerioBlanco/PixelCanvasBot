#!/usr/bin/env python

import logging
import math
import random
import time

from six.moves import range

from .calc_axis import CalcAxis
from .colors import EnumColor
from .i18n import I18n
from .matrix import Matrix

logger = logging.getLogger('bot')



class Strategy(object):
    def apply(self):
        raise NotImplementedError()

    def match(self, canvas, image):
        for x in range(image.width):
            for y in range(image.height):
                color = EnumColor.rgba(self.bot.image.pix[x,y], True)
                if canvas.get_color(x + self.bot.start_x, y + self.bot.start_y) != color and color.rgba[3] > 0:
                    return False
        return True

    def scan_canvas(self):
        for pixel in self.priorities:
            old_pixel = (pixel[0], pixel[1], self.bot.canvas.get_color(pixel[0],pixel[1]))
            if pixel != old_pixel:  
                return pixel


class Randomize(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = range(self.bot.image.width)
        self.yrange = range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.yrange:
                for x in self.xrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            random.shuffle(self.priorities)
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Linear(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.yrange:
                for x in self.xrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})

class LinearVertical(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for x in self.xrange:
                for y in self.yrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class QuickFill(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)
        self.b = True
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.yrange:
                for x in self.xrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        if (x % 2 == self.b):
                            self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
                self.b = not self.b
            self.b = False
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Sketch(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            print(I18n.get('strategy.left_right_top_bottom'))
            near_color = 0

            for y in range(self.bot.image.height):
                for x in range(self.bot.image.width):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.right_left_top_bottom'))

            near_color = 0

            for y in range(self.bot.image.height):
                for x in reversed(range(self.bot.image.width)):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.top_bottom_left_right'))

            near_color = 0

            for x in range(self.bot.image.width):
                for y in range(self.bot.image.height):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.bottom_top_left_right'))

            near_color = 0

            for x in range(self.bot.image.width):
                for y in reversed(range(self.bot.image.height)):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])

        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Status(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        px_total = self.bot.image.height * self.bot.image.width
        correct_px = 0
        ignored = 0
        for y in range(self.bot.image.height):
            for x in range(self.bot.image.width):
                template_color = EnumColor.rgba(self.bot.image.pix[x, y])
                canvas_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)

                # Account for ignored pixels
                if template_color in self.colors_ignored or canvas_color in self.colors_not_overwrite or template_color.rgba[3] == 0:
                    ignored += 1

                # Count as correct if not ignored, and if design matches canvas
                if (template_color not in self.colors_ignored and
                        canvas_color not in self.colors_not_overwrite and
                        template_color.rgba[3] > 0 and
                        canvas_color == template_color):
                    correct_px += 1

        px_active_total = px_total - ignored
        incorrect_px = px_active_total - correct_px
        progress = round(float(correct_px) / px_active_total * 100., 2)

        logger.debug(I18n.get('progress').format(total=px_active_total, correct=correct_px, incorrect=incorrect_px, progress=progress))
        self.bot.wait_time({'waitSeconds': 60})


class Radiate(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, px, py, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.px = px
        self.py = py
        self.xrange = range(self.bot.image.width)
        self.yrange = range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.yrange:
                for x in self.xrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            random.shuffle(self.priorities)
            self.priorities.sort(key=lambda priorities: ((priorities[0]-self.px)**2+(priorities[1]-self.py)**2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Spiral(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, px, py, prioritized):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.px = px
        self.py = py
        if px <= self.bot.start_x:
            self.leftxrange = []
            self.rightxrange = range(self.bot.image.width)
        elif px < self.bot.start_x + self.bot.image.width:
            self.leftxrange = range(px - self.bot.start_x)
            self.rightxrange = range(px - self.bot.start_x, self.bot.image.width)
        else:
            self.leftxrange = range(self.bot.image.width)
            self.rightxrange = []
        if py <= self.bot.start_y:
            self.topyrange = []
            self.bottomyrange = range(self.bot.image.height)
        elif py < self.bot.start_y + self.bot.image.height:
            self.topyrange = range(py - self.bot.start_y)
            self.bottomyrange = range(py - self.bot.start_y, self.bot.image.height)
        else:
            self.topyrange = range(self.bot.image.height)
            self.bottomyrange = []
        self.yrange = range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.topyrange:
                for x in self.rightxrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for x in reversed(self.rightxrange):
                for y in self.bottomyrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for y in reversed(self.bottomyrange):
                for x in reversed(self.leftxrange):
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for x in self.leftxrange:
                for y in reversed(self.topyrange):
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            self.priorities.sort(key=lambda priorities: ((priorities[0]-self.px)**2+(priorities[1]-self.py)**2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.match(self.bot.canvas, self.bot.image):
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class DetectMinTime(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        timeList = []

        while True:

            color = random.choice(EnumColor.ENUM)
            # -999999 / 999999 max range
            coord_x = random.randint(self.bot.min_range, self.bot.max_range)
            coord_y = random.randint(self.bot.min_range, self.bot.max_range)

            self.bot.start_x = coord_x
            self.bot.start_y = coord_y

            self.bot.canvas = self.bot.setup_canvas()

            while self.bot.canvas.get_color(coord_x, coord_y) not in self.colors_not_overwrite:
                self.bot.start_x = coord_x = random.randint(self.bot.min_range, self.bot.max_range)
                self.bot.start_y = coord_y = random.randint(self.bot.min_range, self.bot.max_range)

                self.bot.canvas = self.bot.setup_canvas()

            while self.bot.canvas.get_color(coord_x, coord_y) == color or color in self.colors_ignored:
                color = random.choice(EnumColor.ENUM)

            _wait = self.bot.paint(coord_x, coord_y, color)
            timeList.append([_wait, coord_x, coord_y])

            print(sorted(timeList, key=lambda x: x[0]))


class FactoryStrategy(object):

    @staticmethod
    def build(strategy, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, px, py, prioritized):

        if strategy == 'randomize':
            return Randomize(bot, colors_ignored, colors_not_overwrite, prioritized)

        if strategy == 'linear':
            return Linear(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized)

        if strategy == 'linear_vertical':
            return LinearVertical(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized)

        if strategy == 'qf':
            return QuickFill(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed, prioritized)

        if strategy == 'status':
            return Status(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'sketch':
            return Sketch(bot, colors_ignored, colors_not_overwrite, prioritized)

        if strategy == 'radiate':
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'spiral':
            return Spiral(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'detect':
            return DetectMinTime(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'tlc':
            px = bot.start_x
            py = bot.start_y
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'trc':
            px = bot.start_x + bot.image.width - 1
            py = bot.start_y
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'blc':
            px = bot.start_x
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'brc':
            px = bot.start_x + bot.image.width - 1
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'cnb':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = bot.start_y
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'csb':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'cwb':
            px = bot.start_x
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'ceb':
            px = bot.start_x + bot.image.width - 1
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        if strategy == 'cpd':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)

        print(I18n.get('strategy.auto_select').format(strategy=strategy))

        return Spiral(bot, colors_ignored, colors_not_overwrite, px, py, prioritized)  # Default strategy
