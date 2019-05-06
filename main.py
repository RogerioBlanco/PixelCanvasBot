#!/usr/bin/env python3

import logging
import logging.handlers
import os
from argparse import ArgumentParser
import re
import sys

from colorama import Fore

from src.bot import Bot
from src.custom_exception import NeedUserInteraction
from src.i18n import I18n
from src.image import Image

logger = logging.getLogger('bot')
bar_print = logging.getLogger('loading_bar')


class FileFilter(logging.Filter):
    def filter(self, record):
        # Remove ANSI codes
        record.nocolor = re.sub('\x1b\\[[0-9;]*m', '', record.getMessage())
        # Add level tags
        if record.levelno == logging.WARNING:
            record.nocolor += ' [WARNING]'
        elif record.levelno == logging.ERROR:
            record.nocolor += ' [ERROR]'
        return True


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--image', required=True, dest='file',
                        help=I18n.get('--image'))
    parser.add_argument('-f', '--fingerprint', required=True, dest='fingerprint',
                        help=I18n.get('--fingerprint'))
    parser.add_argument('-x', '--start_x', required=True, type=int, dest='start_x',
                        help=I18n.get('--start_x'))
    parser.add_argument('-y', '--start_y', required=True, type=int, dest='start_y',
                        help=I18n.get('--start_y'))
    parser.add_argument('-ci', '--colors_ignored', required=False, type=int, default=[], nargs='+', dest='colors_ignored',
                        help=I18n.get('--colors_ignored'))
    parser.add_argument('-cno', '--colors_not_overwrite', required=False, type=int, default=[], nargs='+', dest='colors_not_overwrite',
                        help=I18n.get('--colors_not_overwrite'))
    parser.add_argument('-ds', '--draw_strategy', required=False, default='spiral', dest='draw_strategy',
                        help=I18n.get('--draw_strategy'))
    parser.add_argument('--mode_defensive', required=False, default=True, dest='mode_defensive',
                        help=I18n.get('--mode_defensive'))
    parser.add_argument('--proxy_url', required=False, dest='proxy_url',
                        help=I18n.get('--proxy_url'))
    parser.add_argument('--proxy_auth', required=False, dest='proxy_auth',
                        help=I18n.get('--proxy_auth'))
    parser.add_argument('--round_sensitive', required=False, type=int, default=3, dest='round_sensitive',
                        help=I18n.get('--round_sensitive'))
    parser.add_argument('--image_brightness', required=False, type=int, default=15, dest='image_brightness',
                        help=I18n.get('--image_brightness'))
    parser.add_argument('--detect_area_min_range', required=False, type=int, default=-5000, dest='min_range',
                        help=I18n.get('--detect_area_min_range'))
    parser.add_argument('--detect_area_max_range', required=False, type=int, default=5000, dest='max_range',
                        help=I18n.get('--detect_area_max_range'))
    parser.add_argument('--QR_text', required=False, default="", dest='QR_text',
                        help=I18n.get('--QR_text'))
    parser.add_argument('--QR_scale', required=False, type=int, default=3, dest='QR_scale',
                        help=I18n.get('--QR_scale'))
    parser.add_argument('--xreversed', required=False, default=False, dest='xreversed',
                        help=I18n.get('--xreversed'))
    parser.add_argument('--yreversed', required=False, default=False, dest='yreversed',
                        help=I18n.get('--yreversed'))
    parser.add_argument('-px', '--point_x', required=False, type=int, default=None, dest='point_x',
                        help=I18n.get('--point_x'))
    parser.add_argument('-py', '--point_y', required=False, type=int, default=None, dest='point_y',
                        help=I18n.get('--point_y'))
    parser.add_argument('-p', '--prioritized', required=False, default=False, dest='prioritized', action='store_true',
                        help=I18n.get('--prioritized'))
    parser.add_argument('-n', '--notify', required=False, default=False,
                        dest='notify', action='store_true', help=I18n.get('--notify'))
    parser.add_argument('-o', '--output_file', required=False, default='logfile.log',
                        dest='log_file', help=I18n.get('--output_file'))
    parser.add_argument('-v', '--verbose', required=False, default=False,
                        dest='verbose', action='store_true',
                        help=I18n.get('--verbose'))

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
    # \a is ASCII Bell, it makes noise if the terminal supports it
    print(('\a' * 5), end='', flush=True)
    logger.info(message)


def main():
    args = parse_args()
    if args.colors_ignored.count(16) == 0:
        args.colors_ignored.append(16)

    proxy = setup_proxy(args.proxy_url, args.proxy_auth)

    if not args.QR_text == "":
        args.file = "./img/QRcode.png"
        Image.create_QR_image(args.QR_text, args.QR_scale)

    # Setup file handler
    # Remove ANSI codes, log all levels
    # Add date to  file logs
    file_formatter = logging.Formatter('[%(asctime)s] %(nocolor)s',
                                       '%Y-%m-%d %H:%M:%S%z')
    file_filter = FileFilter()
    logfile = os.path.join(os.getcwd(), "log", args.log_file)
    # 5 rotating log files, max 8mb each for discord compatability
    filehandler = logging.handlers.RotatingFileHandler(logfile,
                                                       maxBytes=8*1024*1024,
                                                       backupCount=5)
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(file_formatter)
    filehandler.addFilter(file_filter)

    # Setup stdout handler
    # Don't print DEBUG or WARNING messages unless verbose flag is set
    # Clear line first to prevent issues with the timer
    stream_formatter = logging.Formatter(80 * ' ' + '\r'
                                         + '[%(asctime)s] %(message)s',
                                         '%H:%M:%S')
    streamhandler = logging.StreamHandler(sys.stdout)
    streamhandler.flush = sys.stdout.flush
    if args.verbose:
        streamhandler.setLevel(logging.DEBUG)
    else:
        streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(stream_formatter)

    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(logging.DEBUG)

    # Setup bar logger, to avoid threading issues with print
    bar_stream = logging.StreamHandler(sys.stdout)
    bar_stream.flush = sys.stdout.flush
    bar_stream.terminator = "\r"
    bar_print.addHandler(bar_stream)
    bar_print.setLevel(logging.INFO)

    image = Image(args.file, args.round_sensitive, args.image_brightness)

    bot = Bot(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive, args.colors_ignored, args.colors_not_overwrite, args.min_range, args.max_range, args.point_x, args.point_y, proxy,
              args.draw_strategy, args.xreversed, args.yreversed, args.prioritized, args.notify)

    def run():
        try:
            bot.run()
        except NeedUserInteraction as exception:
            alert(str(exception))
            response = input(I18n.get('paint.has_painted')).lower().strip()[0]
            if response == 'f':
                fingerprint = input(I18n.get('fingerprint.input'))
                while len(fingerprint) != 32:
                    print(I18n.get('fingerprint.invalid', color=Fore.RED))
                    fingerprint = input(I18n.get('fingerprint.input'))
                bot.pixelio.fingerprint = fingerprint
                # Request self after changing fingerprint.
                bot.pixelio.myself()
            elif response == 'n':
                return

            run()

    run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info(I18n.get('exit'))
