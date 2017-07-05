#!/usr/bin/env python

import requests, threading, websocket, math
from six.moves.urllib.parse import urlparse
from struct import unpack_from
from colors import EnumColor
from matrix import Matrix

class PixelCanvasIO(object):
    
    URL = 'http://pixelcanvas.io/'
    HEADER_USER_AGENT = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}
    HEADERS = {
            'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'accept': 'application/json',
            'content-type': 'application/json',
            'Origin': URL,
            'Referer': URL 
        }

    def __init__(self, fingerprint,  proxy = None):
        self.fingerprint = fingerprint
        self.proxy = proxy

    def post(self, url, payload):
        return requests.request('POST', url, data=payload, headers=PixelCanvasIO.HEADERS, proxies = self.proxy)

    def get(self, url, stream = False):
        return requests.get(url, stream=stream, headers=PixelCanvasIO.HEADER_USER_AGENT, proxies = self.proxy)
    
    def myself(self):
        return self.post(PixelCanvasIO.URL + 'api/me', '{"fingerprint":"%s"}' % self.fingerprint).json()

    def send_pixel(self, x, y, color):
        payload = '{"x":%s,"y":%s,"color":%s,"fingerprint":"%s","token":null}' % (x, y, color.index, self.fingerprint)
        response = self.post(PixelCanvasIO.URL + 'api/pixel', payload)

        if response.status_code == 403:
            raise Exception('Oh no, you are using a proxy')

        if response.status_code == 422:
            raise Exception('Oh no, it is need to provide a token. You need to enter in pixelcanvas.io and click in an pixel.')

        if response.status_code == 429:
            raise Exception('Oh no, you tried hard. Rate limit exceeded')
        try:
            return response.json()
        except Exception as e:
            raise Exception(str(response.text) + '-' + str(response.status_code))
    
    def download_canvas(self, center_x, center_y):
        return self.get(PixelCanvasIO.URL + 'api/bigchunk/%s.%s.bmp' % (center_x, center_y), stream = True).content
 
    def get_ws(self):
        return self.get(PixelCanvasIO.URL + 'api/ws').json()['url']

    def connect_websocket(self, canvas, axis = {'start_x' : 0, 'end_x' : 0, 'start_y' : 0, 'end_y' : 0}, print_all_websocket_log = False):
        def on_message(ws, message):
            if unpack_from('B', message, 0)[0] == 193:
                x = unpack_from('!h', message, 1)[0]
                y = unpack_from('!h', message, 3)[0]
                a = unpack_from('!H', message, 5)[0]
                number = (65520 & a) >> 4
                x = int(x * 64 + ((number % 64 + 64) % 64))
                y = int(y * 64 + math.floor(number / 64))
                color = EnumColor.index(15 & a)
                try:
                    canvas.matrix[x][y] = color
                    if (x in xrange(axis['start_x'], axis['end_x'] + 1) and y in xrange(axis['start_y'], axis['end_y'])) or log_all_info:
                        print("Somebody updated %s,%s with %s color" % (str(x), str(y), color.name))
                except Exception as e:
                    pass
                    

        def on_error(ws, error):
            ws.close()

        def on_close(ws):
            #TODO: reopen connetion
            print "### closed ###"
        
        def on_open(ws):
            print "Websocket open"

        url = self.get_ws()
        ws = websocket.WebSocketApp(url + '/?fingerprint=' + self.fingerprint, on_message = on_message, on_open = on_open, on_close = on_close, on_error = on_error)

        def worker(ws, pixel):
            if pixel.proxy:
                proxy = urlparse(pixel.proxy['http'])
                proxy_auth = None
                if proxy.username and proxy.password:
                    proxy_auth = [proxy.username, proxy.password]
                ws.run_forever(http_proxy_host=proxy.hostname, http_proxy_port=proxy.port, http_proxy_auth=proxy_auth)
            else:
                ws.run_forever()

        thread = threading.Thread(target=worker, args=(ws, self))
        thread.setDaemon(True)
        thread.start()