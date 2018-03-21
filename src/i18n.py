#!/usr/bin/env python

import locale, time


class I18n(object):

    @staticmethod
    def get(key, inline='false'):
        if (inline == 'true'):
            return I18n._all[I18n.lang_code][key]
        else:
            return '>> ' + time.strftime("%H:%M:%S") + ' ->' + I18n._all[I18n.lang_code][key]

    _all = {
        'en_GB': {
            'only_time': '',
            'Bye': 'Bye',
            'try_again': 'Oh no, an error occurred. Trying again.',
            'You painted %s in the %s,%s': 'You painted %s in the %s,%s',
            'Waiting %s seconds': 'Waiting %s seconds',
            'Total: %s painted: %s Not painted %s': 'Total image pixel count: %s, Allready painted pixel : %s Not painted pixel: %s',
            ' %s colours rounded %s (%s) ': '%s colours rounded %s (%s)',
            'Oh no, you are using a proxy': 'Oh no, you are using a proxy',
            'refresh_token': 'Oh no, it is need to provide a token. You need to enter in pixelcanvas.io and click in an pixel.',
            'token_resolved': '"Have you already clicked on a pixel in pixelcanvas.io? y/n:',
            'Rate_limit_exceeded': 'Oh no, you tried hard. Rate limit exceeded',
            'Somebody updated %s,%s with %s color': 'Somebody updated %s,%s with %s color',
            '### closed ###': '### closed ###',
            'Websocket open': 'Websocket open',

            ## external
            'Load cached image': 'Load cached image',
            'generating converted image here : %s': 'generating converted image here : %s',
            'Saved image cache file, Loading Now...': 'Saved image cache file, Loading Now...',
            'Create QR Code succes in here: %s': 'Create QR Code succes in here: %s',
            '# From left to right, from top to bottom,': '# From left to right, from top to bottom,',
            '# From right to left, from top to bottom,': '# From right to left, from top to bottom,',
            '# From top to bottom, from left to right,': '# From top to bottom, from left to right,',
            '# From bottom to top, from left to right,': '# From bottom to top, from left to right,',
            'not fonud strategy %s auto selected randomize': 'not fonud strategy %s auto selected randomize',

            ##  Arguments

            '--image': 'The image file containing the desired drawing, respecting the pallets of RGBs: ',
            '--fingerprint': 'The fingerprint of your browser',
            '--start_x': 'The point x axis that will start to draw',
            '--start_y': 'The point y axis that will start to draw',
            '--colors_ignored': 'Ignored current image colors For example image only black and red colors painting. Ex: 0 1 2   4   6 7 8 9 10 11 12 13 15',
            '--colors_not_overwrite': 'Ignored pixelcanvas.io colors For example only black colors removing if this image image not equals black. Ex: 0 1 2   4 5 6 7 8 9 10 11 12 13 15',
            '--draw_strategy': 'Optional draw strategy avaiable strategy list [lineer, randomize, status, sketch] default: randomize',
            '--mode_defensive': 'Put the bot on mode defensive. This will run forever',
            '--proxy_url': 'Proxy url with port. ex: url:port',
            '--proxy_auth': 'Proxy authentication. ex: user:pass',
            '--round_sensitive': 'Color rounding sensitive option. Need this number > 0 ex: 3',
            '--image_brightness': 'Change image brignets, Support negative values ex: 15 or -15',
            '--detect_area_min_range': 'Support negative values ex: 3000 or -3000',
            '--detect_area_max_range': 'Support negative values ex: 3000 or -3000',
            '--QR_text': 'url or some text',
            '--QR_scale': 'QR code pixel length',

            ##   colors

            'white': 'white',
            'gainsboro': 'gainsboro',
            'grey': 'grey',
            'nero': 'nero',
            'carnation pink': 'carnation pink',
            'red': 'red',
            'orange': 'orange',
            'brown': 'brown',
            'yellow': 'yellow',
            'conifer': 'conifer',
            'green': 'green',
            'dark turquoise': 'dark turquoise',
            'pacific blue': 'pacific blue',
            'blue': 'blue',
            'violet': 'violet',
            'purple': 'purple',
        },
        'tr_TR': {
            'only_time': '',
            'Bye': 'Gorusuruz',
            'try_again': 'Beklenmeyen bir hata olustu tekrar deneyin.',
            'You painted %s in the %s,%s': '%s rengi %s,%s konumuna birakildi',
            'Waiting %s seconds': ' %s Saniye bekleniliyor....',
            'Total: %s painted: %s Not painted %s': 'Toplam pixel sayisi: %s, Hazir pixeller : %s Cizilecek Pixeller: %s',
            ' %s colours rounded %s (%s) ': '%s rengi %s (%s) renge cevrildi',
            'Oh no, you are using a proxy': 'Hata proxy kullanildigi icin islem yapilamiyor',
            'refresh_token': 'Token degeri gecersiz oldu. Sorunu duzeltmek icin pixelcanvas.io sitesine girin ve 1 tane pixel birakarak dogrulayin.',
            'token_resolved': '"pixelcanvasa girip pixel koyup dogruladin mi y/n:',
            'Rate_limit_exceeded': 'Hata istek limiti asildi',
            'Somebody updated %s,%s with %s color': 'Birisi %s,%s burayi %s renge boyadi',
            '### closed ###': '### Baglanti Kesildi ###',
            'Websocket open': 'Websockete baglanildi',

            ## external
            'Load cached image': 'Load cached image',
            'generating converted image here : %s': 'generating converted image here : %s',
            'Saved image cache file, Loading Now...': 'Saved image cache file, Loading Now...',
            'Create QR Code succes in here: %s': 'Create QR Code succes in here: %s',
            '# From left to right, from top to bottom,': '# From left to right, from top to bottom,',
            '# From right to left, from top to bottom,': '# From right to left, from top to bottom,',
            '# From top to bottom, from left to right,': '# From top to bottom, from left to right,',
            '# From bottom to top, from left to right,': '# From bottom to top, from left to right,',
            'not fonud strategy %s auto selected randomize': 'not fonud strategy %s auto selected randomize',

            ##  Arguments

            '--image': 'The image file containing the desired drawing, respecting the pallets of RGBs: ',
            '--fingerprint': 'The fingerprint of your browser',
            '--start_x': 'The point x axis that will start to draw',
            '--start_y': 'The point y axis that will start to draw',
            '--colors_ignored': 'Ignored current image colors For example image only black and red colors painting. Ex: 0 1 2   4   6 7 8 9 10 11 12 13 15',
            '--colors_not_overwrite': 'Ignored pixelcanvas.io colors For example only black colors removing if this image image not equals black. Ex: 0 1 2   4 5 6 7 8 9 10 11 12 13 15',
            '--draw_strategy': 'Optional draw strategy avaiable strategy list [lineer, randomize, status, sketch] default: randomize',
            '--mode_defensive': 'Put the bot on mode defensive. This will run forever',
            '--proxy_url': 'Proxy url with port. ex: url:port',
            '--proxy_auth': 'Proxy authentication. ex: user:pass',
            '--round_sensitive': 'Color rounding sensitive option. Need this number > 0 ex: 3',
            '--image_brightness': 'Change image brignets, Support negative values ex: 15 or -15',
            '--detect_area_min_range': 'Support negative values ex: 3000 or -3000',
            '--detect_area_max_range': 'Support negative values ex: 3000 or -3000',
            '--QR_text': 'url or some text',
            '--QR_scale': 'QR code pixel length',

            ##   colors

            'white': 'beyaz',
            'gainsboro': 'Acik Gri',
            'grey': 'Gri',
            'nero': 'Siyah',
            'carnation pink': 'Karanfil pembesi',
            'red': 'kirmizi',
            'orange': 'Portakal',
            'brown': 'kahverengi',
            'yellow': 'Sari',
            'conifer': 'Acik Yesil',
            'green': 'yesil',
            'dark turquoise': 'Koyu turkuaz',
            'pacific blue': 'Pasifik mavisi',
            'blue': 'Mavi',
            'violet': 'Menekse',
            'purple': 'Mor',
        },

    }

    lang_code = locale.getdefaultlocale()[0]
    try:
        _all[lang_code]
    except KeyError:
        lang_code = 'en_GB'
