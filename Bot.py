#!/usr/bin/env python

import PixelCanvasIO

class Bot(object):

    def __init__(self, image, fingerprint, start_x, start_y, mode_defensive, colors_ignored, proxy = None):
        self.image = image
        self.start_x = start_x
        self.start_y =  start_y
        self.mode_defensive = mode_defensive
        self.colors_ignored = colors_ignored
        self.pixelcanvasio = PixelCanvasIO(fingerprint, proxy)

    def run():
        self.canvas = setup_canvas()
        pass

    def setup_canvas():
        center_x, center_y = Axis.get_center_points(self.start_x, self.image.width, self.start_y, self.image.height)
        radius = Axis.calc_radius(self.start_x, self.image.width, self.start_y, self.image.height)

        return None
    def draw_image():
        pass
