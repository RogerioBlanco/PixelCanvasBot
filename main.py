#!/usr/bin/env python

import logging
import logging.handlers
import os
from argparse import ArgumentParser

from src.bot import Bot
from src.custom_exception import *
from src.i18n import I18n
from src.image import Image

logger = logging.getLogger('bot')

try:
    # Python 2
    input = raw_input
except:
    # Python 3
    pass


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--image', required=True, dest='file',
                        help=I18n.get('--image', True))
    parser.add_argument('-f', '--fingerprint', required=True, dest='fingerprint',
                        help=I18n.get('--fingerprint', True))
    parser.add_argument('-x', '--start_x', required=True, type=int, dest='start_x',
                        help=I18n.get('--start_x', True))
    parser.add_argument('-y', '--start_y', required=True, type=int, dest='start_y',
                        help=I18n.get('--start_y', True))
    parser.add_argument('-ci', '--colors_ignored', required=False, type=int, default=[], nargs='+', dest='colors_ignored',
                        help=I18n.get('--colors_ignored', True))
    parser.add_argument('-cno', '--colors_not_overwrite', required=False, type=int, default=[], nargs='+', dest='colors_not_overwrite',
                        help=I18n.get('--colors_not_overwrite', True))
    parser.add_argument('-ds', '--draw_strategy', required=False, default='spiral', dest='draw_strategy',
                        help=I18n.get('--draw_strategy', True))
    parser.add_argument('--mode_defensive', required=False, default=True, dest='mode_defensive',
                        help=I18n.get('--mode_defensive', True))
    parser.add_argument('--proxy_url', required=False, dest='proxy_url',
                        help=I18n.get('--proxy_url', True))
    parser.add_argument('--proxy_auth', required=False, dest='proxy_auth',
                        help=I18n.get('--proxy_auth', True))
    parser.add_argument('--round_sensitive', required=False, type=int, default=3, dest='round_sensitive',
                        help=I18n.get('--round_sensitive', True))
    parser.add_argument('--image_brightness', required=False, type=int, default=15, dest='image_brightness',
                        help=I18n.get('--image_brightness', True))
    parser.add_argument('--detect_area_min_range', required=False, type=int, default=-5000, dest='min_range',
                        help=I18n.get('--detect_area_min_range', True))
    parser.add_argument('--detect_area_max_range', required=False, type=int, default=5000, dest='max_range',
                        help=I18n.get('--detect_area_max_range', True))
    parser.add_argument('--QR_text', required=False, default="", dest='QR_text',
                        help=I18n.get('--QR_text', True))
    parser.add_argument('--QR_scale', required=False, type=int, default=3, dest='QR_scale',
                        help=I18n.get('--QR_scale', True))
    parser.add_argument('--xreversed', required=False, default=False, dest='xreversed',
                        help=I18n.get('--xreversed', True))
    parser.add_argument('--yreversed', required=False, default=False, dest='yreversed',
                        help=I18n.get('--yreversed', True))
    parser.add_argument('-px', '--point_x', required=False, type=int, default=None, dest='point_x',
                        help=I18n.get('--point_x', True))
    parser.add_argument('-py', '--point_y', required=False, type=int, default=None, dest='point_y',
                        help=I18n.get('--point_y', True))
    parser.add_argument('-p', '--prioritized', required=False, default=False, dest='prioritized',
                        help=I18n.get('--yreversed', True))
    parser.add_argument('-n', '--notify', required=False, default=False,
                        dest='notify', action='store_true', help=I18n.get('--notify', True))
    parser.add_argument('-o', '--output_file', required=False, default='logfile.log',
                        dest='log_file', help=I18n.get('--output_file', True))

    return parser.parse_args()


def setup_proxy(proxy_url, proxy_auth):
    if proxy_auth is None:
        proxy_auth = ''
    if proxy_url and proxy_auth:
        proxy_auth = proxy_auth + '@'

    if proxy_url:
        return {'http': 'http://%s%s' % (proxy_auth, proxy_url)}

    return None


def alert(message=''):
    print(('\a' * 5) + message)


def main():
    args = parse_args()
    if args.colors_ignored.count(16) == 0:
        args.colors_ignored.append(16)

    proxy = setup_proxy(args.proxy_url, args.proxy_auth)

    if not args.QR_text == "":
        args.file = "./img/QRcode.png"
        Image.create_QR_image(args.QR_text, args.QR_scale)

    # Setup file log.
    file_formatter = logging.Formatter('%(message)s')
    # Clear line first to prevent issues with the timer
    stream_formatter = logging.Formatter(80 * ' ' + '\r' + '%(message)s')
    logfile = os.path.join(os.getcwd(), "log", args.log_file)
    filehandler = logging.handlers.RotatingFileHandler(logfile,
                                                       maxBytes=8*1024*1024,
                                                       backupCount=5)
    filehandler.setFormatter(file_formatter)
    logger.addHandler(filehandler)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(stream_formatter)
    logger.addHandler(streamhandler)
    logger.setLevel(logging.DEBUG)

    image = Image(args.file, args.round_sensitive, args.image_brightness)

    bot = Bot(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive, args.colors_ignored, args.colors_not_overwrite, args.min_range, args.max_range, args.point_x, args.point_y, proxy,
              args.draw_strategy, args.xreversed, args.yreversed, args.prioritized, args.notify)

    bot.init()

    def run():
        try:
            bot.run()
        except NeedUserInteraction as exception:
            alert(str(exception))
            if input(I18n.get('paint.has_painted')).lower().strip() == 'y':
                run()

    run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.debug(I18n.get('exit'))
