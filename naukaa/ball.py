import pygame, sys, math
from pygame.math import Vector2

win = pygame.display.set_mode((800, 400))

class pilka(object):
    def __init__(self, x, y, radius, color):
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.tickrate = 120
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def Draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius-1)

def redrawwindow():
    win.fill((0, 150, 150))
    golfball.Draw(win)
    pygame.draw.line(win, (0, 0, 0), line[0], line[1])
    pygame.display.update()

golfball = pilka(400, 394, 6, (255, 255, 255))
bound = False
shoot = False
gravacc = 0.04
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
            if golfball.y > 394 or golfball.y < 6:
                vel.x /= 1.2
                vel.y /= -1.3
                golfball.y = 6 if golfball.y<6 else 394
                if abs(vel.x) < 0.1 and abs(vel.y) < 0.1:
                    golfball.y = 394
                    shoot = False
            if golfball.x < 6 or golfball.x > 794:
                vel.x /= -1.2
                golfball.x = 6 if golfball.x<6 else 794
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
                vel.x = round(math.cos(math.radians(angle)) * power) / 12
                vel.y = -round(math.sin(math.radians(angle)) * power) / 12
