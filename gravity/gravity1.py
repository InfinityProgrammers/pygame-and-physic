import pygame, sys, math
import config
from pygame.math import Vector2

 ### wszystkie zmienne

c = config

clock = pygame.time.Clock()
delta = 0
tickrate = 60

click = False
space = False

G = c.G_CONST
power = 0
angleSpeed = 0

poz = Vector2()
vel = Vector2()
pozycja = Vector2()

win = pygame.display.set_mode(c.WIN_SIZE)
pygame.init()


class Orb(object):

    def __init__(self, speed, x, y, radius):
        self.speed = speed
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = Vector2()
        self.acc = Vector2()

    def Draw(self, win): #drawing ball
        pygame.draw.circle(win, (255, 100, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, (0, 100, 0), (int(self.x), int(self.y)), self.radius-2)
    def movement(self): #ball movement
        self.vel += self.acc
        self.x += self.vel.x
        self.y += self.vel.y


def redraw(): #aktualizacja ekranu co tick
    win.fill((0, 0, 0))
    pygame.draw.circle(win, (0, 128, 0), c.PLANET_POS, c.PLANET_SIZE) #draw planet
    ball.Draw(win)
    if click and space:
        drawacc(ball.x, ball.y, ball.acc.x, ball.acc.y)
        drawspeed(ball.x, ball.y, ball.vel.x + vel.x, ball.vel.y-vel.y)
    
def line(pos): #drawing line
    pygame.draw.line(win, (255, 255, 255), [ball.x, ball.y], pos, 3)

def drawacc(x, y, xx, yy): #drawing accelerate
    pygame.draw.line(win, (255, 0, 0),(int(x), int(y)), ((xx*600+x),(yy*600+y)), 2)

def drawspeed(x, y, xx, yy): #drawing velocity
    pygame.draw.line(win, (50, 50, 255),(x, y), (xx*60/2+x, yy*60/2+y), 2)

def planeta(): #planet variables
    global mass_p
    mass_p = c.PLANET_MASS
    pygame.draw.circle(win, (0, 128, 0),c.PLANET_POS, c.PLANET_SIZE)

def speed(): #manipulacja wektorem predkosci
    angle4 = angleSpeed #kopiuje zmienną
    print(angleSpeed)
    angle4 = math.radians(angle4)
    vel.x = round(power * math.cos(angle4) / 3)
    vel.y = round(power * math.sin(angle4) / 3)
    ball.x += vel.x
    ball.y -= vel.y
    print(ball.vel)

def Force(): #generowanie siły grawitacji
    if click and space:
        global angleSpeed
        distancex = ball.x-c.PLANET_POS[0]
        distancey = ball.y-c.PLANET_POS[1]
        distance = math.sqrt(distancex**2+distancey**2)
        if distance != 0:
            sumaccel = G*mass_p/distance**2
            ball.acc.x = abs(sumaccel*distancex/distance)
            ball.acc.y = abs(sumaccel*distancey/distance)
            if distancex > 0:
                ball.acc.x = -ball.acc.x
            if distancey > 0:
                ball.acc.y = -ball.acc.y
            acc = Vector2(-(ball.x-c.PLANET_POS[0]),-(ball.y-c.PLANET_POS[1])) #wektor przyspieszneia
            angle = acc.angle_to(Vector2(-1, 0)) #kąt między wektorem przyspieszenia a osią ox
            angleSpeed = pozycja.angle_to(Vector2(1, 0)) ##kąt między osią ox a linią mocy(prędkosci)
            speed() #manipulacja wektorem predkosci
            ball.movement() #aktualizacja położenia piłki
planeta()
fps = 0
while True:
    delta+= clock.tick()/1000.0
    pygame.display.update()

    while delta > 1/tickrate: ## tyknięcia programu
        delta -= 1/tickrate
        print(fps)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = pos
                ball = Orb(win, pos[0], pos[1], c.ORB_SIZE) #tworze obiekt
                click = True
                clockwise = False
                counterclockwise = False
                space = False
                check = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space == False:
                poz.x = pos[0]
                poz.y = pos[1]
                power = math.sqrt((pos[0] - ball.x) ** 2 + (pos[1] - ball.y) ** 2)/16 #liczę moc obliczając długosc wektora
                pozycja = Vector2((poz.x-start_pos[0]), (poz.y-start_pos[1])) #wektor prędkosci
                space = True
        Force()
        if click == True: ## klikniecie = rysuj obiekt ponownie
            redraw()
            if space == False: ## rysowanie lini
                line(pos)


