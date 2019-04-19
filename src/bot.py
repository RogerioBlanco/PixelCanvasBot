#!/usr/bin/env python

import logging
import random
import threading
import time
from sys import stdout as out

from six.moves import range

from .calc_axis import CalcAxis
from .colors import EnumColor
from .i18n import I18n
from .matrix import Matrix
from .pixelcanvasio import PixelCanvasIO
from .strategy import FactoryStrategy

logger = logging.getLogger('bot')


class Bot(object):
    def __init__(self, image, fingerprint, start_x, start_y, mode_defensive, colors_ignored, colors_not_overwrite, min_range, max_range, point_x, point_y, proxy=None,
                 draw_strategy='randomize', xreversed=False, yreversed=False, prioritized=False, notify=False):
        self.pixel_intent = ()  # Where the bot is currently trying to paint
        self.image = image
        self.start_x = start_x
        self.start_y = start_y
        self.notify = notify
        self.mode_defensive = mode_defensive
        self.colors_ignored = [EnumColor.index(i) for i in colors_ignored]
        if point_x == None:
            self.point_x = random.randrange(start_x, start_x + image.width, 1)
        else:
            self.point_x = point_x
        if point_y == None:
            self.point_y = random.randrange(start_y, start_y + image.height, 1)
        else:
            self.point_y = point_y
        self.strategy = FactoryStrategy.build(draw_strategy, self, self.colors_ignored, [EnumColor.index(
            i) for i in colors_not_overwrite], xreversed, yreversed, self.point_x, self.point_y, prioritized)
        self.pixelio = PixelCanvasIO(fingerprint, proxy, self, notify)
        self.print_all_websocket_log = False  # TODO make an argument
        self.min_range = min_range
        self.max_range = max_range
        self.colors_not_overwrite = colors_not_overwrite
        self.xreversed = xreversed
        self.yreversed = yreversed
        self.prioritized = prioritized
        self.prioritized = prioritized

    def init(self):
        self.canvas = self.setup_canvas()

        interest_area = {'start_x': self.start_x, 'end_x': self.start_x + self.image.width, 'start_y': self.start_y,
                         'end_y': self.start_y + self.image.height}
        self.pixelio.connect_websocket(
            self.canvas, interest_area, self.print_all_websocket_log)

    def run(self):
        me = self.pixelio.myself()

        self.wait_time(me)

        self.strategy.apply()

        while self.mode_defensive:
            self.strategy.apply()
            time.sleep(2)

    def paint(self, x, y, color):
        self.pixel_intent = (x, y, color.index)
        response = self.pixelio.send_pixel(x, y, color)
        while not response['success']:
            logger.debug(I18n.get('error.try_again'))
            self.wait_time(response)
            # Redeclare intent after a timer
            self.pixel_intent = (x, y, color.index)
            response = self.pixelio.send_pixel(x, y, color)

            self.canvas.update(x, y, color)
        logger.debug(I18n.get('paint.user').format(
            color=I18n.get(str(color.name), 'true'), x=x, y=y))
        return self.wait_time(response)

    def wait_time(self, data={'waitSeconds': None}):
        def complete(i, wait):
            return ((100 * (float(i) / float(wait))) * 50) / 100

        if data['waitSeconds'] is not None:
            wait = data['waitSeconds'] + (random.randint(2, 4) / 3.33)
            logger.debug(I18n.get('paint.wait').format(seconds=round(wait, 2)))

            c = i = 0
            while c < 50:
                c = complete(i, wait)
                time.sleep(wait - i if i == int(wait) else 1)
                out.write("[{}]\0\r".format(
                    '+' * int(c) + '-' * (50 - int(c))))
                out.flush()
                i += 1
            out.write("\n")
            out.flush()
            # Clear intent so 3rd party updates are logged.
            self.pixel_intent = ()
            return data['waitSeconds']

        self.pixel_intent = ()
        return 99999999

    def setup_canvas(self):
        def update_canvas(pixelio, canvas, center_x, center_y):
            raw = pixelio.download_canvas(center_x, center_y)
            index = 0
            for block_y in range(center_y - 7, center_y + 8):
                for block_x in range(center_x - 7, center_x + 8):
                    for y in range(64):
                        actual_y = (block_y * 64) + y
                        for x in range(0, 64, 2):
                            actual_x = (block_x * 64) + x

                            canvas.update(actual_x, actual_y,
                                          EnumColor.index(raw[index] >> 4))
                            canvas.update(actual_x + 1, actual_y,
                                          EnumColor.index(raw[index] & 0x0F))
                            index += 1

        # Coordinates of the middle pixel of the template
        middle_x, middle_y = CalcAxis.calc_middle_axis(
            self.start_x, self.image.width, self.start_y, self.image.height)
        # Number of chunks we need to load in any direction
        max_chunks = CalcAxis.calc_max_chunks(
            self.image.width, self.image.height)
        # Number of blocks spanned by the chunks we need
        num_blocks = CalcAxis.calc_num_blocks(max_chunks)
        # Block coordinates of the center of the template, offset to the block grid
        center_block_x, center_block_y, offset_x, offset_y = CalcAxis.calc_centers_axis(
            middle_x, middle_y)
        if offset_x is not 0:
            end = (center_block_x + offset_x + num_blocks) * 64
            logger.debug(I18n.get('chunk.blind.east').format(x=end))
        if offset_y is not 0:
            end = (center_block_y + offset_y + num_blocks) * 64
            logger.debug(I18n.get('chunk.blind.south').format(y=end))
        canvas = Matrix(num_blocks, center_block_x, center_block_y)

        threads = []
        for center_x in range(center_block_x - num_blocks, 1 + center_block_x + num_blocks, 15):
            for center_y in range(center_block_y - num_blocks, 1 + center_block_y + num_blocks, 15):
                logger.debug(I18n.get('chunk.load').format(
                    x=center_x, y=center_y))
                threads.append(threading.Thread(target=update_canvas, args=(
                    self.pixelio, canvas, center_x, center_y)))
                threads[-1].setDaemon(True)
                threads[-1].start()
        for thread in threads:
            thread.join()

        return canvas
