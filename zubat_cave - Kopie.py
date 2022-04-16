from typing import Set
import pygame
import os
from random import randint 
from settings import Settings, Background
from timer import Timer
from animation import Animation

#Ich besitze keinerlei Rechte an den, in diesem Programm, verwendeten Bildern.
#Mit den diesem Programm wird kein kommerzieller Gewinn erzielt.
#Die in diesem Programm verwendeten Bilder stammen von den vollgenden Internetseiten:
#'djungle_rain.png' stammt von https://www.umdiewelt.de/t4455_18 (www.umdiewelt.de)
#'dragonfly.png' stammt von https://miausmiles.com/2011/incredible-random-stuff/draw-something-every-day-035 (www.miausmiles.com)
#'drop.png' stammt von http://www.clipartpanda.com/clipart_images/domain-raindrop-clip-art-19285059 (www.clipartpanda.com)
#Ich bedanke mich bei den Contan Creatorn für ihre gute Arbeit

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.dragonfly_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.centerx = Settings.dragonfly_size[0] + 10
        self.rect.bottom = Settings.window_height // 2
        self.speed = 5
        self.fly = Animation([f"zubat{i}.png" for i in range(0, 8)], False, 50)  #animations Objekt

    def update(self):
        c = self.rect.bottom                                  #position wieder auf die alte festlegen 
        x = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = c
        self.rect.centerx = x

    #Bewegen des Spielers
    def watch_for_move(self):
        press = pygame.key.get_pressed()                       #registiert Tastendruck
        if press[pygame.K_UP]:
            self.rect.top -= self.speed
            self.image = self.fly.next()                       #animation
            self.update()                                      #update aufrufen
        if press[pygame.K_DOWN]:
            self.rect.top += self.speed
            self.image = self.fly.next()
            self.update()
        #Wandkollision
        if self.rect.top <= 5:
            self.rect.top += 5
        if self.rect.bottom >= Settings.window_height -5:
            self.rect.top -= 5  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.drop_size = (90, 180)
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.drop_size)
        self.rect = self.image.get_rect()
        self.rect.left = Settings.window_width
        self.rect.top = Settings.window_height - self.drop_size[1]
        self.speed_h = -5
    
    def update(self):
        self.rect.move_ip((self.speed_h, 0)) 
        if self.rect.right <= 0:
            self.kill()                                          #löschen der Sprites wenn sie Unten ankommen
            game.rocks_dodged += 1                               #erhöhen der ausgewichenen Hindernisse

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("Cave_Stage_Background.png")
        self.dragonfly_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.running = True
        self.counter = 0
        self.dragonflys = 0
        self.lives = 3
        self.rocks_dodged = 0
        self.dragonfly = Dragonfly('zubat0.png')
        self.dragonfly_group.add(self.dragonfly)
        self.rock = Obstacle("rock2 - Kopie2.png")
        self.rock_group.add(self.rock)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.player()
            self.elements()
            self.draw()
        pygame.quit()
        pygame.font.quit()      

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_ESCAPE:   
                    self.running = False
            elif event.type == pygame.QUIT:         
                self.running = False

    def player(self):
        self.dragonfly.watch_for_move()      

    def elements(self):
        self.rock_group.update()
        
    def draw(self):
        self.background.draw(self.screen)
        self.dragonfly_group.draw(self.screen)
        self.rock_group.draw(self.screen)
        #falls alle Leben verbraucht sind wird der End Screen gezeigt
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()