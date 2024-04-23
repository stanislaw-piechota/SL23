"""
Module holding constant values for configuration of looks
"""

import pygame
from os import path

# better not change, as background is fixed size
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 90
LEFT_WIDTH, LEFT_HEIGHT = 400, 400
RIGHT_WIDTH, RIGHT_HEIGHT = 250, 550
ANIMATION_STEPS = 50

# Place on the screen is limited so max number of characters = 5
# 10 creatures in total
# otherwise program crashes
CHARACTERS_NUMBER = 3
SIDES = ["<", ">"]
STARTING_SIDE = "<"

pygame.init()
BACKGROUND = pygame.image.load(path.join(path.dirname(__file__), "src/background.png"))
STARTING_TEXT = pygame.image.load(path.join(path.dirname(__file__), "src/starting_text.png"))
LOSING_TEXT = pygame.image.load(path.join(path.dirname(__file__), "src/lost_text.png"))
WIN_TEXT = pygame.image.load(path.join(path.dirname(__file__), "src/win_text.png"))
CANNIBAL = pygame.image.load(path.join(path.dirname(__file__), "src/cannibal.png"))
MISSIONARY = pygame.image.load(path.join(path.dirname(__file__), "src/missionarie.png"))
FONT = pygame.font.Font(path.join(path.dirname(__file__), "src/CASTELAR.ttf"), 24)
SOUND_PATH = path.join(path.dirname(__file__), "src/background_music.mp3")
HINT_TEXT = "{} moves left to win"
FINAL_TEXT = "You made {} moves but the minimum was {} moves"
TEXT_COLOR = (0, 0, 0)

# playability and hardness of the game are strongly dependent on capacity
# for certain values of capacity and numbers of characters there may be
# no solutions and causes the game to crush
RAFT_CAPACITY = 2
RAFT_IMAGE = pygame.image.load(path.join(path.dirname(__file__), "src/raft.png"))
RAFT = pygame.transform.scale(RAFT_IMAGE, (RAFT_CAPACITY*CANNIBAL.get_width(), RAFT_IMAGE.get_height()))
RAFT_POSITIONS = ((400, 600), (900-RAFT_CAPACITY*CANNIBAL.get_width(), 600))  # these are values determined with tries
RAFT_SPEED = 4
