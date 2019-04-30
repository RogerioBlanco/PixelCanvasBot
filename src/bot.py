import datetime
import logging
import random
import threading
import time

from colorama import Fore
from six.moves import range

from .calc_axis import CalcAxis
from .colors import EnumColor
from .i18n import I18n
from .matrix import Matrix
from .pixelcanvasio import PixelCanvasIO
from .strategy import FactoryStrategy

logger = logging.getLogger('bot')


class Bot(object):
    def __init__(self, image, fingerprint, start_x, start_y, mode_defensive,
                 colors_ignored, colors_not_overwrite, min_range, max_range,
                 point_x, point_y, proxy=None, draw_strategy='randomize',
                 xreversed=False, yreversed=False, prioritized=False,
                 notify=False):
        self.pixel_intent = ()  # Where the bot is currently trying to paint
        self.image = image
        self.start_x = start_x
        self.start_y = start_y
        self.notify = notify
        self.mode_defensive = mode_defensive
        self.colors_ignored = [EnumColor.index(i) for i in colors_ignored]
        if point_x is None:
            self.point_x = random.randrange(start_x, start_x + image.width, 1)
        else:
            self.point_x = point_x
        if point_y is None:
            self.point_y = random.randrange(start_y, start_y + image.height, 1)
        else:
            self.point_y = point_y
        self.strategy = FactoryStrategy.build(
            draw_strategy, self, self.colors_ignored,
            [EnumColor.index(i) for i in colors_not_overwrite],
            xreversed, yreversed, self.point_x, self.point_y, prioritized)
        self.pixelio = PixelCanvasIO(fingerprint, proxy, self, notify)
        self.print_all_websocket_log = False  # TODO make an argument
        self.min_range = min_range
        self.max_range = max_range
        self.colors_not_overwrite = colors_not_overwrite
        self.xreversed = xreversed
        self.yreversed = yreversed
        self.prioritized = prioritized
        self.paint_lag = 0
        self.wait_delta = -2

    def get_delta(self):
        return self.wait_delta - self.paint_lag / 2

    def init(self):
        self.canvas = self.setup_canvas()

        interest_area = {'start_x': self.start_x,
                         'end_x': self.start_x + self.image.width,
                         'start_y': self.start_y,
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
        start = time.time()
        response = self.pixelio.send_pixel(x, y, color)
        end = time.time()
        self.paint_lag = end - start
        while not response['success']:
            logger.debug(I18n.get('error.try_again'))
            self.wait_time(response)
            # Redeclare intent after a timer
            self.pixel_intent = (x, y, color.index)
            response = self.pixelio.send_pixel(x, y, color)

        self.canvas.update(x, y, color)
        logger.debug(I18n.get('paint.user', color=Fore.CYAN).format(
            color=I18n.get(str(color.name), inline=True, end=None), x=x, y=y))
        return self.wait_time(response)

    def wait_time(self, data={'waitSeconds': None}):

        bar_width = 50  # keep this less than 66

        # Print timer progress
        def print_progress_bar(iteration, total, prefix='', suffix='',
                               length=100, fill='█'):
            filled_length = int(length * iteration / total)
            bar = fill * filled_length + '-' * (length - filled_length)
            print('%s|%s| %.2f %s'
                  % (prefix, bar, round(total - iteration, 2), suffix)
                  + (4 * ' '), end='\r', flush=True)

        if data['waitSeconds'] is not None and data['waitSeconds'] > 0:
            # no delta if wait error
            if 'errors' in data and {'msg': 'You must wait'} in data['errors']:
                wait = data['waitSeconds']
                logger.debug(I18n.get('error.cooldown'))
            # apply delta
            else:
                mod_time = data['waitSeconds'] + self.get_delta()
                wait = mod_time if mod_time > 0 else data['waitSeconds']

            formattedWait = str(datetime.timedelta(seconds=int(wait)))
            formattedWait = formattedWait[2:]
            if wait > 60:
                logger.debug(I18n.get('paint.waitmin')
                             .format(time=formattedWait))
            else:
                logger.debug(I18n.get('paint.waitsec')
                             .format(time=formattedWait))

            # initial bar
            print_progress_bar(0, wait, prefix='', suffix='Seconds',
                               length=bar_width)
            # update at 0.1 second intervals
            full = range(int(float(wait) / 0.1))
            for i in full:
                time.sleep(0.1)
                # Update Progress Bar
                print_progress_bar(float(i) * 0.1, wait, prefix='',
                                   suffix='Seconds', length=bar_width)
            # wait for whatever remains
            remaining_time = wait - len(full) * 0.1
            time.sleep(remaining_time)
            print_progress_bar(wait, wait, prefix='', suffix='Seconds',
                               length=bar_width)

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
        # Block coordinates of the center of the template,
        # offset to the block grid
        axis = CalcAxis.calc_centers_axis(middle_x, middle_y)
        center_block_x, center_block_y, offset_x, offset_y = axis
        if offset_x != 0:
            end = (center_block_x + offset_x + num_blocks) * 64
            logger.debug(I18n.get('chunk.blind.east').format(x=end))
        if offset_y != 0:
            end = (center_block_y + offset_y + num_blocks) * 64
            logger.debug(I18n.get('chunk.blind.south').format(y=end))
        canvas = Matrix(num_blocks, center_block_x, center_block_y)

        threads = []
        for center_x in range(center_block_x - num_blocks,
                              1 + center_block_x + num_blocks, 15):
            for center_y in range(center_block_y - num_blocks,
                                  1 + center_block_y + num_blocks, 15):
                logger.debug(I18n.get('chunk.load').format(x=center_x,
                                                           y=center_y))
                threads.append(threading.Thread(
                    target=update_canvas,
                    args=(self.pixelio, canvas, center_x, center_y)))
                threads[-1].setDaemon(True)
                threads[-1].start()
        for thread in threads:
            thread.join()

        return canvas
