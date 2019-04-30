# TraanvasBot

[![Build Status](https://travis-ci.org/traa-pixelcanvas/TraanvasBot.svg?branch=master)](https://travis-ci.org/traa-pixelcanvas/TraanvasBot)

This is a fork of Rogerio's bot for pixelcanvas.io, it has blackjack *and* hookers!
It does not draw faster than placing pixels manually, but it can automate drawing for short spans of time until pixelcanvas.io requests a new captcha token.

### What you can do with this?

Well, you can draw some image and try replicate it in pixelcanvas.io. You can unite with your friends or clan to coordinate your pixel placement better, or defend your 'territory'.

### I can use any image and this bot will draw for me?

You can use any image. The bot will convert your image colors to nearest PixelCanvas.io color for every pixel. Converted images will be placed the ./img/.cache folder if they don't already exist.

# Installation

## Get Python

Download and install python for your operating system from here https://www.python.org/downloads/

**Only Python 3.7 and higher is officially supported**. Using python 2.7 will almost definitely cause issues.

If you are on Windows, ensure you add Python to PATH when installing. Python sometimes calls this setting "Add Python to environment variables". If it is already installed and not in PATH, follow the instructions on this website to add it: https://geek-university.com/python/add-python-to-the-windows-path/

## Download bot

### With git

PixelCanvas.io frequently changes the API validation system. The bot will be updated when we notice. It may be a bit late, and updates are not guaranteed in any way. We recommend using git for the most up to date version.

#### If you have not installed git?

* Get git and install from https://git-scm.com/downloads

#### Clone bot

Open Terminal (git bash, cmd, etc.) and enter this command

* `git clone https://github.com/traa-pixelcanvas/TraanvasBot.git`

### Or, download lastest zip archive [not recommended]

https://github.com/traa-pixelcanvas/TraanvasBot/archive/master.zip

## Setup bot

Navigate to the directory with the Bot

* `cd path-to-directory/TraanvasBot`
* `python setup.py`
    * If you get an error about your pip version being too high, just run the command it tells you to.

If you are on windows, you may need to use backslashes (\\) instead of forward slashes (/) in your path.

If you run into errors on a UNIX machine (Linux/macOS) it might help to run the setup file as a superuser (only as a last resort):

* `sudo python setup.py`

# Usage

## Getting your fingerprint with Chrome

* Go to http://pixelcanvas.io
* Press **F12** to open DevTools
* Open **network** tab
* In **filter** type '**pixel**'
* Place a pixel at any coordinates on the canvas
* In the DevTools window click the request named *pixel*
* Open **headers** tab
* Scoll down to find your fingerprint under **Request Playload**

![image](https://user-images.githubusercontent.com/12828465/28237968-24ca07cc-694a-11e7-9df3-32b4d737b44e.png)

## Basic example with only required parameters:

* `python ./main.py -i <image.png> -f <fingerprint> -x <x> -y <y>`

If the image is not in the same folder as the code, you will need to put its path before it, e.g.: /user/path_to_image/image.png

You should also delete the quotations around your fingerprint, so it looks like this: `e4bca63b3e65a4c7f7aba06818783c47`

The `x` and `y` coordinates are where you want the very top left pixel of your template to sit on the canvas.

## Parameter descriptions

Use `python ./main.py --help` for documentation in your terminal.

* [required] **-i** or **--image**          is the image you want to draw.

* [required] **-f** or **--fingerprint**    is your unique code. See 'Getting your fingerprint with Chrome' above

* [required] **-x** or **--start_x**        is the leftmost X coordinate your template will be placed at. Ex: 156

* [required] **-y** or **--start_y**        is the topmost Y coordinate your template will be placed at. Ex: -4000

* [optional] **-ci** or **--colors_ignored**           is the index of a color in pixelcanvas.io's palette (see reference image below). Pixels of this color in your template will be treated as transparent. By default, transparent pixels and color index 16 (#5B0909) are considered ignored.

* [optional] **-cno** or **--colors_not_overwrite**     is the index of a color in pixelcanvas.io's palette (see reference image below). The bot will avoid overwriting existing canvas pixels of the specified color.

![image](https://i.imgur.com/xUr22sn.png)

Additional color: index 16, hexcode #5B0909

* [optional] **-ds** or **--draw_strategy**            is the strategy the bot will use when deciding how to paint your image.  *spiral* is used by default.

    * *linear* :    paint line by line, left to right, top to bottom.

    * *linear_vertical* :    paint line by line, top to bottom, left to right.

    * *p_linear* :  deprioritize pixels with more transparency in the original image, then paint the priority groups line by line, left to right, top to bottom

    * *qf* :        quickfill; paint every second pixel line by line, left to right, top to bottom. Will draw a 5x5 square in this order:

            | 01 | 14 | 02 | 15 | 03 |
            | 16 | 04 | 17 | 05 | 18 |
            | 06 | 19 | 07 | 20 | 08 |
            | 21 | 09 | 22 | 10 | 23 |
            | 11 | 24 | 12 | 25 | 13 |

    * *randomize* : paint random coordinates within the template area.

    * *status* :    no painting; bot prints comparison of progress on the canvas compared to the given template. Supports **--colors_ignored** and **--colors_not_overwrite**.

    * *sketch* :    attempt to sketch edges in the template image. See: https://github.com/RogerioBlanco/PixelCanvasBot/issues/6

    * *detect* :    ~~Wait time detector. Don't fill image drawing random color pixel to random coordinates every time. Ignored start point and ignored image. this strategy return wait time in any coordinates with pixelcanvas.io [experimental:notFinished]~~ currently broken

    * *radiate* :    fill outwards in a circle from a random point on the template, picks points on it's edge at random. You can pick the point it paints from with the -px and -py arguments.

    * *spiral* :    fill outwards in a circle from a random point on the template, paints these points in a spiral. You can pick the point it paints from with the -px and -py arguments.

    * *tlc* :       fill outwards from the Top Left Corner

    * *trc* :       fill outwards from the Top Right Corner

    * *blc* :       fill outwards from the Bottom Left Corner

    * *brc* :       fill outwards from the Bottom Right Corner

    * *cnb* :       fill outwards from the Centre North Boundary

    * *csb* :       fill outwards from the Centre South Boundary

    * *cwb* :       fill outwards from the Centre West Boundary

    * *ceb* :       fill outwards from the Centre East Boundary

    * *cpd* :       fill outwards from the Centre Point Domain

#### Note:

The rcm-domain based strategies are defined using a number of reference points shown in the figure below:
![image](http://cordex-australasia.wdfiles.com/local--files/rcm-domains/CORDEXDomainDef.jpg)

This strategy will walk the next pixel to be painted randomly from the chosen origin. There may be performance issues with large images.

* [optional] **--mode_defensive**           is a flag to control what the bot will do after finishing a stragtegy. For example with `--draw_strategy linear --mode_defensive False` the bot will not begin again at the start when it finishes iterating through the template once. Usage: `--mode_defensive {True|False}` Default: True

* [optional] **--proxy_url**                is a proxy you want the bot to use. Usage: `--proxy_url <address>:<port>` Note: many proxys are detected and blocked by pixelcanvas.io
j
* [optional] **--proxy_auth**               is your proxy credentials. Usage: `--proxy_auth <username>:<password>`

* [optional] **--round_sensitive**          is a value that modifies how colors are rounded when quantizing input images. Higher values make rounding less sensitive. Must be greater than zero. Default: 1

* [optional] **--image_brightness**         is a brightness modifier for quantizing your image. Supports negative values. Default: 0
#### Note:
*--round_sensitive* *--image_brightness* : more details here https://github.com/RogerioBlanco/PixelCanvasBot/issues/45

* [optional] **--QR_text**     is a text string to be represented as a QR code. The image is outputted as ./img/QRcode.png
Using this flag will cause the bot to ignore the -i tag, and output a QR code instead.

* [optional] **--QR_scale**    is a scale multiplier for generating a QR code. Minimum: 1 Default: 3

* [optional] **--xreversed**    is a True or False flag that determines which side to begin drawing from when using `--draw_strategy linear`. Default: False

* [optional] **--yreversed**    is a True or False flag that determines which side to begin drawing from when using `--draw_strategy linear`. Default: False

* [optional] **--notify** is a True or False flag that toggles desktop notifications when your bot needs you to do a capcha. Default: False

* [optional] **-px** or **--point_x** is the x coordinate (relative to the canvas) you wish the spiral or ratiate strategy to start from on your template.

* [optional] **-py** or **--point_y** is the y coordinate (relative to the canvas) you wish the spiral or ratiate strategy to start from on your template.

#### Note:

The reverse parameters only work on the linear draw strategies (linear and quickfill). Use to choose which corner to draw linearly from (default is top left corner).

# Update bot with last changes

### Clear local changes (if you changed the source code)

* `git reset --hard`

### Update lastest changes from server

* `git pull -ff`

# External: thanks for reference

https://github.com/possatti/pixelbot/blob/master/README.md


# Languages:

## Choosing language.

If you wish to use a language that is not your system language, or the bot isn't using your system language...

* On *nix systems, run `LANG=` followed by your preferred language in the command line.
* On Windows systems, run `set LANG=` followed by your preferred language in the command line.

See specified languages in `i18n.py`.

## Changing/adding translations.

If you need a language added, get our attention by [submitting an issue](https://github.com/traa-pixelcanvas/TraanvasBot/issues/new) or doing the translations yourself and sending a pull request [here](https://github.com/traa-pixelcanvas/TraanvasBot/pulls).
