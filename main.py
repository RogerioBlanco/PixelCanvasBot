#!/usr/bin/env python

from src.custom_exception import *
from src.bot import Bot
from src.image import Image
from src.i18n import I18n
from argparse import ArgumentParser


def parse_args():

    parser = ArgumentParser()
    parser.add_argument('-i', '--image', required=True, dest='file',
                        help=I18n.get('--image', 'true'))
    parser.add_argument('-f', '--fingerprint', required=True, dest='fingerprint',
                        help=I18n.get('--fingerprint', 'true'))
    parser.add_argument('-x', '--start_x', required=True, type=int, dest='start_x',
                        help=I18n.get('--start_x', 'true'))
    parser.add_argument('-y', '--start_y', required=True, type=int, dest='start_y',
                        help=I18n.get('--start_y', 'true'))
    parser.add_argument('-ci', '--colors_ignored', required=False, type=int, default=[], nargs='+', dest='colors_ignored',
                        help=I18n.get('--colors_ignored', 'true'))
    parser.add_argument('-cno', '--colors_not_overwrite', required=False, type=int, default=[], nargs='+', dest='colors_not_overwrite',
                        help=I18n.get('--colors_not_overwrite', 'true'))
    parser.add_argument('-ds', '--draw_strategy', required=False, default='randomize', dest='draw_strategy',
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
    parser.add_argument('-n', '--notify', required=False, default=False, dest='notify', action='store_true', help=I18n.get('--notify','true'))

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

    image = Image(args.file, args.round_sensitive, args.image_brightness)

    bot = Bot(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive, args.colors_ignored, args.colors_not_overwrite, args.min_range, args.max_range, proxy,
              args.draw_strategy, args.xreversed, args.yreversed, args.notify)

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
