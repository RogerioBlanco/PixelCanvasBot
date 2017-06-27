#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import websocket
import math
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

def post(url, payload, headers =
             {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
              'accept': 'application/json',
              'content-type': 'application/json',
              'Origin': URL_BASE,
              'Referer': URL_BASE
              }
         ):
    return requests.request('POST', url, data=payload, headers=headers)

def get(url, stream = False, headers = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}):
    return requests.get(url, stream=stream, headers=headers)

def myself(fingerprint):
    return post(URL_BASE + 'api/me', '{"fingerprint":"%s"}' % fingerprint).json()

def send_pixel(x, y, color, fingerprint):
    return post(URL_BASE + 'api/pixel', '{"x":%s,"y":%s,"color":%s,"fingerprint":"%s","token":null}' % (x, y, color, fingerprint)).json()

def wait_time(data = {'waitSeconds':None}):
    if data['waitSeconds'] is not None:
        print 'Waiting %s seconds' % str(data['waitSeconds'] + 1)
        time.sleep(data['waitSeconds'] + 1)

def update_map(arg):
    #TODO create a map of colors
    pass

def connect_websocket(fingerprint):
    def on_message(ws, message):
        if unpack_from('B', message, 0)[0] == REPLACE_CODE:
            number = unpack_from('!H', message, 5)[0]
            x = unpack_from('!h', message, 1)[0] * MAGIC_NUMBER + ((number % MAGIC_NUMBER + MAGIC_NUMBER) % MAGIC_NUMBER)
            y = unpack_from('!h', message, 3)[0] * MAGIC_NUMBER + math.floor(number / MAGIC_NUMBER)
            update_map({'x':x, 'y':y, 'color':15 & number})
            
    def on_error(ws, error):
        ws.close()

    def on_close(ws):
        #TODO: reopen connetion
        print "### closed ###"
        
    url = get(URL_BASE + 'api/ws').json()['url']
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url + '/?fingerprint=' + fingerprint, on_error = on_error, on_close = on_close)
    ws.on_message = on_message
    ws.run_forever()

def draw_image(file, fingerprint, start_x, start_y):
    im = Image.open(file).convert('RGB')
    pix = im.load() 
    width, height = im.size
    for y in range(0, height):
        for x in range(0, width):
            color = COLORS_RGB[pix[x,y]]
            print 'Pixel color %s in %s,%s' % (color, str(start_x + x),str(start_y + y))
            return_p =  send_pixel(start_x + x, start_y + y, COLORS_INDEX[color], fingerprint)
            wait_time(return_p)

    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-file', required=True)
    parser.add_argument('-fingerprint', required=True)
    parser.add_argument('-start_x', required=True, type=int)
    parser.add_argument('-start_y', required=True, type=int)
    file, fingerprint, start_x, start_y = parser.parse_args()
    
    myself = myself(fingerprint)
    wait_time(myself)
    draw_image(file, fingerprint, start_x, start_y)
