import logging
import random

from colorama import Fore
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
        self.recently_changed = []

    def pixels(self):
        raise NotImplementedError()

    def _template_is_done(self):
        for x in self.x_range:
            for y in self.y_range:
                color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                if self.canvas.get_color(x, y) != color and color.alpha > 0:
                    return False
        return True

    def _next_pixel(self):
        for pixel in self.priorities:
            old_pixel = (pixel[0], pixel[1], self.canvas.get_color(pixel[0], pixel[1]))
            if pixel != old_pixel:
                return pixel

    def _next_recent(self):
        for pixel in self.recently_changed:
            self.recently_changed.remove(pixel)
            old_pixel = (pixel[0], pixel[1], self.canvas.get_color(pixel[0], pixel[1]))
            if pixel != old_pixel:
                return pixel

    def _should_replace(self, old_color, new_color):
        return new_color not in self.colors_ignored \
            and old_color not in self.colors_not_overwrite \
            and new_color.alpha > 0

    def change_detected(self, x, y):
        for pixel in self.priorities:
            if pixel[0] == x and pixel[1] == y:
                self.recently_changed.reverse()
                self.recently_changed.append(pixel)
                self.recently_changed.reverse()
                return


class Randomize(Strategy):
    def pixels(self):
        if self.priorities == []:
            for y in self.y_range:
                for x in self.x_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            random.shuffle(self.priorities)
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


class Linear(Strategy):
    def pixels(self):
        if self.priorities == []:
            for y in self.y_range:
                for x in self.x_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


class LinearVertical(Strategy):
    def pixels(self):
        if self.priorities == []:
            for x in self.x_range:
                for y in self.y_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


class QuickFill(Strategy):
    def pixels(self):
        if self.priorities == []:
            for is_even in (True, False):
                for y in self.y_range:
                    for x in self.x_range:
                        color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                        old_color = self.canvas.get_color(x, y)
                        if self._should_replace(old_color, color):
                            if (x % 2 == is_even):
                                self.priorities.append((x, y, color))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


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

        while not self._template_is_done():
            self.bot.paint(*self.scan_canvas())
        self.bot.wait_time({'waitSeconds': 20})


class Status(Strategy):
    def run(self):
        px_total = self.image.height * self.image.width
        correct_px = 0
        ignored = 0
        for y in self.y_range:
            for x in self.x_range:
                template_color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y])
                canvas_color = self.canvas.get_color(x, y)

                # Account for ignored pixels
                if template_color in self.colors_ignored \
                        or canvas_color in self.colors_not_overwrite \
                        or template_color.alpha == 0:
                    ignored += 1

                # Count as correct if not ignored, and if design matches canvas
                if self._should_replace(canvas_color, template_color) \
                        and canvas_color == template_color:
                    correct_px += 1

        px_active_total = px_total - ignored
        incorrect_px = px_active_total - correct_px
        progress = round(float(correct_px) / px_active_total * 100., 2)

        logger.debug(I18n.get('progress').format(total=px_active_total, correct=correct_px, incorrect=incorrect_px, progress=progress))
        return progress


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
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            random.shuffle(self.priorities)
            self.priorities.sort(key=lambda priorities: ((priorities[0] - self.px) ** 2 + (priorities[1] - self.py) ** 2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


class Spiral(Strategy):
    def __init__(self, *args, **kwargs):
        self.px = kwargs["px"]
        self.py = kwargs["py"]
        super().__init__(*args)

        if self.px <= self.start_x:
            self.leftx_range = []
            self.rightx_range = range(self.start_x, self.start_x + self.image.width)
        elif self.px < self.start_x + self.image.width:
            self.leftx_range = range(self.start_x, self.px)
            self.rightx_range = range(self.px, self.start_x + self.image.width)
        else:
            self.leftx_range = range(self.start_x, self.start_x + self.image.width)
            self.rightx_range = []

        if self.py <= self.start_y:
            self.topy_range = []
            self.bottomy_range = range(self.start_y, self.start_y + self.image.height)
        elif self.py < self.start_y + self.image.height:
            self.topy_range = range(self.start_y, self.py)
            self.bottomy_range = range(self.py, self.start_y + self.image.height)
        else:
            self.topy_range = range(self.start_y, self.start_y + self.image.height)
            self.bottomy_range = []

    def pixels(self):
        if self.priorities == []:
            for y in self.topy_range:
                for x in self.rightx_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            for x in reversed(self.rightx_range):
                for y in self.bottomy_range:
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            for y in reversed(self.bottomy_range):
                for x in reversed(self.leftx_range):
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            for x in self.leftx_range:
                for y in reversed(self.topy_range):
                    color = EnumColor.rgba(self.image.pix[x - self.start_x, y - self.start_y], True)
                    old_color = self.canvas.get_color(x, y)
                    if self._should_replace(old_color, color):
                        self.priorities.append((x, y, color))
            self.priorities.sort(key=lambda priorities: ((priorities[0] - self.px) ** 2 + (priorities[1] - self.py) ** 2))
            if self.prioritized:
                self.priorities.sort(reverse=True, key=lambda priorities: priorities[2].alpha)
        while not self._template_is_done():
            if self.recently_changed != []:
                yield self._next_recent()
            else:
                yield self._next_pixel()


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
                                  colors_not_overwrite, prioritized, xreversed,
                                  yreversed)

        if strategy == 'qf':
            return QuickFill(bot.canvas, bot.image, bot.start_x, bot.start_y,
                             colors_ignored, colors_not_overwrite, prioritized,
                             xreversed, yreversed)

        if strategy == 'status':
            return Status(bot.canvas, bot.image, bot.start_x, bot.start_y,
                          colors_ignored, colors_not_overwrite)

        if strategy == 'sketch':
            logger.error(I18n.get('strategy.sketch_is_dead', color=Fore.RED))
            exit()
            # return Sketch(bot, colors_ignored, colors_not_overwrite, prioritized)

        if strategy == 'radiate':
            return Radiate(bot.canvas, bot.image, bot.start_x,
                           bot.start_y, colors_ignored, colors_not_overwrite,
                           prioritized, px=px, py=py)

        if strategy == 'spiral':
            return Spiral(bot.canvas, bot.image, bot.start_x, bot.start_y,
                          colors_ignored, colors_not_overwrite, prioritized,
                          px=px, py=py)

        if strategy == 'tlc':
            px = bot.start_x
            py = bot.start_y
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'trc':
            px = bot.start_x + bot.image.width - 1
            py = bot.start_y
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'blc':
            px = bot.start_x
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'brc':
            px = bot.start_x + bot.image.width - 1
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'cnb':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = bot.start_y
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'csb':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = bot.start_y + bot.image.height - 1
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'cwb':
            px = bot.start_x
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'ceb':
            px = bot.start_x + bot.image.width - 1
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        if strategy == 'cpd':
            px = (2 * bot.start_x + bot.image.width) // 2
            py = (2 * bot.start_y + bot.image.height) // 2
            return Radiate(bot.canvas, bot.image, bot.start_x, bot.start_y,
                           colors_ignored, colors_not_overwrite, prioritized,
                           px=px, py=py)

        print(I18n.get('strategy.auto_select').format(strategy=strategy))

        return Spiral(bot.canvas, bot.image, bot.start_x, bot.start_y,
                    colors_ignored, colors_not_overwrite, prioritized,
                    px=px, py=py)
