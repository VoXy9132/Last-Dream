#Moduls
import pygame as pg
import sys
import os
from ctypes import *
from time import time
from random import random, choice

#init
pg.init()
width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1) * 0.93

def check_pos_in_area(pos_object, pos_area):
    if pos_area[2] > pos_object[0] > pos_area[0] and pos_area[3] > pos_object[1] > pos_area[1]:
        return True
    else:
        return False

def search_the_winner(count):
    temp_random = choice(range(3))
    if count == temp_random:
        return ('not a loser', temp_random)
    elif count == 0 and temp_random == 2:
        return ('loser', temp_random)
    elif count == 2 and temp_random == 0:
        return ('winner', temp_random)
    elif count < temp_random and count != 0 and temp_random != 2:
        return ('winner', temp_random)
    else:
        return ('loser', temp_random)

def filterscreen(screen):
    global width, height
    n = 150
    for i in range(0, int(height), int(height / n)):
        pg.draw.rect(screen, (0, 0, 0), (0, i, width, 1), int(height / n / 1.9))

def frame_display(fps=60):
    pg.time.Clock().tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.flip()

def Comparision(Pos1, Pos2, Diff=1):
    if Pos1[0] + (Diff - 1) * Pos1[2] < Pos2[0] and Pos1[2] + Pos1[0] > Pos2[0] + Pos2[2] * Diff:
        if Pos1[1] + (Diff - 1) * Pos1[3] < Pos2[1] and Pos1[3] + Pos1[1] > Pos2[1] + Pos2[3] * Diff:
            return True
    else:
        return False


#Class
class NPC:
    health = 1
    frame = 0
    animation = 0

    def __init__(self, name, size):
        self.name = name
        self.k = size[0] / size[1]
        self.image = [pg.image.load(fr'Image\NPC\{name}\{name}{count_an}.png') for count_an in range(1, 3)]

    def create(self):
        self.frame += 1
        if self.frame >= 2:
            self.frame = 0
            self.animation += 1
            if self.animation >= 2:
                self.animation = 0
        return self.image[self.animation]

class Player:
    health_max = health = 2
    speed = 1
    inventory = {'hills': 0, 'bombs': 0}
    size = (1, 2)
    animation = {'stand_up': [pg.image.load(r'Image\Player\Up.png')],
                 'stand_down': [pg.image.load(r'Image\Player\Down.png')],
                 'goes_up': [pg.image.load(fr'Image\Player\Up{temp}.png') for temp in range(1,3)],
                 'goes_left': [pg.image.load(f'Image\Player\Left{temp}.png') for temp in range(1,3)],
                 'goes_right': [pg.image.load(f'Image\Player\Right{temp}.png') for temp in range(1,3)],
                 'goes_down': [pg.image.load(f'Image\Player\Down{temp}.png') for temp in range(1,3)]}
    animation_current = [0, 1, animation['stand_down'], False]
    cadr = 0
    k = 320 / 624

    def animation_cadr(self):
        self.cadr += 1
        if self.cadr >= 3:
            self.cadr = 0
            self.animation_current[0] += 1

    def create(self, screen, screen_size, Move):
        self.animation_cadr()
        self.animation_current[3] = False
        if Move:
            if pg.key.get_pressed()[pg.K_w]:
                self.animation_current[2] = self.animation['goes_up']
                self.animation_current[1] = 2
                self.animation_current[3] = True
            elif pg.key.get_pressed()[pg.K_s]:
                self.animation_current[2] = self.animation['goes_down']
                self.animation_current[1] = 2
                self.animation_current[3] = True
            elif pg.key.get_pressed()[pg.K_a]:
                self.animation_current[2] = self.animation['goes_left']
                self.animation_current[1] = 2
                self.animation_current[3] = True
            elif pg.key.get_pressed()[pg.K_d]:
                self.animation_current[2] = self.animation['goes_right']
                self.animation_current[1] = 2
                self.animation_current[3] = True
            else:
                self.animation_current[1] = 1
        if self.animation_current[0] >= self.animation_current[1]:
            self.animation_current[0] = 0
        temp_pgtransform = pg.transform.scale(self.animation_current[2][self.animation_current[0]],
                                       (int(screen_size[1] * 0.2 * self.k), int(screen_size[1] * 0.2)))
        screen.blit(temp_pgtransform, temp_pgtransform.get_rect(center=(screen_size[0] / 2, screen_size[1] / 2)))

    def add_health(self, add_hp=-1):
        if add_hp > 0:
            if self.health_max >= self.health + add_hp:
                self.health += add_hp

    def add_item(self, item='hills', add_count=1):
        if self.inventory[item] >= self.inventory[item] + add_count:
            self.inventory[item] += self.inventory[item] + add_count
        elif self.inventory[item] + add_count <= 0:
            self.inventory[item] = 0

class Interface:
    health_image = pg.image.load('Image\Interface\health .png')
    def __init__(self, screen_size=(0, 0)):
        self.health_pos = (screen_size[0] * 0.05, screen_size[1] * 0.9, screen_size[0] * 0.35, screen_size[1] * 0.07)
        self.inventory_pos = (screen_size[0] * 0.7, screen_size[1] * 0.9, screen_size[0] * 0.25, screen_size[1] * 0.07)
        self.exit_pos = (screen_size[0] * 0.05, screen_size[1] * 0.05, screen_size[0] * 0.14, screen_size[1] * 0.07)
        self.screen_size = screen_size

    def create(self, screen, health_player):
        pg.draw.rect(screen, (255, 255, 255), (int(self.screen_size[0] * 0.05), int(self.screen_size[1] * 0.85),
                                         int(self.screen_size[0] * 0.15),
                                         int(self.screen_size[1] * 0.1)), int(height / 200))
        health_temp_tr = pg.transform.scale(self.health_image, (int(self.screen_size[1] * 0.095 * (288 / 256)),
                                                               int(self.screen_size[1] * 0.095)))
        for count_health in range(health_player):
            screen.blit(health_temp_tr, (int(self.screen_size[0] * 0.06 + self.screen_size[1] * 0.095 * (288 / 256) *
                                             count_health + self.screen_size[0] * 0.01 * count_health),
                                         int(self.screen_size[1] * 0.8525)))


class Gaming:
    sound_dead_health = pg.mixer.Sound('sounds\hit.wav')
    sound_dead_mob = pg.mixer.Sound('sounds\Death.wav')
    sound_dead_player = pg.mixer.Sound('sounds\Game_Over.wav')
    npc = [NPC('Zombie', (400, 400)), NPC('whosthat', (320, 560)), NPC('Big - eared Nanny', (288, 560))]
    BattleFrameimage = pg.image.load(fr'Image\Interface\battle screen.png')
    money = 0
    background = []
    back_y = 3
    back_x = 3
    load_image = [pg.image.load('Image\Objects\glass.png')]
    for temp_count_back_y in range(back_y):
        for temp_count_back_x in range(back_x):
            background.append([temp_count_back_x, temp_count_back_y])
    cadr = 0
    Battle = None
    move = True

    def __init__(self, width, height):
        self.interface = Interface((width, height))
        self.player = Player()
        self.screen_size = (width, height)
        temp_background = []
        for temp_back in range(len(self.background)):
            temp_background.append([(self.background[temp_back][0] * (width / (self.back_x - 2))
                                     - (width / (self.back_x - 2))),
                                          (self.background[temp_back][1] * (height / (self.back_y - 2)) -
                                           (height / (self.back_y - 2)))])

        self.background = temp_background

    def create(self, screen, screen_size):
        if self.Battle == None:
            self.move = True
        else:
            self.move = False
        speed = self.screen_size[0] * 0.01
        if self.move:
            for temp_back in range(len(self.background)):
                if pg.key.get_pressed()[pg.K_w]:
                    self.background[temp_back][1] = int(self.background[temp_back][1] + speed)
                    if self.background[temp_back][1] >= screen_size[1]:
                        self.background[temp_back][1] = int(-screen_size[1] / (self.back_y - 2))
                elif pg.key.get_pressed()[pg.K_s]:
                    self.background[temp_back][1] = int(self.background[temp_back][1] - speed)
                    if self.background[temp_back][1] <= -screen_size[1] / (self.back_y - 2):
                        self.background[temp_back][1] = int(screen_size[1])
                elif pg.key.get_pressed()[pg.K_a]:
                    self.background[temp_back][0] = int(self.background[temp_back][0] + speed)
                    if self.background[temp_back][0] >= screen_size[0]:
                        self.background[temp_back][0] = int(-(screen_size[0] / (self.back_x - 2)))
                elif pg.key.get_pressed()[pg.K_d]:
                    self.background[temp_back][0] = int(self.background[temp_back][0] - speed)
                    if self.background[temp_back][0] <= -screen_size[0] / (self.back_x - 2):
                        self.background[temp_back][0] = int(screen_size[0])

        for temp_back in self.background:
            screen.blit(pg.transform.scale(self.load_image[0], (int(self.screen_size[0] / (self.back_x - 2)),
                                                                int(self.screen_size[1] / (self.back_y - 2)))),
                        temp_back)
        self.player.create(screen, screen_size, self.move)
        if self.Battle == None and random() >= 0.8 and random() >= 0.8:
            self.Battle = Battle(self.BattleFrameimage, choice(self.npc), screen_size)
            pg.mixer.music.load('sounds\Battle.wav')
            pg.mixer.music.play()
        elif self.Battle != None:
            temp_result = self.Battle.create(screen, screen_size)
            if temp_result == 'win':
                self.player.health = self.player.health_max
                self.Battle = None
                self.sound_dead_mob.play()
                pg.mixer.music.load('sounds\Music.wav')
                pg.mixer.music.play()
            elif temp_result == 'defeat':
                self.player.health -= 1
                self.sound_dead_health.play()
                if self.player.health == 0:
                    self.sound_dead_player.play(maxtime=2500)
                    pg.mixer.music.load('sounds\Music.wav')
                    pg.mixer.music.play()
                    self.Battle = None
                    self.player.health = self.player.health_max
        self.interface.create(screen, self.player.health)

class Button:
    clamp_sound = pg.mixer.Sound(r'sounds\button.wav')
    colors = {'clamp': (255, 100, 100), 'standart': False, 'clamp_off': (255, 255, 255)}
    def __init__(self, image, position, highlighting=False):
        position = [int(temp) for temp in position]
        self.image = pg.transform.scale(image, (position[2], position[3]))
        self.position = position
        self.color = self.colors['standart']
        self.highlighting = highlighting

    def create(self, screen):
        screen.blit(self.image, self.position)
        if self.highlighting:
            if self.color:
                rect_position = (self.position[0], self.position[1], self.position[2],
                                 self.position[3])
                pg.draw.rect(screen, self.color, rect_position, int(self.position[3] * 0.03))


    def event(self):
        event_position = (self.position[0], self.position[1], self.position[2] + self.position[0],
                          self.position[3] + self.position[1])
        if self.highlighting:
            if check_pos_in_area(pg.mouse.get_pos(), event_position):
                self.color = self.colors['clamp_off']
                if pg.mouse.get_pressed()[0]:
                    self.color = self.colors['clamp']
                    self.clamp_sound.play()
                    return True
            else:
                self.color = self.colors['standart']
            return False
        else:
            if check_pos_in_area(pg.mouse.get_pos(), event_position):
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.clamp_sound.play()
                            return True
                if pg.mouse.get_pressed()[0]:
                    self.clamp_sound.play()
                    return True
            return False
class Battle:
    attacks_name = ('cut', 'paper', 'stone')
    attacks_frame = None
    text_winner_rule = None
    color_took = (255, 0, 0)
    def __init__(self, BFI, npc, screen_size):
        width, height = screen_size
        self.BattleFrameimage = BFI
        self.npc_im = npc
        self.cadr_end = None
        self.BFI_attack = [Button(pg.image.load(fr'Image\Attack\{temp_image_name}_Attack.png'),
                                  (int(width * 0.47), int(height * 0.025 + (height - height * 0.15) / 5 * temp_count),
                                   (int(height * 0.15 * 2)),
                                    int((height - height * 0.15) / 5)
                                  )) for temp_image_name, temp_count in (('Cut', 0), ('Paper', 1), ('Stone', 2))]


    def create(self, screen, screen_size):
        font = pg.font.Font(pg.font.match_font('impact.ttf'), int(screen_size[1] * 0.075))
        width, height = screen_size
        screen.blit(pg.transform.scale(self.BattleFrameimage, (int(width * 0.45), int(height * 0.825))), (int(width * 0.015),
                                                                                                    int(height * 0.025)))
        for BFI_att in self.BFI_attack:
            BFI_att.create(screen)
        BFI_mob_im_tr = pg.transform.scale(self.npc_im.create(), (int(width * 0.35 * (self.npc_im.k)),
                                                                  int(height * 0.7)))
        screen.blit(BFI_mob_im_tr, BFI_mob_im_tr.get_rect(center = (int(width * 0.465 / 2), int(height * 0.90 / 2))))
        screen.blit(font.render(self.npc_im.name, False, (255, 255, 255)), (int(width * 0.045), int(height * 0.06)))
        if self.cadr_end == None:
            x = 0
        for temp_click_attack in range(len(self.BFI_attack)):
            if self.BFI_attack[temp_click_attack].event():
                self.text_winner_rule = search_the_winner(temp_click_attack)
                self.color_took = (255, 0, 0)
        if self.text_winner_rule != None:
            screen.blit(font.render(fr'Mob took the {self.attacks_name[self.text_winner_rule[1]]}', False,
                                    self.color_took), (int(width * 0.75), int(height * 0.06)))
            if self.color_took == (255, 0, 0):
                self.color_took = (255, 255, 255)
            if self.text_winner_rule[0] == 'winner':
                self.text_winner_rule = None
                return 'win'
            elif self.text_winner_rule[0] == 'loser':
                self.text_winner_rule = None
                return  'defeat'
        self.text_winner_rule = None
        return None




#width, height = 800, 600

#image_load
LAST_DREAM_logo_menu = pg.image.load('Image\Main_menu\logo.png')
LAST_DREAM_start_menu = pg.image.load('Image\Main_menu\start.png')
LAST_DREAM_exit_menu = pg.image.load('Image\Main_menu\exit.png')

#Button_load
button_menu_start = Button(LAST_DREAM_start_menu, (width * 0.4, height * 0.6, width * 0.2, height * 0.12))
button_menu_exit = Button(LAST_DREAM_exit_menu, (width * 0.4, height * 0.77, width * 0.2, height * 0.12))

temp_count = 1
temp_time = 0


#Code
pg.display.set_caption('Last dream')
pg.display.set_icon(pg.image.load('Image\Window\icon.png'))
screen = pg.display.set_mode((width, height))
main_menu = True
game_role = False
pg.mixer.music.load('sounds\Music.wav')
pg.mixer.music.play()
while True:
    game = Gaming(width, height)
    while main_menu:
        temp_count += 1
        temp_time_start = time()
        screen.fill((0, 0, 0))
        screen.blit(pg.transform.scale(LAST_DREAM_logo_menu, (int(width * 0.9), int(height * 0.5))),
                    (width * 0.05, height * 0.05))
        button_menu_start.create(screen)
        if button_menu_start.event():
            game_role = True
            main_menu = False
        button_menu_exit.create(screen)
        if button_menu_exit.event():
            pg.quit()
            sys.exit()
        filterscreen(screen)
        frame_display()
        temp_time += time() - temp_time_start
        if temp_count == 100:
            print(temp_time / temp_count)
            temp_count = 1
            temp_time = 0

    while game_role:
        bind = pg.event.get()
        screen.fill((0, 0, 0))
        game.create(screen, [width, height])
        filterscreen(screen)
        frame_display()