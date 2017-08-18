# PixelCanvasBot

This is a functional bot for pixelcanvas.io.
We will not provide you with a faster drawing.
It does not allow you to easily draw your image. You need to spend some effort.
This bot can draw images that you can't normally draw on your place.

#### Why I am doing this? 
Well, I think this is a fun game and I wanted learn another program language and challenge myself.

#### What you can do with this?
Well, you can draw some image and try replicate in pixelcanvas.io. You can combine with your friends or clan, whatever for combine forces to draw more quickly or defend your 'territory'.

#### I can use any image and this bot will draw for me?
**YES READY.** You can use any image. Converted to the nearest PixelCanvas.io color for every pixel.
Conversion result images if not exist in ./img/.cache folder created. You can interfere with this file or you can preview it to be drawn 
Optional use *--round_sensitive* *--image_brightness* parameters to You can change the degree of rounding precision, or you can make the picture that is to be drawn darker - lighter.
see work result: https://github.com/RogerioBlanco/PixelCanvasBot/issues/45

# Installation

#### why git?

PixelCanvas.io frequently changes the API validation system.
We are updated after we notice. It can be a bit late, we can not guarantee it in any way. Recommend GIT for the current use

* get git and install from https://git-scm.com/downloads

* git clone -b master --single-branch --depth 10 https://github.com/RogerioBlanco/PixelCanvasBot.git
* git pull --ff origin master (optional update command)

#### How you can use this?

Well, first you need Python 2.7 and install required packages:
* cd PixelCanvasBot
* python ./setup.py

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

* python ./main.py -i image.png -f $FINGERPRINT$ -x 0 -y 0

### What is each parameter? 
    Need to help?
    Try it 'python ./main.py --help' maybe more usefull.
* **-i** or **--image** [required] it is the image you want to draw.
* **-f** or **--fingerprint** [required] it is your unique code. You can get in the requisition when you open Chrome DevTools.
* **-x** or **--start_x** [required] it is the point X axis what you want to begin. Ex: 156
* **-y** or **--start_y** [required] it is the point y axis what you want to begin. Ex: -4000
* **--colors_ignored** [optional] Colors of your image that will be ignored. Ex: 0 1 2 3 8 15
* **--draw_strategy** [optional] draw strategy default by: *randomize* Avaiable strategy list : 
    * *linear* : line by line paint, 
    * *randomize* : pixel paint random coordinates, 
    * *status* : not painted only list paint status --support colors ignored parameters, don't suppurt sketch mode--
    * *sketch* : Don't fill image drawing image only bordes. see more information https://github.com/RogerioBlanco/PixelCanvasBot/issues/6
* **--mode_defensive** [optional] is the mode who put the program mode deamon. Default: True
* **--proxy_url** [optional] it is you proxy. Ex: proxy.yourcompany.com:8080
* **--proxy_auth** [optional] it is your credentials for the proxy. Ex: username:password
* **--round_sensitive** [optional] it is color rounding sensitive option. Need this number > 0 ex: 3
* **--image_brightness** [optional] it is change image brignets, Support negative values ex: 15 or -15
