"""
Module holding all static configurable values,
mostly connected to visuals and objects starting parameters.
"""

import pygame
pygame.font.init()  # neccessary to create font as a constant

STARTING_TICK = 150  # increases speed of entire game
SCREEN_SIZE = (1200, 700)
BACKGROUND_COLOR = (0, 0, 0)
OBJECTS_COLOR = (255, 255, 255)
TEXT_COLOR = (125, 125, 125)
BALL_RADIUS = 10
PAD_SIZE = (20, 200)
PAD_1_KEYS = [pygame.K_w, pygame.K_s]
PAD_2_KEYS = [pygame.K_UP, pygame.K_DOWN]
# change speed of ball/pad independently from another one
PAD_SPEED = 4
BALL_SPEED = 12
FONT = pygame.font.SysFont('bahnschrift', 128)
