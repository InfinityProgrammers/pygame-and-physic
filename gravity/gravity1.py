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

dPosition = Vector2()
stars=[]
win = pygame.display.set_mode(WIN_SIZE)
pygame.init()

class Body(object):
    def __init__(self, win, x, y, mass, st = True):
        self.win = win
        self.pos = Vector2(x,y)
        self.mass = mass
        self.isStatic = st

class Planet(Body):

    def __init__ (self, win, x, y, mass, radius, color = (255,255,255), st = True):
        super().__init__(win,x,y,mass,st)
        self.radius = radius
        self.color = color

    def Draw(self):
        pygame.draw.circle(self.win, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))


class Orb(Planet):

    def __init__(self, win, x, y, mass, radius, color = (255,255,255), dispayVectors=False,st=False):
        super().__init__(win, x, y, mass, radius, color,st)
        self.vel = Vector2(0,0)
        self.p_vel = Vector2(0,0)
        self.dVec = dispayVectors
        self.forceW = Vector2(0,0)

    def Draw(self): #drawing ball
        super().Draw()
        pygame.draw.circle(self.win, (0, 100, 0), (int(self.pos.x), int(self.pos.y)), int(self.radius-2))
        if self.dVec:
            if DRAW_ACC_VEC:
                self.drawacc()
                self.p_vel=Vector2(self.vel)
            if DRAW_S_VEC:
                self.drawspeed()

    def drawacc(self): #drawing accelerate
        pygame.draw.line(self.win, (255, 0, 0),self.pos, (self.vel-self.p_vel)*ACC_VECTOR_SCALE + self.pos, 2)
    def drawspeed(self): #drawing velocity
        pygame.draw.line(self.win, (50, 50, 255),self.pos, self.vel*60 + self.pos, 2)

    def movement(self): #ball movement
        self.vel += self.forceW/self.mass*VEL_SCALE 
        self.pos += self.vel

    def Fuze(self, obj):
        self.vel = (self.vel*self.mass + obj.vel*obj.mass)/(self.mass + obj.mass)
        self.mass += obj.mass
        self.forceW += obj.forceW
        self.pos += (obj.pos - self.pos)/(1+((self.radius/obj.radius)**2))
        self.radius = math.sqrt(self.radius**2+obj.radius**2)

def redraw():
    win.fill((0, 0, 0))
    for obj in stars:
        obj.Draw()
    
def line(pos): #drawing line
    pygame.draw.line(win, (255, 255, 255), [ball.pos.x, ball.pos.y], pos, 3)

def DeltaVector(pos1,pos2,scale):
    vec = Vector2(0,0)
    distanceX = pos2.x - pos1.x
    distanceY = pos2.y - pos1.y
    distance = math.sqrt(distanceX**2+distanceY**2)
    if distance != 0:
        Sum = scale / distance**2
        vec.x = Sum*distanceX/distance
        vec.y = Sum*distanceY/distance
    return vec
    

def Gravity(object1,object2): #creating gravity force
    F = DeltaVector(object1.pos,object2.pos,G * object1.mass * object2.mass)
    if not object1.isStatic:
        object1.forceW += F
    if not object2.isStatic:
        object2.forceW -= F


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
                stars.append(ball)
                click = True
                space = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space == False:
                ball.vel = (m_pos-ball.pos) * POWER_SCALE / 60
                space = True

        if click:
            redraw()
            if not space:
                line(m_pos)
            else:
                for nr1 in range(len(stars)):
                    for nr2 in range(nr1+1,len(stars)):
                        Gravity(stars[nr1],stars[nr2])
                for obj in stars:
                    obj.movement()

                for object1 in stars:
                    for object2 in stars:
                        if object1 == object2:
                            continue
                        elif object1.pos.distance_to(object2.pos) < max(object1.radius,object2.radius):
                            object1.Fuze(object2)
                            stars.remove(object2)
                for obj in stars:
                    obj.forceW*=0



