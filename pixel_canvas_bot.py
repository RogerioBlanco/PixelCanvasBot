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

COLORS_INDEX = {
    'WHITE': 0,
    'GAINSBORO': 1,
    'GREY': 2,
    'NERO': 3,
    'CARNATION_PINK': 4,
    'RED': 5,
    'ORANGE': 6,
    'BROWN': 7,
    'YELLOW': 8,
    'CONIFER': 9,
    'GREEN': 10,
    'DARK_TURQUOISE': 11,
    'PACIFIC_BLUE': 12,
    'BLUE': 13,
    'VIOLET': 14,
    'PURPLE': 15
}

COLORS_RGB = {
    (255, 255, 255): 'WHITE',
    (228, 228, 228): 'GAINSBORO',
    (136, 136, 136): 'GREY',
    (34, 34, 34): 'NERO',
    (255, 167, 209): 'CARNATION_PINK',
    (229, 0, 0): 'RED',
    (229, 149, 0): 'ORANGE',
    (160, 106, 66): 'BROWN',
    (229, 217, 0): 'YELLOW',
    (148, 224, 68): 'CONIFER',
    (2, 190, 1): 'GREEN',
    (0, 211, 221): 'DARK TURQUOISE',
    (0, 131, 199): 'PACIFIC_BLUE',
    (0, 0, 234): 'BLUE',
    (207, 110, 228): 'VIOLET',
    (130, 0, 128): 'PURPLE'
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
    response = requests.request('POST', url, data=payload, headers=headers, proxies = GLOBAL_PROXY)
    
    if response.status_code != 200:
        raise Exception('Occurred an problem.\nMsg: ' + response.text)

    return response

def get(url, stream = False, headers = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}):
    response = requests.get(url, stream=stream, headers=headers, proxies = GLOBAL_PROXY)
    
    if response.status_code != 200:
        raise Exception('Occurred an problem.\nMsg: ' + response.text)
    
    return response

def myself(fingerprint):
    return post(URL_BASE + 'api/me', '{"fingerprint":"%s"}' % fingerprint).json()

def send_pixel(x, y, color, fingerprint):
    return post(URL_BASE + 'api/pixel', '{"x":%s,"y":%s,"color":%s,"fingerprint":"%s","token":null}' % (x, y, color, fingerprint)).json()

def wait_time(data = {'waitSeconds':None}):
    if data['waitSeconds'] is not None:
        wait = data['waitSeconds'] + randint(0, 9)
        print 'Waiting %s seconds' % str(wait)
        time.sleep(wait)

def download_big_chuck(start_x, start_y, width, height):
    return None

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
    for y in range(0, image['height']):
        for x in range(0, image['width']):
            color = COLORS_RGB[image['pix'][x, y]]
            if color and MAP_PIXELS[x][y] != COLORS_INDEX[color]:
                response = send_pixel(start_x + x, start_y + y, COLORS_INDEX[color], fingerprint)
                while not response['success']:
                    wait_time(response)
                    print 'Oh no, an error occurred. Trying again.'
                    response = send_pixel(start_x + x, start_y + y, COLORS_INDEX[color], fingerprint)

                wait_time(response)
                update_map(start_x + x, start_y + y, COLORS_INDEX[color])
                print 'Set pixel color %s in %s,%s' % (color, str(start_x + x), str(start_y + y))

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
    MAP_PIXELS = [[0 for y in range(start_y, start_y + height)] for x in range(start_x, start_x + width)]

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

    canvas = download_big_chuck(args.start_x, args.start_y, image['width'], image['height'])

    setup_map(canvas, image['width'], image['height'], args.start_x, args.start_y)

    connect_websocket(args.fingerprint)
    
    myself = myself(args.fingerprint)

    wait_time(myself)
    
    draw_image(image, args.fingerprint, args.start_x, args.start_y, args.mode_defensive)
