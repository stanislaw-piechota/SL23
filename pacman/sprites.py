"""Module with all editable sprites on the board"""
from os import path
from random import choice
from time import sleep
from threading import Thread
import pygame
from constants import *
from functions import *


class Player(pygame.sprite.Sprite):
    """Class with main characters of player"""

    # class atribute players to avoid reduntant argument passing
    players = pygame.sprite.Group()

    def __init__(self, player_id, back):
        pygame.sprite.Sprite.__init__(self)
        self.id = player_id
        self.keys = CONTROLS[self.id-1]
        self.borders = back.borders
        self.back = back
        self.moving = 0
        self.sprites = pygame.image.load(path.join(path.dirname(__file__), f"imgs\\sprite{player_id}.png"))
        self.new = True
        self.powerup = False

        self.image = load_sprite_image(self.id, 0)
        self.rect = self.image.get_rect()
        self.set_beginning_position()
        Player.players.add(self)

    def set_beginning_position(self):
        """
        Calculating beginning position specifically for player (in corners)
        depending on player id
        """
        offset = (CELL_SIZE+BORDER_WIDTH)//2
        match self.id:
            case 1:
                new_pos = (offset, offset)
            case 2:
                new_pos = (FIELD_WIDTH*CELL_SIZE-offset+BORDER_WIDTH, offset)
            case 3:
                new_pos = (offset, FIELD_HEIGHT*CELL_SIZE-offset+BORDER_WIDTH)
            case 4:
                new_pos = (FIELD_WIDTH*CELL_SIZE-offset+BORDER_WIDTH, FIELD_HEIGHT*CELL_SIZE-offset+BORDER_WIDTH)
        self.rect.center = new_pos

    def _undo_last_move(self):
        match self.moving:
            case 1:
                self.rect.y += SPRITE_SPEED
            case 2:
                self.rect.y -= SPRITE_SPEED
            case 3:
                self.rect.x -= SPRITE_SPEED
            case 4:
                self.rect.x += SPRITE_SPEED

    def _correct_vertical(self, cell):
        """Correct x position when moving in vertical axis to avoid being stopped by the wall

        Args:
            cell (pygame.Rect): Rect constraning the cell field of given index
        """
        if self.rect.left < cell.left:
            self.rect.x += SPRITE_SPEED
        elif self.rect.right > cell.right:
            self.rect.x -= SPRITE_SPEED

    def _correct_horizontal(self, cell):
        """Correct y position when moving in horizontal axis to avoid being stopped by the wall

        Args:
            cell (pygame.Rect): Rect constraning the cell field of given index
        """
        if self.rect.top < cell.top:
            self.rect.y += SPRITE_SPEED
        elif self.rect.bottom > cell.bottom:
            self.rect.y -= SPRITE_SPEED

    def move(self):
        """Function of movement with relation to collisions with walls and playres"""
        match self.moving:
            case 1:
                self.rect.y -= SPRITE_SPEED
            case 2:
                self.rect.y += SPRITE_SPEED
            case 3:
                self.rect.x += SPRITE_SPEED
            case 4:
                self.rect.x -= SPRITE_SPEED

        if self.rect.collidelist(self.borders) >= 0:
            self._undo_last_move()
            cell_addr = position_to_id(self.rect.center)
            # extracting cell from the list
            cell = self.back.cells[cell_addr[0]*FIELD_WIDTH+cell_addr[1]][0]
            match self.moving:
                case 1:
                    self._correct_vertical(cell)
                case 2:
                    self._correct_vertical(cell)
                case 3:
                    self._correct_horizontal(cell)
                case 4:
                    self._correct_horizontal(cell)

        if len(pygame.sprite.spritecollide(self, Player.players, 0)) > 1:
            self._undo_last_move()
            self.moving = 0
            self.image = load_sprite_image(self.id, 0, sprites=self.sprites)

    # overriding pygame.Group.update()
    def update(self):
        self.move()

    # overriding pygame.Group.draw()
    def draw(self):
        if self.powerup:
            pygame.draw.circle(self.back.board, POWER_COLOR, self.rect.center, radius=CELL_SIZE//2*.8)
        self.back.board.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    """Class of the enemy"""

    # analogically to Player.players
    enemies = pygame.sprite.Group()

    def __init__(self, field):
        pygame.sprite.Sprite.__init__(self)
        self.field = field
        self.sprites = pygame.image.load(path.join(path.dirname(__file__), "imgs\\sprite5.png"))
        self.dx, self.dy = 0, 0
        self.xframe, self.yframe = 0, 0
        self.animation_step = 0
        self.active = True
        self.inactive_thread = Thread(target=self.non_active_counter)

        self.image = load_sprite_image(5, self.xframe, yframe=self.yframe, sprites=self.sprites)
        self.rect = self.image.get_rect()
        self.cell = ()
        Enemy.enemies.add(self)

    def choose_direction(self):
        """
        Calculate dx and dy to determine direction of movement
        Taking into considerection constraints set by maze walls
        """
        next_cells = get_possible_cells(self.cell, self.field.connections)
        try:
            if len(next_cells) == 1:
                self.dy, self.dx = self._get_deltas(next_cells[0])
                return
            next_cells.remove(self._get_prev_cell())
        except ValueError:
            pass
        finally:
            self.dy, self.dx = self._get_deltas(choice(next_cells))

    def change_image(self):
        """Flip the image according to the direction"""
        if self.dx > 0:
            self.xframe = 0
        elif self.dx < 0:
            self.xframe = 1

    def animate_image(self):
        """Animation of the sprite with after certain amount of frames"""
        if self.animation_step < SPRITE_ANIMATION_MAX_STEPS:
            self.animation_step += 1
            return
        self.animation_step = 0

        if self.yframe:
            self.yframe = 0
        else:
            self.yframe = 1

        self.image = load_sprite_image(5, self.xframe, yframe=self.yframe, sprites=self.sprites)

    def move_cell(self, dest):
        """Movement script

        Args:
            dest (tuple(int, int)): destination cell
        """
        # moving up to the point when the center of next cell is reached
        if self.dx and (CELL_SIZE*dest[1]+OFFSET-self.rect.centerx)*self.dx > 0:
            self.rect.x += self.dx*PACKMAN_SPEED
        elif self.dy and (CELL_SIZE*dest[0]+OFFSET-self.rect.centery)*self.dy > 0:
            self.rect.y += self.dy*PACKMAN_SPEED
        else:
            self.cell = position_to_id(self.rect.center)
            self.choose_direction()
        self.change_image()

    def _get_deltas(self, next_cell):
        return next_cell[0]-self.cell[0], next_cell[1]-self.cell[1]

    def _get_prev_cell(self):
        return self.cell[0]-self.dy, self.cell[1]-self.dx

    def _get_next_cell(self):
        return self.cell[0]+self.dy, self.cell[1]+self.dx

    # overriding pygame.Group.update()
    def update(self):
        # spawning pacmans in the same place where they were deactivated
        if not self.active:
            return

        next_cell = self._get_next_cell()
        self.move_cell(next_cell)
        self.animate_image()

    # overriding pygame.Group.draw()
    def draw(self):
        if self.active:
            self.field.board.blit(self.image, self.rect)

    def non_active_counter(self):
        """
        Thread function to prevent freezing the game.
        Used to deactivate enemy for certain amount of time
        """
        timer = 0
        while timer < ENEMY_INACTIVE_TIME:
            sleep(1)
            timer += 1
        self.active = True


class Point(pygame.sprite.Sprite):
    """Class holding a rect symbolising a point to collect"""

    # analogically to Player.players
    points = pygame.sprite.Group()

    def __init__(self, x, y, special=False):
        pygame.sprite.Sprite.__init__(self, Point.points)
        self.x, self.y = x, y
        # attribute determinig whether the point is powerup
        self.special = special

        if not special:
            self.rect = pygame.Rect(0, 0, CELL_SIZE*0.1, CELL_SIZE*0.1)
            self.rect.center = (self.x*CELL_SIZE+OFFSET, self.y*CELL_SIZE+OFFSET)
            self.image = pygame.Surface((CELL_SIZE*.1, CELL_SIZE*.1))
            self.image.fill(POINT_COLOR)
        else:
            self.image = load_sprite_image(6, 0)
            self.rect = self.image.get_rect(center=(self.x*CELL_SIZE+OFFSET, self.y*CELL_SIZE+OFFSET))
        Point.points.add(self)
