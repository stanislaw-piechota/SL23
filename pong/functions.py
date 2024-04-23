"""
Module with other functions, more of mathematical nature
"""


from random import choice
from math import atan, sin, cos, pi, sqrt
from settings import PAD_SPEED, PAD_SIZE, BALL_SPEED


def rand_direction() -> list[float]:
    """
    Randomly choses direction of the ball velocity
    after each point score.

    Args:
        None

    Returns:
        (list[float], list[float]): numbers representing ball.dx, ball.dy
    """
    # After such event ball is supposed to fly with 45 bounce
    # degree and thats why dx/dy is sqrt(BALL_SPEED)
    return choice([-sqrt(BALL_SPEED), sqrt(BALL_SPEED)]),\
        choice([-sqrt(BALL_SPEED), sqrt(BALL_SPEED)])


def sgn(n: float) -> int:
    """
    Signum function
    *) for n = 0 -> 1

    Args:
        n (float): real number

    Returns:
        (int): vlaue of the *signum function
    """
    return (n >= 0) - (n < 0)


def moving_in_same_direction(pad_speed: float, ball_dy: int) -> bool:
    return sgn(pad_speed) == sgn(ball_dy)


def calculate_new_deltas(ball, pad_speed: float, pad_top_position: int):
    """
    Calculates new angle of reflection in dependence of
    pad velocity and place which hit the ball

    Args:
        ball (objects.Ball): ball instance with dx and dy
        pad_speed (float): average speed of the pad
        pad_top_position (int): pad.rect.top alias

    Returns:
        dx (float): new delta x for ball object
        dy (float): new delta y for ball object
    """

    # calculates value of angle of incidence in degrees
    current_angle = atan(abs(ball.dx)/abs(ball.dy))*180/pi
    # creates multiplier of the angle depending on pad speed
    # and distance from the point where the bounced to the center of the pad
    multiplier = 1 - (1 - pad_speed/PAD_SPEED) *\
        abs(0.5 - (ball.rect.centery-pad_top_position)/PAD_SIZE[1])
    # changes angle when directions are different
    if moving_in_same_direction(pad_speed, ball.dy):
        new_angle = current_angle * multiplier
    else:
        new_angle = current_angle / multiplier

    # angle constraints
    if new_angle < 15:
        new_angle = 15
    elif new_angle > 75:
        new_angle = 75

    # converting to radians
    new_angle *= pi / 180
    # calculating dx and dy
    dx = sin(new_angle) * ball.speed * sgn(ball.dx) * -1
    dy = cos(new_angle) * ball.speed * sgn(ball.dy)

    return dx, dy
