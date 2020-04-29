#!/usr/bin/env python

from src.custom_exception import *
from src.bot import Bot
from src.image import Image
from src.i18n import I18n
import argparse
import sys
import string
from random import choice
import ntpath


def parse_args():
    def str2bool(v):
        if isinstance(v, bool):
           return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', required=True, dest='file',
                        help=I18n.get('--image', 'true'))
    parser.add_argument('-f', '--fingerprint', required=False, dest='fingerprint',
                        help=I18n.get('--fingerprint', 'true'))
    parser.add_argument('-x', '--start_x', required=False, type=int, dest='start_x',
                        help=I18n.get('--start_x', 'true'))
    parser.add_argument('-y', '--start_y', required=False, type=int, dest='start_y',
                        help=I18n.get('--start_y', 'true'))
    parser.add_argument("--stealth", type=str2bool, nargs='?', const=True, default=False,
                        help=I18n.get('--stealth', 'true'))
    parser.add_argument('--colors_ignored', required=False, type=int, default=[], nargs='+', dest='colors_ignored',
                        help=I18n.get('--colors_ignored', 'true'))
    parser.add_argument('--colors_not_overwrite', required=False, type=int, default=[], nargs='+', dest='colors_not_overwrite',
                        help=I18n.get('--colors_not_overwrite', 'true'))
    parser.add_argument('--draw_strategy', required=False, default='randomize', dest='draw_strategy',
                        help=I18n.get('--draw_strategy', 'true'))
    parser.add_argument('--mode_defensive', required=False, default=True, dest='mode_defensive',
                        help=I18n.get('--mode_defensive', 'true'))
    parser.add_argument('--proxy_url', required=False, dest='proxy_url',
                        help=I18n.get('--proxy_url', 'true'))
    parser.add_argument('--proxy_auth', required=False, dest='proxy_auth',
                        help=I18n.get('--proxy_auth', 'true'))
    parser.add_argument('--round_sensitive', required=False, type=int, default=3, dest='round_sensitive',
                        help=I18n.get('--round_sensitive', 'true'))
    parser.add_argument('--image_brightness', required=False, type=int, default=15, dest='image_brightness',
                        help=I18n.get('--image_brightness', 'true'))
    parser.add_argument('--detect_area_min_range', required=False, type=int, default=-5000, dest='min_range',
                        help=I18n.get('--detect_area_min_range', 'true'))
    parser.add_argument('--detect_area_max_range', required=False, type=int, default=5000, dest='max_range',
                        help=I18n.get('--detect_area_max_range', 'true'))
    parser.add_argument('--QR_text', required=False, default="", dest='QR_text',
                        help=I18n.get('--QR_text', 'true'))
    parser.add_argument('--QR_scale', required=False, type=int, default=3, dest='QR_scale',
                        help=I18n.get('--QR_scale', 'true'))
    parser.add_argument('--xreversed', required=False, default=False, dest='xreversed',
                        help=I18n.get('--xreversed', 'true'))
    parser.add_argument('--yreversed', required=False, default=False, dest='yreversed',
                        help=I18n.get('--yreversed', 'true'))

    parsed_args = parser.parse_args()

    if parsed_args.fingerprint is None:
        parsed_args.fingerprint = ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(32))

    if parsed_args.start_x is None or parsed_args.start_y is None:
        name = ntpath.splitext(ntpath.basename(parsed_args.file))[0]
        arr = name.split('_')
        if len(arr) != 3:
            parser.print_usage()
            print('Error: ' + I18n.get('no-coords', 'true'))
            sys.exit(1)
        parsed_args.start_x = int(arr[1])
        parsed_args.start_y = int(arr[2])

    return parsed_args


def setup_proxy(proxy_url, proxy_auth):
    if not proxy_url:
        return None

    if proxy_auth is None:
        proxy_auth = ''
    else:
        proxy_auth = proxy_auth + '@'

    url_split = proxy_url.split('://')
    if (len(url_split) == 2):
        proxy_url = '%s://%s%s' % (url_split[0], proxy_auth, url_split[1])
    else:
        proxy_url = 'http://%s%s' % (proxy_auth, proxy_url)

    return {'http': proxy_url, 'https': proxy_url}


def alert(message=''):
    print(('\a' * 5) + message)


def main():
    args = parse_args()

    proxy = setup_proxy(args.proxy_url, args.proxy_auth)


    if not args.QR_text == "":
        args.file = "./img/QRcode.png"
        Image.create_QR_image(args.QR_text, args.QR_scale)

    image = Image(args.file, args.round_sensitive, args.image_brightness)
    
    bot = Bot(image, args.fingerprint, args.start_x, args.start_y, args.stealth, args.mode_defensive, args.colors_ignored, args.colors_not_overwrite, args.min_range, args.max_range, proxy,
              args.draw_strategy, args.xreversed, args.yreversed)

    bot.init()

    def run():
        try:
            bot.run()
        except NeedUserInteraction as exception:
            alert(str(exception))
            try:
                if raw_input(I18n.get('token_resolved')).strip() == 'y':
                    run()
            except NameError as e:
                if input(I18n.get('token_resolved')).strip() == 'y':
                    run()

    run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(I18n.get('Bye'))
