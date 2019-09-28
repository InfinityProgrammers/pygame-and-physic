import pygame, sys, math
import config
from config import *
from pygame.math import Vector2

win = pygame.display.set_mode(WIN_SIZE)
#TODO: recode this bcs is awful
class ball(object):
    def __init__(self, x, y, radius, color):
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.tickrate = TICK_RATE
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def Draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius-1)

def redrawwindow():
    win.fill(WIN_COLOR)
    golfball.Draw(win)
    pygame.draw.line(win, (0, 0, 0), line[0], line[1])
    pygame.display.update()

golfball = ball(WIN_SIZE[0]/2, WIN_SIZE[1]-BALL_RADIUS, BALL_RADIUS, BALL_COLOR)
bound = False
shoot = False
gravacc = GRAV_ACC
vel = Vector2(0, 0)

while True:
    golfball.delta += golfball.clock.tick()/ 1000.0
    pos = pygame.mouse.get_pos()
    line = [(golfball.x, golfball.y), pos]
    redrawwindow()
    while golfball.delta > 1/golfball.tickrate:
        golfball.delta -= 1/golfball.tickrate
        if shoot:
            vel.y += gravacc
            golfball.x += vel.x
            golfball.y += vel.y
            if golfball.y > WIN_SIZE[1]-BALL_RADIUS or golfball.y < BALL_RADIUS:
                vel.x /= SD_X
                vel.y /= -SD_Y
                golfball.y = BALL_RADIUS if golfball.y<BALL_RADIUS else WIN_SIZE[1]-BALL_RADIUS
                if abs(vel.x) < 0.1 and abs(vel.y) < 0.1:
                    golfball.y = WIN_SIZE[1]-BALL_RADIUS
                    shoot = False
            if golfball.x < BALL_RADIUS or golfball.x > WIN_SIZE[0]-BALL_RADIUS:
                vel.x /= -SD_X
                golfball.x = BALL_RADIUS if golfball.x<BALL_RADIUS else WIN_SIZE[0]-BALL_RADIUS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shoot == False:
                    shoot= True
                posss = pygame.mouse.get_pos()
                poss = Vector2(posss[0] - golfball.x, posss[1] - golfball.y)
                power = math.sqrt((golfball.x-posss[0])**2+(golfball.y-posss[1])**2)/3
                angle = poss.angle_to(Vector2(1, 0))
                vel.x = round(math.cos(math.radians(angle)) * power) * POWER_SCALE
                vel.y = -round(math.sin(math.radians(angle)) * power) * POWER_SCALE
