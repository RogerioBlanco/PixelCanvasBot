#!/usr/bin/env python

import time
from src.bot import Bot
from src.image import Image
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i','--image', required=True, dest='file', help='The image file containing the desired drawing, respecting the pallets of RGBs: ')
    parser.add_argument('-f','--fingerprint', required=True, dest='fingerprint', help='The fingerprint of your browser')
    parser.add_argument('-x','--start_x', required=True, type=int, dest='start_x', help='The point x axis that will start to draw')
    parser.add_argument('-y','--start_y', required=True, type=int, dest='start_y', help='The point y axis that will start to draw')
    parser.add_argument('--colors_ignored', required=False, type=int, default = [], nargs='+', dest='colors_ignored', help='Colors of your image that will be ignored. Ex: 0 1 2 3 8 15')
    parser.add_argument('--draw_strategy', required=False, default='randomize', dest='draw_strategy', help='Optional draw strategy avaiable strategy list [lineer, randomize, status] default: randomize')
    parser.add_argument('--mode_defensive', required=False, default=True, dest='mode_defensive', help='Put the bot on mode defensive. This will run forever')
    parser.add_argument('--proxy_url', required=False, dest='proxy_url', help='Proxy url with port. ex: url:port')
    parser.add_argument('--proxy_auth', required=False, dest='proxy_auth', help='Proxy authentication. ex: user:pass')

    return parser.parse_args()

def setup_proxy(proxy_url, proxy_auth):
    if proxy_url and proxy_auth:
        proxy_auth = proxy_auth + '@'

    if proxy_url:
        return {'http': 'http://%s%s' % (proxy_auth, proxy_url)}

    return None

def main():
    args = parse_args()

    proxy = setup_proxy(args.proxy_url, args.proxy_auth)

    image = Image(args.file)

    bot = Bot(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive, args.colors_ignored, proxy, args.draw_strategy)

    bot.run()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('>> ' + time.strftime("%H:%M:%S") + ' ->' + 'Bye')