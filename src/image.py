#!/usr/bin/env python

from PIL import Image as pillow
import hashlib, os

class Image(object):
    def __init__(self, file):
        self.checksum = self.md5(file);
        self.image = self.load_image(file)
        self.width, self.height = self.image.size
        self.pix = self.image.load()

    def load_image(self, file):

        if (os.path.isfile(self.checksum)):
            print self.checksum
        if (os.path.isfile(file)):
            print file

        return pillow.open(file).convert('RGB')

    def md5(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()