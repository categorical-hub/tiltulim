#!/usr/bin/python
__author__ = 'sagi'
import random, pygame, sys, math
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE      = (  0,   0, 255)

BGCOLOR = WHITE


spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 100)
enemies = []
hero_energy = 5

class hero(object):
    def __init__(self):
        self.x=300
        self.y=300
        self.direction = 240
        self.speed = 7.0
        self.radius = 10
        self.energy = 5

    def move(self):
        self.x = self.x + math.cos(math.radians(self.direction)) * self.speed
        self.y = self.y + math.sin(math.radians(self.direction)) * self.speed
        if self.y <= 0 + self.radius:
            self.y = 0 + self.radius
        if self.x <= 0 + self.radius:
            self.x = 0 +self. radius
        if self.x >= WINDOWWIDTH - self.radius:
            self.x = WINDOWWIDTH - self.radius
        if self.y >= WINDOWHEIGHT - self.radius:
            self.y = WINDOWHEIGHT - self.radius

    def set_direction(self, direction):
        self.direction = direction

    def draw_hero(self):
        pygame.draw.circle(DISPLAYSURF, RED, (int(self.x), int(self.y)), self.radius)
        my_font = pygame.font.Font('freesansbold.ttf', 18)
        lable = my_font.render(str(self.energy),1,WHITE)
        DISPLAYSURF.blit(lable, (self.x-self.radius + 5, self.y-self.radius))


class enemy(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.direction = 240

        self.radius = 10
        self.energy = random.randrange(4,hero_energy * 2)
        self.speed = 5.0

    def move(self):
        self.x = self.x + math.cos(math.radians(self.direction)) * self.speed
        self.y = self.y + math.sin(math.radians(self.direction)) * self.speed
        if self.y <= 0 + self.radius:
            self.y = 0 + self.radius
        if self.x <= 0 + self.radius:
            self.x = 0 +self. radius
        if self.x >= WINDOWWIDTH - self.radius:
            self.x = WINDOWWIDTH - self.radius
        if self.y >= WINDOWHEIGHT - self.radius:
            self.y = WINDOWHEIGHT - self.radius

    def set_direction(self, direction):
        self.direction = direction

    def set_speed(self, speed):
        self.speed = speed

    def draw_enemy(self):
        #pygame.draw.rect(DISPLAYSURF, RED, appleRect)

        pygame.draw.circle(DISPLAYSURF, BLUE, (int(self.x), int(self.y)), 8)
        my_font = pygame.font.Font('freesansbold.ttf', 14)
        lable = my_font.render(str(self.energy),1,WHITE)
        DISPLAYSURF.blit(lable, (self.x-self.radius + 3, self.y-self.radius))

my_hero = hero()

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    print('omfg1')
    pygame.init()
    #print(pygame.font.get_fonts())
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('TILTULIM')


    while True:
        ret = run_game()
        if ret == -1:
            return

    print('omfg')

def terminate():
    pygame.quit()
    sys.exit()


def spawn_enemy():
    if random.randrange(0,3) == 1:
        new_enemy = enemy(random.randrange(0, WINDOWWIDTH), random.randrange(0, WINDOWHEIGHT))
        enemies.append(new_enemy)

def run_game():
    global my_hero, enemies, hero_energy
    direction = my_hero.direction
    DISPLAYSURF.fill(BGCOLOR)


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == spawn_event:
                spawn_enemy()
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) :
                    direction = 180

                elif (event.key == K_RIGHT or event.key == K_d) :
                    direction = 360

                elif (event.key == K_UP or event.key == K_w):
                    direction = 270

                elif (event.key == K_DOWN or event.key == K_s):
                    direction = 90

                elif event.key == K_ESCAPE:
                    terminate()



        my_hero.set_direction(direction)
        my_hero.move()
        my_hero.draw_hero()



        for i in range(0, len(enemies)):
            try:
                delta_x = my_hero.x - enemies[i].x
                delta_y = my_hero.y - enemies[i].y
                hero_direction = math.atan2(delta_y,delta_x)*180/math.pi
                hero_distance = math.sqrt(math.pow(delta_x,2)+math.pow(delta_y,2))

                if enemies[i].energy < my_hero.energy:
                    hero_direction = -1 * hero_distance

                enemies[i].set_direction(hero_direction)
                enemies[i].move()

                for j in range(0, len(enemies) - 1):
                    if j == i: continue



                if (hero_distance<7):
                    print('col')
                    if enemies[i].energy > my_hero.energy:
                        return -1
                    else:
                        my_hero.energy += enemies[i].energy
                        hero_energy = my_hero.energy
                        enemies.remove(enemies[i])

                enemies[i].draw_enemy()

            except:
                pass


        #print ('x:' + str(x) + ' y: ' + str(y))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return 0

main()