import pygame, sys, math
import config
from config import *
from pygame.math import Vector2

clock = pygame.time.Clock()
delta = 0
tickrate = TICK_RATE

click = False
space = False

G = G_CONST
power = 0
angleSpeed = 0

vel = Vector2()
dPosition = Vector2()

win = pygame.display.set_mode(WIN_SIZE)
pygame.init()

class Body(object):
    def __init__(self, win, x, y, mass, st = True):
        self.win = win
        self.x = x
        self.y = y
        self.mass = mass
        self.isStatic = st

class Planet(Body):

    def __init__ (self, win, x, y, mass, radius, color = (255,255,255), st = True):
        super().__init__(win,x,y,mass,st)
        self.radius = radius
        self.color = color

    def Draw(self):
        pygame.draw.circle(self.win, self.color, (int(self.x), int(self.y)), int(self.radius))


class Orb(Planet):

    def __init__(self, win, x, y, mass, radius, color = (255,255,255), dispayVectors=False,st=False):
        super().__init__(win, x, y, mass, radius, color,st)
        self.vel = Vector2()
        self.p_vel = Vector2()
        self.dVec = dispayVectors

    def Draw(self): #drawing ball
        super().Draw()
        pygame.draw.circle(self.win, (0, 100, 0), (int(self.x), int(self.y)), self.radius-2)
        if self.dVec:
            if DRAW_ACC_VEC:
                self.drawacc()
                self.p_vel=Vector2(self.vel)
            if DRAW_S_VEC:
                self.drawspeed()

    def drawacc(self): #drawing accelerate
        pygame.draw.line(self.win, (255, 0, 0),(self.x, self.y), (self.x+(self.vel.x-self.p_vel.x)*ACC_VECTOR_SCALE, self.y+(self.vel.y-self.p_vel.y)*ACC_VECTOR_SCALE), 2)

    def drawspeed(self): #drawing velocity
        pygame.draw.line(self.win, (50, 50, 255),(self.x,self.y), (self.vel.x*SPEED_VECTOR_SCALE+self.x, self.vel.y*SPEED_VECTOR_SCALE+self.y), 2)

    def movement(self): #ball movement
        self.x += self.vel.x
        self.y += self.vel.y

def redraw(): #TODO list of elements to draw
    win.fill((0, 0, 0))
    planet1.Draw() #draw planet
    planet2.Draw()
    ball.Draw()
    
def line(pos): #drawing line
    pygame.draw.line(win, (255, 255, 255), [ball.x, ball.y], pos, 3)

def DeltaVector(pos1,pos2,scale):
    vec = Vector2(0,0)
    distanceX = pos2.x - pos1.x
    distanceY = pos2.y - pos1.y
    distance = math.sqrt(distanceX**2+distanceY**2)
    if distance != 0:
        Sum = scale / distance**2
        vec.x = Sum*distanceX/distance
        vec.y = Sum*distanceY/distance
        print(vec.x,vec.y)
        return vec

def Gravity(object1,object2): #creating gravity force
    acc = DeltaVector(Vector2(object1.x,object1.y),Vector2(object2.x,object2.y),G * object1.mass * object2.mass)
    if not object1.isStatic:
        object1.vel.x += acc.x
        object1.vel.y += acc.y
        object1.movement()
    if not object2.isStatic:
        object2.vel.x += -acc.x
        object2.vel.y += -acc.y
        object2.movement()

planet1 = Planet(win,PLANET_POS.x,PLANET_POS.y,PLANET_MASS,PLANET_SIZE,PLANET_COLOR)
planet1.Draw()
planet2 = Planet(win,PLANET_POS.x+700,PLANET_POS.y,PLANET_MASS*3/2,PLANET_SIZE*3/2,PLANET_COLOR)
planet2.Draw()

while True:
    delta+= clock.tick()/1000.0
    pygame.display.update()

    while delta > 1/tickrate:

        delta -= 1/tickrate
        m_pos = Vector2 (pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = m_pos
                ball = Orb(win, m_pos.x, m_pos.y, ORB_MASS, ORB_SIZE,ORB_COLOR, True)
                click = True
                space = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space == False:
                ball.vel = Vector2(m_pos.x-ball.x,m_pos.y-ball.y)*POWER_SCALE
                space = True

        if click:
            redraw()
            if not space:
                line(m_pos)
            else:
                Gravity(ball,planet1)
                Gravity(ball,planet2)



