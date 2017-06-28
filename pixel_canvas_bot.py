#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import websocket
import math
import thread

from random import randint
from six.moves.urllib.parse import urlparse
from argparse import ArgumentParser
from struct import unpack_from
from PIL import Image

COLORS_NAME = [
    'WHITE',
    'GAINSBORO',
    'GREY',
    'NERO',
    'CARNATION PINK',
    'RED',
    'ORANGE',
    'BROWN',
    'YELLOW',
    'CONIFER',
    'GREEN',
    'DARK_TURQUOISE',
    'PACIFIC_BLUE',
    'BLUE',
    'VIOLET',
    'PURPLE'
]

COLORS_RGB = {
    (255, 255, 255): 0,
    (228, 228, 228): 1,
    (136, 136, 136): 2,
    (34, 34, 34): 3,
    (255, 167, 209): 4,
    (229, 0, 0): 5,
    (229, 149, 0): 6,
    (160, 106, 66): 7,
    (229, 217, 0): 8,
    (148, 224, 68): 9,
    (2, 190, 1): 10,
    (0, 211, 221): 11,
    (0, 131, 199):12,
    (0, 0, 234): 13,
    (207, 110, 228): 14,
    (130, 0, 128): 15
}

#WebSocket
REPLACE_CODE = 193
MAGIC_NUMBER = 64

URL_BASE = 'http://pixelcanvas.io/'

#Globals Variables
GLOBAL_PROXY = None
MAP_PIXELS = None

def post(url, payload, headers =
             {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
              'accept': 'application/json',
              'content-type': 'application/json',
              'Origin': URL_BASE,
              'Referer': URL_BASE
              }
         ):
    return requests.request('POST', url, data=payload, headers=headers, proxies = GLOBAL_PROXY)

def get(url, stream = False, headers = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}):
    return requests.get(url, stream=stream, headers=headers, proxies = GLOBAL_PROXY)

def myself(fingerprint):
    return post(URL_BASE + 'api/me', '{"fingerprint":"%s"}' % fingerprint).json()

def send_pixel(x, y, color, fingerprint):
    response = post(URL_BASE + 'api/pixel', '{"x":%s,"y":%s,"color":%s,"fingerprint":"%s","token":null}' % (x, y, color, fingerprint))

    if response.status_code == 422:
        raise Exception('Oh no, it is need to provide a token. Wait a few minutes and try again.')

    if response.status_code == 429:
        raise Exception('Oh no, you tried hard. Rate limit exceeded')

    return response.json()
def wait_time(data = {'waitSeconds':None}):
    if data['waitSeconds'] is not None:
        wait = data['waitSeconds'] + randint(0, 9)
        print 'Waiting %s seconds' % str(wait)
        time.sleep(wait)

def download_canvas(start_x, start_y):
    point_x, point_y = (start_x - (start_x % 64)) / 64, (start_y - (start_y % 64)) / 64

    matrix = {}

    for init_x in xrange((point_x - 7) * 64, (point_x + 8) * 64):
        matrix[init_x] = {}
        for init_y in xrange((point_y - 7) * 64, (point_y + 8) * 64):
            matrix[init_x][init_y] = None

    raw = get(URL_BASE + 'api/bigchunk/%s.%s.bmp' % (point_x, point_y), stream = True).content
    index = 0

    for block_y in xrange(point_y - 7, point_y + 8):
        for block_x in xrange(point_x - 7, point_x + 8):
            for y in xrange(64):
                for x in xrange(0, 64, 2):
                    matrix[block_x * 64 + x][block_y * 64 + y] = ord(raw[index]) >> 4
                    matrix[block_x * 64 + x+1][block_y * 64 + y] = ord(raw[index]) & 0x0F
                    index += 1
    return matrix

def connect_websocket(fingerprint):
    def on_message(ws, message):
        if unpack_from('B', message, 0)[0] == REPLACE_CODE:
            number = unpack_from('!H', message, 5)[0]
            x = unpack_from('!h', message, 1)[0] * MAGIC_NUMBER + ((number % MAGIC_NUMBER + MAGIC_NUMBER) % MAGIC_NUMBER)
            y = unpack_from('!h', message, 3)[0] * MAGIC_NUMBER + math.floor(number / MAGIC_NUMBER)
            update_map(int(x), int(y), int(15 & number))
            
    def on_error(ws, error):
        ws.close()

    def on_close(ws):
        #TODO: reopen connetion
        print "### closed ###"
    
    def on_open(ws):
        print "Websocket open"

    url = get(URL_BASE + 'api/ws').json()['url']
    ws = websocket.WebSocketApp(url + '/?fingerprint=' + fingerprint, on_error = on_error, on_close = on_close, on_open = on_open)
    ws.on_message = on_message

    def run(*args):
        if GLOBAL_PROXY:
            proxy = urlparse(GLOBAL_PROXY['http'])
            proxy_auth = None
            if proxy.username and proxy.password:
                proxy_auth = [proxy.username, proxy.password]

            ws.run_forever(http_proxy_host=proxy.hostname, http_proxy_port=proxy.port, http_proxy_auth=proxy_auth)
        else:
            ws.run_forever()

    thread.start_new_thread(run, ())

def load_image(file):
    im = Image.open(file).convert('RGB')
    width, height = im.size
    pix = im.load()
    return {'width':width, 'height': height, 'pix': pix}

def draw_image(image, fingerprint, start_x, start_y, mode_defensive):
    for y in xrange(0, image['height']):
        for x in xrange(0, image['width']):
            color = COLORS_RGB[image['pix'][x, y]]
            if color is not None and MAP_PIXELS[start_x + x][start_y + y] != color:
                response = send_pixel(start_x + x, start_y + y, color, fingerprint)

                while not response['success']:
                    print 'Oh no, an error occurred. Trying again.'
                    wait_time(response)
                    response = send_pixel(start_x + x, start_y + y, color, fingerprint)

                update_map(start_x + x, start_y + y, color)
                
                print 'Set pixel color %s in %s,%s' % (COLORS_NAME[color], str(start_x + x), str(start_y + y))
                wait_time(response)

def setup_global_proxy(proxy_url, proxy_auth):
    global GLOBAL_PROXY 
    GLOBAL_PROXY = {
        'http': 'http://%s%s' % (proxy_auth + '@', proxy_url),
        'https': 'http://%s%s' % (proxy_auth + '@', proxy_url)
        }

def coordinates_exist(x, y):
    try:
        MAP_PIXELS[x][y]
    except IndexError:
        return False
    return True

def update_map(x, y, color):
    global MAP_PIXELS
    if coordinates_exist(x, y):
        print "Updated %s %s with %s index color" % (str(x), str(y), str(color))
        MAP_PIXELS[x][y] = color

def setup_map(canvas, width, height, start_x, start_y):
    global MAP_PIXELS
    end_x, end_y = (start_x + width), (height + start_y)

    MAP_PIXELS = {}
    for x in xrange(start_x, end_x):
        MAP_PIXELS[x] = {}
        for y in xrange(start_y, end_y):
            MAP_PIXELS[x][y] = None

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            MAP_PIXELS[x][y] = canvas[x][y]

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i','--image', required=True, dest='file', 
        help='''The image file containing the desired drawing, respecting the pallets of RGBs: ''' + str(COLORS_RGB))
    parser.add_argument('-f','--fingerprint', required=True, dest='fingerprint', help='The fingerprint of your browser')
    parser.add_argument('-x','--start_x', required=True, type=int, dest='start_x', help='The point x axis that will start to draw')
    parser.add_argument('-y','--start_y', required=True, type=int, dest='start_y', help='The point y axis that will start to draw')
    parser.add_argument('--mode_defensive', required=False, default=True, dest='mode_defensive', help='Not implemented yet.')
    parser.add_argument('--proxy_url', required=False, dest='proxy_url', help='Proxy url with port. ex: url:port')
    parser.add_argument('--proxy_auth', required=False, dest='proxy_auth', help='Proxy authentication. ex: user:pass')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.proxy_url or (args.proxy_url and args.proxy_auth):
        setup_global_proxy(args.proxy_url, args.proxy_auth)

    image = load_image(args.file)

    canvas_complete = download_canvas(args.start_x, args.start_y)

    setup_map(canvas_complete, image['width'], image['height'], args.start_x, args.start_y)

    connect_websocket(args.fingerprint)
    
    myself = myself(args.fingerprint)

    wait_time(myself)
    
    draw_image(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive)