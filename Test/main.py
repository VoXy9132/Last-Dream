import pygame as pg
import sys
from ctypes import windll
from random import random

def PY_QUITGAME():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.flip()


class Battle:
    def __init__(self, BFI, BFI_attack, npc):
        self.BattleFrameimage = BFI
        self.BFI_attack = BFI_attack
        self.npc_im = npc

    def create(self, screen, screen_size):
        width, height = screen_size
        screen.blit(pg.transform.scale(self.BattleFrameimage, (int(width * 0.45), int(height * 0.85))), (int(width * 0.015),
                                                                                                    int(height * 0.025)))
        for temp_count_frame_pos in range(len(self.BFI_attack)):
            screen.blit(pg.transform.scale(self.BFI_attack[temp_count_frame_pos], (int(width * 0.25),
                                                                              int((height - height * 0.15) / 5))),
                        (int(width * 0.47), int(height * 0.025 + (height - height * 0.15) / 5 * temp_count_frame_pos)))
        BFI_mob_im_tr = pg.transform.scale(self.npc_im.create(), (int(width * 0.35 * (self.npc_im.k)),
                                                                  int(height * 0.7)))
        screen.blit(BFI_mob_im_tr, BFI_mob_im_tr.get_rect(center = (int(width * 0.465 / 2), int(height * 0.90 / 2))))


class NPC:
    health = 3
    frame = 0
    animation = 0

    def __init__(self, name, size):
        self.name = name
        self.k = size[0] / size[1]
        self.image = [pg.image.load(fr'Test\Mobs\{name}{count_an}.png') for count_an in range(1, 3)]

    def create(self):
        self.frame += 1
        if self.frame >= 7:
            self.frame = 0
            self.animation += 1
            if self.animation >= 2:
                self.animation = 0
        return self.image[self.animation]


pg.init()
width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1) * 0.9
screen = pg.display.set_mode((width, height))
FPS = pg.time.Clock()
x = 0
#Image
whosthat = NPC('whosthat', (320, 560))
BattleFrameimage = pg.image.load(fr'Test\Attack\battle screen.png')
BFI_attack = [pg.image.load(fr'Test\Attack\{temp_count_attack}_Attack.png') for temp_count_attack in ['Cut',
                                                                                             'Paper',
                                                                                             'Stone']]

#
rule = False
while True:
    FPS.tick(60)
    x += 1
    if x == 10:
        x = 0
    screen.fill((x, x, x))
    if random() >= 0.85 and random() >= 0.9 and not rule:
        rule = True
        batle = Battle(BattleFrameimage, BFI_attack, whosthat)
    if rule:
        batle.create(screen, (width, height))
# Attack Frame pos

# Attack Frame Buttons pos

# Attack Frame npc pos

    PY_QUITGAME()
