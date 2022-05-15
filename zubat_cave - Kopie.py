from typing import Set
import pygame
import os
from random import randint 
from settings import Settings, Background
from timer import Timer
from animation import Animation
from spawn_check import spawn_check
from powerups import sonic_power
from login import *
from data_save import save_state, rank

#Ich besitze keinerlei Rechte an den, in diesem Programm, verwendeten Bildern.
#Mit den diesem Programm wird kein kommerzieller Gewinn erzielt.
#Die in diesem Programm verwendeten Bilder stammen von den vollgenden Internetseiten:
#'djungle_rain.png' stammt von https://www.umdiewelt.de/t4455_18 (www.umdiewelt.de)
#'dragonfly.png' stammt von https://miausmiles.com/2011/incredible-random-stuff/draw-something-every-day-035 (www.miausmiles.com)
#'drop.png' stammt von http://www.clipartpanda.com/clipart_images/domain-raindrop-clip-art-19285059 (www.clipartpanda.com)
#Ich bedanke mich bei den Contan Creatorn für ihre gute Arbeit


class Zubat(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.zubat_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.left = 20
        self.rect.centery = Settings.window_height // 2
        self.speed = 6
        self.fly = Animation([f"zubat{i}.png" for i in range(0, 8)], False, 50)  #animations Objekt

    def animate(self):
        self.image = self.fly.next()                       #animation
        self.image = pygame.transform.scale(self.image, Settings.zubat_size) #Größe neu anpassen

        c = self.rect.bottom                                  #position wieder auf die alte festlegen 
        x = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = c
        self.rect.centerx = x

    #Bewegen des Spielers
    def update(self):
        press = pygame.key.get_pressed()                       #registiert Tastendruck
        if press[pygame.K_UP]:
            self.rect.top -= self.speed
            self.animate()                                      #update aufrufen
        if press[pygame.K_DOWN]:
            self.rect.top += self.speed
            self.animate()
        #Wandkollision
        if self.rect.top <= self.speed:
            self.rect.top += self.speed
        if self.rect.bottom >= Settings.window_height - self.speed:
            self.rect.top -= self.speed  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        if self.position == 1:
            self.filename = "rock1_unten.png"
        elif self.position == 2:
            self.filename = "rock1_oben.png"
        self.rock_size = (90, randint(90, Settings.window_height - (80 + Settings.zubat_size[1])))
        self.image = pygame.image.load(os.path.join(Settings.path_image, self.filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.rock_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.window_width, Settings.window_width * 2)
        if self.position == 1:
            self.rect.bottom = Settings.window_height
        if self.position == 2:
            self.rect.top = 0
        self.speed_h = -5
    
    def update(self):
        self.rect.move_ip((self.speed_h, 0)) 
        if self.rect.right <= 0:
            self.kill()                                          #löschen der Sprites wenn sie Unten ankommen
            if game.mega_up == True:
                game.rocks_dodged += 5                               #erhöhen der ausgewichenen Hindernisse
            else:
                game.rocks_dodged += 1


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Event(pygame.sprite.Sprite):
    def __init__(self, filename, speed) -> None:
        super().__init__()
        self.ball_size = (50, 50)
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.ball_size)
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.window_width, Settings.window_width * 2)
        self.rect.centery = Settings.window_height // 2
        self.speed_h = speed
    
    def update(self):
        self.rect.move_ip((self.speed_h, 0)) 
        if self.rect.right <= 0:
            self.kill()                                          #löschen der Sprites wenn sie Unten ankommen

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
        self.running = True
        self.background = Background("Cave_Stage_Background.png")
        self.font_message = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.zubat_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()
        self.powerup_1_group = pygame.sprite.Group()
        self.powerup_2_group = pygame.sprite.Group()
        self.zubat = Zubat('zubat0.png')
        self.zubat_group.add(self.zubat)
        self.rock_timer = Timer(5000)
        self.powerup_1_mark = randint(30, 50)
        self.powerup_2_mark = randint(30, 50)
        self.ball_mark = 30
        self.up1_timer = Timer(20000)
        self.up2_timer = Timer(20000)
        self.cooldown_timer = Timer(3000)
        self.cooldown = False
        self.mega_up = False
        self.sound_up = False
        self.game_end = False
        self.fp = 1000
        self.rocks_dodged = 0
        self.powerup_1_count = 0
        self.powerup_2_count = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.event()
            self.rock_spawn()
            self.update()
            self.collision()
            self.draw()
        pygame.quit()
        pygame.font.quit()      

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_ESCAPE:   
                    self.running = False
                if event.key == pygame.K_m:  # activieren des ersten Powerups
                    if self.powerup_1_count > 0:
                        self.mega_up = True
                        self.up1_timer = Timer(20000)
                        print("Mega Up")
                if event.key == pygame.K_s:
                    if self.powerup_2_count > 0:
                        self.sound_up = True
                        self.up2_timer = Timer(20000)
                        print("Sonic Up")
            if event.type == pygame.KEYUP:        
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:   # wenn die tasten losgelassen werden, werden einem Punkte abgezogen 
                    if self.fp != 0:
                        if self.mega_up == False:
                            self.fp -= 10
            elif event.type == pygame.QUIT:         
                self.running = False

    def update(self):
        if self.fp > 0:
            self.zubat_group.update()    
            self.ball_group.update()
            self.powerup_1_group.update()  
            self.rock_group.update()

            if self.fp <= 0:
                self.zubat_group.empty()              #spieler wird entfernt 
    
    def collision(self):
        if self.cooldown_timer.is_next_stop_reached():
            self.cooldown = False
            
        if self.cooldown == False:
            #print("hass")
            if pygame.sprite.groupcollide(self.zubat_group, self.rock_group, False, False, pygame.sprite.collide_mask): #collision mit hindernissen
                #print("hit")
                self.cooldown_timer = Timer(3000)
                self.cooldown = True
                if self.mega_up == False:
                    self.fp -= 50
                    if self.fp <= 0:
                        self.fp = 0
                    print("hit")
                    print(self.fp)
            
            if pygame.sprite.groupcollide(self.zubat_group, self.ball_group, False, True):
                self.fp = 1000
                print(self.fp)

            if pygame.sprite.groupcollide(self.zubat_group, self.powerup_1_group, False, True):
                if self.powerup_1_count < Settings.max_power:
                    self.powerup_1_count += 1
            
            if pygame.sprite.groupcollide(self.zubat_group, self.powerup_2_group, False, True):
                if self.powerup_2_count < Settings.max_power:
                    self.powerup_2_count += 1
    
    def rock_spawn(self):
        if len(self.ball_group) == 0:
            if self.rock_timer.is_next_stop_reached():
                for r in range (0, randint(1, Settings.max_ostacles)):  #Anzahl der Gleichzeitigen Hindernisse in Settings mimimal 1
                    self.rock = Obstacle(randint(1,2))
                    self.rock_group.add(self.rock)
                    spawn_check(self.rock_group, 90)
    
    def event(self):                                   #powerups und pokebälle spawnen
        if self.ball_mark == self.rocks_dodged: #pokebälle
            #self.rock_group.empty()
            self.ball = Event("rock2_unten.png", -2)
            self.ball_group.add(self.ball)
            self.ball_mark += 20 #zeitabstand verlängern, um schwierigkeit zu steigern

        if self.powerup_1_mark == self.rocks_dodged:
            self.up1 = Event("drop.png", -5)
            self.powerup_1_group.add(self.up1)
            self.powerup_1_mark += 20
        
        if self.powerup_2_mark == self.rocks_dodged:
            self.up1 = Event("dragonfly.png", -5)
            self.powerup_2_group.add(self.up1)
            self.powerup_2_mark += 20
        
        if self.mega_up:
            if self.up1_timer.is_next_stop_reached():
                self.mega_up = False
        
        if self.sound_up:
            sonic_power(self.rock_group, self.sound_up)
            if self.up2_timer.is_next_stop_reached():
                self.sound_up = False
                sonic_power(self.rock_group, self.sound_up)

    def draw(self):
        #print(pygame.time.get_ticks())
        self.background.draw(self.screen)
        self.zubat_group.draw(self.screen)
        self.rock_group.draw(self.screen)
        self.ball_group.draw(self.screen)
        self.powerup_1_group.draw(self.screen)
        self.powerup_2_group.draw(self.screen)
        if self.fp <= 0: # ausgae am ende mit bestspieler liste
            top_three = rank()
            if not self.game_end:
                save_state(app.name, self.rocks_dodged)
                self.game_end = True
            self.end_screen = self.font_message.render(f"You lost! Your Score is {self.rocks_dodged}", True, [0, 0, 0])
            self.best_screen = self.font_message.render(f"The best player was '{top_three[0][1]}', with {top_three[0][0]} Points", True, [0, 0, 0])
            #self.retry_screen = self.font_message.render("Press [x] if you want to try again", True, [0, 0, 0])
            self.screen.blit(self.end_screen, (Settings.window_width//2 - self.end_screen.get_rect().centerx, Settings.window_height//2 - self.end_screen.get_rect().centery))
            self.screen.blit(self.best_screen, (Settings.window_width//2 - self.best_screen.get_rect().centerx, Settings.window_height//2 - self.best_screen.get_rect().centery + 30))
            #self.screen.blit(self.retry_screen, (Settings.window_width//2 - self.retry_screen.get_rect().centerx, Settings.window_height//2 - self.retry_screen.get_rect().centery + 60))
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    app = Application(master=root)
    app.mainloop()

    game = Game()
    game.run()