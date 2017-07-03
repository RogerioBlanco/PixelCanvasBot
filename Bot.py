#!/usr/bin/env python

import time, random
from PixelCanvasIO import PixelCanvasIO
from CalcAxis import CalcAxis
from Matrix import Matrix
from Colors import EnumColor

class Bot(object):

    def __init__(self, image, fingerprint, start_x, start_y, mode_defensive, colors_ignored, proxy = None , draw_strategy = 'randomize'):
        self.image = image
        self.start_x = start_x
        self.start_y =  start_y
        self.mode_defensive = mode_defensive
        self.colors_ignored = [EnumColor.index(i) for i in colors_ignored]
        self.draw_strategy = draw_strategy
        self.pixelio = PixelCanvasIO(fingerprint, proxy)


    def run(self):
        self.canvas = self.setup_canvas()

        self.pixelio.connect_websocket(self.canvas)

        me = self.pixelio.myself()

        self.wait_time(me)

        self.draw_image()
        while self.mode_defensive:
            self.draw_image()
            time.sleep(2)

    def draw_image(self):
        if self.draw_strategy == 'row_line':
            for y in xrange(self.image.height):
                for x in xrange(self.image.width):
                    color = EnumColor.rgb(self.image.pix[x,y])
                    if self.canvas.get_color(self.start_x + x, self.start_y + y) != color and not color in self.colors_ignored:
                        response = self.pixelio.send_pixel(self.start_x + x, self.start_y + y, color)
                        while not 'success' in response:
                            print 'Oh no, an error occurred. Trying again.'
                            self.wait_time(response)
                            self.pixelio.send_pixel(self.start_x + x, self.start_y + y, color)

                        self.canvas.update(self.start_x + x, self.start_y + y, color)
                        print 'You painted %s in the %s,%s' % (str(color.name), str(self.start_x + x), str(self.start_y + y))

                        self.wait_time(response)

        if self.draw_strategy == 'randomize':
            #infinity loop
            while True:
                rnd_x = random.randint(self.start_x, self.start_x + self.image.width-1)
                rnd_y = random.randint(self.start_y, self.start_y + self.image.height-1)

                color = EnumColor.rgb(self.image.pix[rnd_x - self.start_x ,rnd_y - self.start_y])
                if self.canvas.get_color(rnd_x, rnd_y) != color and not color in self.colors_ignored:
                    response = self.pixelio.send_pixel(rnd_x, rnd_y, color)
                    while not 'success' in response:
                        print 'Oh no, an error occurred. Trying again.'
                        self.wait_time(response)
                        self.pixelio.send_pixel(rnd_x, rnd_y, color)

                    self.canvas.update(rnd_x, rnd_y, color)
                    print 'You painted %s in the %s,%s' % (str(color.name), str(rnd_x), str(rnd_y))

                    self.wait_time(response)

    def wait_time(self, data = {'waitSeconds':None}):
        if data['waitSeconds'] is not None:
            wait = data['waitSeconds'] + random.randint(0, 9)
            print 'Waiting %s seconds' % str(wait)
            time.sleep(wait)
    
    def setup_canvas(self):
        point_x, point_y = CalcAxis.calc_middle_axis(self.start_x, self.image.width, self.start_y, self.image.height)
        radius = CalcAxis.calc_radius(self.start_x, self.image.width, self.start_y, self.image.height)
        iteration = CalcAxis.calc_iteration(radius)
        axis_x, axis_y = CalcAxis.calc_centers_axis(point_x, point_y)
        canvas = Matrix(iteration, axis_x, axis_y)

        for center_x in xrange(axis_x - iteration, 1 + axis_x + iteration, 15):
            for center_y in xrange(axis_y - iteration, 1 + axis_y + iteration, 15):
                raw = self.pixelio.download_canvas(center_x, center_y)
                index = 0
                for block_y in xrange(center_y - 7, center_y + 8):
                    for block_x in xrange(center_x - 7, center_x + 8):
                        for y in xrange(64):
                            actual_y = (block_y * 64) + y
                            for x in xrange(0, 64, 2):
                                actual_x = (block_x * 64) + x
                                canvas.update(actual_x, actual_y, EnumColor.index(ord(raw[index]) >> 4))
                                canvas.update(actual_x+1, actual_y, EnumColor.index(ord(raw[index]) & 0x0F))
                                index += 1
        return canvas
