#!/usr/bin/env python

import time, random
from sys import stdout as out
from .pixelcanvasio import PixelCanvasIO
from .calc_axis import CalcAxis
from .matrix import Matrix
from .colors import EnumColor
from .strategy import FactoryStrategy
from .i18n import I18n
from six.moves import range


class Bot(object):

    def __init__(self, image, fingerprint, start_x, start_y, stealth, mode_defensive, colors_ignored, colors_not_overwrite, min_range, max_range, proxy=None,
                 draw_strategy='randomize', xreversed=False, yreversed=False):
        self.image = image
        self.start_x = start_x
        self.start_y = start_y
        self.stealth = stealth
        self.mode_defensive = mode_defensive
        self.strategy = FactoryStrategy.build(draw_strategy, self, [EnumColor.index(i) for i in colors_ignored],[EnumColor.index(i) for i in colors_not_overwrite], xreversed, yreversed)
        self.pixelio = PixelCanvasIO(fingerprint, proxy)
        self.print_all_websocket_log = False  # TODO make an argument
        self.min_range = min_range
        self.max_range = max_range
        self.colors_not_overwrite = colors_not_overwrite
        self.xreversed = xreversed
        self.yreversed = yreversed

    def init(self):
        self.canvas = self.setup_canvas()

        interest_area = {'start_x': self.start_x, 'end_x': self.start_x + self.image.width, 'start_y': self.start_y,
                         'end_y': self.start_y + self.image.height}
        self.pixelio.connect_websocket(self.canvas, interest_area, self.print_all_websocket_log)

    def run(self):
        me = self.pixelio.myself()

        self.wait_time(me)

        self.strategy.apply()

        while self.mode_defensive:
            self.strategy.apply()
            time.sleep(2)

    def paint(self, x, y, color):
        response = self.pixelio.send_pixel(x, y, color)
        while not response['success']:
            print(I18n.get('try_again'))
            self.wait_time(response)
            response = self.pixelio.send_pixel(x, y, color)

            self.canvas.update(x, y, color)
        print(I18n.get('You painted %s in the %s,%s') % (I18n.get(str(color.name), 'true'), str(x), str(y)))

        return self.wait_time(response)

    def wait_time(self, data={'waitSeconds': None}):
        def complete(i, wait):
            return ((100 * (float(i) / float(wait))) * 50) / 100

        if data['waitSeconds'] is not None:
            wait = data['waitSeconds']
            if self.stealth:
                wait += 0.33 + random.random()
            else:
                wait -= 2
            print(I18n.get('Waiting %s seconds') % str(wait))

            c = i = 0
            while c < 50:
                c = complete(i, wait)
                time.sleep(wait - i if i == int(wait) else 1)
                out.write("[{}]\0\r".format('+' * int(c) + '-' * (50 - int(c))))
                out.flush()
                i += 1
            out.write("\n")
            out.flush()
            return data['waitSeconds']
        return 99999999

    def setup_canvas(self):
        point_x, point_y = CalcAxis.calc_middle_axis(self.start_x, self.image.width, self.start_y, self.image.height)
        radius = CalcAxis.calc_radius(self.start_x, self.image.width, self.start_y, self.image.height)
        iteration = CalcAxis.calc_iteration(radius)
        axis_x, axis_y = CalcAxis.calc_centers_axis(point_x, point_y)
        canvas = Matrix(iteration, axis_x, axis_y)

        for center_x in range(axis_x, axis_x + iteration, 15):
            for center_y in range(axis_y, axis_y + iteration, 15):
                raw = self.pixelio.download_canvas(center_x, center_y)
                index = 0
                for block_y in range(center_y - 7, center_y + 8):
                    for block_x in range(center_x - 7, center_x + 8):
                        for y in range(64):
                            actual_y = (block_y * 64) + y
                            for x in range(0, 64, 2):
                                actual_x = (block_x * 64) + x
                                canvas.update(actual_x, actual_y, EnumColor.index(raw[index] >> 4))
                                canvas.update(actual_x + 1, actual_y, EnumColor.index(raw[index] & 0x0F))
                                index += 1

        return canvas
