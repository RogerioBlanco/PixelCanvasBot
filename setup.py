#!/usr/bin/env python

import os

try:
    import pip
except ImportError, e:
    print "installing pip"
    os.system("get-pip.py")
    import pip

print "Checking required packages"
pkgs = ['websocket-client', 'Pillow', 'requests', 'pyqrcode', 'pypng', 'six']
try:
    for package in pkgs:
        try:
            import package
        except ImportError, e:
                pip.main(['install', package])

    print "OK"
except AttributeError, e:
    print("It seems you pip version is over 10.0, please install the required packages manually, "
          "by executing following command:\n"
          "pip install websocket-client Pillow requests pyqrcode pypng six")
