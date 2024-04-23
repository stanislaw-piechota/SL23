"""Module holding all constant values to configure game"""
from os import path
import pygame


# FONTS
pygame.font.init()
FONT = pygame.font.SysFont("verdana", 40)
TITLE_FONT = pygame.font.SysFont("verdana", 80)

# MUSIC
pygame.mixer.init()
BACKGROUND_MUSIC = pygame.mixer.Sound(path.join(path.dirname(__file__), "src/", "background_music.wav"))
BACKGROUND_MUSIC.set_volume(0.1)
END_MUSIC = pygame.mixer.Sound(path.join(path.dirname(__file__), "src/", "end_music.wav"))
LOGIN_MUSIC = pygame.mixer.Sound(path.join(path.dirname(__file__), "src/", "login_music.wav"))
POWERUP_MUSIC = pygame.mixer.Sound(path.join(path.dirname(__file__), "src/", "powerup_music.wav"))

# COLORS
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 255)
# NOTE: obsolete instruction
CELL_COLORS = [(0, 0, 0), (0, 0, 0)]
POINT_COLOR = (184, 16, 67)
READY_COLOR = (0, 255, 0)
POWER_COLOR = (0, 185, 255)

# SIZES
SCREEN_WIDTH = 1400  # in pixels
SCREEN_HEIGHT = 700  # in pixels
FIELD_WIDTH = 20  # in cells
SCORE_PANEL_BASIC_WIDTH = 200  # in pixels
SPRITE_SIZE = 400
BORDER_WIDTH = 8-FIELD_WIDTH//5
CELL_SIZE = (SCREEN_WIDTH-SCORE_PANEL_BASIC_WIDTH)//FIELD_WIDTH  # in pixels
FIELD_HEIGHT = SCREEN_HEIGHT//CELL_SIZE  # in cels
MARGIN_TOP = (SCREEN_HEIGHT - FIELD_HEIGHT*CELL_SIZE)//2  # in pixels
MARGIN_LEFT = SCREEN_WIDTH - SCORE_PANEL_BASIC_WIDTH - FIELD_WIDTH*CELL_SIZE  # in pixels
SCORE_PANEL_WIDTH = SCORE_PANEL_BASIC_WIDTH - 2*BORDER_WIDTH
OFFSET = (CELL_SIZE+BORDER_WIDTH)//2

# CONTROLS
FPS = 60
PLAYER1 = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
PLAYER2 = (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
PLAYER3 = (pygame.K_KP5, pygame.K_KP2, pygame.K_KP3, pygame.K_KP1)
PLAYER4 = (pygame.K_i, pygame.K_k, pygame.K_l, pygame.K_j)
CONTROLS = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]
PROBABILITY_OF_HOLE = 0.1
SPRITE_SPEED = 4
PACKMAN_SPEED = 3
MAX_PACKMANS_PER_PLAYER = 5
SPRITE_ANIMATION_MAX_STEPS = 20
ROUND_TIME = 60
MAX_NUMBER_OF_PLAYERS = 4
MIN_NUMBER_OF_PLAYRES = 1
ENEMY_INACTIVE_TIME = 10
POWERUPS_PER_PLAYER = 2

# POINTS
KILL_POINTS = -25
DOT_POINT = 2
SPECIAL_POINTS = 50
