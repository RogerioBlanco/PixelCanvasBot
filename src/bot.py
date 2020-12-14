#!/usr/bin/env python

import time, random, math
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
        try:
            self.canvas.update(x,y, color)
            print(I18n.get('You painted %s in the %s,%s') % (I18n.get(str(color.name), 'true'), str(x), str(y)))
        except Exception as e:
            print("Exception during paiting occured", e)
            pass

        return self.wait_time(response)

    def wait_time(self, data={'waitSeconds': None}):
        def complete(i, wait):
            return ((100 * (float(i) / float(wait))) * 50) / 100

        if data['waitSeconds'] is not None:
            wait = data['waitSeconds']
            if self.stealth:
                if random.random() > 0.2:
                    h1 = wait * random.random() / 5
                    wait += h1
                if random.random() > 0.82:
                    h2 = wait * random.random()/10
                    h3 = 3 + (random.random() * 30)
                    wait += h2 + h3
                if random.random() > 0.98:
                    h4 = 15 + (random.random() * 150)
                    wait += h4
                if random.random() > 0.99:
                    h5 = 15 + (random.random() * 250)
                    wait += h5
            elif wait > 2:
                wait -= 2

            h0 = 0.11 + random.random() # Human reaction
            wait += h0

            niceWait = math.floor(wait*1000)/1000
            print(I18n.get('Waiting %s seconds') % str(niceWait))

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
        x = self.start_x
        y = self.start_y
        w = self.image.width
        h = self.image.height

        canvas = Matrix(x, y, w, h)

        wc = (x + w + 448) // 960
        hc = (y + h + 448) // 960
        xc = (x + 448) // 960
        yc = (y + 448) // 960
        for iy in range(yc, hc + 1):
            for ix in range(xc, wc + 1):
                data = self.pixelio.download_canvas(ix * 15, iy * 15)
                i = 0
                off_x = ix * 960 - 448
                off_y = iy * 960 - 448
                for b in data:
                    tx = off_x + ((i // (64 * 64))  % 15) * 64 + (i % (64 * 64)) % 64
                    ty = off_y + i // (64 * 64 * 15) * 64 + (i % (64 * 64)) // 64
                    c = b >> 4
                    canvas.update(tx, ty, EnumColor.index(c))
                    i += 1
                    tx = off_x + ((i // (64 * 64))  % 15) * 64 + (i % (64 * 64)) % 64
                    ty = off_y + i // (64 * 64 * 15) * 64 + (i % (64 * 64)) // 64
                    c = b & 0xF
                    canvas.update(tx, ty, EnumColor.index(c))
                    i += 1
                #print("Got chunk with " + str(i) + " pixels", "PixelCanvasGetter")
        return canvas
