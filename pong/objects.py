"""
Module which contains object responsible for gameplay
and graphic representation on the screen
"""

import functions
import pygame
from settings import *
from math import sqrt


class Ball():
    """
    Object which flies through the screen
    and collides with pads

    Args:
        screen (pygame.surface.Surface): display area
        scoreboard (objects.Scoreboard): object containg points variables
    """
    def __init__(self, screen: pygame.surface.Surface, scoreboard):
        self.screen = screen
        self.scoreboard = scoreboard
        self.dx, self.dy = functions.rand_direction()
        self.touches_vertical_wall = False
        self.set_beginning_position()
        self.show()
        self.speed = sqrt(self.dx**2 + self.dy**2)

    def set_beginning_position(self):
        self.rect = pygame.Rect(SCREEN_SIZE[0]//2-BALL_RADIUS,
                                SCREEN_SIZE[1]//2-BALL_RADIUS,
                                BALL_RADIUS*2, BALL_RADIUS*2)

    def show(self):
        pygame.draw.rect(self.screen, OBJECTS_COLOR, self.rect)

    def update_direction(self):
        """
        Changes ball direction if touches horizontal walls
        and changes values of the flag touches_vertical_wall
        which pauses the game

        Args:
            None

        Returns:
            None
        """
        if self.rect.centerx + BALL_RADIUS >= SCREEN_SIZE[0]:
            self.touches_vertical_wall = True
            self.scoreboard.left_points += 1
        elif self.rect.centerx - BALL_RADIUS <= 0:
            self.touches_vertical_wall = True
            self.scoreboard.right_points += 1
        if self.rect.centery + BALL_RADIUS >= SCREEN_SIZE[1] or\
                self.rect.centery - BALL_RADIUS <= 0:
            self.dy *= -1

    def update_position(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy


class Pad():
    """
    Pallete which is controlled by the player

    Args:
        screen (pygame.surface.Surface): display area
        x_position (int): x coordinate where pad should be located,
                          varies for left and right pad
        keys (list[int]): list of ascii codes representing keys for control
    """
    def __init__(self, screen: pygame.surface.Surface, x_position: int,
                 keys: list[int]):
        self.screen = screen
        self.keys = keys
        self.x_position = x_position
        self.moving_up = False
        self.moving_down = False
        self.set_beginning_position()
        self.speed_history = [0 for _ in range(20)]
        self.average_speed = 0

    def set_beginning_position(self):
        self.rect = pygame.Rect(self.x_position,
                                (SCREEN_SIZE[1]-PAD_SIZE[1])//2,
                                PAD_SIZE[0], PAD_SIZE[1])

    def show(self):
        pygame.draw.rect(self.screen, OBJECTS_COLOR, self.rect)

    def update_position(self, dy: int):
        """
        Updates Rect of the pad so it maches keyboard events.
        Moving_up and moving_down flags are used to keep track
        of constant movement and pause when hitting the wall

        Args:
            dy (int): 1 for moving_up
                      -1 for moving_down

        Returns:
            None
        """
        if self.rect.top <= 0 and self.moving_up:
            self.moving_up, dy = False, 0
        elif self.rect.bottom >= SCREEN_SIZE[1] and self.moving_down:
            self.moving_down, dy = False, 0
        dy *= PAD_SPEED
        self.rect.centery += dy
        self.calculate_average_speed(dy)

    def calculate_average_speed(self, dy: int):
        """
        Calculates average speed of the pad using
        speed history from the last 20 frames

        Args:
            dy (int): value of instantaneous speed
        """
        self.speed_history.append(dy)
        self.speed_history.pop(0)
        self.average_speed = sum(self.speed_history)/20


class Scoreboard():
    """
    Object that keeps track of number of each player points
    Creates and renders texts/scoreboard on the screen.

    Args:
        screen (pygame.surface.Surface): display area
    """
    def __init__(self, screen):
        self.screen = screen
        self.left_points, self.right_points = 0, 0

    def render_texts(self):
        """
        Renders texts, places them in the right places
        and displays them on the screen

        Args:
            None

        Returns:
            None
        """
        self.left_text = FONT.render(str(self.left_points),
                                     True, TEXT_COLOR)
        self.right_text = FONT.render(str(self.right_points),
                                      True, TEXT_COLOR)
        self.left_rect = self.left_text.get_rect()
        self.left_rect.center = (SCREEN_SIZE[0]//4, SCREEN_SIZE[1]//2)
        self.right_rect = self.right_text.get_rect()
        self.right_rect.center = (SCREEN_SIZE[0]//4*3, SCREEN_SIZE[1]//2)
        self.screen.blit(self.left_text, self.left_rect)
        self.screen.blit(self.right_text, self.right_rect)
