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
            'Websocket open':'Websocket open',
            ##   colors
            'white':'white',
            'gainsboro':'gainsboro',
            'grey':'grey',
            'nero':'nero',
            'carnation pink':'carnation pink',
            'red':'red',
            'orange':'orange',
            'brown':'brown',
            'yellow':'yellow',
            'conifer':'conifer',
            'green':'green',
            'dark turquoise':'dark turquoise',
            'pacific blue':'pacific blue',
            'blue':'blue',
            'violet':'violet',
            'purple':'purple',
        },
        'tr_TR':{
            'only_time':'',
            'Bye':'Gorusuruz',
            'try_again':'Beklenmeyen bir hata olustu tekrar deneyin.',
            'You painted %s in the %s,%s':'%s rengi %s,%s konumuna birakildi',
            'Waiting %s seconds':' %s Saniye bekleniliyor....',
            'Total: %s painted: %s Not painted %s':'Toplam pixel sayisi: %s, Hazir pixeller : %s Cizilecek Pixeller: %s',
            ' %s colours rounded %s ':'%s rengi %s renge cevrildi',
            'Oh no, you are using a proxy':'Hata proxy kullanildigi icin islem yapilamiyor',
            'refresh_token':'Token degeri gecersiz oldu. Sorunu duzeltmek icin pixelcanvas.io sitesine girin ve 1 tane pixel birakarak dogrulayin.',
            'Rate_limit_exceeded':'Hata istek limiti asildi',
            'Somebody updated %s,%s with %s color':'Birisi %s,%s burayi %s renge boyadi',
            '### closed ###':'### Baglanti Kesildi ###',
            'Websocket open':'Websockete baglanildi',
            ##   colors
            'white':'beyaz',
            'gainsboro':'Gainsboro',
            'grey':'Gri',
            'nero':'Kara',
            'carnation pink':'Karanfil pembe',
            'red':'kirmizi',
            'orange':'Portakal',
            'brown':'kahverengi',
            'yellow':'Sari',
            'conifer':'Kozalakli',
            'green':'yesil',
            'dark turquoise':'Koyu turkuaz',
            'pacific blue':'Pasifik mavisi',
            'blue':'Mavi',
            'violet':'Menekse',
            'purple':'Mor',
        },

    }

    lang_code = locale.getdefaultlocale()[0]
    try:
        _all[lang_code]
    except KeyError:
        lang_code = 'en_GB'