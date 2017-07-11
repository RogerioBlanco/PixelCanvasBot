#!/usr/bin/env python

import time, random
from calc_axis import CalcAxis
from matrix import Matrix
from colors import EnumColor
from i18n import I18n


class Strategy(object):
    def apply(self):
        raise NotImplementedError()
        
class Randomize(Strategy):
    
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.size_limit = self.bot.image.width * self.bot.image.height
        self.colors_ignored = colors_ignored

    def apply(self):
        count = 0
        while count <= self.size_limit:
            x, y, color = self.roll_dice(self.bot.canvas)
            if self.bot.canvas.get_color(x, y) != color and not color in self.colors_ignored:
                self.bot.paint(x, y, color)
            count += 1
                
    def roll_dice(self, canvas):
        rnd_x = self.random(self.bot.start_x, self.bot.start_x + self.bot.image.width  - 1)
        rnd_y = self.random(self.bot.start_y, self.bot.start_y + self.bot.image.height - 1)
        color = EnumColor.rgb(self.bot.image.pix[rnd_x - self.bot.start_x, rnd_y - self.bot.start_y])
        if canvas.get_color(rnd_x, rnd_y) == color:
            return self.roll_dice(canvas)
        return rnd_x, rnd_y, color
        
    def random(self, start, end):
        return random.randint(start, end)

class Linear(Strategy):
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored
        
    def apply(self):
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x,y])
                if self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y) != color and not color in self.colors_ignored:
                    self.bot.paint(self.bot.start_x + x, self.bot.start_y + y, color)
                    
                    
class Status(Strategy):
    def __init__(self, bot, colors_ignored):
        self.bot = bot
        self.colors_ignored = colors_ignored
        
    def apply(self):
        px_total = self.bot.image.height * self.bot.image.width
        px_ok = 0
        px_not_yet = 0
        for y in xrange(self.bot.image.height):
            for x in xrange(self.bot.image.width):
                color = EnumColor.rgb(self.bot.image.pix[x,y])
                px_ok = px_ok + 1
                if self.bot.canvas.get_color(self.bot.start_x + x, self.bot.start_y + y) != color and not color in self.colors_ignored:
                    px_not_yet = px_not_yet + 1
                    px_ok = px_ok - 1
        print(I18n.get('Total: %s painted: %s Not painted %s') % (str(px_total), str(px_ok), str(px_not_yet)))
        time.sleep(60)

class FactoryStrategy(object):

    @staticmethod
    def build(strategy, bot, colors_ignored):
        if strategy == 'randomize':
            return Randomize(bot, colors_ignored)
        
        if strategy == 'linear':
            return Linear(bot, colors_ignored)
        
        if strategy == 'status':
            return Status(bot, colors_ignored)
            
        return Randomize(bot, colors_ignored)#Default strategy
