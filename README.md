# PixelCanvasBot

This is a prototype of an bot for pixelcanvas.io, partially functional.

### Why I am doing this? 
Well, I think this is a fun game and I wanted learn another program language and challenge myself.

### What you can do with this?
Well, you can draw some image and try replicate in pixelcanvas.io. You can combine with your friends or clan, whatever for combine forces to draw more quickly or defend your 'territory'.

### I can use any image and this bot will draw for me?
Yes and no. You can use any image **BUT** for every pixel must to respect the RGBs below:

* WHITE: (255, 255, 255),
* GAINSBORO: (228, 228, 228)
* GREY: (136, 136, 136)
* NERO: (34, 34, 34)
* CARNATION_PINK: (255, 167, 209)
* RED: (229, 0, 0)
* ORANGE: (229, 149, 0)
* BROWN: (160, 106, 66)
* YELLOW: (229, 217, 0)
* CONIFER: (148, 224, 68)
* GREEN: (2, 190, 1)
* DARK_TURQUOISE: (0, 211, 221)
* PACIFIC_BLUE: (0, 131, 199)
* BLUE: (0, 0, 234)
* VIOLET: (207, 110, 228)
* PURPLE' : (130, 0, 128) 

### How you can use this?

Well, first you need Python 2.7 and install this:
* pip install websocket-client
* pip install Pillow
* pip install requests

#### for windows
if you needs pip 
save from https://bootstrap.pypa.io/get-pip.py
* python get-pip.py

after pip installation

* python -m pip install websocket-client
* python -m pip install Pillow
* python -m pip install requests


#####After you can execute the code like this:

* ./Main.py -i image.png -f $FINGERPRINT$ -x 0 -y 0

### What is each parameter? 

* **-i** or **--image** it is the image you want to draw.
* **-f** or **--fingerprint** it is your unique code. You can get in the requisition when you open Chrome DevTools.
* **-x** or **--start_x**' it is the point X axis what you want to begin. Ex: 156
* **-y** or **--start_y**' it is the point y axis what you want to begin. Ex: -4000
* **--mode_defensive**' is the mode who put the program mode deamon.
* **--proxy_url** it is you proxy. Ex: proxy.yourcompany.com:8080
* **--proxy_auth** it is your credentials for the proxy. Ex: username:password
