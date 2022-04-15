from typing import Set
import pygame
import os
from random import randint 
from timer import Timer 

class Settings(object):
    window_height = 500
    window_width = 900
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images1")
    dragonfly_size = (50, 60) 
    title = "Zubat in a Cave"
    
    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path_image, name)

class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass