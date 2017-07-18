# PixelCanvasBot

This is a functional bot for pixelcanvas.io.

#### Why I am doing this? 
Well, I think this is a fun game and I wanted learn another program language and challenge myself.

#### What you can do with this?
Well, you can draw some image and try replicate in pixelcanvas.io. You can combine with your friends or clan, whatever for combine forces to draw more quickly or defend your 'territory'.

#### I can use any image and this bot will draw for me?
**YES READY.** You can use any image. Converted to the nearest PixelCanvas.io color for every pixel 

# Installation

#### why git?

PixelCanvas.io frequently changes the API validation system.
We are updated after we notice. It can be a bit late, we can not guarantee it in any way. Recommend GIT for the current use

* get git and install from https://git-scm.com/downloads
* git clone -b master --single-branch --depth 10 https://github.com/RogerioBlanco/PixelCanvasBot.git
* git pull --ff origin master (update)

#### How you can use this?

Well, first you need Python 2.7 and install this:
* pip install websocket-client
* pip install Pillow
* pip install requests

#### For windows
you needs pip for other installations 
save from https://bootstrap.pypa.io/get-pip.py
* python get-pip.py

after pip installation

* python -m pip install websocket-client
* python -m pip install Pillow
* python -m pip install requests

# Using

### Geting yours fingerprint Chrome or chromium
* go http://pixelcanvas.io/@0,0
* press **F12**
* open **network** tab
* in **filter** input paste '**pixel**'
* put yours pixel any coordinates
* click request name *pixel*
* open **headers** tab
* your fingerprint is under **Request Playload**

![image](https://user-images.githubusercontent.com/12828465/28237968-24ca07cc-694a-11e7-9df3-32b4d737b44e.png)

## Easy to use, only required parameters:

* ./main.py -i image.png -f $FINGERPRINT$ -x 0 -y 0

### What is each parameter? 
    Need to help?
    Try it 'python ./main.py --help' maybe more usefull.
* **-i** or **--image** it is the image you want to draw.
* **-f** or **--fingerprint** it is your unique code. You can get in the requisition when you open Chrome DevTools.
* **-x** or **--start_x** it is the point X axis what you want to begin. Ex: 156
* **-y** or **--start_y** it is the point y axis what you want to begin. Ex: -4000
* **--colors_ignored** Colors of your image that will be ignored. Ex: 0 1 2 3 8 15
* **--draw_strategy** Optional draw strategy default by: *randomize* Avaiable strategy list : 
    * *linear* : line by line paint, 
    * *randomize* : pixel paint random coordinates, 
    * *status* : not painted only list paint status --support colors ignored parameters, don't suppurt sketch mode--
    * *sketch* : Don't fill image drawing image only bordes. see more information https://github.com/RogerioBlanco/PixelCanvasBot/issues/6
* **--mode_defensive** is the mode who put the program mode deamon. Default: True
* **--proxy_url** it is you proxy. Ex: proxy.yourcompany.com:8080
* **--proxy_auth** it is your credentials for the proxy. Ex: username:password
