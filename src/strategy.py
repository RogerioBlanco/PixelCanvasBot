#!/usr/bin/env python

import logging
import random

from six.moves import range

from .colors import EnumColor
from .i18n import I18n

logger = logging.getLogger('bot')


class Strategy(object):
    def __init__(self, canvas, image, start_x, start_y, colors_ignored=None,
                 colors_not_overwrite=None, prioritized=False, x_reversed=False,
                 y_reversed=False):
        if colors_ignored is None:
            colors_ignored = []
        if colors_not_overwrite is None:
            colors_not_overwrite = []
        self.canvas = canvas
        self.image = image
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.start_x = start_x
        self.start_y = start_y
        self.x_range = list(reversed(range(start_x, start_x + image.width))) \
            if x_reversed else range(start_x, start_x + image.width)
        self.y_range = list(reversed(range(start_y, start_y + image.height))) \
            if y_reversed else range(start_y, start_y + image.height)
        self.prioritized = prioritized
        self.priorities = []

    def pixels(self):
        raise NotImplementedError()

    def template_is_done(self):
        for x in self.x_range:
            for y in self.y_range:
                color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                if self.canvas.get_color(x, y) != color and color.alpha > 0:
                    return False
        return True

    def next_pixel(self):
        for pixel in self.priorities:
            old_pixel = (pixel[0], pixel[1], self.canvas.get_color(pixel[0], pixel[1]))
            if pixel != old_pixel:
                return pixel


class Randomize(Strategy):
    def pixels(self):
        if self.priorities == []:
            for y in self.y_range:
                for x in self.x_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if color not in self.colors_ignored \
                            and old_color not in self.colors_not_overwrite \
                            and color.alpha > 0:
                        self.priorities.append((x, y, color))
            random.shuffle(self.priorities)
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self.template_is_done():
            yield self.next_pixel()


class Linear(Strategy):
    def pixels(self):
        if self.priorities == []:
            for y in self.y_range:
                for x in self.x_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if color not in self.colors_ignored \
                            and old_color not in self.colors_not_overwrite \
                            and color.alpha > 0:
                        self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self.template_is_done():
            yield self.next_pixel()


class LinearVertical(Strategy):
    def pixels(self):
        if self.priorities == []:
            for x in self.x_range:
                for y in self.y_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if color not in self.colors_ignored \
                            and old_color not in self.colors_not_overwrite \
                            and color.alpha > 0:
                        self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self.template_is_done():
            yield self.next_pixel()


class QuickFill(Strategy):
    def pixels(self):
        if self.priorities == []:
            for is_even in (True, False):
                for y in self.y_range:
                    for x in self.x_range:
                        color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                        old_color = self.canvas.get_color(x, y)
                        if old_color != color \
                                and color not in self.colors_ignored \
                                and old_color not in self.colors_not_overwrite \
                                and color.alpha > 0:
                            if (x % 2 == is_even):
                                self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self.template_is_done():
            yield self.next_pixel()


class Sketch(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, prioritized):
        self.bot = bot
        self.canvas = bot.canvas
        self.image = bot.image
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
                    if color != near_color and old_color != color and color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.right_left_top_bottom'))

            near_color = 0

            for y in range(self.bot.image.height):
                for x in reversed(range(self.bot.image.width)):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.top_bottom_left_right'))

            near_color = 0

            for x in range(self.bot.image.width):
                for y in range(self.bot.image.height):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            print(I18n.get('strategy.bottom_top_left_right'))

            near_color = 0

            for x in range(self.bot.image.width):
                for y in reversed(range(self.bot.image.height)):
                    color = EnumColor.rgba(self.bot.image.pix[x, y])
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color != near_color and old_color != color and color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    near_color = color
                near_color = 0

            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])

        while not self.template_is_done():
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Status(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.canvas = bot.canvas
        self.image = bot.image
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
    def __init__(self, *args, **kwargs):
        self.px = kwargs["px"]
        self.py = kwargs["py"]
        super().__init__(*args)

    def pixels(self):
        if self.priorities == []:
            for y in self.y_range:
                for x in self.x_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if color not in self.colors_ignored \
                            and old_color not in self.colors_not_overwrite \
                            and color.alpha > 0:
                        self.priorities.append((x, y, color))
            random.shuffle(self.priorities)
            self.priorities.sort(key=lambda priorities: ((priorities[0] - self.px) ** 2 + (priorities[1] - self.py) ** 2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self.template_is_done():
            yield self.next_pixel()


class Spiral(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, px, py, prioritized):
        self.bot = bot
        self.canvas = bot.canvas
        self.image = bot.image
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.px = px
        self.py = py
        if px <= self.bot.start_x:
            self.leftx_range = []
            self.rightx_range = range(self.bot.image.width)
        elif px < self.bot.start_x + self.bot.image.width:
            self.leftx_range = range(px - self.bot.start_x)
            self.rightx_range = range(px - self.bot.start_x, self.bot.image.width)
        else:
            self.leftx_range = range(self.bot.image.width)
            self.rightx_range = []
        if py <= self.bot.start_y:
            self.topy_range = []
            self.bottomy_range = range(self.bot.image.height)
        elif py < self.bot.start_y + self.bot.image.height:
            self.topy_range = range(py - self.bot.start_y)
            self.bottomy_range = range(py - self.bot.start_y, self.bot.image.height)
        else:
            self.topy_range = range(self.bot.image.height)
            self.bottomy_range = []
        self.y_range = range(self.bot.image.height)
        self.prioritized = prioritized
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.topy_range:
                for x in self.rightx_range:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for x in reversed(self.rightx_range):
                for y in self.bottomy_range:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for y in reversed(self.bottomy_range):
                for x in reversed(self.leftx_range):
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            for x in self.leftx_range:
                for y in reversed(self.topy_range):
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if color not in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            self.priorities.sort(key=lambda priorities: ((priorities[0]-self.px)**2+(priorities[1]-self.py)**2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        while not self.template_is_done():
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class DetectMinTime(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.canvas = bot.canvas
        self.image = bot.image
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
    def build(strategy, bot, colors_ignored, colors_not_overwrite, xreversed,
              yreversed, px, py, prioritized):

        if strategy == 'randomize':
            return Randomize(bot.canvas, bot.image, bot.start_x, bot.start_y,
                             colors_ignored, colors_not_overwrite, prioritized)

        if strategy == 'linear':
            return Linear(bot.canvas, bot.image, bot.start_x, bot.start_y,
                          colors_ignored, colors_not_overwrite, prioritized,
                          xreversed, yreversed)

        if strategy == 'linear_vertical':
            return LinearVertical(bot.canvas, bot.image, bot.start_x,
                                  bot.start_y, colors_ignored,
                                  colors_not_overwrite, xreversed, yreversed,
                                  prioritized)

        if strategy == 'qf':
            return QuickFill(bot.canvas, bot.image, bot.start_x, bot.start_y,
                             colors_ignored, colors_not_overwrite, xreversed,
                             yreversed, prioritized)

        if strategy == 'status':
            return Status(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'sketch':
            return Sketch(bot, colors_ignored, colors_not_overwrite, prioritized)

        if strategy == 'radiate':
            return Radiate(bot.canvas, bot.image, bot.start_x,
                           bot.start_y, colors_ignored, colors_not_overwrite,
                           prioritized, px=px, py=py)

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
