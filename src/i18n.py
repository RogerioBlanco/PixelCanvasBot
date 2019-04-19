#!/usr/bin/env python

import locale
import time


class I18n(object):

    @staticmethod
    def get(key, inline='false'):
        if (inline == 'true'):
            return I18n._all[I18n.lang_code][key]
        else:
            return '>> ' + time.strftime("%H:%M:%S") + ' ->' + I18n._all[I18n.lang_code][key]

    _all = {
        'en_GB': {
            'exit': 'Bye!',
            'colors.round': '{rgba} colors rounded {diff_min} ({name})',
            'chunk.blind.east': 'This bot may be blind for all pixels east of {x}',
            'chunk.blind.south': 'This bot may be blind for all pixels south of {y}',
            'chunk.load': 'Loading chunk ({x}, {y})...',

            'error.try_again': 'Oh no, an error occurred. Trying again.',
            'error.proxy': 'Oh no, you are using a proxy',
            'error.token': 'Oh no, a new token is required. Please open pixelcanvas.io and paint a pixel',
            'error.rate_limit': 'Oh no, you tried too hard! Rate limit exceeded',
            'error.connection': 'Connection broke :(',

            'paint.has_painted': 'Have you painted a pixel in pixelcanvas.io? y/n:',
            'paint.user': 'You painted {color} at {x},{y}',
            'paint.wait': 'Waiting {seconds} seconds',
            'progress': 'Total active pixel count: {total}. Correct pixels: {correct}. Incorrect pixels: {incorrect}. Progress: {progress}%.',

            'paint.ally': 'Somebody updated {x},{y} with {color} [ALLY]',
            'paint.outside': 'Somebody updated {x},{y} with {color} [OUTSIDE TEMPLATE]',
            'paint.enemy': 'Somebody updated {x},{y} with {color} [ENEMY]',

            'websocket.closed': 'Websocket closed',
            'websocket.opened': 'Websocket opened',

            'strategy.left_right_top_bottom': 'Drawing from left to right, from top to bottom',
            'strategy.right_left_top_bottom': 'Drawing from right to left, from top to bottom',
            'strategy.top_bottom_left_right': 'Drawing from top to bottom, from left to right',
            'strategy.bottom_top_left_right': 'Drawing from bottom to top, from left to right',
            'strategy.auto_select': 'Invalid strategy "{strategy}". Defaulting to strategy "spiral"',

            'external.load_cache': 'Loading cached image',
            'external.generating': 'Generating converted image here : {path}',
            'external.saved_cache': 'Saved image cache file, loading now...',
            'qr_created': 'QR Code successfully saved here: {path}',

            # Arguments
            '--image': 'The image to draw. Quantizes colors to the palette as defined in colors.py so the bot can draw correctly.',
            '--fingerprint': 'Your fingerprint. See README.md for instructions on how to retrieve it.',
            '--start_x': 'The x coordinate at which to start drawing',
            '--start_y': 'The y coordinate at which to start drawing',
            '--colors_ignored': 'Any colors listed here, if contained within the quantized image, will be treated as transparent for the purposes of drawing.',
            '--colors_not_overwrite': 'The colors listed here will not be overwritten if they appear on the canvas where the image is being drawn.',
            '--draw_strategy': 'Optional draw strategy. Choose from the strategy list [linear, p_linear, qf, randomize, status, sketch, radiate, spiral] default: randomize',
            '--mode_defensive': 'Put the bot in daemon mode (run in background). This will run forever.',
            '--proxy_url': 'Proxy url with port. ex: url:port . DEPRECATED',
            '--proxy_auth': 'Proxy authentication. ex: user:pass . DEPRECATED',
            '--round_sensitive': 'Color rounding sensitivity. This number must be > 0. ex: 3',
            '--image_brightness': 'Change image brightness. Supports negative values. ex: 15 or -15',
            '--detect_area_min_range': 'Supports negative values ex: 3000 or -3000',
            '--detect_area_max_range': 'Supports negative values ex: 3000 or -3000',
            '--QR_text': 'url or some text',
            '--QR_scale': 'QR code pixel width',
            '--xreversed': 'Draw from right to left. Set to True or False (default False)',
            '--yreversed': 'Draw from bottom to top. Set to True or False (default False)',
            '--point_x': 'Target x coordinate for strategies that radiate from a single point, such as radiate and spiral; defaults to center',
            '--point_y': 'Target y coordinate for strategies that radiate from a single point, such as radiate and spiral; defaults to center',
            '--prioritized': 'Sorts the order in which pixels are placed so that pixels that are more opaque in the source image are given priority over the more transparent pixels; allows for establishing strategic hotspots in a template',
            '--notify': 'Send a system notification if a captcha is encountered by the bot. Notification remains for 30 seconds or until dismissed.',
            '--output_file': 'Output the logs to a file. This is completely optional.',

            # Colors
            'white': 'white',
            'gainsboro': 'bright grey',
            'grey': 'grey',
            'nero': 'black',
            'carnation pink': 'pink',
            'red': 'red',
            'orange': 'orange',
            'brown': 'brown',
            'yellow': 'yellow',
            'conifer': 'conifer',
            'green': 'green',
            'dark turquoise': 'turquoise',
            'pacific blue': 'navy blue',
            'blue': 'blue',
            'violet': 'violet',
            'purple': 'purple',
        },
    }

    lang_code = locale.getdefaultlocale()[0]
    try:
        _all[lang_code]
    except KeyError:
        lang_code = 'en_GB'
