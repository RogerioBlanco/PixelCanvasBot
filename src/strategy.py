#!/usr/bin/env python

import time, random
from calc_axis import CalcAxis
from matrix import Matrix
from colors import EnumColor
from i18n import I18n


class Strategy(object):
    def apply(self):
        raise NotImplementedError()


class Randomize(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.size_limit = self.bot.image.width * self.bot.image.height
        self.colors_ignored = colors_ignored

    def apply(self):
        count = 0
        while not self.match(self.bot.canvas, self.bot.image):
            x, y, color = self.roll_dice(self.bot.canvas)
            if self.bot.canvas.get_color(x, y) != color and not color in self.colors_ignored:
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
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y], True)
                if self.bot.canvas.get_color(self.bot.start_x + x,
                                             self.bot.start_y + y) != color and not color in self.colors_ignored:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)


class Sketch(Strategy):
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        # todo make I18N
        print '# From left to right, from top to bottom,'
        near_color = 0;

        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored:
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
                if color != near_color and old_color != color and not color in self.colors_ignored:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        # todo make I18N
        print '# From top to bottom, from left to right,'
        near_color = 0;

        for x in xrange(self.bot.image.width):
            for y in xrange(self.bot.image.height):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0

        # todo make I18N
        print '# From bottom to top, from left to right,'
        near_color = 0;

        for x in xrange(self.bot.image.width):
            for y in reversed(xrange(self.bot.image.height)):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                old_color = self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y)
                if color != near_color and old_color != color and not color in self.colors_ignored:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                near_color = color
            near_color = 0


class Status(Strategy):
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        px_total = self.bot.image.height * self.bot.image.width
        px_ok = 0
        px_not_yet = 0
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x, y])
                px_ok = px_ok + 1
                if self.bot.canvas.get_color(self.bot.start_x + x,
                                             self.bot.start_y + y) != color and not color in self.colors_ignored:
                    px_not_yet = px_not_yet + 1
                    px_ok = px_ok - 1
        print(I18n.get('Total: %s painted: %s Not painted %s') % (str(px_total), str(px_ok), str(px_not_yet)))
        self.bot.wait_time({'waitSeconds': 60})

class TopLeftCorner(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = 0
        _startY = 0

        _endX = self.bot.image.width -1
        _endY = self.bot.image.height -1

        _dirX = 1
        _dirY = 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class TopRightCorner(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = 0

        _endX = 0
        _endY = self.bot.image.height -1

        _dirX = -1
        _dirY = 1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class BottomLeftCorner(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = 0
        _startY = self.bot.image.height -1

        _endX = self.bot.image.width -1
        _endY = 0

        _dirX = 1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class BottomRightCorner(Strategy):
    
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class CentreNorthBoundary(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class CentreSouthBoundary(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class CentreWestBoundary(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class CentreEastBoundary(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY

class CentrePointDomain(Strategy):

    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored

    def apply(self):
        _startX = self.bot.image.width -1
        _startY = self.bot.image.height -1

        _endX = 0
        _endY = 0

        _dirX = -1
        _dirY = -1

        _currentX = _startX
        _currentY = _startY

        while True:

            color = EnumColor.rgb(self.bot.image.pix[_currentX, _currentY], True)
            if self.bot.canvas.get_color(self.bot.start_x + _currentX,
                                         self.bot.start_y + _currentY) != color and not color in self.colors_ignored:
                self.bot.paint(self.bot.start_x + _currentX, self.bot.start_y + _currentY, color)
                _currentX = _startX
                _currentY = _startY

            if (random.random() < 0.5):
                _currentX += _dirX
            else:
                _currentY += _dirY

            if _currentX == _endX or _currentY == _endY:
                _currentX = _startX
                _currentY = _startY


class FactoryStrategy(object):

    @staticmethod
    def build(strategy, bot, colors_ignored):
        if strategy == 'randomize':
            return Randomize(bot, colors_ignored)

        if strategy == 'linear':
            return Linear(bot, colors_ignored)

        if strategy == 'status':
            return Status(bot, colors_ignored)

        if strategy == 'sketch':
            return Sketch(bot, colors_ignored)

        if strategy == 'tlc':
            return TopLeftCorner(bot, colors_ignored)

        if strategy == 'trc':
            return TopRightCorner(bot, colors_ignored)

        if strategy == 'blc':
            return BottomLeftCorner(bot, colors_ignored)

        if strategy == 'brc':
            return BottomRightCorner(bot, colors_ignored)

        if strategy == 'cnb':
            return CentreNorthBoundary(bot, colors_ignored)

        if strategy == 'csb':
            return CentreSouthBoundary(bot, colors_ignored)

        if strategy == 'cwb':
            return CentreWestBoundary(bot, colors_ignored)

        if strategy == 'ceb':
            return CentreEastBoundary(bot, colors_ignored)

        if strategy == 'cpd':
            return CentrePointDomain(bot, colors_ignored)

        return Randomize(bot, colors_ignored)  # Default strategy
