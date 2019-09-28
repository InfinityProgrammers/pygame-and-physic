import pygame
from pygame.math import Vector2

WIN_SIZE = (1600,800)

G_CONST = 6.674 * 10 ** (-17)

PLANET_POS = Vector2(512,400)
PLANET_MASS = 5.972 * 10 ** 19
PLANET_SIZE = 75
PLANET_COLOR = (0,128,0)

ORB_SIZE = 10
ORB_COLOR = (255, 100, 100)

DRAW_S_VEC = True
DRAW_ACC_VEC = True
SPEED_VECTOR_SCALE = 20
ACC_VECTOR_SCALE = 20*20

POWER_SCALE = 1/30