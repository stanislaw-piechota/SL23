"""Module with classes creating background and scoreboard"""

from random import choice, randint
import pygame
from constants import *
from functions import load_sprite_image


class Battlefield():
    """Generating a labirynth and a frame containing that maze"""
    def __init__(self, screen: pygame.Surface):
        self.board = pygame.Surface((FIELD_WIDTH*CELL_SIZE+BORDER_WIDTH, FIELD_HEIGHT*CELL_SIZE+BORDER_WIDTH))
        self.screen = screen
        self.initialise_board()

    def initialise_board(self):
        """(re)initialise basic arguments"""
        self.borders, self.cells = [], []
        self.occupied = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.connections = [[[] for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.generate_board(row=randint(0, FIELD_HEIGHT-1), col=randint(0, FIELD_WIDTH-1))
        self.generate_borders()

    def get_neighbours(self, row=randint(0, FIELD_HEIGHT-1), col=randint(0, FIELD_WIDTH)):
        """Similiar to modules.fucntions.get_neighbours, but modified for algorithm needs"""
        neighbours = []
        # border conditions
        if row > 0:
            neighbours.append((row-1, col))
        if row < FIELD_HEIGHT - 1:
            neighbours.append((row+1, col))
        if col > 0:
            neighbours.append((row, col-1))
        if col < FIELD_WIDTH - 1:
            neighbours.append((row, col+1))
        return neighbours

    def generate_board(self, row=0, col=0):
        """Recursive algorithm of generating a path"""
        next_cells = self.get_neighbours(row, col)
        self.occupied[row][col] = 1
        while next_cells:
            next_cell = choice(next_cells)
            if self.occupied[next_cell[0]][next_cell[1]]:
                if next_cell in self.connections[row][col]:
                    pass
                # choosing whether to create hole in a map
                elif choice([0 for _ in range(int(100*(1-PROBABILITY_OF_HOLE)))] +
                            [1 for _ in range(int(100*PROBABILITY_OF_HOLE))]):
                    self.connections[row][col].append(next_cell)
                    self.connections[next_cell[0]][next_cell[1]].append((row, col))
                next_cells.remove(next_cell)
                continue
            self.connections[row][col].append(next_cell)
            self.connections[next_cell[0]][next_cell[1]].append((row, col))
            next_cells.remove(next_cell)
            self.generate_board(row=next_cell[0], col=next_cell[1])

    def generate_borders(self):
        """Create graphic representation of the maze"""
        for row, row_connections in enumerate(self.connections):
            for col, connections in enumerate(row_connections):
                if (row-1, col) not in connections:
                    self.borders.append(pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE+BORDER_WIDTH, BORDER_WIDTH))
                if (row+1, col) not in connections:
                    self.borders.append(pygame.Rect(col*CELL_SIZE, (row+1)*CELL_SIZE, CELL_SIZE, BORDER_WIDTH))
                if (row, col-1) not in connections:
                    self.borders.append(pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, BORDER_WIDTH, CELL_SIZE+BORDER_WIDTH))
                if (row, col+1) not in connections:
                    self.borders.append(pygame.Rect((col+1)*CELL_SIZE, row*CELL_SIZE, BORDER_WIDTH, CELL_SIZE))
                self.cells.append((pygame.Rect(col*CELL_SIZE+BORDER_WIDTH,
                                               row*CELL_SIZE+BORDER_WIDTH,
                                               CELL_SIZE-BORDER_WIDTH, CELL_SIZE-BORDER_WIDTH),
                                   choice(CELL_COLORS)))

    def draw_field(self):
        """Draw maze onto the frame"""
        self.board.fill(BACKGROUND_COLOR)
        for cell in self.cells:
            pygame.draw.rect(self.board, cell[1], cell[0])
        for border in self.borders:
            pygame.draw.rect(self.board, BORDER_COLOR, border)


class Scoreboard():
    """Class containg surface and controls of the scorboard"""
    def __init__(self, number_of_players, screen: pygame.Surface):
        self.screen = screen
        self.frame = pygame.Surface((SCORE_PANEL_WIDTH, SCREEN_HEIGHT))
        self.number_of_players = number_of_players
        self.points = [-DOT_POINT for _ in range(self.number_of_players)]
        self.timer = ROUND_TIME + 2
        self.load_images()
        self.load_points()
        self.update_time()

    def update_time(self):
        """Decrease timer and render new timer text"""
        self.timer -= 1
        self.time_text = FONT.render(f"{self.timer//60:2d} : {self.timer % 60:02d}", True, TEXT_COLOR)
        self.time_rect = self.time_text.get_rect(center=(
            SCORE_PANEL_WIDTH//2-OFFSET//2,
            SCREEN_HEIGHT//(self.number_of_players+2))
        )

    def load_images(self):
        self.images_rects = []
        self.images = [
            load_sprite_image(i, 0, size=SCORE_PANEL_WIDTH//2) for i in range(1, self.number_of_players+1)
        ]
        for i, sprite in enumerate(self.images):
            rect = sprite.get_rect()
            rect.centery = SCREEN_HEIGHT//(self.number_of_players+2)*(i+2)
            rect.centerx = rect.width//2
            self.images_rects.append(rect)

    def load_points(self):
        """Render new text with points"""
        self.texts = []
        self.text_rects = []
        sprite_width = self.images_rects[0].width
        for i in range(self.number_of_players):
            img = FONT.render(str(self.points[i]), True, TEXT_COLOR, BACKGROUND_COLOR)
            rect = img.get_rect()
            rect.centery = SCREEN_HEIGHT//(self.number_of_players+2)*(i+2)
            rect.centerx = (SCORE_PANEL_WIDTH+sprite_width)//2
            self.texts.append(img)
            self.text_rects.append(rect)

    def draw_scoreboard(self):
        self.frame.fill(BACKGROUND_COLOR)
        for i, image in enumerate(self.images):
            self.frame.blit(image, self.images_rects[i])
            self.frame.blit(self.texts[i], self.text_rects[i])
        self.frame.blit(self.time_text, self.time_rect)
        self.screen.blit(self.frame, (SCREEN_WIDTH-SCORE_PANEL_WIDTH+OFFSET//2, 0))
