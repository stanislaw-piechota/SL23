"""Module holding functions used across several modules
or not directly connected to one class"""
from os import path
import pygame
from constants import FIELD_WIDTH, FIELD_HEIGHT, SPRITE_SIZE, CELL_SIZE, OFFSET


def position_to_id(pos):
    x, y = pos
    return y//CELL_SIZE, x//CELL_SIZE


def load_sprite_image(player_id, xframe, yframe=0, sprites=None, size=CELL_SIZE, mult=.6):
    """Load image from spritesheet

    Args:
        player_id (int): Id of the spritesheet to be loaded
        xframe (_type_): x index on the spritesheet
        yframe (int, optional): y index on the spritesheet. Defaults to 0.
        sprites (pygame.Surface, optional): image with loaded spritesheet, avoids unnecessary operations.
                                            Defaults to None.
        size (int, optional): Size of the resulting image. Defaults to CELL_SIZE.
        mult (float, optional): Multiplier of size. Ensures sprite can easily go through the maze. Defaults to .6.

    Returns:
        pygame.Surface: resulting image
    """
    if not sprites:
        sprites = pygame.image.load(path.join(path.dirname(__file__), f"imgs\\sprite{player_id}.png"))
    image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
    image.set_colorkey((0, 0, 0))
    image.blit(sprites, (0, 0), (xframe*SPRITE_SIZE, yframe*SPRITE_SIZE,
                                 SPRITE_SIZE, SPRITE_SIZE))
    return pygame.transform.scale(image, (size*mult, size*mult))


def configure_enemy(enemy, number_of_players, i, j):
    """Configure enemy attributes outside of __init__ method

    Args:
        enemy (modules.Enemy): enemy instance
        number_of_players (int): self-explanatory
        i (int): cell x position
        j (int): cell y position
    """
    x_id = FIELD_WIDTH//2-number_of_players//2+i-1
    y_id = FIELD_HEIGHT//2+j-1
    enemy.cell = (y_id, x_id)
    enemy.rect.center = (x_id*CELL_SIZE+OFFSET, y_id*CELL_SIZE+OFFSET)


def get_possible_cells(cell, connections):
    """Generate list of cell connected to specific cell

    Args:
        cell (tuple(int, int)): Examined cell address
        connections (list): List of connections describing the maze

    Returns:
        list: possible cells to continue movement
    """
    possible = []
    i, j = cell

    if i-1 >= 0 and (new_cell := (i-1, j)) in connections[i][j]:
        possible.append(new_cell)
    if i+1 < FIELD_HEIGHT and (new_cell := (i+1, j)) in connections[i][j]:
        possible.append(new_cell)
    if j-1 >= 0 and (new_cell := (i, j-1)) in connections[i][j]:
        possible.append(new_cell)
    if j+1 < FIELD_WIDTH and (new_cell := (i, j+1)) in connections[i][j]:
        possible.append(new_cell)
    return possible
