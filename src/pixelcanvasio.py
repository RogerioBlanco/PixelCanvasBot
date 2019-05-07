import json
import logging
import math
import threading
from struct import unpack_from
import datetime as dt

import requests
import websocket
from colorama import Fore
from plyer import notification
from six.moves import range
from six.moves.urllib.parse import urlparse

from .colors import EnumColor
from .custom_exception import NeedUserInteraction, UnknownError
from .i18n import I18n
from .safetynet import retry
from .rate_track import RateTrack

logger = logging.getLogger('bot')


class PixelCanvasIO(object):
    URL = 'https://pixelcanvas.io/'
    HEADER_USER_AGENT = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 '
        'Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
        'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
    }
    HEADERS = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 '
        'Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json',
        'Host': 'pixelcanvas.io',
        'Origin': URL,
        'Referer': URL
    }

    def __init__(self, fingerprint, proxy=None, bot=None, notify=False):
        self.fingerprint = fingerprint
        self.proxy = proxy
        self.cookies = None
        self.duck = 'z'
        self.bot = bot
        self.notify = notify
        # max 37.5 pixel requests per 5 minutes
        self.pxrate = RateTrack(dt.timedelta(minutes=5), 37.5)

    def post(self, url, payload):
        return requests.post(url, json=payload, headers=PixelCanvasIO.HEADERS,
                             proxies=self.proxy, cookies=self.cookies)

    def get(self, url, stream=False):
        return requests.get(url, stream=stream,
                            headers=PixelCanvasIO.HEADER_USER_AGENT,
                            proxies=self.proxy)

    def myself(self):
        response = self.post(PixelCanvasIO.URL + 'api/me',
                             {'fingerprint': self.fingerprint})
        self.duck = 'a'

        if ('duck' in response.cookies):
            self.duck = ('h' if response.cookies['DUCK'] is None
                         else response.cookies['DUCK'])
        self.cookies = response.cookies
        return response.json()

    @retry((KeyError, UnknownError))
    def send_pixel(self, x, y, color):
        payload = {
            'x': x,
            'y': y,
            self.duck: x + y + 8,
            'color': color.index,
            'fingerprint': self.fingerprint,
            'token': None
        }
        response = None
        # Use RateTrack to manage pixel rate limit
        try:
            response = self.post(PixelCanvasIO.URL + "api/pixel", payload)
        except requests.exceptions.ConnectionError:
            logger.debug(I18n.get('error.connection'))
            return self.pxrate.update({'success': 0, 'waitSeconds': 5})

        if response.status_code == 403:
            self.pxrate.update()
            raise Exception(I18n.get('error.proxy'))

        if response.status_code == 422:
            if self.notify:
                notification.notify(
                    title='Canvas Bot Alert',
                    message='A captcha has been encountered by the bot, '
                            'and it requires your human abilities to solve '
                            'the captcha before it can continue painting. '
                            'Please do this as soon as possible.',
                    app_name='PixelTraanvas Bot',
                    app_icon='res/robotto.ico',
                    timeout=60)
            raise NeedUserInteraction(I18n.get('error.token'))

        if response.status_code == 429:
            self.pxrate.update()
            raise Exception(I18n.get('error.rate_limit'))

        if response.status_code == 504:
            return self.pxrate.update({'success': 0, 'waitSeconds': 120})

        if response.status_code >= 500:
            return self.pxrate.update({'success': 0, 'waitSeconds': 5})

        try:
            response_dict = response.json()
            if 'waitSeconds' in response_dict:
                return self.pxrate.update(response_dict)
            else:
                self.pxrate.update()
                raise KeyError("No wait time specified by the server.")
        except Exception:
            self.pxrate.update()
            raise UnknownError(str(response.text) + '-'
                               + str(response.status_code))

    def download_canvas(self, center_x, center_y):
        x = bytearray(self.get(PixelCanvasIO.URL + 'api/bigchunk/%s.%s.bmp'
                               % (center_x, center_y), stream=True).content)
        return x

    @retry(json.decoder.JSONDecodeError,
           log_on_failure=I18n.get('websocket.failed_collect'), fatal=True)
    def get_ws(self):
        return self.get(PixelCanvasIO.URL + 'api/ws').json()['url']

    @retry(Exception, log_on_failure=I18n.get('websocket.failed_connect'),
           fatal=True)
    def connect_websocket(self, canvas,
                          axis={'start_x': 0, 'end_x': 0,
                                'start_y': 0, 'end_y': 0},
                          print_all_websocket_log=False):
        def on_message(ws, message):
            if unpack_from('B', message, 0)[0] == 193:
                x = unpack_from('!h', message, 1)[0]
                y = unpack_from('!h', message, 3)[0]
                a = unpack_from('!H', message, 5)[0]
                number = (65520 & a) >> 4
                x = int(x * 64 + ((number % 64 + 64) % 64))
                y = int(y * 64 + math.floor(number / 64))
                color = EnumColor.index(15 & a)
                pixel = (x,y)
                try:
                    canvas.matrix[x][y] = color
                    # Check that message is relevant,
                    # and not being modified by self.
                    if ((x in range(axis['start_x'], axis['end_x'] + 1) and
                            y in range(axis['start_y'], axis['end_y'])) and
                            (x, y, color.index) != self.bot.pixel_intent):
                        template_color = EnumColor.rgba(
                            self.bot.image.pix[x - self.bot.start_x,
                                               y - self.bot.start_y])
                        color_name = I18n.get(color.name, inline=True,
                                              end=None)
                        if (template_color in self.bot.colors_ignored
                                or template_color.rgba[3] == 0):
                            logger.debug(
                                I18n.get('paint.outside', color=Fore.YELLOW)
                                .format(x=x, y=y, color=color_name))
                        elif color == template_color:
                            logger.debug(
                                I18n.get('paint.ally', color=Fore.GREEN)
                                .format(x=x, y=y, color=color_name))
                        else:
                            logger.debug(
                                I18n.get('paint.enemy', color=Fore.RED)
                                .format(x=x, y=y, color=color_name))
                            if (self.bot.mode_defensive):
                                self.bot.strategy.change_detected(*pixel)
                    elif (x, y, color.index) == self.bot.pixel_intent:
                        # Clear intent after one matching pixel is detected
                        self.bot.pixel_intent = ()

                except Exception:
                    pass

        def on_error(ws, error):
            ws.close()

        def on_close(ws):
            logger.debug(I18n.get('websocket.closed'))
            open_connection()

        def on_open(ws):
            logger.debug(I18n.get("websocket.opened"))

        def open_connection():
            url = self.get_ws()
            ws = websocket.WebSocketApp(
                url + '/?fingerprint=' + self.fingerprint,
                on_message=on_message, on_open=on_open, on_close=on_close,
                on_error=on_error)

            def worker(ws, pixel):
                if pixel.proxy:
                    proxy = urlparse(pixel.proxy['http'])
                    proxy_auth = ''
                    if proxy.username and proxy.password:
                        proxy_auth = [proxy.username, proxy.password]
                    ws.run_forever(http_proxy_host=proxy.hostname,
                                   http_proxy_port=proxy.port,
                                   http_proxy_auth=proxy_auth)
                else:
                    ws.run_forever()

            thread = threading.Thread(target=worker, args=(ws, self))
            thread.setDaemon(True)
            thread.start()

        open_connection()
