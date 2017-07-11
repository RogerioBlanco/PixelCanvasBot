#!/usr/bin/env python

import locale, time

class I18n(object):

    @staticmethod
    def get(key):
        return '>> ' + time.strftime("%H:%M:%S") + ' ->' + I18n._all[I18n.lang_code][key]

    _all = {
        'en_GB':{
            'only_time':'',
            'Bye':'Bye',
            'try_again':'Oh no, an error occurred. Trying again.',
            'You painted %s in the %s,%s':'You painted %s in the %s,%s',
            'Waiting %s seconds':'Waiting %s seconds',
            'Total: %s painted: %s Not painted %s':'Total image pixel count: %s, Allready painted pixel : %s Not painted pixel: %s',
            ' %s colours rounded %s ':'%s colours rounded %s ',
            'Oh no, you are using a proxy':'Oh no, you are using a proxy',
            'refresh_token':'Oh no, it is need to provide a token. You need to enter in pixelcanvas.io and click in an pixel.',
            'Rate_limit_exceeded':'Oh no, you tried hard. Rate limit exceeded',
            'Somebody updated %s,%s with %s color':'Somebody updated %s,%s with %s color',
            '### closed ###':'### closed ###',
            'Websocket open':'Websocket open'
            },
    }

    lang_code = locale.getdefaultlocale()[0]
    try:
        _all[lang_code]
    except KeyError:
        lang_code = 'en_GB'