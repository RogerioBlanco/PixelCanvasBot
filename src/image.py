#!/usr/bin/env python

from PIL import Image as pillow
from colors import EnumColor
import hashlib, os, pyqrcode


class Image(object):
    def __init__(self, file, sens, brig):
        self.sensitive = sens
        self.brightness = brig
        self.checksum = self.md5(file);
        self.image = self.load_image(file)
        self.width, self.height = self.image.size
        self.pix = self.image.load()

    def load_image(self, file):
        tmb_full_path = os.getcwd() + '/img/.cache/' + self.checksum + '.png'

        if (os.path.isfile(tmb_full_path)):
            print "Load cached image"
            return pillow.open(tmb_full_path).convert('RGB')

        print 'generating converted image here : ' + tmb_full_path
        new_image = self.convert_pixels(pillow.open(file).convert('RGB'))
        self.save_image(new_image, tmb_full_path)

        print 'Saved image cache file, Loading Now...'
        return pillow.open(tmb_full_path).convert('RGB')

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # refUrl: https://www.codementor.io/isaib.cicourel/image-manipulation-in-python-du1089j1u

    def save_image(self, image, path):
        image.save(path, 'png')

    # Create a new image with the given size
    def create_image(self, i, j):
        image = pillow.new("RGB", (i, j), "white")
        return image

    def get_pixel(self, image, i, j):
        # Inside image bounds?
        width, height = image.size
        if i > width or j > height:
            return None

        pixel = image.getpixel((i, j))
        return pixel

    def convert_pixels(self, image):
        width, height = image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for j in range(height):
                pixel = self.get_pixel(image, i, j)
                new_color = EnumColor.rgb(pixel, True, self.sensitive, self.brightness)
                pixels[i, j] = (int(new_color.rgb[0]), int(new_color.rgb[1]), int(new_color.rgb[2]))

        return new

    @staticmethod
    def create_QR_image(text, scale):
        full_QR_path = os.getcwd() + '/img/QRcode.png'
        url = pyqrcode.create(text)
        url.png(full_QR_path, scale)
        print('Create QR Code succes in here: ' + full_QR_path)
        print(url.text())