#!/usr/bin/env python

import requests, threading, websocket, math
from six.moves.urllib.parse import urlparse
from struct import unpack_from
from colors import EnumColor
from matrix import Matrix
from i18n import I18n


class PixelCanvasIO(object):
    
    URL = 'http://pixelcanvas.io/'
    HEADER_USER_AGENT = {'User-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'}
    HEADERS = {
            'User-agent':'Mozilla/5.0 (Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36)',
            'accept': 'application/json',
            'content-type': 'application/json',
            'Origin': URL,
            'Referer': URL
        }
    
    def __init__(self, fingerprint,  proxy = None):
        self.fingerprint = fingerprint
        self.proxy = proxy
        self.cookies = None
        self.duck = 'z'

    def post(self, url, payload):
        return requests.request('POST', url, data=payload, headers=PixelCanvasIO.HEADERS, proxies = self.proxy, cookies = self.cookies)

    def get(self, url, stream = False):
        return requests.get(url, stream=stream, headers=PixelCanvasIO.HEADER_USER_AGENT, proxies = self.proxy)
    
    def myself(self):
        response = self.post(PixelCanvasIO.URL + 'api/me', '{"fingerprint":"%s"}' % self.fingerprint)
        self.duck = 'a'

        if ('duck' in response.cookies):
            self.duck = ('h' if response.cookies['DUCK'] is None else response.cookies['DUCK'])
        self.cookies = response.cookies
        return response.json()

    def send_pixel(self, x, y, color):
        payload = '{"x":%s,"y":%s,"%s":%s,"color":%s,"fingerprint":"%s","token":null}' % (x, y, self.duck, x + y + 8, color.index, self.fingerprint)
        response = self.post(PixelCanvasIO.URL + 'api/pixel', payload)

        if response.status_code == 403:
            raise Exception(I18n.get('Oh no, you are using a proxy'))

        if response.status_code == 422:
            raise Exception(I18n.get('refresh_token'))

        if response.status_code == 429:
            raise Exception(I18n.get('Rate_limit_exceeded'))

        if response.status_code == 504:
            print '[debug]504 retry to 60 seconds'
            return {'succes':false,'waitSeconds':120}
        try:
            return response.json()
        except Exception as e:
            raise Exception(I18n.get('only_time') + str(response.text) + '-' + str(response.status_code))
    
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
                        print(I18n.get('Somebody updated %s,%s with %s color') % (str(x), str(y), I18n.get(color.name)))
                except Exception as e:
                    pass
                    

        def on_error(ws, error):
            ws.close()

        def on_close(ws):
            print(I18n.get("### closed ###"))
            open_connection()
        
        def on_open(ws):
            print(I18n.get("Websocket open"))

        def open_connection():
            url = self.get_ws()
            ws = websocket.WebSocketApp(url + '/?fingerprint=' + self.fingerprint, on_message = on_message, on_open = on_open, on_close = on_close, on_error = on_error)
            
            def worker(ws, pixel):
                if pixel.proxy:
                    proxy = urlparse(pixel.proxy['http'])
                    proxy_auth = ''
                    if proxy.username and proxy.password:
                        proxy_auth = [proxy.username, proxy.password]
                    ws.run_forever(http_proxy_host=proxy.hostname, http_proxy_port=proxy.port, http_proxy_auth=proxy_auth)
                else:
                    ws.run_forever()

            thread = threading.Thread(target=worker, args=(ws, self))
            thread.setDaemon(True)
            thread.start()
        
        open_connection()
