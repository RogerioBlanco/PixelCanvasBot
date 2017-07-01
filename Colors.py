#!/usr/bin/env python

class EnumColor:
    class Color(object):
        def __init__(self, index, name, rgb):
            self.name = name
            self.rgb = rgb
            self.index = index
    
    ENUM = [
        Color(0,    'white',            (255,255,255)),
        Color(1,    'gainsboro',        (228,228,228)),
        Color(2,    'grey',             (136,136,136)),
        Color(3,    'nero',             ( 34, 34, 34)),
        Color(4,    'carnation pink',   (255,167,209)),
        Color(5,    'red',              (229,  0,  0)),
        Color(6,    'orange',           (229,149,  0)),
        Color(7,    'brown',            (160,106, 66)),
        Color(8,    'yellow',           (229,217,  0)),
        Color(9,    'conifer',          (148,224, 68)),
        Color(10,   'green',            (  2,190,  1)),
        Color(11,   'dark turquoise',   (  0,211,221)),
        Color(12,   'pacific blue',     (  0,131,199)),
        Color(13,   'blue',             (  0,  0,234)),
        Color(14,   'violet',           (207,110,228)),
        Color(15,   'purple',           (130,  0,128)),
    ]

    
    
    @staticmethod
    def index(i):
        for color in EnumColor.ENUM:
            if i == color.index:
                return color
        #White is default color
        return EnumColor.ENUM[0]