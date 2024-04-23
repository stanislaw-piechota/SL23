"""
Main file of the game
consolidating function and constants
from all other modules
"""

import objects
import pygame
from events import EventsController
from settings import *


def run_game(screen: pygame.surface.Surface) -> int:
    """
    Function responsible for initializing neccessary
    data, structures and main loop of the game.

    Args:
        screen (pygame.surface.Surface): display area

    Returns:
        (int): difference between players points
    """
    timer = pygame.time.Clock()
    scoreboard = objects.Scoreboard(screen)
    ball = objects.Ball(screen, scoreboard)
    pads = [objects.Pad(screen, 20, PAD_1_KEYS),
            objects.Pad(screen, SCREEN_SIZE[0]-PAD_SIZE[0]-20, PAD_2_KEYS)]
    events_controller = EventsController(screen, ball, pads, scoreboard)

    # main loop of the game
    while scoreboard.left_points < 5 and scoreboard.right_points < 5:
        events_controller.trigger_all_events()
        timer.tick(events_controller.tick)

    pygame.time.wait(1000)

    return scoreboard.left_points - scoreboard.right_points


def display_end_message(points_diff: int, screen: pygame.surface.Surface):
    """
    Function that display message which player won the game
    and renders adequate text to do so

    Args:
        points_diff (int): Difference between players scores.
                           x > 0 => 1st player won
                           x < 0 => 2nd player won
        screen (pygame.surface.Surface): display area

    Returns:
        None
    """
    if points_diff > 0:
        end_text = "Player 1 won"
    else:
        end_text = "Player 2 won"

    text_render = FONT.render(end_text, True, TEXT_COLOR, BACKGROUND_COLOR)
    text_rect = text_render.get_rect()
    text_rect.center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

    screen.fill(BACKGROUND_COLOR)
    screen.blit(text_render, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pong game")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    display_end_message(run_game(screen), screen)
