#!/usr/bin/env python

import os

try:
    import pip
except ImportError, e:
    print "installing pip"
    os.system("get-pip.py")
    import pip

print "Checking required packages"
pkgs = ['websocket-client', 'Pillow', 'requests', 'pyqrcode', 'pypng']
for package in pkgs:
    try:
        import package
    except ImportError, e:
        pip.main(['install', package])

print "OK"
