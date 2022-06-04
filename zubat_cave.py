from msilib.schema import Icon
from typing import Set
import pygame
import os
from random import randint 
from settings import Settings, Background
from timer import Timer
from animation import Animation
from spawn_check import spawn_check   #selbst erstelllte Funktionen, ausgelagert in andere Datei
from powerups import sonic_power, sonic_extra
from login import *                   #Tkinter Anwendung
from data_save import save_state, rank

#Ich besitze keinerlei Rechte an den, in diesem Programm verwendeten Bildern.
#Mit den diesem Programm wird kein kommerzieller Gewinn erzielt.
#Die in diesem Programm verwendeten Bilder stammen von den vollgenden Internetseiten:
#'zubat.png' stammt von https://www.spriters-resource.com/ds_dsi/pokemonblackwhite/sheet/45921/ (www.spriters-resource.com)
#'rock.png' stammt von https://www.deviantart.com/redballbomb/art/Rock-Sprites-788773535 (www.deviantart.com), es wurden verschiedene Abwandlungen dieses bilges genutzt, z.B. rock1_unten.png
#'cave_stage_background.png' stammt von https://www.moddb.com/games/grapple-knight/images/level-2-the-caves (www.clipartmax.com)
#'mega.png' stammt von https://poke-monde.weebly.com/meacutega-eacutevolution.html (poke-monde.weebly.com)
#'sonic.png' stammt von https://www.clipartmax.com/max/m2i8i8Z5d3Z5Z5G6/ (www.clipartmax.com)
#'pokeball.png' stammt von https://warosu.org/vr/thread/550984 (warosu.org)
#'cave_theme.pgg' stammt von https://www.nayuki.io/page/transcription-of-pokemon-game-boy-music (www.nayuki.io)
#Ich bedanke mich bei den Contant Creatorn für ihre gute Arbeit


class Zubat(pygame.sprite.Sprite):    #Spieler
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.zubat_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.left = 20
        self.rect.centery = Settings.window_height // 2
        self.speed = 6
        self.fly = Animation([f"zubat{i}.png" for i in range(3, 5)], False, 200)
        self.up = Animation([f"zubat{i}.png" for i in range(0, 8)], False, 50)
        self.down = Animation([f"zubat{i}.png" for i in range(7, 8)], False, 50)

    def animate(self, anim):
        self.image = anim.next()
        self.image = pygame.transform.scale(self.image, Settings.zubat_size)

        c = self.rect.bottom
        x = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = c
        self.rect.centerx = x

    #Bewegen des Spielers
    def update(self):
        self.animate(self.fly)                  #dauer Animation

        press = pygame.key.get_pressed()
        if press[pygame.K_UP]:
            self.rect.top -= self.speed
            self.animate(self.up)          #bewegungs Animation
        if press[pygame.K_DOWN]:
            self.rect.top += self.speed
            self.animate(self.down)
        #Wandkollision
        if self.rect.top <= self.speed:         #verlassen des Bildschirms verhindern 
            self.rect.top += self.speed
        if self.rect.bottom >= Settings.window_height - self.speed:
            self.rect.top -= self.speed  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):      #Hindernisse
    def __init__(self, position) -> None:
        super().__init__()
        self.position = position
        if self.position == 1:                      #zwei verschiedene Arten von Bildern, Felsen von oben/unten
            self.filename = "rock1_unten.png"       #hängt davon ab welche Variable er übergeben bekommt 
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
        self.speed_h = Settings.object_speed
    
    def update(self):
        self.rect.move_ip((self.speed_h, 0)) 
        if self.rect.right <= 0:
            self.kill()
            game.rocks_dodged += 1 
            if game.mega_up == True:
                game.score += 5                           #erhaltene Punkte durch Powerup gesteigert 
            else:
                game.score += 1                           #Punkte erhalten


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Event(pygame.sprite.Sprite):      #Powerups und Erholungspunkte 
    def __init__(self, filename) -> None:
        super().__init__()
        self.event_size = (50, 50)
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.event_size)
        self.rect = self.image.get_rect()
        self.rect.left = randint(Settings.window_width, Settings.window_width * 2)
        self.rect.centery = Settings.window_height // 2
        self.speed_h = Settings.object_speed
    
    def update(self):
        self.rect.move_ip((self.speed_h, 0)) 
        if self.rect.right <= 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class LifeBar(pygame.sprite.Sprite):     #Lebensbalken 
    def __init__(self, size) -> None:
        super().__init__()
        self.bar_size = size
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "lifebar_red.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, self.bar_size)
        self.rect = self.image.get_rect()
        self.rect.left = Settings.points_position_x
        self.rect.top = Settings.points_position_y + 20
        self.scale = {'width': self.rect.width, 'height': self.rect.height}
    
    def update(self):     #größe des Balkens an Punktestand anpassen
        l = self.rect.left
        b = self.rect.bottom
        if game.mega_up:
            self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "lifebar_green.png")).convert_alpha()
        else:
            self.image_orig = pygame.image.load(os.path.join(Settings.path_image, "lifebar_red.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (self.get_scale())) 
        self.rect = self.image.get_rect()
        self.rect.left = l
        self.rect.bottom = b

        self.scale['width'] = game.fp // 5 

    def get_scale(self):
        return (self.scale['width'], self.scale['height'])

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
class Symbol(pygame.sprite.Sprite):     #Darstellung der gesammelten Powerups als kleine Bilder
    def __init__(self, filename, x_position, y_position) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, Settings.symbol_size)
        self.rect = self.image.get_rect()
        self.rect.left = x_position
        self.rect.bottom = y_position
    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
            

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = Background("cave_stage_background.png")
        self.font_message = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.font_counter = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.zubat_group = pygame.sprite.Group()
        self.rock_group = pygame.sprite.Group()
        self.ball_group = pygame.sprite.Group()        #Erholungspunkte
        self.powerup_1_group = pygame.sprite.Group()   #Mega Powerup
        self.powerup_2_group = pygame.sprite.Group()   #Sonic Powerup
        self.symbols1_group = pygame.sprite.Group()
        self.symbols2_group = pygame.sprite.Group()
        self.zubat = Zubat('zubat0.png')
        self.zubat_group.add(self.zubat)
        self.rock_timer = Timer(5000)
        self.ball_mark = 30
        self.powerup_1_mark = randint(40, 60)
        self.powerup_2_mark = randint(30, 50)
        self.increase_b = 20
        self.increase_s = 30
        self.increase_m = 30
        self.up1_timer = Timer(20000)             #Zeitlimit der Powerups, nach aktivierung 
        self.up2_timer = Timer(30000)
        self.cooldown_timer = Timer(3000)
        self.cooldown = False
        self.mega_up = False
        self.sonic_up = False
        self.game_end = False
        self.fp = Settings.standard_fp           #Wichtig: FP/ Flug Punkte, Lebensspunkte 
        self.rocks_dodged = 0
        self.score = 0
        self.powerup_1_count = 0
        self.powerup_2_count = 0
        self.life = LifeBar((self.fp // 5, 20))
        self.life_group = pygame.sprite.Group()
        self.life_group.add(self.life)
        self.volume = Settings.default_volume
    
    def game_music(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(Settings.path_music, Settings.soundtrack))
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.volume)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.game_music()
            self.watch_for_events()
            self.event()
            self.rock_spawn()
            self.symbol_count(self.powerup_1_count, self.symbols1_group, "mega.png", 10)
            self.symbol_count(self.powerup_2_count, self.symbols2_group, "sonic.png", Settings.symbol_size[1] + 20)
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
                if event.key == pygame.K_m:  #activieren des Mega Powerups
                    if self.powerup_1_count > 0:
                        self.powerup_1_count -= 1
                        self.mega_up = True
                        self.up1_timer = Timer(20000)
                if event.key == pygame.K_s:  #activieren der Sonic Powerups
                    if self.powerup_2_count > 0:
                        self.powerup_2_count -= 1
                        self.sonic_up = True
                        self.up2_timer = Timer(20000)
            if event.type == pygame.KEYUP:        
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:   #wenn die tasten losgelassen werden, werden einem Punkte abgezogen 
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
            self.powerup_2_group.update()  
            self.rock_group.update()
            self.life_group.update()

        if self.fp <= 0:
            self.zubat_group.empty()
    
    def collision(self):
        if self.cooldown_timer.is_next_stop_reached(): #benötigt für kurzzeitige unverwundbarkeit nach einem Treffer
            self.cooldown = False
            
        if self.cooldown == False:
            if pygame.sprite.groupcollide(self.zubat_group, self.rock_group, False, False, pygame.sprite.collide_mask): #collision mit hindernissen
                self.cooldown_timer = Timer(3000)
                self.cooldown = True
                if self.mega_up == False:
                    self.fp -= 50
                    if self.fp <= 0:
                        self.fp = 0
            
            if pygame.sprite.groupcollide(self.zubat_group, self.ball_group, False, True):  #event Objekte einsammeln
                self.fp = Settings.standard_fp

            if pygame.sprite.groupcollide(self.zubat_group, self.powerup_1_group, False, True):
                if self.powerup_1_count < Settings.max_power:
                    self.powerup_1_count += 1
            
            if pygame.sprite.groupcollide(self.zubat_group, self.powerup_2_group, False, True):
                if self.powerup_2_count < Settings.max_power:
                    self.powerup_2_count += 1
            
            pygame.sprite.groupcollide(self.rock_group, self.ball_group, True, False) #Sicherstellen, dass Powerups nich in Hindernissen Spawnen
            pygame.sprite.groupcollide(self.rock_group, self.powerup_1_group, True, False) 
            pygame.sprite.groupcollide(self.rock_group, self.powerup_2_group, True, False)
    
    def rock_spawn(self):
        if len(self.ball_group) == 0:
            if self.rock_timer.is_next_stop_reached():
                for r in range (0, randint(1, Settings.max_ostacles)):
                    self.rock = Obstacle(randint(1,2))
                    self.rock_group.add(self.rock)
                    spawn_check(self.rock_group, (Settings.zubat_size[0] + 40))   #Überprüfung des Abstandes aller Hindernisse zu einander, 
                                                                                  #an Größe des Spielers angepasst, dammit keine Passage unmöglich zu passieren ist
    
    def event(self):     #powerups und pokebälle spawnen
        if self.ball_mark == self.rocks_dodged:       #Spawnen von Powerups, ist abhängig von Passierten Hindernissen
            self.ball = Event("pokeball.png")
            self.ball_group.add(self.ball)
            self.increase_b += 5
            self.ball_mark += self.increase_b                      #Hinderniss Anforderrung erhöhen, um Schwierigkeit zu steigern

        if self.powerup_1_mark == self.rocks_dodged:
            self.up1 = Event("mega.png")
            self.powerup_1_group.add(self.up1)
            self.increase_m += 5
            self.powerup_1_mark += self.increase_m
        
        if self.powerup_2_mark == self.rocks_dodged:
            self.up1 = Event("sonic.png")
            self.powerup_2_group.add(self.up1)
            self.increase_s += 5
            self.powerup_2_mark += self.increase_s
        
        if self.mega_up:                                 #Zeitlimit für Powerups
            if self.up1_timer.is_next_stop_reached():
                self.mega_up = False
        
        if self.sonic_up:
            sonic_power(self.rock_group, self.sonic_up)
            sonic_extra(self.ball_group, self.sonic_up)
            sonic_extra(self.powerup_1_group, self.sonic_up)
            sonic_extra(self.powerup_2_group, self.sonic_up)
            if self.up2_timer.is_next_stop_reached():
                self.sonic_up = False
                sonic_power(self.rock_group, self.sonic_up)
                sonic_extra(self.ball_group, self.sonic_up)
                sonic_extra(self.powerup_1_group, self.sonic_up)
                sonic_extra(self.powerup_2_group, self.sonic_up)
    
    def symbol_count(self, count, group, image, offset):      #darstellen der gesammelten Powerups
        if count != len(group):
            group.empty()
            x = Settings.points_position_x
            for q in range (0, count):
                self.i = Symbol(image, x, Settings.points_position_y - offset)
                group.add(self.i)
                x += self.i.rect.width + 5
        

    def draw(self):
        if self.mega_up:             #Megapowerup sichtbar durch Farbveränderung
            self.color = [0, 255, 0]
        else:
            self.color = [255, 0, 0]
        self.fp_counter = self.font_counter.render('FP: ' + str(self.fp), True, self.color)
        self.score_counter = self.font_counter.render('Score: ' + str(self.score), True, self.color)
        self.background.draw(self.screen)
        self.zubat_group.draw(self.screen)
        self.rock_group.draw(self.screen)
        self.ball_group.draw(self.screen)
        self.powerup_1_group.draw(self.screen)
        self.powerup_2_group.draw(self.screen)
        self.life_group.draw(self.screen)
        self.symbols1_group.draw(self.screen)
        self.symbols2_group.draw(self.screen)
        if self.fp <= 0: # ausgae am ende mit bestspieler liste
            top_three = rank()                                      #Laden der Bestenliste bei Spielende
            if not self.game_end:
                save_state(app.name, self.score)
                self.game_end = True
            self.end_screen = self.font_message.render(f"You lost! Your Score is {self.score}", True, [0, 0, 0])
            self.one_screen = self.font_message.render(f"Number 1: '{top_three[0][1]}', with {top_three[0][0]} Points", True, [0, 0, 0])
            self.two_screen = self.font_message.render(f"Number 2: '{top_three[1][1]}', with {top_three[1][0]} Points", True, [0, 0, 0])
            self.three_screen = self.font_message.render(f"Number 3: '{top_three[2][1]}', with {top_three[2][0]} Points", True, [0, 0, 0])
            self.screen.blit(self.end_screen, (Settings.window_width//2 - self.end_screen.get_rect().centerx, Settings.window_height//2 - self.end_screen.get_rect().centery))
            self.screen.blit(self.one_screen, (Settings.window_width//2 - self.one_screen.get_rect().centerx, Settings.window_height//2 - self.one_screen.get_rect().centery + 30))
            self.screen.blit(self.two_screen, (Settings.window_width//2 - self.two_screen.get_rect().centerx, Settings.window_height//2 - self.two_screen.get_rect().centery + 60))
            self.screen.blit(self.three_screen, (Settings.window_width//2 - self.three_screen.get_rect().centerx, Settings.window_height//2 - self.three_screen.get_rect().centery + 90))
        self.screen.blit(self.fp_counter, (Settings.points_position_x, Settings.points_position_y))
        self.screen.blit(self.score_counter, (Settings.points_position_x, 20))
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    app = Application(master=root)  #Tkinter Anwendung, zum eingeben von Spielerdaten, gespeichert in einer Json Datei
    app.mainloop()

    game = Game()
    game.run()