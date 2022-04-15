from email.mime import image
import pygame
from pygame.constants import (QUIT, K_ESCAPE, KEYDOWN)
import os
from settings import Settings
from timer import Timer

class Animation(object):
    def __init__(self, namelist, endless, animationtime, colorkey=None):
        self.images = []
        self.endless = endless
        self.timer = Timer(animationtime)
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self):
        if self.timer.is_next_stop_reached():
            self.imageindex += 1 
            if self.imageindex >= len(self.images):
                game.FLY = False
                if self.endless:
                    self.imageindex = len(self.images) - 1
                else:
                    self.imageindex = 0 
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False