#!/usr/bin/env python

import time, random, math
from calc_axis import CalcAxis
from matrix import Matrix
from colors import EnumColor
from i18n import I18n


class Strategy(object):
    def apply(self):
        raise NotImplementedError()


class Randomize(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.size_limit = self.bot.image.width * self.bot.image.height
        self.colors_ignored = colors_ignored

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        count = 0
        while not self.match(self.bot.canvas, self.bot.image):
            x, y, color = self.roll_dice(self.bot.canvas)
            if self.bot.canvas.get_color(x,
                                         y) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                x, y) not in self.colors_not_overwrite:
                self.bot.paint(x, y, color)
            count += 1

    def roll_dice(self, canvas):
        rnd_x = rnd_y = color = None
        while all(v is None for v in [rnd_x, rnd_y, color]) or canvas.get_color(rnd_x, rnd_y) == color:
            rnd_x = self.random(self.bot.start_x, self.bot.start_x + self.bot.image.width - 1)
            rnd_y = self.random(self.bot.start_y, self.bot.start_y + self.bot.image.height - 1)
            color = EnumColor.rgb(self.bot.image.pix[rnd_x - self.bot.start_x, rnd_y - self.bot.start_y], True)
        color = EnumColor.rgb(self.bot.image.pix[rnd_x - self.bot.start_x, rnd_y - self.bot.start_y])
        return rnd_x, rnd_y, color

    def random(self, start, end):
        return random.randint(start, end)

    def match(self, canvas, image):
        for x in xrange(0, image.width):
            for y in xrange(0, image.height):
                if canvas.get_color(x + self.bot.start_x, y + self.bot.start_y) != EnumColor.rgb(
                        self.bot.image.pix[x, y], True):
                    return False
        return True


class Linear(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y], True)
                if self.bot.canvas.get_color(self.bot.start_x + x,
                                             self.bot.start_y + y) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                    self.bot.start_x + x,
                    self.bot.start_y + y) not in self.colors_not_overwrite:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)


class Sketch(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        # todo make I18N
        print '# From left to right, from top to bottom,'
        near_color = 0

        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        # todo make I18N
        print '# From right to left, from top to bottom,'
        near_color = 0

        for y in xrange(self.bot.image.height):
            for x in reversed(xrange(self.bot.image.width)):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        # todo make I18N
        print '# From top to bottom, from left to right,'
        near_color = 0

        for x in xrange(self.bot.image.width):
            for y in xrange(self.bot.image.height):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        # todo make I18N
        print '# From bottom to top, from left to right,'
        near_color = 0

        for x in xrange(self.bot.image.width):
            for y in reversed(xrange(self.bot.image.height)):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored and old_color not in self.colors_not_overwrite:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0


class Status(Strategy):
    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        px_total = self.bot.image.height * self.bot.image.width
        px_ok = 0
        px_not_yet = 0
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                px_ok = px_ok + 1
                if self.bot.canvas.get_color(self.bot.start_x + x,
                                             self.bot.start_y + y) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                    self.bot.start_x + x,
                    self.bot.start_y + y) not in self.colors_not_overwrite:
                    px_not_yet = px_not_yet + 1
                    px_ok = px_ok - 1
        print(I18n.get('Total: %s painted: %s Not painted %s') % (str(px_total), str(px_ok), str(px_not_yet)))
        self.bot.wait_time({'waitSeconds': 60})


class TopLeftCorner(Strategy):

    def __init__(self, bot, colors_ignored, colors_not_overwrite):
        self.bot = bot
        self.colors_ignored = colors_ignored

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = 0

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = self.bot.image.height - 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = 0
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = self.bot.image.width - 1
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
        self.colors_not_overwrite = colors_not_overwrite

    def apply(self):
        _startX = int(math.floor((self.bot.image.width - 1) / 2))
        _startY = int(math.floor((self.bot.image.height - 1) / 2))

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored and self.bot.canvas.get_color(
                self.bot.start_x + _currentX,
                self.bot.start_y + _currentY) not in self.colors_not_overwrite:
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

        # todo Need Tester
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
    def build(strategy, bot, colors_ignored, colors_not_overwrite):

        if strategy == 'randomize':
            return Randomize(bot, colors_ignored, colors_not_overwrite)

        if strategy == 'linear':
            return Linear(bot, colors_ignored, colors_not_overwrite)

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

        #todo make I18N
        print('not fonud strategy "' + strategy + '" auto selected randomize')
        return Randomize(bot, colors_ignored, colors_not_overwrite)  # Default strategy
