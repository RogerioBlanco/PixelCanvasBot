#!/usr/bin/env python

import time, random, math
from .calc_axis import CalcAxis
from .matrix import Matrix
from .colors import EnumColor
from .i18n import I18n
from six.moves import range


class Strategy(object):
    def apply(self):
        raise NotImplementedError()


class Randomize(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.size_limit = self.bot.image.width * self.bot.image.height
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        count = 0
        while not self.match(self.bot.canvas, self.bot.image):
            x, y, color = self.roll_dice(self.bot.canvas)
            if self.bot.canvas.get_color(x, y) != color and not color in self.colors_ignored and self.bot.canvas.get_color(x, y) not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(x, y, color)
            count += 1

    def roll_dice(self, canvas):
        rnd_x = rnd_y = color = None
        while all(v is None for v in [rnd_x, rnd_y, color]) or canvas.get_color(rnd_x, rnd_y) == color:
            rnd_x = self.random(self.bot.start_x, self.bot.start_x + self.bot.image.width - 1)
            rnd_y = self.random(self.bot.start_y, self.bot.start_y + self.bot.image.height - 1)
            color = EnumColor.rgba(self.bot.image.pix[rnd_x - self.bot.start_x, rnd_y - self.bot.start_y], True)
        color = EnumColor.rgba(self.bot.image.pix[rnd_x - self.bot.start_x, rnd_y - self.bot.start_y])
        return rnd_x, rnd_y, color

    def random(self, start, end):
        return random.randint(start, end)

    def match(self, canvas, image):
        for x in range(0, image.width):
            for y in range(0, image.height):
                if canvas.get_color(x + self.bot.start_x, y + self.bot.start_y) != EnumColor.rgba(
                        self.bot.image.pix[x, y], True):
                    return False
        return True


class Prioritized_Linear(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)
        self.priorities = []

    def apply(self):
        if self.priorities == []:
            for y in self.yrange:
                for x in self.xrange:
                    color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                    old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                    if not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 0:
                        self.priorities += [(self.bot.start_x + x, self.bot.start_y + y, color)]
            self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].rgba[3])
        for pixel in self.priorities:
            old_color = self.bot.canvas.get_color(pixel[0],pixel[1])
            if old_color != pixel[2]:
                self.bot.paint(*pixel)


class Linear(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)

    def apply(self):
        for y in self.yrange:
            for x in self.xrange:
                color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)


class QuickFill(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed):
        self.bot = bot
        self.colors_ignored = colors_ignored
        self.colors_not_overwrite = colors_not_overwrite
        self.xrange = list(reversed(range(self.bot.image.width))) if xreversed else range(self.bot.image.width)
        self.yrange = list(reversed(range(self.bot.image.height))) if yreversed else range(self.bot.image.height)
        self.b = True

    def apply(self):
        for y in self.yrange:
            for x in self.xrange:
                color = EnumColor.rgba(self.bot.image.pix[x, y], True)
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    if (x % 2 == self.b):
                        self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
            self.b = not self.b
        self.b = False


class Sketch(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        print(I18n.get('# From left to right, from top to bottom,'))
        near_color = 0

        for y in range(self.bot.image.height):
            for x in range(self.bot.image.width):
                color = EnumColor.rgba(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        print(I18n.get('# From right to left, from top to bottom,'))

        near_color = 0

        for y in range(self.bot.image.height):
            for x in reversed(range(self.bot.image.width)):
                color = EnumColor.rgba(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        print(I18n.get('# From top to bottom, from left to right,'))

        near_color = 0

        for x in range(self.bot.image.width):
            for y in range(self.bot.image.height):
                color = EnumColor.rgba(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        print(I18n.get('# From bottom to top, from left to right,'))

        near_color = 0

        for x in range(self.bot.image.width):
            for y in reversed(range(self.bot.image.height)):
                color = EnumColor.rgba(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0


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
                if template_color in self.colors_ignored or canvas_color in self.colors_not_overwrite or template_color.rgba[3] < 128:
                    ignored += 1

                # Count as correct if not ignored, and if design matches canvas
                if (template_color not in self.colors_ignored and
                        canvas_color not in self.colors_not_overwrite and
                        template_color.rgba[3] > 127 and
                        canvas_color == template_color):
                    correct_px += 1

        px_active_total = px_total - ignored
        incorrect_px = px_active_total - correct_px
        progress = round(float(correct_px) / px_active_total * 100., 2)

        print(I18n.get('Total: %s painted: %s Not painted: %s Progress: %s%%') % (str(px_active_total), str(correct_px), str(incorrect_px), str(progress)))
        self.bot.wait_time({'waitSeconds': 60})


class TopLeftCorner(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class TopRightCorner(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class BottomLeftCorner(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class BottomRightCorner(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class CentreNorthBoundary(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class CentreSouthBoundary(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class CentreWestBoundary(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class CentreEastBoundary(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


class CentrePointDomain(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgba(self.bot.image.pix[_currentX, _currentY], True)
            old_color = self.bot.canvas.get_color(self.bot.start_x + _currentX, self.bot.start_y + _currentY)
            if old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite and color.rgba[3] > 127:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                if (random.random() < 0.5):
                    _currentX += 1
                else:
                    _currentX += -1
            else:
                if (random.random() < 0.5):
                    _currentY += 1
                else:
                    _currentY += -1

            if _currentX >= self.bot.image.width or _currentY >= self.bot.image.height or _currentX < 0 or _currentY < 0:
                _currentX = _startX
                _currentY = _startY


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
    def build(strategy, bot, colors_ignored, colors_not_overwrite, xreversed, yreversed):

        if strategy == 'randomize':
            return Randomize(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'linear':
            return Linear(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed)
        
        if strategy == 'p_linear':
            return Prioritized_Linear(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed)

        if strategy == 'qf':
            return QuickFill(bot, colors_ignored, colors_not_overwrite, xreversed, yreversed)

        if strategy == 'status':
            return Status(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'sketch':
            return Sketch(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'tlc':
            return TopLeftCorner(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'trc':
            return TopRightCorner(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'blc':
            return BottomLeftCorner(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'brc':
            return BottomRightCorner(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'cnb':
            return CentreNorthBoundary(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'csb':
            return CentreSouthBoundary(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'cwb':
            return CentreWestBoundary(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'ceb':
            return CentreEastBoundary(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'cpd':
            return CentrePointDomain(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'detect':
            return DetectMinTime(bot, colors_ignored, colors_not_overwrite)

        print(I18n.get('not found strategy %s auto selected randomize') % str(strategy))

        return Randomize(bot, colors_ignored, colors_not_overwrite)  # Default strategy
