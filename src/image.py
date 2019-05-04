import hashlib
import logging
import os

from PIL import Image as pillow

import pyqrcode

from .colors import EnumColor
from .i18n import I18n

logger = logging.getLogger('bot')


class Image(object):
    def __init__(self, file, sens, brig):
        self.sensitive = sens
        self.brightness = brig
        self.checksum = self.md5(file)
        self.image = self.load_image(file)
        self.width, self.height = self.image.size
        self.pix = self.image.load()

    def load_image(self, file):
        tmb_full_path = os.getcwd() + '/img/.cache/' + self.checksum + '.png'

        if (os.path.isfile(tmb_full_path)):
            logger.info(I18n.get('external.load_cache'))
            return pillow.open(tmb_full_path).convert('RGBA')

        logger.info(I18n.get('external.generating').format(
            path=tmb_full_path))

        new_image = self.convert_pixels(pillow.open(file).convert('RGBA'))
        self.save_image(new_image, tmb_full_path)

        logger.info(I18n.get('external.saved_cache'))
        return pillow.open(tmb_full_path).convert('RGBA')

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
        image = pillow.new("RGBA", (i, j), "white")
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
                new_color = EnumColor.rgba(
                    pixel, True, self.sensitive, self.brightness)
                pixels[i, j] = (int(new_color.rgba[0]), int(new_color.rgba[1]), int(
                    new_color.rgba[2]), int(new_color.rgba[3]))

        return new

    @staticmethod
    def create_QR_image(text, scale):
        full_QR_path = os.getcwd() + '/img/QRcode.png'
        url = pyqrcode.create(text)
        url.png(full_QR_path, scale)

        logger.info(I18n.get('qr_created').format(path=full_QR_path))
        logger.info(url.text())
