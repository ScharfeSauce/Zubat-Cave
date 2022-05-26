from typing import Set
import pygame
import os
from random import randint 
#from timer import Timer 

class Settings(object):
    window_height = 500
    window_width = 900
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    path_data = os.path.join(path_file, "player_data.json")
    standard_fp = 500
    zubat_size = (50, 50) 
    symbol_size = (20, 20)
    title = "Zubat in a Cave"
    max_ostacles = 4
    max_power = 3
    object_speed = -5
    points_position_x = window_width - 150
    points_position_y = window_height - 50
    
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