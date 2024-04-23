"""
Module including function for controlling
keyboard events, screen updates and objects behaviour
"""

import pygame
import sys
from functions import *
from settings import BACKGROUND_COLOR, BALL_RADIUS, STARTING_TICK


class EventsController():
    """
    Class storing functions neccessary to control
    events and objects movement + interaction.

    Args:
        screen (pygame.surface.Surface): display area
        ball (objects.Ball): instance of Ball class
        pads (list[objects.Pad]): two-elements list of Pads (players)
    """
    def __init__(self,
                 screen: pygame.surface.Surface,
                 ball, pads: list, scoreboard):
        self.screen = screen
        self.ball, self.pads = ball, pads
        self.scoreboard = scoreboard
        self.tick = STARTING_TICK

    def check_events(self):
        """
        Function that checks if any keyboard events occur
        and trigger apropriate reaction.

        Args:
            None

        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.change_moving_parameters(event.key, True)
            elif event.type == pygame.KEYUP:
                self.change_moving_parameters(event.key, False)

    def change_moving_parameters(self, key: int, value: bool):
        """
        Changing value of pads direction parameters
        depending on event type (KEYDOWN, KEYUP) and key pressed

        Args:
            key (int): ascii code of key that was pressed or released
            value (bool): True for KEYDOWN, False for KEYUP

        Returns:
            None
        """
        for pad in self.pads:
            if key == pad.keys[0]:
                pad.moving_up = value
            elif key == pad.keys[1]:
                pad.moving_down = value

    def check_collisions(self):
        """
        Functions supposed to check if ball collides with one of the
        pads. If so, it changes ball direction adequately to the
        velocity of the pad. It also ensures that ball
        cannot pass through the pad. After every collision it increases
        speed of the game.

        Args:
            None

        Returns:
            None
        """
        left_pad, right_pad = self.pads

        # left pad case
        if left_pad.rect.colliderect(self.ball):
            # ball touches the pad "on the front"
            if self.ball.rect.centerx > left_pad.rect.right:
                self.ball.dx, self.ball.dy = calculate_new_deltas(
                    self.ball, left_pad.average_speed, left_pad.rect.top)
                # because ball.dx, ball.dy are float and in many cases bigger
                # than BALL_RADIUS, so it's a way to prevent pall
                # from getting into the pad
                self.ball.rect.centerx = left_pad.rect.right + BALL_RADIUS
            # ball touches the pad on the bottom or on the top
            else:
                self.react_to_top_collisions(left_pad)
            # game speed increased
            self.tick += 5

        # analogical for the right pad
        if right_pad.rect.colliderect(self.ball):
            if self.ball.rect.centerx < right_pad.rect.left:
                self.ball.dx, self.ball.dy = calculate_new_deltas(
                    self.ball, right_pad.average_speed, right_pad.rect.top)
                self.ball.rect.centerx = right_pad.rect.left - BALL_RADIUS
            else:
                self.react_to_top_collisions(right_pad)
            self.tick += 5

    def react_to_top_collisions(self, pad):
        """
        Reacts when a ball hits bottom or top of the pad
        and doesn't let it fall through it

        Args:
            pad (objects.Pad): palette which collided with the ball

        Returns:
            None
        """
        self.ball.dy *= -1
        if self.ball.rect.top < pad.rect.top:
            self.ball.rect.centery = pad.rect.top - BALL_RADIUS
        else:
            self.ball.rect.centery = pad.rect.bottom + BALL_RADIUS

    def update_objects(self):
        """
        Changes all crucial parameters of movement
        of all objects, like direction, speed, and position.
        Because collision require change of ball direction
        method check_collision is also invoked

        Args:
            None

        Returns:
            None
        """
        self.check_collisions()
        for pad in self.pads:
            pad.update_position(pad.moving_down - pad.moving_up)
        self.ball.update_direction()
        self.ball.update_position()

    def update_screen(self):
        """
        Function rendering objects on screen.

        Args:
            None

        Returns:
            None
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.scoreboard.render_texts()
        self.ball.show()
        for pad in self.pads:
            pad.show()

        pygame.display.flip()

    def check_and_react_if_scored(self):
        """
        Checks if ball touches wall and eventually
        resets some parameters of the game adequalty.
        Than stops the game for a few seconds, letting
        the players prepare

        Args:
            None

        Returns:
            None
        """
        if self.ball.touches_vertical_wall:
            self.ball.touches_vertical_wall = False
            self.ball.set_beginning_position()
            for pad in self.pads:
                pad.set_beginning_position()
            self.update_objects()
            self.update_screen()
            self.tick = STARTING_TICK
            self.ball.dx, self.ball.dy = rand_direction()
            pygame.time.wait(3000)

    def trigger_all_events(self):
        """
        Runs all events in apropriate order.

        Args:
            None

        Returns:
            None
        """
        self.check_events()
        self.update_objects()
        self.update_screen()
        self.check_and_react_if_scored()
