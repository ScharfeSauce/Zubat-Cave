import pygame
import os
from settings import Settings
def sonic_power(group, active):    #Funktionsweise des Sonic Powerups
    f = ""
    s = 0
    for i in group:
        if i.position == 1:
            if active:
                f = "rock2_unten.png"
                s = -2
            else:
                f = "rock1_unten.png"
                s = -5
        elif i.position == 2:
            if active:
                f = "rock2_oben.png"
                s = -2
            else:
                f = "rock1_oben.png"
                s = -5

        i.image = pygame.image.load(os.path.join(Settings.path_image, f )).convert_alpha()
        i.image = pygame.transform.scale(i.image, i.rock_size)
        c = i.rect.bottom
        x = i.rect.centerx
        i.rect = i.image.get_rect()
        i.rect.bottom = c
        i.rect.centerx = x

        i.speed_h = s

def sonic_extra(group, active):
    for i in group:
        if active:
            i.speed_h = -2
        else:
            i.speed_h = -5