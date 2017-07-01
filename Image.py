#!/usr/bin/env python

import PIL

class Image(object):
    
    def __init__(self, file):
        self.image = self.load_image(file)
        self.width, self.height = self.image.size
        self.pix = pix

    def load_image(file):
        return PIL.Image.open(file).convert('RGB')