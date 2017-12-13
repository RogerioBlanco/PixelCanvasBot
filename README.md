# PixelCanvasBot

This is a functional bot for pixelcanvas.io.
We will not provide you with a faster drawing.
It does not allow you to easily draw your image. You need to spend some effort.
This bot can draw images that you can't normally draw on your place.
 
### What you can do with this?
Well, you can draw some image and try replicate in pixelcanvas.io. You can combine with your friends or clan, whatever for combine forces to draw more quickly or defend your 'territory'.

### I can use any image and this bot will draw for me?
You can use any image. 
Converted your image colors to nearest PixelCanvas.io color for every pixel.
Conversion result images if not exist in ./img/.cache folder created.
You can interfere with this file or you can preview it to be drawn.

# Installation

## get python
install python for yours operation systems in here https://www.python.org/downloads/release/python-2713/
Recomments 'Python 2.7' 32bit versions,
Important Python 3 not supported (Help wanted a few critical error) 

## Download bot

### With git
PixelCanvas.io frequently changes the API validation system.
We are updated after we notice. It can be a bit late, we can not guarantee it in any way. Recommend GIT for the current use

#### If you have not installed git?
* get git and install from https://git-scm.com/downloads

#### Clone bot
Open Terminal (git bash, cmd vs.)
enter this command

* git clone https://github.com/RogerioBlanco/PixelCanvasBot.git

### Optional downlad from release
https://github.com/RogerioBlanco/PixelCanvasBot/archive/v1.0.zip

## Setup bot 
go bot directory

* cd PixelCanvasBot
* python ./setup.py

# Using

## Geting yours fingerprint Chrome or chromium
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

## What is each parameter? 
    Need to help?
    Try it 'python ./main.py --help' maybe more usefull.
* [required] **-i** or **--image**          it is the image you want to draw.

* [required] **-f** or **--fingerprint**    it is your unique code. You can get in the requisition when you open Chrome DevTools.

* [required] **-x** or **--start_x**        it is the point X axis what you want to begin. Ex: 156

* [required] **-y** or **--start_y**        it is the point y axis what you want to begin. Ex: -4000

* [optional] **--colors_ignored**           Colors of your image that will be ignored. Ex: 0 1 2 3 8 15

* [optional] **--draw_strategy**            draw strategy default by: *randomize* Avaiable strategy list : 

    * *linear* :    line by line paint, 
    
    * *randomize* : pixel paint random coordinates, 
    
    * *status* :    not painted only list paint status --support colors ignored parameters, don't suppurt sketch mode--
    
    * *sketch* :    Don't fill image drawing image only bordes. see more information https://github.com/RogerioBlanco/PixelCanvasBot/issues/6
    
    * *tlc* :       Print start fill Top Left Corner -randomize select all pixel start with corner-
        
    * *trc* :       Print start fill TopRightCorner -randomize select all pixel start with corner-
        
    * *blc* :       Print start fill BottomLeftCorner -randomize select all pixel start with corner-
        
    * *brc* :       Print start fill BottomRightCorner -randomize select all pixel start with corner-

#### Note:
The Corner based strategyes are defined using a number of reference points shown in the figure below:
![image](http://cordex-australasia.wdfiles.com/local--files/rcm-domains/CORDEXDomainDef.jpg)
    
    
* [optional] **--mode_defensive**           is the mode who put the program mode deamon. Default: True

* [optional] **--proxy_url**                it is you proxy. Ex: proxy.yourcompany.com:8080

* [optional] **--proxy_auth**               it is your credentials for the proxy. Ex: username:password

* [optional] **--round_sensitive**          it is color rounding sensitive option. Need this number > 0 ex: 3

* [optional] **--image_brightness**         it is change image brignets, Support negative values ex: 15 or -15

#### Note:
*--round_sensitive* *--image_brightness* parameters to You can change the degree of rounding precision,
or you can make the picture that is to be drawn darker - lighter.
see work result: https://github.com/RogerioBlanco/PixelCanvasBot/issues/45

# Update bot with last changes
### Clear local changes (if you changes source code) 
* git reset --hard
### Update from server server
* git pull -ff
# External: thanks for reference
https://github.com/possatti/pixelbot/blob/master/README.md 
