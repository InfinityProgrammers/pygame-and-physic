import pygame, sys, math
from pygame.math import Vector2

win = pygame.display.set_mode((800, 400))

class pilka(object):
    def __init__(self, x, y, radius, color):
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.tickrate = 10
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


x = 0
y = 0
time = 0
power = 0
angle = 0
shoot = False
vel = Vector2(0, 0)
gravacc = Vector2(0, 0)


while True:
    print(angle)
    golfball.delta += golfball.clock.tick()/ 1000.0
    while golfball.delta > 1/golfball.tickrate:
        golfball.delta -= 1/golfball.tickrate
        if shoot:
            print("leci")
            if angle > 90:
                vel.x -= round(math.sin(angle) * power)
                vel.y -= round(math.cos(angle) * power)
                golfball.x += vel.x
                golfball.y += vel.y
            else:
                vel.x += round(math.sin(angle)*power)
                vel.y -= round(math.cos(angle)*power)
                golfball.x += vel.x
                golfball.y += vel.y
        pos = pygame.mouse.get_pos()
        poss = Vector2(pos[0]-golfball.x, pos[1]-golfball.y)
        line = [(golfball.x, golfball.y), pos]
        redrawwindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shoot == False:
                    shoot = True
                    print("leci")
                    x = golfball.x
                    y = golfball.y
                    power = math.sqrt((line[1][0]-line[0][0])**2+(line[0][1]-line[1][1])**2)/8
                    angle = poss.angle_to(Vector2(1, 0))




