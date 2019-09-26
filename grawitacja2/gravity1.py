import pygame, sys, math
from pygame.math import Vector2

win = pygame.display.set_mode((1024, 800))

clock = pygame.time.Clock()
delta = 0
tickrate = 60

click = False
space = False
G = 6.674 * 10 ** (-18)
power = 0

poz = Vector2()
vel = Vector2()
pozycja = Vector2()

pygame.init()
class Cialo(object):

    def __init__(self, speed, x, y, radius):
        self.speed = speed
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = Vector2()
        self.acc = Vector2()

    def Draw(self, win):
        pygame.draw.circle(win, (255, 100, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, (0, 100, 0), (int(self.x), int(self.y)), self.radius-2)

    def movement(self):
        self.vel += self.acc
        self.x += self.vel.x
        self.y += self.vel.y

def redraw():
    win.fill((0, 0, 0))
    pilka.Draw(win)
    drawacc(pilka.x, pilka.y)
    drawspeed(pilka.x, pilka.y, pilka.vel.x, pilka.vel.y)

def line(pos):
    pygame.draw.line(win, (255, 255, 255), [pilka.x, pilka.y], pos, 3)

def planeta():
    pygame.draw.circle(win, (0, 128, 0), (512, 400), 100)
    global mass_p
    mass_p = 5.972 * 10 ** 19

def drawacc(x, y):
    if click and space:
        pygame.draw.line(win, (255, 0, 0),(int(x), int(y)), (512, 400), 2)

def drawspeed(x, y, xx, yy):
    if click and space:
        poz.x += xx+vel.x
        poz.y += yy-vel.y
        pygame.draw.line(win, (0, 0, 255), (int(x),int(y)), poz, 2)

def speed(power, accel, vel):
    angle = pozycja.angle_to(Vector2(0,0))
    angle = math.radians(angle)
    vel.x = power*math.cos(angle)/4
    vel.y = power*math.sin(angle)/4
    dlugosc = math.sqrt((vel.x) ** 2 + (vel.y) ** 2)
    ##if accel != 0:
    ##if angle1 > 90:
    ##    vel = vel.rotate(angle1-90)
    pilka.x += vel.x
    pilka.y -= vel.y

def Force():
    if click and space:
        distancex = pilka.x-512
        distancey = pilka.y-400
        distance = math.sqrt(distancex**2+distancey**2)
        if distance != 0:
            sumaccel = G*mass_p/distance**2
            pilka.acc.x = abs(sumaccel*distancex/distance)
            pilka.acc.y = abs(sumaccel*distancey/distance)
            if distancex > 0:
                pilka.acc.x = -pilka.acc.x
            if distancey > 0:
                pilka.acc.y = -pilka.acc.y
            pilka.movement()
            speed(power, sumaccel, vel)

while True:
    delta+= clock.tick()/1000.0
    planeta()
    pygame.display.update()
    while delta > 1/tickrate:
        delta -= 1/tickrate
        Force()
        if click == True:
            redraw()
            if space == False:
                pos = pygame.mouse.get_pos()
                line(pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                posss = pygame.mouse.get_pos()
                pilka = Cialo(win, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10)
                click = True
                space = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space == False:
                    poss = pygame.mouse.get_pos()
                    poz.x = poss[0]
                    poz.y = poss[1]
                    power = math.sqrt((poss[0] - pilka.x) ** 2 + (poss[1] - pilka.y) ** 2)/16
                    pozycja = Vector2((poz.x-posss[0]), (poz.y-posss[1]))
                    space = True
