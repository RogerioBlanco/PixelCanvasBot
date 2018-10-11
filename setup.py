#!/usr/bin/env python

import os

try:
    import pip
except ImportError as e:
    print "installing pip"
    os.system("get-pip.py")
    import pip

print "Checking required packages"
pkgs = ['websocket-client', 'Pillow', 'requests', 'pyqrcode', 'pypng', 'six']
for package in pkgs:
    try:
        import package
    except ImportError as e:
        pip.main(['install', package])

print "OK"
