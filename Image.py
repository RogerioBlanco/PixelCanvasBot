#!/usr/bin/env python

from PIL import Image as pillow

class Image(object):
    
    def __init__(self, file):
        self.image = self.load_image(file)
        self.width, self.height = self.image.size
        self.pix = self.image.load()

    def load_image(self, file):
        return pillow.open(file).convert('RGB')